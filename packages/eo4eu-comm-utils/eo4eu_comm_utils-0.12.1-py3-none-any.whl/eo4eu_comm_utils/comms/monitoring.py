import os
import json
from pathlib import Path
from datetime import datetime

from .interface import Comm, LogLevel
from ..kafka import KafkaProducer


_namespace_path = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")


class MonitoringComm(Comm):
    def __init__(
        self,
        producer: KafkaProducer,
        namespace: str|None = None,
        source: str = "Component",
        prefix: str = "Component",
        level_dict: dict[LogLevel,tuple[str,str]]|None = None,
        **kwargs
    ):
        if namespace is None:
            try:
                namespace = _namespace_path.read_text()
            except Exception:
                namespace = "unknown"

        if level_dict is None:
            level_dict = {
                LogLevel.DEBUG:    ("INFO",     "Info"),
                LogLevel.INFO:     ("INFO",     "Info"),
                LogLevel.WARNING:  ("WARNING",  "Warning"),
                LogLevel.ERROR:    ("WARNING",  "Error"),
                LogLevel.CRITICAL: ("CRITICAL", "Critical"),
                LogLevel.SUCCESS:  ("SUCCESS",  "Info"),
            }

        self.producer = producer
        self.namespace = namespace
        self.source = source
        self.prefix = prefix
        self.level_dict = level_dict
        self.kwargs = kwargs
        try:
            self.pod = os.environ["HOSTNAME"]
        except Exception:
            self.pod = "unknown"

    def send(
        self,
        level: LogLevel,
        description: str,
        *args,
        description_business: str = None,
        **kwargs
    ):
        if description_business is None:
            description_business = description

        level_name, msg_name = self.level_dict[level]
        message = {
            "source": self.source,
            "name": f"{self.prefix}{msg_name}",
            "level": level_name,
            "description": description,
            "description_business": description_business,
            "timestamp": datetime.utcnow().isoformat(),
            "extra": {
                "namespace": self.namespace,
                "pod": self.pod,
                **(self.kwargs | kwargs),
            }
        }

        # trying to be compatible with the different kafka producers
        # floating around
        previous_topic = "monitoring.notify"
        try:
            previous_topic = self.producer._topic
        except Exception:
            pass
        self.producer.set_topic("monitoring.notify")
        self.producer.send_message(
            key = self.source,
            msg = json.dumps(message)
        )
        self.producer.set_topic(previous_topic)
