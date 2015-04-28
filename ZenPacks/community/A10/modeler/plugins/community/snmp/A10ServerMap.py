# Module-level documentation will automatically be shown as additional
# information for the modeler plugin in the web interface.
"""
A10ServerMap
Models servers for a A10 devices
"""


# The name of the class within this file must match the filename.

# SnmpPlugin is the base class that provides lots of help in modeling data
# that's available over SNMP.
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap


class A10ServerMap(SnmpPlugin):
    """ Map Servers to A10 Device """
    maptype = "A10ServerMap"
    modname = "ZenPacks.community.A10.A10Server"
    relname = "a10Servers"


    # axServerEntry = 1.3.6.1.4.1.22610.2.4.3.2.1.2.1

    snmpGetTableMaps = (
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
        )

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s", self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        # If no data supplied then simply return
        axServertable = tabledata.get('axServerEntry')
        if not axServertable:
            log.warn(' No SNMP response from %s for the %s plugin  for Server Table' % ( device.id, self.name() ) )
            log.warn( "Data= %s", tabledata )
            return

        for oid, data in axServertable.items():
            try:
                om=self.objectMap(data)
                # prepId santises names if they have odd characters....
                om.id = self.prepId(om.ServerName)
                om.ServerName = self.prepId(om.ServerName)
                om.snmpindex = oid.strip('.')
                log.debug( 'om is %s \n' % (om))

            except (KeyError, IndexError, AttributeError, TypeError), errorInfo:
                log.warn( ' Error in A10ServerMap modeler plugin %s', errorInfo)
                continue

            rm.append(om)
            #log.debug('rm %s' % (rm) )
        return rm


