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
Collects and organizes data for a duct for a Ventilation System.
-
EM Feb. 25, 2020
    Args:
        ductLength_: <Optional> Input either a number for the length of the duct from the Ventilation Unit to the building enclusure, or geometry representing the duct (curve / line)
        ductWidth_: <Optional> Input the diameter (mm) of the duct. Default is 101mm (4")
        insulThickness_: <Optional> Input the thickness (mm) of insulation on the duct. Default is 52mm (2")
        insulConductivity_: <Optional> Input the Lambda value (W/m-k) of the insualtion. Default is 0.04 W/mk (Fiberglass)
    Returns:
        hrvDuct_: A Duct object for the Ventilation System. Connect to the 'hrvDuct_01_' or 'hrvDuct_02_' input on the 'Create Vent System' to build a PHPP-Style Ventialtion System.
"""

ghenv.Component.Name = "BT_CreateNewPHPPVentDuct"
ghenv.Component.NickName = "Vent Duct"
ghenv.Component.Message = 'FEB_25_2020'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "BT"
ghenv.Component.SubCategory = "01 | Model"

import rhinoscriptsyntax as rs
import ghpythonlib.components as gh
import scriptcontext as sc

# Classes and Defs
preview = sc.sticky['Preview']
PHPP_Sys_Duct = sc.sticky['PHPP_Sys_Duct']

def getDuctLength(ductLength_):
    # Find the Duct length
    # Takes eiether a list of numbers (panel)
    # Or a Rhino curve object representing the path of the duct
    if len(ductLength_)>0:
        lengthsList = []
        for each in ductLength_:
            try:
                # if its a number input, just take that
                lengthsList.append(float(each))
            except:
                # if it isn't a number, try finding geometry
                try:
                    crv = rs.coercecurve(each)
                    lengthsList.append(gh.Length(crv))
                except:
                    pass
        lenM = sum(lengthsList)
    else:
        lenM = 5
    
    return lenM

hrvDuct_ = PHPP_Sys_Duct(
        getDuctLength(ductLength_),
        ductWidth_ if ductWidth_ else 104,
        insulThickness_ if insulThickness_ else 52,
        insulConductivity_ if insulConductivity_ else 0.04 )

preview(hrvDuct_)
