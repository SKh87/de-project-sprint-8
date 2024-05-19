#!/bin/bash

docker run -it -v /tmp/CA.pem:/data/CA.pem -v /tmp/messages.kafka:/data/messages.kafka --network=host edenhill/kcat:1.7.1 \
kafkacat -b "host":"port" \
-X security.protocol=SASL_SSL \
-X sasl.mechanisms=SCRAM-SHA-512 \
-X sasl.username="ваш_username" \
-X sasl.password="ваш_пароль" \
-X ssl.ca.location=/data/CA.pem \
-t "topic_in" \
-P /data/messages.kafka
