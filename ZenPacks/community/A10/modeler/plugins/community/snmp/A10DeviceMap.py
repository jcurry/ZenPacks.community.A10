##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 April 2nd 2015
# Revised:		
#
# A10Device modeler plugin
#
# This program can be used under the GNU General Public License version 2
#
##########################################################################

__doc__ = """A10DeviceMap

Gather information from A10 devices.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.plugins.DataMaps import ObjectMap


class A10DeviceMap(SnmpPlugin):
    maptype = "A10DeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.22610.2.4.1.6.2.0' : '_serialNumber',
        '.1.3.6.1.4.1.22610.2.4.1.2.1.0': '_totalMemory',
        '.1.3.6.1.4.1.22610.2.4.1.2.2.0': 'memoryUsed',
        '.1.3.6.1.2.1.1.1.0' : '_snmpDescr',
        '.1.3.6.1.2.1.1.2.0' : '_snmpOid',


         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not getdata:
            log.warn(' No SNMP response from %s for the %s plugin ' % ( device.id, self.name() ) )
            return
        maps = []
        OSModelDict = {
                '1.3.6.1.4.1.22610.1.3' : 'a10AX',
                '1.3.6.1.4.1.22610.1.3.1' : 'a10AX2100',
                '1.3.6.1.4.1.22610.1.3.2' : 'a10AX3100',
                '1.3.6.1.4.1.22610.1.3.3' : 'a10AX3200',
                '1.3.6.1.4.1.22610.1.3.4' : 'a10AX2200',
                '1.3.6.1.4.1.22610.1.3.5' : 'a10AX2000',
                '1.3.6.1.4.1.22610.1.3.6' : 'a10AX1000',
                '1.3.6.1.4.1.22610.1.3.7' : 'a10AX5200',
                '1.3.6.1.4.1.22610.1.3.8' : 'a10AX2500',
                '1.3.6.1.4.1.22610.1.3.9' : 'a10AX2600',
                '1.3.6.1.4.1.22610.1.3.10' : 'a10AX3000',
                '1.3.6.1.4.1.22610.1.3.11' : 'a10HitachiBladeServer',
                '1.3.6.1.4.1.22610.1.3.12' : 'a10AX5100',
                '1.3.6.1.4.1.22610.1.3.13' : 'a10SoftAX',
                '1.3.6.1.4.1.22610.1.3.14' : 'a10AX3030',
                '1.3.6.1.4.1.22610.1.3.15' : 'a10AX1030',
                '1.3.6.1.4.1.22610.1.3.16' : 'a10AX3200-12',
                '1.3.6.1.4.1.22610.1.3.17' : 'a10AX3400',
                '1.3.6.1.4.1.22610.1.3.18' : 'a10AX3530',
                '1.3.6.1.4.1.22610.1.3.19' : 'a10AX5630',
                '1.3.6.1.4.1.22610.1.3.20' : 'a10TH6430',
                '1.3.6.1.4.1.22610.1.3.21' : 'a10TH5430',
                '1.3.6.1.4.1.22610.1.3.22' : 'a10TH3030S',
                '1.3.6.1.4.1.22610.1.3.23' : 'a10TH1030S',
                '1.3.6.1.4.1.22610.1.3.24' : 'a10TH930S',
                '1.3.6.1.4.1.22610.1.3.25' : 'a10TH4430',
                '1.3.6.1.4.1.22610.1.3.26' : 'a10TH5330',
                '1.3.6.1.4.1.22610.1.3.27' : 'a10TH4330',
                '1.3.6.1.4.1.22610.1.3.28' : 'a10TH5630',
                '1.3.6.1.4.1.22610.1.3.29' : 'a10TH6630',
            }

        #om = self.objectMap(getdata)
        try:
    	    serialNumber = getdata.get('_serialNumber', None)
            # SNMP memory values are in KB - convert to bytes
	    memoryUsed = getdata.get('memoryUsed', None) * 1024
            # Default map is A10DeviceMap (in maptype statement at top)
	    maps.append(ObjectMap({'setHWSerialNumber': serialNumber}))
	    maps.append(ObjectMap({'memoryUsed': memoryUsed}))
            # Get Hw Model
            manufacturer = 'Raksha Networks Inc.'
            HwModel = getdata.get('_snmpOid', None)
            log.info(' HwModel is %s \n' % (HwModel))
            if HwModel:
                try:
                    model = OSModelDict[HwModel.strip('.')]
                except:
                    model = None
                    pass
                log.info(' Model is %s \n' % (model))
                if model:
                    model = manufacturer + '  ' + model
                    maps.append(ObjectMap({'setHWProductKey' : MultiArgs(model, manufacturer)}))

            SwModel = getdata.get('_snmpDescr', None)
            if SwModel:
                maps.append(ObjectMap({'setOSProductKey' : MultiArgs(SwModel, manufacturer)}))

            # totalMemory is part of the standard os component so compname is added to next maps.append
	    maps.append(ObjectMap({ 'totalMemory': getdata['_totalMemory'] * 1024}, compname='hw'))

        except (KeyError, IndexError, AttributeError, TypeError), errorInfo:
            log.warn( ' Error in %s modeler plugin %s' % ( self.name(), errorInfo))

        return maps

