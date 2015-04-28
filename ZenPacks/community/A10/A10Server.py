from Products.ZenRelations.RelSchema import ToManyCont, ToOne, ToMany
from Globals import InitializeClass
from .A10Component import A10Component

class A10Server(A10Component):
    meta_type = portal_type = "A10Server"

    ServerName = None
    ServerAddress = None
    ServerHealthMonitor = None
    ServerEnabledState = 0
    ServerMonitorState = 0
    ServerServiceGroupList = []
    ServerVirtualServerList = []

    _properties = A10Component._properties + (
        {'id':'snmpindex', 'type':'string', 'mode':''},
        {'id': 'ServerName', 'type': 'string', 'mode': ''},
        {'id': 'ServerAddress', 'type': 'string', 'mode': ''},
        {'id': 'ServerHealthMonitor', 'type': 'string', 'mode': ''},
        {'id': 'ServerEnabledState', 'type': 'int', 'mode': ''},
        {'id': 'ServerMonitorState', 'type': 'int', 'mode': ''},
        {'id': 'ServerServiceGroupList', 'type': 'lines', 'mode': ''},
        {'id': 'ServerVirtualServerList', 'type': 'lines', 'mode': ''},
    )

    _relations = A10Component._relations + (
        ('a10Device', ToOne(ToManyCont,
            'ZenPacks.community.A10.A10Device',
            'a10Servers',
            ),
        ),
        ('a10SServiceGroups', ToMany(ToMany,
            'ZenPacks.community.A10.A10ServiceGroup',
            'a10SgServers',
            ),
        ),
        ('a10SVirtualServers', ToMany(ToMany,
            'ZenPacks.community.A10.A10VirtualServer',
            'a10VsServers',
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

    """
    @property
    def a10VirtualServer_name(self):
        return self.a10ServiceGroup().a10VirtualServer().title

    @property
    def a10ServiceGroup_name(self):
        return self.a10ServiceGroup().title
    """


InitializeClass(A10Server)

