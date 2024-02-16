from confluent_kafka import Producer, Consumer
import sys

from config import *

def produce_message(producer, value):
    producer.produce(topic=TOPIC, value=value, callback=_delivery_report)
    print("Produced message:", value)
    print("On topic:", TOPIC)
    producer.flush(1)


def handle_sigterm(signum, frame):
    print("Received SIGTERM. Exiting...")
    sys.exit(0)


def _delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        logger.warning(f"Message delivery failed: {err} \n \n")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] \n \n")


def create_producer_by_config(config: Config) -> Producer:
    return Producer(
        {
            "bootstrap.servers": config.servers,
            "group.id": config.group_id,
            "client.id": config.client_id,
            "security.protocol": "ssl",
            "ssl.key.location": config.pki_key,
            "ssl.certificate.location": config.pki_cert,
            "ssl.ca.location": config.pki_cacert,
        }
    )


def create_consumer_by_config(config: Config) -> Consumer:
    return Consumer(
        {
            "bootstrap.servers": config.servers,
            "group.id": config.group_id,
            "client.id": config.client_id,
            "security.protocol": "ssl",
            "ssl.key.location": config.pki_key,
            "ssl.certificate.location": config.pki_cert,
            "ssl.ca.location": config.pki_cacert,
            "auto.offset.reset": "latest",
        }
    )

# def create_consumer():
#     try:
#         consumer = Consumer(
#             {
#                 "bootstrap.servers": BROKERS,
#                 "group.id": GROUP_ID,
#                 "client.id": CLIENT_ID,
#                 "security.protocol": "ssl",
#                 "ssl.key.location": PKI_KEY,
#                 "ssl.certificate.location": PKI_CERT,
#                 "ssl.ca.location": PKI_CACERT,
#             }
#         )
#         return consumer
#     except KafkaException as e:
#         print(f"Failed to create consumer: {e}")
#         sys.exit(1)


# def create_producer():
#     try:
#         producer = Producer(
#             {
#                 "bootstrap.servers": BROKERS,
#                 "client.id": CLIENT_ID,
#                 "security.protocol": "ssl",
#                 "ssl.key.location": PKI_KEY,
#                 "ssl.certificate.location": PKI_CERT,
#                 "ssl.ca.location": PKI_CACERT,
#             }
#         )
#         return producer
#     except KafkaException as e:
#         print(f"Failed to create producer: {e}")
#         sys.exit(1)

