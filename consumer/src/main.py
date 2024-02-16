
import sys
import signal

from config import *
import kafka


def main():

    run_logs_generation()
    signal.signal(signal.SIGTERM, handle_sigterm)


def run_logs_generation():
    config = create_dsh_config()

    consumer = kafka.create_consumer_by_config(config)
    consumer.subscribe([TOPIC])

    while True:
        run_consumer(consumer)
        signal.signal(signal.SIGTERM, handle_sigterm)


def run_consumer(consumer):
    event = consumer.poll(1.0)
    sub_logs = ["LogLevel", "LogType", "Environment"]

    if event is None or event.error():
        pass
    else:
        value = event.value()
        if value is not None and all([sub_log in str(event.value())for sub_log in sub_logs]):
            print(f"Got event: {event.value()}")


def handle_sigterm(signum, frame):
    logger.warning("Receiving sigterm")
    sys.exit(1)

if __name__ == "__main__":
    main()