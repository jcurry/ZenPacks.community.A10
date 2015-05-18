=====================================
ZenPack to support A10 load balancers
=====================================

Description
===========
This ZenPack supports A10 load balancers.

It creates new component types for:
    * Virtual Server
    * Service Group
    * Server

Each of these components are direct subcomponents of the A10Device type.  

There are ManyToMany relationships between each of the subcomponents though these are not
currently modeled.

The /Network/A10 device class is supplied with appropriate zProperties, modeler plugins
and templates applied.

Two modeler plugins are supplied:
    * A10DeviceMap      sets total memory, serial number and Hardware / software manufcaturer / model
    * A10Map            models the virtual servers, service groups and servers

A device template, A10MemCpu delivers memory and cpu data and graphs.

Component templates for A10VirtualServer, A10ServiceGroup and A10Server provides data and graphs for these
components with:
    * Packets In
    * Bytes In
    * Packets Out
    * Bytes Out
    * Current connections

The component display for a Virtual Server includes related Service Groups and a dropdown that shows
all Servers.  The component display for a Service Group includes related Servers and a dropdown for all servers.

The following MIBs are included:
    * A10-COMMON-MIB
    * A10-AX-MIB
    * A10-AX-TRAPS
    * A10-AX-NOTIFICATIONS

An A10 Event Class is included with a class transform to provide a more meaningful event summary, based on
data on an incoming A10 Trap / notification.  Three event mappings are provided to provide correlation between
VirtualServerPort Up/Down events and for ServiceGroupMember Up/Down events.  (Note that the devices tested do not
appear to send axServiceGroupMemberDown discrete events (trap 33). You only see trap 32 events with a message that
may have both up and down in the text.  I believe this is an A10 bug).



Requirements & Dependencies
===========================

    * Zenoss Versions Supported: 4.x
    * External Dependencies: 
    * ZenPack Dependencies:
    * Installation Notes: Restart zenoss entirely after installation
    * Configuration:



Download
========
Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 4.0+ `Latest Package for Python 2.7`_

ZenPack installation
======================

This ZenPack can be installed from the .egg file using either the GUI or the
zenpack command line but, since it is demonstration code that you are likely to 
want to modify, it is more likely installed in development mode.  From github - 
https://github.com/jcurry/ZenPacks.community.A10  use the ZIP button
(top left) to download a tgz file and unpack it to a local directory, say,
$ZENHOME/local.  Install from $ZENHOME/local with:

zenpack --link --install ZenPacks.community.A10

Restart zenoss after installation.



Change History
==============
* 1.0.0
   * Initial Release
*1.0.1
   * With all components as direct subcomponents of A10Device
* 1.0.2
   * Added A10 event class with class transform and 3 mappings
   * Updated A10 MIBs
   * Added data sources to component templates for packets / bytes in / out

Screenshots
===========

.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.7: https://github.com/jcurry/ZenPacks.community.A10/blob/master/dist/ZenPacks.community.A10-1.0.2-py2.7.egg?raw=true

