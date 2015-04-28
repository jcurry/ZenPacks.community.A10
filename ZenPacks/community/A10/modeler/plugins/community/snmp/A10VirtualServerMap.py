# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
A10VirtualServerMap
Models virtual servers for a A10 devices
"""


# The name of the class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap


class A10VirtualServerMap(SnmpPlugin):
    """ Map VirtualServers to A10 Device """
    maptype = "A10VirtualServerMap"
    modname = "ZenPacks.community.A10.A10VirtualServer"
    relname = "a10VirtualServers"


    # axVirtualServerEntry = 1.3.6.1.4.1.22610.2.4.3.4.1.2.1

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
                    '.9'  : 'VirtualServerStatCurrCons',
                }
            ),
        )

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s", self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        # If no data supplied then simply return
        axVirtualServertable = tabledata.get('axVirtualServerEntry')
        axVirtualServerStattable = tabledata.get('axVirtualServerStatEntry')
        if not axVirtualServertable:
            log.warn(' No SNMP response from %s for the %s plugin  for VirtualServer Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        for oid, data in axVirtualServertable.items():
            try:
                om=self.objectMap(data)
                # prepId santises names if they have odd characters....
                om.id = self.prepId(om.VirtualServerName)
                om.VirtualServerName = self.prepId(om.VirtualServerName)
                om.VirtualServerDisplayStatusString = self.operatingStateLookup[om.VirtualServerDisplayStatus]
                # Need to set snmpindex with value from VirtualServerStatAddress
                for oid1, data1 in axVirtualServerStattable.items():
                    if data['VirtualServerAddress'] == data1['VirtualServerStatAddress']:
                        om.snmpindex = oid1.strip('.')
                #log.debug( 'om is %s \n' % (om))

            except (KeyError, IndexError, AttributeError, TypeError), errorInfo:
                log.warn( ' Error in A10VirtualServerMap modeler plugin %s', errorInfo)
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

