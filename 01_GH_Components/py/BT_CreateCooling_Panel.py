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
Set the parameters for a Panel Cooling Element. Sets the values on the 'Cooling Unit' worksheet.
-
EM August 11, 2020
    Args:
        SEER_: (W/W) Default=3
    Returns:
        panelCooling_: 
"""

ghenv.Component.Name = "BT_CreateCooling_Panel"
ghenv.Component.NickName = "Cooling | Panel"
ghenv.Component.Message = 'AUG_11_2020'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "BT"
ghenv.Component.SubCategory = "01 | Model"

import scriptcontext as sc
import Grasshopper.Kernel as ghK

# Classes and Defs
preview = sc.sticky['Preview']

class Cooling_Panel:
    def __init__(self, _seer=3):
        self.SEER = _seer
    
    def getValsForPHPP(self):
        return self.SEER
    
    def __repr__(self):
        return "A Cooling: Panel Params Object"

def cleanInputs(_in, _nm, _default):
    # Apply defaults if the inputs are Nones
    out = _in if _in != None else _default
    
    try:
        return float(out)
    except:
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, '"{}" input should be a number'.format(_nm))
        return _default

seer = cleanInputs(SEER_, 'SEER_', 3)

panelCooling_ = Cooling_Panel(seer)

preview(panelCooling_)
