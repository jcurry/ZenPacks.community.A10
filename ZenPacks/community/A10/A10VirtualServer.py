from .A10Component import A10Component
from Products.ZenRelations.RelSchema import ToManyCont, ToOne, ToMany
from Globals import InitializeClass

class A10VirtualServer(A10Component):
    meta_type = portal_type = "A10VirtualServer"

    VirtualServerName = None
    VirtualServerAddress = None
    VirtualServerEnabled = 0
    VirtualServerDisplayStatus = 0
    VirtualServerDisplayStatusString = None
    VirtualServerPortNum = 0
    VirtualServerPortType = 0
    VirtualServerPortTypeString = None
    VirtualServerPortEnabled = 0
    VirtualServerPortEnabledString = None
    VirtualServerPortServiceGroup = None
    VirtualServerServiceGroupList = []
    VirtualServerServiceGroupObjectList = []
    VirtualServerServerList = []

    _properties = A10Component._properties + (
        {'id':'snmpindex', 'type':'string', 'mode':''},
        {'id': 'VirtualServerName', 'type': 'string', 'mode': ''},
        {'id': 'VirtualServerAddress', 'type': 'string', 'mode': ''},
        {'id': 'VirtualServerEnabled', 'type': 'int', 'mode': ''},
        {'id': 'VirtualServerDisplayStatus', 'type': 'int', 'mode': ''},
        {'id': 'VirtualServerDisplayStatusString', 'type': 'string', 'mode': ''},
        {'id': 'VirtualServerPortNum', 'type': 'int', 'mode': ''},
        {'id': 'VirtualServerPortType', 'type': 'int', 'mode': ''},
        {'id': 'VirtualServerPortTypeString', 'type': 'string', 'mode': ''},
        {'id': 'VirtualServerPortEnabled', 'type': 'int', 'mode': ''},
        {'id': 'VirtualServerPortEnabledString', 'type': 'string', 'mode': ''},
        {'id': 'VirtualServerPortServiceGroup', 'type': 'string', 'mode': ''},
        {'id': 'VirtualServerServiceGroupList', 'type': 'lines', 'mode': ''},
        {'id': 'VirtualServerServiceGroupObjectList', 'type': 'lines', 'mode': ''},
        {'id': 'VirtualServerServerList', 'type': 'lines', 'mode': ''},
    )

    _relations = A10Component._relations + (
        ('a10Device', ToOne(ToManyCont,
            'ZenPacks.community.A10.A10Device',
            'a10VirtualServers',
            ),
        ),
        ('a10VsServiceGroups', ToMany(ToMany,
            'ZenPacks.community.A10.A10ServiceGroup',
            'a10SgVirtualServers',
            ),
        ),
        ('a10VsServers', ToMany(ToMany,
            'ZenPacks.community.A10.A10Server',
            'a10SVirtualServers',
            ),
        ),
    )

    # Custom components must always implement the device method. The method
    # should return the device object that contains the component.
    def device(self):
        return self.a10Device()

    def viewName(self):
        """Pretty version human readable version of this object"""
        return self.id


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName

InitializeClass(A10VirtualServer)

