from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE

class A10Component(DeviceComponent, ManagedEntity):
    """
    Abstract base class to avoid repeating boilerplate code in all of the
    DeviceComponent subclasses in this ZenPack.
    """

    # Disambiguate multi-inheritence.
    _properties = ManagedEntity._properties
    _relations = ManagedEntity._relations

    # This makes the "Templates" component display available.
    factory_type_information = ({
        'actions': ({
	'id': 'perfConf',
	'name': 'Template',
	'action': 'objTemplates',
	'permissions': (ZEN_CHANGE_DEVICE,),
        },),
    },)

    # Query for events by id instead of name.
    event_key = "ComponentId"

