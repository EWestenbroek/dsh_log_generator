
import sys
import signal

from config import *
import kafka
from logstructs import *


def main():

    run_logs_generation()
    signal.signal(signal.SIGTERM, handle_sigterm)

def run_logs_generation():
    # log_counter = 0
    log_generator = LogGenerator(
        interval_mins=INTERVAL_REVERSE_PERCENTILE,
        duration_mins=DURATION_REVERSE_PERCENTILE,
        nof_ip_addresses=NOF_IP_ADDRESSES
        )
    config = create_dsh_config()

    consumer = kafka.create_consumer_by_config(config)
    consumer.subscribe([TOPIC])

    producer = kafka.create_producer_by_config(config)

    while True:
        run_consumer(consumer)
        message_value = log_generator.generate_log_message()
        kafka.produce_message(producer, message_value)
        signal.signal(signal.SIGTERM, handle_sigterm)

def run_consumer(consumer):
    event = consumer.poll(1.0)

    if event is None or event.error():
        pass
    else:
        value = event.value()
        if value is not None:
            print(f"Got event: {event}")


def handle_sigterm(signum, frame):
    logger.warning("Receiving sigterm")
    sys.exit(1)

if __name__ == "__main__":
    main()