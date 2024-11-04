import logging
from enum import StrEnum

sendi_logger = logging.getLogger("sendi")


class SecurityLevel(StrEnum):
    SIMPLE = "simple"
    ENCRYPTED = "encrypted"


class ConnectionType(StrEnum):
    STANDARD = "standard"  # for both starttls and unencrypted
    TLS = "tls"
