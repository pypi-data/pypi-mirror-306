class EmLogCfg:
    def __init__(self, enabled, debug, discardSize, discardMemoryRate, formatConcurrency,
                 ioBufferSize, ioConcurrency, ioInterval, clrTimeout, tcpRetryInterval, reportInterval, peakMode,
                 hasReportRule, hasFileTarget, deploy, variables, layouts, targets, rules):
        self.enabled = enabled
        self.debug = debug
        self.discardSize = discardSize
        self.discardMemoryRate = discardMemoryRate
        self.formatConcurrency = formatConcurrency
        self.ioBufferSize = ioBufferSize
        self.ioConcurrency = ioConcurrency
        self.ioInterval = ioInterval
        self.clrTimeout = clrTimeout
        self.tcpRetryInterval = tcpRetryInterval
        self.reportInterval = reportInterval
        self.peakMode = peakMode
        self.hasReportRule = hasReportRule
        self.hasFileTarget = hasFileTarget
        self.deploy = deploy
        self.variables = variables
        self.layouts = layouts
        self.targets = targets
        self.rules = rules


class PeakModeCfg:
    def __init__(self, isOnPeakMode, peakModeLogCnt, peakModeSleepMs):
        self.isOnPeakMode = isOnPeakMode
        self.peakModeLogCnt = peakModeLogCnt
        self.peakModeSleepMs = peakModeSleepMs


class DeployCfg:
    def __init__(self, appID, envType, zoneID):
        self.appID = appID
        self.envType = envType
        self.zoneID = zoneID


class VariableCfgItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class LayoutCfgItem:
    def __init__(self, type, name, oriFormat, lineBreak, maxLength, encoding, formatMode, format):
        self.type = type
        self.name = name
        self.oriFormat = oriFormat
        self.lineBreak = lineBreak
        self.maxLength = maxLength
        self.encoding = encoding
        self.formatMode = formatMode
        self.format = format


class TargetCfgItem:
    def __init__(self, layout, name, fileName, address, fixed, path, dateExp):
        self.layout = layout
        self.name = name
        self.fileName = fileName
        self.address = address
        self.fixed = fixed
        self.path = path
        self.dateExp = dateExp


class RuleCfgItem:
    def __init__(self, name, minLevel, maxLevel, writeTo, isFinal):
        self.name = name
        self.minLevel = minLevel
        self.maxLevel = maxLevel
        self.writeTo = writeTo
        self.isFinal = isFinal
