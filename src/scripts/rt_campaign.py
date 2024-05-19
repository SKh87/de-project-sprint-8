from pyspark.sql import SparkSession, DataFrame
from datetime import datetime, timezone
from pyspark.sql.functions import from_json, to_json, col, lit, struct
from pyspark.sql.types import StructType, StructField, StringType, LongType

from settings import *


# метод для записи данных в 2 target: в PostgreSQL для фидбэков и в Kafka для триггеров
def foreach_batch_function(df: DataFrame, epoch_id):
    # сохраняем df в памяти, чтобы не создавать df заново перед отправкой в Kafka
    df.persist()

    # записываем df в PostgreSQL с полем feedback
    df.write.format("jdbc") \
        .options(**DATABASE) \
        .option("schema", "public") \
        .option("dbtable", "subscribers_feedback") \
        .mode("append").save()

    # создаём df для отправки в Kafka. Сериализация в json.
    df_without_feedback = df.select(to_json(struct(
        col("restaurant_id"),
        col("adv_campaign_id"),
        col("adv_campaign_content"),
        col("adv_campaign_owner"),
        col("adv_campaign_owner_contact"),
        col("adv_campaign_datetime_start"),
        col("adv_campaign_datetime_end"),
        col("datetime_created"),
        col("client_id"),
        col("trigger_datetime_created"),
    )).alias("value")).select("value")

    # отправляем сообщения в результирующий топик Kafka без поля feedback
    df_without_feedback \
        .write \
        .format("kafka") \
        .options(**KAFKA["option"]) \
        .option("topic", KAFKA["topic_out"]).save()
    # очищаем память от df
    df.unpersist()


# создаём spark сессию с необходимыми библиотеками в spark_jars_packages для интеграции с Kafka и PostgreSQL
spark = SparkSession.builder \
    .appName("RestaurantSubscribeStreamingService") \
    .config(map=SPARK["config"]) \
    .getOrCreate()

# читаем из топика Kafka сообщения с акциями от ресторанов
restaurant_read_stream_df = spark.readStream \
    .format('kafka') \
    .options(**KAFKA["option"]) \
    .option('subscribe', KAFKA["topic_in"]) \
    .load()

# определяем схему входного сообщения для json
incomming_message_schema = StructType([
    StructField("restaurant_id", StringType(), True),
    StructField("adv_campaign_id", StringType(), True),
    StructField("adv_campaign_content", StringType(), True),
    StructField("adv_campaign_owner", StringType(), True),
    StructField("adv_campaign_owner_contact", StringType(), True),
    StructField("adv_campaign_datetime_start", LongType(), True),
    StructField("adv_campaign_datetime_end", LongType(), True),
    StructField("datetime_created", LongType(), True)
])

# определяем текущее время в UTC в миллисекундах, затем округляем до секунд
dt = datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
current_timestamp_utc = int(utc_time.timestamp())

# десериализуем из value сообщения json и фильтруем по времени старта и окончания акции
filtered_read_stream_df = restaurant_read_stream_df.select(
    from_json(col("value").cast("string"), incomming_message_schema).alias("parsed_value")
).select(
    col("parsed_value.restaurant_id").alias("restaurant_id"),
    col("parsed_value.adv_campaign_id").alias("adv_campaign_id"),
    col("parsed_value.adv_campaign_content").alias("adv_campaign_content"),
    col("parsed_value.adv_campaign_owner").alias("adv_campaign_owner"),
    col("parsed_value.adv_campaign_owner_contact").alias("adv_campaign_owner_contact"),
    col("parsed_value.adv_campaign_datetime_start").alias("adv_campaign_datetime_start"),
    col("parsed_value.adv_campaign_datetime_end").alias("adv_campaign_datetime_end"),
    col("parsed_value.datetime_created").alias("datetime_created")
).filter(
    lit(current_timestamp_utc).between(col("adv_campaign_datetime_start"), col("adv_campaign_datetime_end"))
)

# вычитываем всех пользователей с подпиской на рестораны
subscribers_restaurant_df = spark.read \
    .format('jdbc') \
    .options(**DATABASE) \
    .option("schema", "public") \
    .option('dbtable', 'subscribers_restaurants') \
    .load() \
    .select(col("client_id"), col("restaurant_id"))

# джойним данные из сообщения Kafka с пользователями подписки по restaurant_id (uuid). Добавляем время создания события.
result_df = filtered_read_stream_df.join(subscribers_restaurant_df, on="restaurant_id", how="inner"). \
    withColumn("trigger_datetime_created", lit(current_timestamp_utc))

# запускаем стриминг
result_df.writeStream \
    .foreachBatch(foreach_batch_function) \
    .start() \
    .awaitTermination()
