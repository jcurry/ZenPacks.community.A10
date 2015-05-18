# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
A10Map
Models A10 devices
"""


# The name of the class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap
from Products.ZenUtils.Utils import prepId


class A10Map(SnmpPlugin):
    """ Maps A10 Device """

    snmpGetTableMaps = (
            GetTableMap('axVirtualServerEntry',
                '1.3.6.1.4.1.22610.2.4.3.4.1.2.1',
                {
                    '.1'  : 'VirtualServerName',
                    '.2'  : 'VirtualServerAddress',
                    '.3'  : 'VirtualServerEnabled',
                    '.5'  : 'VirtualServerDisplayStatus',
                }
            ),
            GetTableMap('axVirtualServerStatEntry',
                '1.3.6.1.4.1.22610.2.4.3.4.2.1.1',
                {
                    '.1'  : 'VirtualServerStatAddress',
                    '.2'  : 'VirtualServerStatName',
                }
            ),
            GetTableMap('axVirtualServerPortEntry',
                '1.3.6.1.4.1.22610.2.4.3.4.3.1.1',
                {
                    '.1'  : 'VirtualServerPortName',
                    '.2'  : 'VirtualServerPortType',
                    '.3'  : 'VirtualServerPortNum',
                    '.4'  : 'VirtualServerPortAddress',
                    '.5'  : 'VirtualServerPortEnabled',
                    '.6'  : 'VirtualServerPortServiceGroup',
                }
            ),
            GetTableMap('axServiceGroupEntry',
                '.1.3.6.1.4.1.22610.2.4.3.3.1.2.1',
                {
                    '.1'  : 'ServiceGroupName',
                    '.2'  : 'ServiceGroupType',
                    '.4'  : 'ServiceGroupDisplayStatus',
                }
            ),
            GetTableMap('axServiceGroupMemberStatEntry',
                '.1.3.6.1.4.1.22610.2.4.3.3.4.1.1',
                {
                    '.1'  : 'axServiceGroupMemberStatName',
                    '.2'  : 'axServiceGroupMemberStatAddrType',
                    '.3'  : 'axServerNameInServiceGroupMemberStat',
                    '.4'  : 'axServerPortNumInServiceGroupMemberStat',
                }
            ),
            GetTableMap('axServerEntry',
                '1.3.6.1.4.1.22610.2.4.3.2.1.2.1',
                {
                    '.1'  : 'ServerName',
                    '.2'  : 'ServerAddress',
                    '.3'  : 'ServerEnabledState',
                    '.4'  : 'ServerHealthMonitor',
                    '.5'  : 'ServerMonitorState',
                }
            ),
            GetTableMap('axServerStatEntry',
                '1.3.6.1.4.1.22610.2.4.3.2.2.2.1',
                {
                    '.1'  : 'ServerStatAddress',
                    '.2'  : 'ServerStatName',
                }
            ),
        )

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s", self.name(), device.id)
        maps = []
        rel_maps = []
        getdata, tabledata = results
        # If no data supplied then simply return
        axVirtualServertable = tabledata.get('axVirtualServerEntry')
        axVirtualServerStattable = tabledata.get('axVirtualServerStatEntry')
        axVirtualServerPorttable = tabledata.get('axVirtualServerPortEntry')
        axServiceGrouptable = tabledata.get('axServiceGroupEntry')
        axServiceGroupMemberStattable = tabledata.get('axServiceGroupMemberStatEntry')
        axServertable = tabledata.get('axServerEntry')
        axServerStattable = tabledata.get('axServerStatEntry')

        # Start with VirtualServer component
        if not axVirtualServertable:
            log.warn(' No SNMP response from %s for the %s plugin  for VirtualServer Table' % ( device.id, self.name() ) )
            log.info( "Data= %s", tabledata )
            return
        if not axVirtualServerStattable:
            log.warn(' No SNMP response from %s for the %s plugin  for VirtualServer Stat Table' % ( device.id, self.name() ) )
            log.info( "Data= %s", tabledata )
            return
        if not axVirtualServerPorttable:
            log.warn(' No SNMP response from %s for the %s plugin  for VirtualServer Port Table' % ( device.id, self.name() ) )
            log.info( "Data= %s", tabledata )
            return

        virtualservers = []
        for oid, data in axVirtualServertable.items():
            vsn = prepId(data['VirtualServerName'])
            vsdata = {
                'id': vsn,
                'VirtualServerName':vsn,
                'VirtualServerAddress': data['VirtualServerAddress'],
                'VirtualServerEnabled': data['VirtualServerEnabled'],
                'VirtualServerDisplayStatus': data['VirtualServerDisplayStatus'],
                'VirtualServerDisplayStatusString': self.operatingStateLookup[data['VirtualServerDisplayStatus']],
            }
            # snmpindex is into the axVirtualServerStat table
            for oid1, data1 in axVirtualServerStattable.items():
                if data['VirtualServerAddress'] == data1['VirtualServerStatAddress']:
                    vsdata['snmpindex'] = oid1.strip('.')
                    break
            serviceGroupList = []
            for oid2, data2 in axVirtualServerPorttable.items():
                if data['VirtualServerName'] == data2['VirtualServerPortName']:
                    portNum = data2['VirtualServerPortNum']
                    # Set the id to be <VirtualServerName>_<VirtualServerPort>
                    vsdata['id'] = vsn + '_' + str(portNum)
                    #vsdata['VirtualServerPortNum'] = portNum
                    #vsdata['VirtualServerPortType'] = data2['VirtualServerPortType']
                    #try:
                    #    vsdata['VirtualServerPortTypeString'] = self.vsPortTypeLookup[data2['VirtualServerPortType']]
                    #except:
                    #    vsdata['VirtualServerPortTypeString'] = 0
                    #    continue
                    #vsdata['VirtualServerPortEnabled'] = data2['VirtualServerPortEnabled']
                    #vsdata['VirtualServerPortEnabledString'] = self.operatingStateLookup[data2['VirtualServerPortEnabled']]
                    vsdata['VirtualServerPortServiceGroup'] = data2['VirtualServerPortServiceGroup']
                    serviceGroupList.append(data2['VirtualServerPortServiceGroup'])
            vsdata['VirtualServerServiceGroupList'] = serviceGroupList 
       
            virtualservers.append(ObjectMap(vsdata))

        maps.append(RelationshipMap(
            relname='a10VirtualServers',
            modname = 'ZenPacks.community.A10.A10VirtualServer',
            objmaps = virtualservers))

        # Now do ServiceGroups

        if not axServiceGrouptable:
            log.warn(' No SNMP response from %s for the %s plugin  for ServiceGroup Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        if not axServiceGroupMemberStattable:
            log.warn(' No SNMP response from %s for the %s plugin  for axServiceGroupMemberStattable Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        servicegroups = []
        for oid, data in axServiceGrouptable.items():
	    sgn = prepId(data['ServiceGroupName'])
	    sgdata = {
		'id': sgn,
		'ServiceGroupName': sgn,
		'ServiceGroupType': data['ServiceGroupType'],
		'ServiceGroupDisplayStatusString': self.operatingStateLookup[data['ServiceGroupDisplayStatus']],
		'ServiceGroupTypeString': self.typeLookup[data['ServiceGroupType']],
	    }
	    # Now index into the axServiceGroupMemberStatEntry table to get servers and ports
	    serverPortList = []
	    serverList = []

	    # Also set snmpindex to index into axServiceGroupStatEntry
	    sgdata['snmpindex'] = oid.strip('.')

	    for oid1, data1 in axServiceGroupMemberStattable.items():
		if data['ServiceGroupName'] == data1['axServiceGroupMemberStatName']:
		    #sgdata['ServiceGroupServer'] = data1['axServerNameInServiceGroupMemberStat']
		    #sgdata['ServiceGroupPort'] = data1['axServerPortNumInServiceGroupMemberStat']
		    serverPortList.append((data1['axServerNameInServiceGroupMemberStat'], str(data1['axServerPortNumInServiceGroupMemberStat'])))
                    serverList.append(data1['axServerNameInServiceGroupMemberStat'])
	    serverPortString = ''
	    for sp in serverPortList:
		serverPortString = serverPortString + ','.join(sp) + ','
	    sgdata['ServiceGroupServer'] = serverPortString
            sgdata['ServiceGroupServerList'] = serverList
	    servicegroups.append(ObjectMap(sgdata))

        maps.append(RelationshipMap(
            relname='a10ServiceGroups',
            modname='ZenPacks.community.A10.A10ServiceGroup',
            objmaps=servicegroups))

        # Now do Servers

        if not axServertable:
            log.warn(' No SNMP response from %s for the %s plugin  for axServertable Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        if not axServerStattable:
            log.warn(' No SNMP response from %s for the %s plugin  for axServerStattable Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        servers = []
        for oid, data in axServertable.items():
            sn = prepId(data['ServerName'])
	    sdata = {
		'id': sn,
		'ServerName': sn,
		'ServerAddress': data['ServerAddress'],
		'ServerEnabledState': data['ServerEnabledState'],
		'ServerHealthMonitor': data['ServerHealthMonitor'],
		'ServerMonitorState': data['ServerMonitorState'],
		}
		#Set the snmpindex to index into the ServerStat table, not the Server table
	    for oid1, data1 in axServerStattable.items():
		if data['ServerAddress'] == data1['ServerStatAddress']:
		    sdata['snmpindex'] = oid1.strip('.')
		    break
	    servers.append(ObjectMap(sdata))

        maps.append(RelationshipMap(
            relname='a10Servers',
            modname='ZenPacks.community.A10.A10Server',
            objmaps=servers))
  
        # Finished all 3 components

        return maps

    operatingStateLookup = { 0: 'Unknown',
                             1: 'All Up',
                             2: 'Functionally Up',
                             3: 'Partially Up',
                             4: 'Stopped'
                           }


    typeLookup = { 0: 'Unknown',
                   1: 'firewall',
                   2: 'tcp',
                   3: 'udp'
                 }

    vsPortTypeLookup = { 0: 'Unknown',
                   1: 'firewall',
                   2: 'tcp',
                   3: 'udp',
                   5: 'others',
                   8: 'rtsp',
                   9: 'ftp',
                   10: 'mms',
                   11: 'sip',
                   12: 'fastHTTP',
                   14: 'http',
                   15: 'https',
                   16: 'sslProxy',
                   17: 'smtp',
                   18: 'sip-TCP',
                   19: 'sips',
                   22: 'dns'
                 }

