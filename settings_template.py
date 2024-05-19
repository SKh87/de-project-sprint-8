SPARK = {
    "app_name": "practicum",
    "config": {
        "spark.jars.packages": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.4.0",
        "spark.sql.session.timeZone": "UTC"
    }
}

KAFKA = {
    "option": {
        'kafka.bootstrap.servers': 'АДРЕС:ПОРТ',
        'kafka.security.protocol': 'SASL_SSL',
        'kafka.sasl.mechanism': 'SCRAM-SHA-512',
        'kafka.sasl.jaas.config': 'org.apache.kafka.common.security.scram.ScramLoginModule required username=\"ЛОГИН\" password=\"ПАРОЛЬ\";',
        'kafka.ssl.truststore.location': "ПУТЬ К cacerts"
    },
    "topic_in": 'ТОПИК ДЛЯ ЧТЕНИЯ',
    "topic_out": 'ТОПИК ДЛЯ ЗАПИСИ'
}

DATABASE = {
    "url": "URL БД",
    "driver": "org.postgresql.Driver",
    "user": "ЛОГИН",
    "password": "ПАРОЛЬ",
}
