# This file is the conventional place for "Info" adapters. Info adapters are
# a crucial part of the Zenoss API and therefore the web interface for any
# custom classes delivered by your ZenPack. Examples of custom classes that
# will almost certainly need info adapters include datasources, custom device
# classes and custom device component classes.

# Mappings of interfaces (interfaces.py) to concrete classes and the factory
# (these info adapter classes) used to create info objects for them are managed
# in the configure.zcml file.

from zope.component import adapts
from zope.interface import implements

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info

from ZenPacks.community.A10.A10Server import A10Server
from ZenPacks.community.A10.A10VirtualServer import A10VirtualServer
from ZenPacks.community.A10.A10ServiceGroup import A10ServiceGroup
from ZenPacks.community.A10 import interfaces

class A10VirtualServerInfo(ComponentInfo):
    implements(interfaces.IA10VirtualServerInfo)
    adapts(A10VirtualServer)

    VirtualServerName = ProxyProperty("VirtualServerName")
    VirtualServerAddress = ProxyProperty("VirtualServerAddress")
    VirtualServerEnabled = ProxyProperty("VirtualServerEnabled")
    VirtualServerDisplayStatus = ProxyProperty("VirtualServerDisplayStatus")
    VirtualServerDisplayStatusString = ProxyProperty("VirtualServerDisplayStatusString")
    VirtualServerPortNum = ProxyProperty("VirtualServerPortNum")
    VirtualServerPortType = ProxyProperty("VirtualServerPortType")
    VirtualServerPortTypeString = ProxyProperty("VirtualServerPortTypeString")
    VirtualServerPortEnabled = ProxyProperty("VirtualServerPortEnabled")
    VirtualServerPortEnabledString = ProxyProperty("VirtualServerPortEnabledString")
    VirtualServerPortServiceGroup = ProxyProperty("VirtualServerPortServiceGroup")
    VirtualServerServiceGroupList = ProxyProperty("VirtualServerServiceGroupList")
    snmpindex = ProxyProperty("snmpindex")
    id = ProxyProperty("id")

    @property
    @info
    def VirtualServerServiceGroupObjectList(self):
        VsSgObjsList = []
        dev = self._object.a10Device()
        for sgo in dev.a10ServiceGroups():
            if sgo.ServiceGroupName in self._object.VirtualServerServiceGroupList:
                VsSgObjsList.append(sgo)
        return VsSgObjsList

class A10ServiceGroupInfo(ComponentInfo):
    implements(interfaces.IA10ServiceGroupInfo)
    adapts(A10ServiceGroup)

    ServiceGroupName = ProxyProperty("ServiceGroupName")
    ServiceGroupType = ProxyProperty("ServiceGroupType")
    ServiceGroupTypeString = ProxyProperty("ServiceGroupTypeString")
    ServiceGroupDisplayStatus = ProxyProperty("ServiceGroupDisplayStatus")
    ServiceGroupDisplayStatusString = ProxyProperty("ServiceGroupDisplayStatusString")
    ServiceGroupServerList = ProxyProperty("ServiceGroupServerList")
    ServiceGroupServer = ProxyProperty("ServiceGroupServer")
    ServiceGroupPort = ProxyProperty("ServiceGroupPort")
    #a10VirtualServer_name = ProxyProperty("a10VirtualServer_name")
    snmpindex = ProxyProperty("snmpindex")

    @property
    @info
    def ServiceGroupServerObjectList(self):
        SgSObjsList = []
        dev = self._object.a10Device()
        for so in dev.a10Servers():
            if so.ServerName in self._object.ServiceGroupServerList:
                SgSObjsList.append(so)
        return SgSObjsList


class A10ServerInfo(ComponentInfo):
    implements(interfaces.IA10ServerInfo)
    adapts(A10Server)

    ServerName = ProxyProperty("ServerName")
    ServerAddress = ProxyProperty("ServerAddress")
    ServerHealthMonitor = ProxyProperty("ServerHealthMonitor")
    ServerEnabledState = ProxyProperty("ServerEnabledState")
    ServerMonitorState = ProxyProperty("ServerMonitorState")
    #a10ServiceGroup_name = ProxyProperty("a10ServiceGroup_name")
    #a10VirtualServer_name = ProxyProperty("a10VirtualServer_name")
    snmpindex = ProxyProperty("snmpindex")

