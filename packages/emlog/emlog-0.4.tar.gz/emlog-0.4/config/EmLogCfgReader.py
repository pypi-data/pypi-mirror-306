import xml.etree.ElementTree as ET


class EmLogCfgReader:
    config = None

    @staticmethod
    def loadXml():
        EmLogCfgReader.deserialize()

    @staticmethod
    def deserialize():
        tree = ET.parse("EmLog.xml")
        root = tree.getroot()

        enabled = bool(root.get("enabled", default="false"))
        debug = int(root.get("debug", default="0"))
        discardSize = int(root.get("discardSize", default="1048576"))
        discardMemoryRate = float(root.get("discardMemoryRate", default="1"))
        formatConcurrency = int(root.get("formatConcurrency", default="1"))
        ioBufferSize = int(root.get("ioBufferSize", default="8192"))
        ioConcurrency = int(root.get("ioConcurrency", default="4"))
        ioInterval = int(root.get("ioInterval", default="100"))
        clrTimeout = int(root.get("clrTimeout", default="180000"))
        tcpRetryInterval = int(root.get("tcpRetryInterval", default="5000"))
        reportInterval = int(root.get("reportInterval", default="60000"))
        peakMode = EmLogCfgReader.getPeakModeCfg(root.get("peakMode", default=None))
        # deployConfig =
        # variablesConfig =
        # layoutsConfig =
        # targetsConfig =
        # rulesConfig =

    @staticmethod
    def getPeakModeCfg(peakModeStr):

        try:
            if not peakModeStr:
                return None

        except Exception as e:
            print(e)


def generateString():
    return "frankli"

a = generateString()
print(a)
