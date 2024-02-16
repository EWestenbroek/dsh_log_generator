import json
import os, sys
from dataclasses import dataclass
from typing import Optional
import logging


# Set up logging
logger = logging.getLogger("kafka_feed")
loglevel = "DEBUG"
logger.setLevel(loglevel)
logger.addHandler(logging.StreamHandler(sys.stdout))


@dataclass
class Config:
    """
    If tenant_config is set, it will be used to set the servers and group_id.
    otherwise, servers and group_id must be set.
    """

    # tenant_name: str
    # topic: Optional[str] = None
    pki_cacert: str
    pki_key: str
    pki_cert: str
    client_id: str
    group_id: Optional[str] = None
    servers: Optional[str] = None
    tenant_config: Optional[str] = None

    # if tenant_config is set, use it to set servers and group_id
    def __post_init__(self):
        if self.tenant_config:
            json_config = json.loads(self.tenant_config)
            self.servers = ",".join(json_config["brokers"])
            self.group_id = json_config["shared_consumer_groups"][-1]

        if not self.tenant_config and not (self.servers and self.group_id):
            return ValueError(
                "Either tenant_config or servers and group_id must be set"
            )


def create_dsh_config() -> Config:
    dshconfig = Config(
        pki_cacert=os.environ["DSH_PKI_CACERT"],
        pki_key=os.environ["DSH_PKI_KEY"],
        pki_cert=os.environ["DSH_PKI_CERT"],
        client_id=os.environ["MESOS_TASK_ID"],
        tenant_config=os.environ["JSON_TENANT_CONFIG"],
    )
    return dshconfig

NOF_IP_ADDRESSES = ""
MAX_NOF_SPECIAL_EVENTS = ""

INTERVAL_REVERSE_PERCENTILE = {}
DURATION_REVERSE_PERCENTILE = {}

LOG_TYPE_PERCENTILES = -1
LOG_ENV_PERCENTILES = -1
LOG_LEVEL_PERCENTILES = -1
ABSOLUTE_PRIORITIES = -1

def get_env_vars():
    global MAX_NOF_SPECIAL_EVENTS
    global INTERVAL_REVERSE_PERCENTILE, DURATION_REVERSE_PERCENTILE, NOF_IP_ADDRESSES
    global LOG_TYPE_PERCENTILES, LOG_ENV_PERCENTILES, LOG_LEVEL_PERCENTILES
    global ABSOLUTE_PRIORITIES
    

    try:
        NOF_IP_ADDRESSES = int(os.getenv("NOF_IP_ADDRESSES"))
        print(f"NOF_IP_ADDRESSES used from env vars, with value: {NOF_IP_ADDRESSES}")
    except:
        # print(f"Error in parsing NOF_IP_ADDRESSES: {err}")
        NOF_IP_ADDRESSES = 10
        print(f"NOF_IP_ADDRESSES: Using default value of: {NOF_IP_ADDRESSES}")

    try:
        MAX_NOF_SPECIAL_EVENTS = int(os.getenv("MAX_NOF_SPECIAL_EVENTS"))
        print(f"MAX_NOF_SPECIAL_EVENTS used from env vars, with value: {MAX_NOF_SPECIAL_EVENTS}")
    except:
        # print(f"Error in parsing MAX_NOF_SPECIAL_EVENTS: {err}")
        MAX_NOF_SPECIAL_EVENTS = None
        print(f"MAX_NOF_SPECIAL_EVENTS: Using default value of: {MAX_NOF_SPECIAL_EVENTS}")

    # ---------- LOG PERCENTILES ----------
    try:
        INTERVAL_REVERSE_PERCENTILE = float(os.getenv("INTERVAL_REVERSE_PERCENTILE"))
        print(f"INTERVAL_REVERSE_PERCENTILE used from env vars, with value: {INTERVAL_REVERSE_PERCENTILE}")
    except:
        INTERVAL_REVERSE_PERCENTILE = 5.0
        print(f"INTERVAL_REVERSE_PERCENTILE: Using default value of: {INTERVAL_REVERSE_PERCENTILE}")

    try:
        DURATION_REVERSE_PERCENTILE = float(os.getenv("DURATION_REVERSE_PERCENTILE"))
        print(f"DURATION_REVERSE_PERCENTILE used from env vars, with value: {DURATION_REVERSE_PERCENTILE}")
    except:
        DURATION_REVERSE_PERCENTILE = 0.05
        print(f"DURATION_REVERSE_PERCENTILE: Using default value of: {DURATION_REVERSE_PERCENTILE}")

    try:
        LOG_TYPE_PERCENTILES = os.getenv("LOG_TYPE_PERCENTILES")
        LOG_TYPE_PERCENTILES = LOG_TYPE_PERCENTILES.replace("-(", "{").replace(")-", "}").replace("'", "\"")
        LOG_TYPE_PERCENTILES = dict(json.loads(LOG_TYPE_PERCENTILES))
        print(f"LOG_TYPE_PERCENTILES used from env vars, with value: {LOG_TYPE_PERCENTILES}")
    except:
        LOG_TYPE_PERCENTILES = -1
        print(f"Using default value for LOG_TYPE_PERCENTILES")

    try:
        LOG_ENV_PERCENTILES = os.getenv("LOG_ENV_PERCENTILES")
        LOG_ENV_PERCENTILES = LOG_ENV_PERCENTILES.replace("-(", "{").replace(")-", "}").replace("'", "\"")
        LOG_ENV_PERCENTILES = dict(json.loads(LOG_ENV_PERCENTILES))
        print(f"LOG_ENV_PERCENTILES used from env vars, with value: {LOG_ENV_PERCENTILES}")
    except:
        LOG_ENV_PERCENTILES = -1
        print(f"Using default value for LOG_ENV_PERCENTILES")

    try:
        LOG_LEVEL_PERCENTILES = os.getenv("LOG_LEVEL_PERCENTILES")
        LOG_LEVEL_PERCENTILES = LOG_LEVEL_PERCENTILES.replace("-(", "{").replace(")-", "}").replace("'", "\"")
        LOG_LEVEL_PERCENTILES = dict(json.loads(LOG_LEVEL_PERCENTILES))
        print(f"LOG_LEVEL_PERCENTILES used from env vars, with value: {LOG_LEVEL_PERCENTILES}")
    except:
        LOG_LEVEL_PERCENTILES = -1
        print(f"Using default value for LOG_LEVEL_PERCENTILES")

    try:
        ABSOLUTE_PRIORITIES = os.getenv("ABSOLUTE_PRIORITIES")
        ABSOLUTE_PRIORITIES = ABSOLUTE_PRIORITIES.replace("'", "\"")
        ABSOLUTE_PRIORITIES = ABSOLUTE_PRIORITIES.split(",")
        print(f"ABSOLUTE_PRIORITIES used from env vars, with value: {ABSOLUTE_PRIORITIES}")
    except:
        ABSOLUTE_PRIORITIES = []
        print(f"Using default value for ABSOLUTE_PRIORITIES")


get_env_vars()
TENANT_NAME = os.getenv("TENANT_NAME")
PKI_CACERT = os.getenv("DSH_PKI_CACERT")
PKI_KEY = os.getenv("DSH_PKI_KEY")
PKI_CERT = os.getenv("DSH_PKI_CERT")
TOPIC = os.getenv("STREAM")
CLIENT_ID = os.getenv("MESOS_TASK_ID")
