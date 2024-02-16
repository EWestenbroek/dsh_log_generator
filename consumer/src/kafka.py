from confluent_kafka import Consumer

from config import *


def handle_sigterm(signum, frame):
    print("Received SIGTERM. Exiting...")
    sys.exit(0)


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


