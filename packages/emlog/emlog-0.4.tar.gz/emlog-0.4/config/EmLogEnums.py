from enum import Enum


class EnumLogLevel(Enum):
    Debug = 0
    Trace = 1
    Info = 2
    Warn = 3
    Error = 4
    Fatal = 5


class EnumLogTarget(Enum):
    Console = 0
    File = 1
    Logstash = 2
    Protocol = 3
    Kafka = 4
    Rabbitmq = 5
    Mongo = 6
    Redis = 7
    Couchbase = 8


class EnumLogType(Enum):
    Unknown = 0
    Invoke = 1
    Return = 2
    InvokeAndReturn = 3
    InvokeError = 4
    Ado = 5
    WcfCall = 6
    WebApiCall = 7
    Business = 8
    Aop = 9


class EnumFormatMode(Enum):
    Text = 0
    Json = 1
    JsonIndented = 2


class EnumLogObjType(Enum):
    Text = 0
    Dynamic = 1


class LogCfgToken:
    PeakModeTime = "(2[0-3]|[0-1]?\\d):[0-5]?\\d"
    PeakMode = "{0}-{0}(,{0}-{0})*;[1-9]\\d*;[1-9]\\d*"
