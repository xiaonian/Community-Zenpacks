# ==============================================================================
# IBMIMMComponentVpdMap modeler plugin
#
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 1.0
#
# (C) Copyright IBM Corp. 2011. All Rights Reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ==============================================================================

__doc__="""IBMIMMComponentVpdMap maps chassis component VPD entries associated with an IMM"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "1.0.0"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class IBMIMMComponentVpdMap(SnmpPlugin):

    relname = "IMMCOMPVPD"
    modname = "ZenPacks.community.IBMSystemxIMM.IMMComponentVpd"

    columns = {
               '.1': 'componentLevelVpdIndex',
               '.2': 'componentLevelVpdFruNumber',
               '.3': 'componentLevelVpdFruName',
               '.4': 'componentLevelVpdSerialNumber',
               '.5': 'componentLevelVpdManufacturingId',
              }

    # snmpGetTableMaps gets tabular data
    snmpGetTableMaps = (
        # Chassis component VPD table
        GetTableMap('systemComponentLevelVpdEntry', '.1.3.6.1.4.1.2.3.51.3.1.5.18.1', columns),
    )
	   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        # Collect the data from device
        getdata, tabledata = results
        
        # Debug: print data retrieved from device.
        log.debug( "Get data = %s", getdata )
        log.debug( "Table data = %s", tabledata )

        VpdTable = tabledata.get("systemComponentLevelVpdEntry")

        # If no data retrieved return nothing.
        if not VpdTable:
            log.warn( 'No data collected from %s for the %s plugin', device.id, self.name() )
            log.debug( "Data = %s", getdata )
            log.debug( "Columns = %s", self.columns )
            return

        rm = self.relMap()
	   
        for oid, data in VpdTable.items():
            om = self.objectMap(data)
            om.id = self.prepId(om.componentLevelVpdFruName)
            om.componentLevelVpdIndex = int(om.componentLevelVpdIndex)

            # Debug: print values of object map.
#           for key,value in om.__dict__.items():
#              log.warn("om key=value: %s = %s", key,value)
	    
            rm.append(om) 
        return rm
