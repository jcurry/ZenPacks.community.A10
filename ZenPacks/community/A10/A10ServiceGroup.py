from .A10Component import A10Component
from Products.ZenRelations.RelSchema import ToManyCont, ToOne, ToMany
from Globals import InitializeClass

class A10ServiceGroup(A10Component):
    meta_type = portal_type = "A10ServiceGroup"

    ServiceGroupName = None
    ServiceGroupType = 0
    ServiceGroupTypeString = None
    ServiceGroupDisplayStatus = 0
    ServiceGroupDisplayStatusString = None
    ServiceGroupServer = None
    ServiceGroupPort = 0
    ServiceGroupVirtualServerList = []
    ServiceGroupServerList = []
    ServiceGroupServerObjectList = []

    _properties = A10Component._properties + (
        {'id':'snmpindex', 'type':'string', 'mode':''},
        {'id': 'ServiceGroupName', 'type': 'string', 'mode': ''},
        {'id': 'ServiceGroupType', 'type': 'int', 'mode': ''},
        {'id': 'ServiceGroupTypeString', 'type': 'string', 'mode': ''},
        {'id': 'ServiceGroupDisplayStatus', 'type': 'int', 'mode': ''},
        {'id': 'ServiceGroupDisplayStatusString', 'type': 'string', 'mode': ''},
        {'id': 'ServiceGroupServer', 'type': 'string', 'mode': ''},
        {'id': 'ServiceGroupPort', 'type': 'int', 'mode': ''},
        {'id': 'ServiceGroupVirtualServerList', 'type': 'lines', 'mode': ''},
        {'id': 'ServiceGroupServerList', 'type': 'lines', 'mode': ''},
        {'id': 'ServiceGroupServerObjectList', 'type': 'lines', 'mode': ''},
    )

    _relations = A10Component._relations + (
        ('a10Device', ToOne(ToManyCont,
            'ZenPacks.community.A10.A10Device',
            'a10ServiceGroups',
            ),
        ),
        ('a10SgServers', ToMany(ToMany,
            'ZenPacks.community.A10.A10Server',
            'a10SServiceGroups',
            ),
        ),
        ('a10SgVirtualServers', ToMany(ToMany,
            'ZenPacks.community.A10.A10VirtualServer',
            'a10VsServiceGroups',
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
        return self.a10VirtualServer().title
    """

InitializeClass(A10ServiceGroup)

