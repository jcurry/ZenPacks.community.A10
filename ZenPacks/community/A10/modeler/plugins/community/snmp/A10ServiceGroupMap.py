# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
A10ServiceGroupMap
Models service group for A10 devices
"""


# The name of the class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap


class A10ServiceGroupMap(SnmpPlugin):
    """ Map ServiceGroups to A10 Device """
    maptype = "A10ServiceGroupMap"
    modname = "ZenPacks.community.A10.A10ServiceGroup"
    relname = "a10ServiceGroups"


    # axServiceGroupEntry = 1.3.6.1.4.1.22610.2.4.3.3.1.2.1

    snmpGetTableMaps = (
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
        )

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s", self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        # If no data supplied then simply return
        axServiceGrouptable = tabledata.get('axServiceGroupEntry')
        axServiceGroupMemberStattable = tabledata.get('axServiceGroupMemberStatEntry')
        if not axServiceGrouptable:
            log.warn(' No SNMP response from %s for the %s plugin  for ServiceGroup Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        for oid, data in axServiceGrouptable.items():
            try:
                om=self.objectMap(data)
                # prepId santises names if they have odd characters....
                om.id = self.prepId(om.ServiceGroupName)
                om.ServiceGroupName = self.prepId(om.ServiceGroupName)
                om.ServiceGroupDisplayStatusString = self.operatingStateLookup[om.ServiceGroupDisplayStatus]
                om.ServiceGroupTypeString = self.typeLookup[om.ServiceGroupType]
                # Now index into the axServiceGroupMemberStatEntry table to get server and port 
                for oid1, data1 in axServiceGroupMemberStattable.items():
                    if data['ServiceGroupName'] == data1['axServiceGroupMemberStatName']:
                        om.ServiceGroupServer = data1['axServerNameInServiceGroupMemberStat']
                        om.ServiceGroupPort = data1['axServerPortNumInServiceGroupMemberStat']
                        # Also set snmpindex to index into axServiceGroupMemberStatEntry
                        om.snmpindex = oid1.strip('.')

                #log.debug( 'om is %s \n' % (om))

            except (KeyError, IndexError, AttributeError, TypeError), errorInfo:
                log.warn( ' Error in A10ServiceGroupMap modeler plugin %s', errorInfo)
                continue

            rm.append(om)
            #log.debug('rm %s' % (rm) )
        return rm


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

