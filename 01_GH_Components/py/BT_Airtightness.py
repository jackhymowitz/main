#
# IDF2PHPP: A Plugin for exporting an EnergyPlus IDF file to the Passive House Planning Package (PHPP). Created by blgdtyp, llc
# 
# This component is part of IDF2PHPP.
# 
# Copyright (c) 2020, bldgtyp, llc <info@bldgtyp.com> 
# IDF2PHPP is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# IDF2PHPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# For a copy of the GNU General Public License
# see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
#
"""
Will calculate the PHPP Envelope Airtightness using the PHPP Rooms as the reference volume. Connect the ouputs from this component to a Honeybee 'setEPZoneLoads' and then set the Infiltration Schedule to 'CONSTANT'. Use a Honeybee 'Constant Schedule' with a value of 1 and a _schedTypeLimit of 'FRACTIONAL', then connect that to an HB 'setEPZoneSchdeules' component.
-
EM Aug. 10, 2020

    Args:
        _HBZones: Honeybee Zones to apply this leakage rate to.
        _n50: (ACH) The target ACH leakage rate
        _q50: (m3/hr-m2-surface) The target leakage rate per m2 of exposed surface area
        _blowerPressure: (Pascal) Blower Door pressure for the airtightness measurement. Default is 50Pa
    Returns:
        _HBZones: Connect to the '_HBZones' input on the Honeybee 'setEPZoneLoads' Component
        infiltrationRatePerFloorArea_: (m3/hr-m2-floor)
        infiltrationRatePerFacadeArea_: (m3/hr-m2-facade) Connect to the 'infilRatePerArea_Facade_' input on the Honeybee 'setEPZoneLoads' Component
"""

ghenv.Component.Name = "BT_Airtightness"
ghenv.Component.NickName = "Airtightness"
ghenv.Component.Message = 'AUG_10_2020'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "BT"
ghenv.Component.SubCategory = "01 | Model"

import scriptcontext as sc
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper.Kernel as ghK
import math

hb_hive = sc.sticky["honeybee_Hive"]()
HBZoneObjects = hb_hive.callFromHoneybeeHive(_HBZones)
infiltrationRatePerFloorArea_ = []
infiltrationRatePerFacadeArea_ = []

# Clean up inputs
n50 = _n50 if _n50 else 0 # ACH
q50 = _q50 if _q50 else 0 # m3/m2-facade
blowerPressure = _blowerPressure if _blowerPressure else 50 # Pa

for zone in HBZoneObjects:
    if 'PHPProoms' not in zone.__dict__.keys():
        msg = "Could not get the Volume for zone: '{}'. Be sure that you\n"\
        "Be sure that you use this component AFTER the 'PHPP Rooms from Rhino' component\n"\
        "and that you have valid 'rooms' in the model in order to determin the volume correctly.".format(zone.name)
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)
        continue
    
    # --------------------------------------------------------------------------
    # Get all the relevant information needed from the zones
    zoneVolume_Vn50 = sum([room.RoomNetClearVolume for room in zone.PHPProoms])
    zoneFloorArea_Gross = zone.getFloorArea()
    zoneVolume_Gross = zone.getZoneVolume()
    zoneExposedSurfaceArea = zone.getExposedArea()
    flowBy_n50 = zoneVolume_Vn50 * n50 / 3600
    flowBy_q50 = zoneExposedSurfaceArea * q50 / 3600
    
    print 'Zone PHPP Room Volumes: {} m3'.format(zoneVolume_Vn50)
    print 'Zone Floor Area (from EP Model): {:.1f} m2'.format(zoneFloorArea_Gross)
    print 'Zone Volume: {:.1f} m3'.format(zoneVolume_Gross)
    print 'Zone Exposed Surface Area: {:.1f} m2'.format(zoneExposedSurfaceArea)
    print 'Zone Infiltration Flow by n50: {:.1f} m3/hr ({:.4f} m3/s) @ 50Pa'.format(flowBy_n50*60*60, flowBy_n50)
    print 'Zone Infiltration Flow by q50: {:.1f} m3/hr ({:.4f} m3/s) @ 50Pa'.format(flowBy_q50*60*60, flowBy_q50)
    print '----'
    # --------------------------------------------------------------------------
    # Decide which flow rate to use and Calc Standard
    # Flow Rate incorporating Blower Pressure
    if flowBy_n50 != 0.0:
        standardFlowRate = flowBy_n50/(math.pow((blowerPressure/4),0.63)) # m3/s
    elif flowBy_q50 != 0.0:
        standardFlowRate = flowBy_q50/(math.pow((blowerPressure/4),0.63)) # m3/s
    else:
        standardFlowRate = 0
    
    # --------------------------------------------------------------------------
    # Calc the Zone's Infiltration Rate in m3/hr-2 of floor area (zone gross)
    zoneinfilRatePerFloorArea = standardFlowRate /  zoneFloorArea_Gross  #m3/s---> m3/hr-m2
    infiltrationRatePerFloorArea_.append(zoneinfilRatePerFloorArea)
    
    zoneinfilRatePerFacadeArea = standardFlowRate /  zoneExposedSurfaceArea  #m3/s---> m3/hr-m2
    infiltrationRatePerFacadeArea_.append(zoneinfilRatePerFacadeArea)
    
    print 'Zone Infiltration Flow Per Unit of Floor Area: {:.4f} m3/hr-m2 ({:.6f} m3/s-m2) @ Normal Pressure'.format(zoneinfilRatePerFloorArea*60*60, zoneinfilRatePerFloorArea)
    print 'Zone Infiltration Flow Per Unit of Facade Area: {:.4f} m3/hr-m2 ({:.6f} m3/s-m2) @ Normal Pressure'.format(zoneinfilRatePerFacadeArea*60*60, zoneinfilRatePerFacadeArea)
    print 'Zone Infiltration ACH: {:.4f} @ Normal Pressure'.format(standardFlowRate*60*60 / zoneVolume_Gross)
    print 'zone Ref Volume: {:.02f} m3'.format(zoneVolume_Vn50)

if _HBZones:
    HBZones_ = _HBZones
