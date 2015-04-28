from Products.Zuul.form import schema
from Products.Zuul.interfaces.component import IComponentInfo

# ZuulMessageFactory is the translation layer. You will see strings intended to
# been seen in the web interface wrapped in _t(). This is so that these strings
# can be automatically translated to other languages.
from Products.Zuul.utils import ZuulMessageFactory as _t

# In Zenoss 3 we mistakenly mapped TextLine to Zope's multi-line text
# equivalent and Text to Zope's single-line text equivalent. This was
# backwards so we flipped their meanings in Zenoss 4. The following block of
# code allows the ZenPack to work properly in Zenoss 3 and 4.

# Until backwards compatibility with Zenoss 3 is no longer desired for your
# ZenPack it is recommended that you use "SingleLineText" and "MultiLineText"
# instead of schema.TextLine or schema.Text.
from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION
from Products.ZenUtils.Version import Version
if Version.parse('Zenoss %s' % ZENOSS_VERSION) >= Version.parse('Zenoss 4'):
    SingleLineText = schema.TextLine
    MultiLineText = schema.Text
else:
    SingleLineText = schema.Text
    MultiLineText = schema.TextLine

class IA10VirtualServerInfo(IComponentInfo):
    VirtualServerName = SingleLineText(title=_t(u"Name"))
    VirtualServerAddress = SingleLineText(title=_t(u"Address"))
    VirtualServerEnabled = schema.Int(title=_t(u"Enabled"))
    VirtualServerDisplayStatus = schema.Int(title=_t(u"Status"))
    VirtualServerDisplayStatusString = SingleLineText(title=_t(u"Status String"))
    VirtualServerPortNum = schema.Int(title=_t(u"Port Num."))
    VirtualServerPortType = schema.Int(title=_t(u"Port Type"))
    VirtualServerPortTypeString = SingleLineText(title=_t(u"Port Type String"))
    VirtualServerPortEnabled = schema.Int(title=_t(u"Port Enabled"))
    VirtualServerPortEnabledString = SingleLineText(title=_t(u"Port Enabled String"))
    VirtualServerPortServiceGroup = SingleLineText(title=_t(u"Service Group"))
    VirtualServerServiceGroupList = schema.List(title=_t(u"Service Group List"))
    snmpindex = SingleLineText(title=_t(u"snmp index"))
    id = SingleLineText(title=_t(u"Id"))
    VirtualServerServiceGroupObjectList = schema.Entity(_t(u"Service Group Object List"))


class IA10ServiceGroupInfo(IComponentInfo):
    ServiceGroupName = SingleLineText(title=_t(u"Service Group Name"))
    ServiceGroupType = schema.Int(title=_t(u"Service Group Type"))
    ServiceGroupTypeString = SingleLineText(title=_t(u"Service Group TypeString"))
    ServiceGroupDisplayStatus = schema.Int(title=_t(u"Service Group Status"))
    ServiceGroupDisplayStatusString = SingleLineText(title=_t(u"Service Group StatusString"))
    ServiceGroupServerList = schema.List(_t(u"Server List"))
    ServiceGroupServer = SingleLineText(title=_t(u"Service Group Server"))
    ServiceGroupPort = schema.Int(title=_t(u"Service Group Port"))
    #a10VirtualServer = schema.Entity(_t(u"Virtual Server"))
    snmpindex = SingleLineText(title=_t(u"snmp index"))
    ServiceGroupServerObjectList = schema.Entity(_t(u"Servers Object List"))

class IA10ServerInfo(IComponentInfo):
    ServerName = SingleLineText(title=_t(u"Server Name"))
    ServerAddress = SingleLineText(title=_t(u"Server Address"))
    ServerHealthMonitor = SingleLineText(title=_t(u"Health Monitor"))
    ServerEnabledState = schema.Int(title=_t(u"Server Enabled"))
    ServerMonitorState = schema.Int(title=_t(u"Server Monitoring State"))
    #a10ServiceGroup = schema.Entity(title=_t(u"Service Group"))
    #a10VirtualServer = schema.Entity(title=_t(u"Virtual Server"))
    snmpindex = SingleLineText(title=_t(u"snmp index"))

