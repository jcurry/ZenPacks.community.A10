from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Globals import InitializeClass
from copy import deepcopy


class A10Device(Device):
    """
    A10 device subclass. In this case the reason for creating a subclass of
    device is to add a new type of relation. We want many "A10ServiceGroup" and "A10VirtualServer"
    components to be associated with each of these devices.

    If you set the zPythonClass of a device class to
    ZenPacks.community.A10Device, any devices created or moved
    into that device class will become this class and be able to contain
    A10ServiceGroups and A10VirtualServers.
    """

    meta_type = portal_type = 'A10Device'

    memoryUsed= 0

    _properties = Device._properties + (
        {'id':'memoryUsed', 'type':'int', 'mode':''},
        )

    # This is where we extend the standard relationships of a device to add
    # the "a10Servers", "a10ServiceGroups" and "a10VirtualServers" relationships that must be filled with components
    # of our custom "A10Server", "A10ServiceGroup" and "A10VirtualServer" classes.
    _relations = Device._relations + (
        ('a10VirtualServers', ToManyCont(ToOne,
            'ZenPacks.community.A10.A10VirtualServer',
            'a10Device',
            ),
        ),
        ('a10ServiceGroups', ToManyCont(ToOne,
            'ZenPacks.community.A10.A10ServiceGroup',
            'a10Device',
            ),
        ),
        ('a10Servers', ToManyCont(ToOne,
            'ZenPacks.community.A10.A10Server',
            'a10Device',
            ),
        ),
    )

    factory_type_information = deepcopy(Device.factory_type_information)


    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(A10Device)


