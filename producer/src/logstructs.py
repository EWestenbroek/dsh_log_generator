import os
import socket
import random
import time
from enum import Enum
from config import *


class LogLevel(Enum):
    Level123 = 0
    Level456 = 1
    Level789 = 2

    @staticmethod
    def convert_from_string(string):
        string = string.lower()
        if string == "level123":
            return LogLevel.Level123
        elif string == "level456":
            return LogLevel.Level456
        elif string == "level789":
            return LogLevel.Level789


class Environment(Enum):
    Acceptatie = 0
    Development = 1
    Staging = 2
    Productie = 3
    Public = 4
    Test = 5

    @staticmethod
    def convert_from_string(string):
        string = string.lower()
        if string == "acceptatie":
            return Environment.Acceptatie
        elif string == "development":
            return Environment.Development
        elif string == "staging":
            return Environment.Staging
        elif string == "productie":
            return Environment.Productie
        elif string == "public":
            return Environment.Public
        elif string == "test":
            return Environment.Test


class LogType(Enum):
    Critical = 0
    Alert = 1
    Warning = 2
    Debug = 3
    Info = 4

    @staticmethod
    def convert_from_string(string):
        string = string.lower()
        if string == "critical":
            return LogType.Critical
        elif string == "alert":
            return LogType.Alert
        elif string == "warning":
            return LogType.Warning
        elif string == "debug":
            return LogType.Debug
        elif string == "info":
            return LogType.Info


class Log:
    def __init__(self, log_id, log_level, log_type, env, client_ip, server_ip, message):
        self.id = log_id
        self.level = log_level
        self.type = log_type
        self.env = env
        self.client_ip = client_ip
        self.server_ip = server_ip
        self.message = message

    def __str__(self):
        return (
            f"LogEvent(logId: {self.id}, logLevel: {self.level}, type: {self.type}, "
            f"env: {self.env}, clientIP: {self.client_ip}, serverIP: {self.server_ip}, message: {self.message})"
        )


class LogGenerator:
    def __init__(self, interval_mins=5, duration_mins=1, nof_ip_addresses=10) -> None:
        self._interval_counter = 0
        self.last_log_id_state = 0
        self.log_type_percentiles = None
        self.log_level_percentiles = None
        self.log_env_percentile = None
        self.set_percetiles()
        self.random_ip_addresses = self.fill_ip_addresses(nof_ip_addresses)
        self.interval_revers_percentiles = {
            "interval_mins": interval_mins*60,
            "duration_mins": duration_mins*60,
            }
        self.max_nof_special_events = MAX_NOF_SPECIAL_EVENTS
        self._start_new_interval = True
        self.quotes = self.get_quotes()
        self.start_time = time.time()
        self.absolute_priorities = self.get_absolute_priorities()
        print("\n\n")

    def get_absolute_priorities(self):
        result = []
        for abs_prio_string in ABSOLUTE_PRIORITIES:
            abs_prio_string = abs_prio_string.strip()
            abs_prio = LogType.convert_from_string(abs_prio_string)
            if abs_prio:
                result.append(abs_prio)
                print("found absolute prio match:", abs_prio)
                continue
            abs_prio = LogLevel.convert_from_string(abs_prio_string)
            if abs_prio:
                result.append(abs_prio)
                print("found absolute prio match:", abs_prio)
                continue
            abs_prio = Environment.convert_from_string(abs_prio_string)
            if abs_prio:
                result.append(abs_prio)
                print("found absolute prio match:", abs_prio)
                continue
        return result

    def generate_log_message(self):
        current_time_str = str(time.time())
        log = self.generate_log()
        message_str = f"{{{log} - t:{current_time_str}}}"
        return message_str

    def generate_log(self):
        do_special_event = False
        mod_time = (time.time() - self.start_time) % self.interval_revers_percentiles["interval_mins"]
        # print("times - mod_time:", mod_time, "cur:", (time.time() - self.start_time), "intrvl: ", self.interval_revers_percentiles["interval_mins"], "duration:", self.interval_revers_percentiles["duration_mins"])
        if 0 <= mod_time <= self.interval_revers_percentiles["duration_mins"]:
            do_special_event = True
            self._interval_counter += 1
            print("----- SPECIAL INTERVAL -----", self._interval_counter)

        log_level = self.log_value_selector(self.log_level_percentiles, do_special_event)
        log_type = self.log_value_selector(self.log_type_percentiles, do_special_event)
        env = self.log_value_selector(self.log_env_percentile, do_special_event)

        log = Log(
            log_id=self.last_log_id_state,
            log_level=log_level,
            log_type=log_type,
            env=env,
            client_ip=random.choice(self.random_ip_addresses),
            server_ip=random.choice(self.random_ip_addresses),
            message=random.choice(self.quotes),
        )
        self.last_log_id_state += 1
        return log
    
    def is_special_interval(self, do_special_event):
        if self.max_nof_special_events and self.max_nof_special_events > 0:
            return do_special_event and self._start_new_interval and self._interval_counter < self.max_nof_special_events
        else:
           return do_special_event and self._start_new_interval 
    
    def log_value_selector(self, prob_distr_dict, do_special_event):
        enum_list = list(prob_distr_dict.keys())
        if self.is_special_interval(do_special_event):
            current_probs = [1 - prob for prob in prob_distr_dict.values()]
            # When absolute priority values are provided, these are solely used (only 1 per type/enum)
            for abs_prio in self.absolute_priorities:
                if abs_prio in enum_list:
                    return abs_prio
        else:
            current_probs = list(prob_distr_dict.values())
            self._interval_counter = 0
            # reset _start_new_interval only when do_special_event was turned off
            if not do_special_event:
                self._start_new_interval = True
            else:
                self._start_new_interval = False
        selected_enum = random.choices(enum_list, weights=current_probs)[0]
        return selected_enum

    def set_default_percetiles(self):
        self.log_type_percentiles = {
            LogType.Critical: float(1/20),
            LogType.Alert: float(1/20),
            LogType.Warning: float(2/20),
            LogType.Debug: float(2/20),
            LogType.Info: float(14/20),  # default
        }
        self.log_level_percentiles = {
            LogLevel.Level123: float(2/6),  # default
            LogLevel.Level456: float(2/6),
            LogLevel.Level789: float(2/6),
        }
        self.log_env_percentile = {
            Environment.Acceptatie: float(1/12),
            Environment.Development: float(1/12),
            Environment.Staging: float(1/12),
            Environment.Test: float(1/12),
            Environment.Productie: float(4/12),  # default
            Environment.Public: float(4/12),
        }

    def fill_ip_addresses(self, amount):
        random_ips = []
        for _ in range(amount):
            random_ip = self.generate_random_ipv6()
            random_ips.append(random_ip)
        return random_ips

    def generate_random_ipv6(self):
        ip = os.urandom(16)
        ip = bytearray(ip)
        ip[0] = 0x60
        for i in range(8, 14):
            ip[i] = 0
        ip[8] &= 0xFE
        return socket.inet_ntop(socket.AF_INET6, bytes(ip))
    
    def set_percetiles(self):
        self.set_default_percetiles()

        global LOG_TYPE_PERCENTILES, LOG_ENV_PERCENTILES, LOG_LEVEL_PERCENTILES
        if type(LOG_TYPE_PERCENTILES) == dict:
            LOG_TYPE_PERCENTILES = envvar_log_type_converter(LOG_TYPE_PERCENTILES)
            self.log_type_percentiles = LOG_TYPE_PERCENTILES
        if type(LOG_ENV_PERCENTILES) == dict:
            LOG_ENV_PERCENTILES = envvar_log_env_converter(LOG_ENV_PERCENTILES)
            self.log_env_percentiles = LOG_ENV_PERCENTILES
        if type(LOG_LEVEL_PERCENTILES) == dict:
            LOG_LEVEL_PERCENTILES = envvar_log_level_converter(LOG_LEVEL_PERCENTILES)
            self.log_level_percentiles = LOG_LEVEL_PERCENTILES

    def get_quotes(self):
        quotes = [
            "1. May the Force be with you.",
            "2. I've got a bad feeling about this.",
            "3. I am your father.",
            "4. The Force will be with you, always.",
            "5. Do or do not, there is no try.",
            "6. It's a trap!",
            "7. You were the chosen one!",
            "8. I love you. I know.",
            "9. I find your lack of faith disturbing.",
            "10. You don't know the power of the dark side.",
            "11. Help me, Obi-Wan Kenobi, you're my only hope.",
            "12. The Force is strong with this one.",
            "13. It's over, Anakin! I have the high ground!",
            "14. You underestimate my power!",
        ]
        return quotes

def envvar_log_type_converter(envvar_json):
    log_type_percentiles = {}
    converted_vals = []
    for k, v in envvar_json.items():
        log_type_percentiles[LogType.convert_from_string(k)] = float(v)
        converted_vals.append(LogType.convert_from_string(k))

    all_vals = list(LogType)
    if len(all_vals) != len(converted_vals):
        for val in all_vals:
            if val not in converted_vals:
                print(f"WARNING: {val} was not found in LOG_TYPE_PERCENTILES read from the DSH Config.")
                print(f"This results in {val} NOT popping up in the generated logs.")
        for val in all_vals:
            if val not in converted_vals:
                print(f"WARNING: {val} was not found in accepted values.")
                print(f"As such, this results in {val} NOT popping up in the generated logs.")

    return log_type_percentiles


def envvar_log_level_converter(envvar_json):
    log_level_percentiles = {}
    converted_vals = []
    for k, v in envvar_json.items():
        log_level_percentiles[LogLevel.convert_from_string(k)] = float(v)
        converted_vals.append(LogLevel.convert_from_string(k))

    all_vals = list(LogLevel)
    if len(all_vals) != len(converted_vals):
        for val in converted_vals:
            if val not in all_vals:
                print(f"WARNING: {val} was not found in LOG_LEVEL_PERCENTILES read from the DSH Config.")
                print(f"This results in {val} NOT popping up in the generated logs.")
        for val in all_vals:
            if val not in converted_vals:
                print(f"WARNING: {val} was not found in accepted values.")
                print(f"As such, this results in {val} NOT popping up in the generated logs.")

    return log_level_percentiles


def envvar_log_env_converter(envvar_json):
    log_env_percentiles = {}
    converted_vals = []
    for k, v in envvar_json.items():
        log_env_percentiles[Environment.convert_from_string(k)] = float(v)
        converted_vals.append(Environment.convert_from_string(k))

    all_vals = list(Environment)
    if len(all_vals) != len(converted_vals):
        for val in converted_vals:
            if val not in all_vals:
                print(f"WARNING: {val} was not found in LOG_ENV_PERCENTILES read from the DSH Config.")
                print(f"This results in {val} NOT popping up in the generated logs.")
        for val in all_vals:
            if val not in converted_vals:
                print(f"WARNING: {val} was not found in accepted values.")
                print(f"As such, this results in {val} NOT popping up in the generated logs.")

    return log_env_percentiles
