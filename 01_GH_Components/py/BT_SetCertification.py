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
Inputs for 'Verification' worksheet Certification Type items
-
EM August 1, 2020
    Args:
        energyStandard_: Input either "1-Passive House", "2-EnerPHit", "3-PHI Low Energy Building" or "4-Other"
        class_: Input either "1-Classic", "2-Plus" or "3-Premium"
        primaryEnergy_: Input either "1-PE (non-renewable)" or "2-PER (renewable)"
        enerPHitMethod_: Input either "1-Component method" or "2-Energy demand method"
        retrofit_: Input either "1-New building", "2-Retrofit" or "3-Step-by-step retrofit"
    Returns:
        certification_: A Certification Object with all its parameter values. Connect this to the 'certification_' input in a 'PHPP Setup' component.
"""

ghenv.Component.Name = "BT_SetCertification"
ghenv.Component.NickName = "Certification"
ghenv.Component.Message = 'AUG_01_2020'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "BT"
ghenv.Component.SubCategory = "02 | IDF2PHPP"

import scriptcontext as sc

# Classes and Defs
preview = sc.sticky['Preview']

class certification:
    def __init__(self, _stand, _cert, _pe, _enerphit, retrofit ):
        self.energy_standard = _stand
        self.cert_class = _cert
        self.pe_type = _pe
        self.enerphit_type = _enerphit
        self.retrofit = retrofit
    
    def __repr__(self):
        str= ("A Certification Types Object with:",
            '  > Energy Standard: {}'.format(self.energy_standard),
            '  > Certification Class: {}'.format(self.cert_class),
            '  > Primary Energy Method: {}'.format(self.pe_type),
            '  > EnerPHit Type: {}'.format(self.enerphit_type),
            '  > Retrofit: {}'.format(self.retrofit)
            )
        
        return '\n'.join(str)

# Default Inputs, Clean
if energyStandard_:
    if '4' in str(energyStandard_) or 'Other' in str(energyStandard_): energyStandard = '4-Other'
    elif '3' in str(energyStandard_) or 'Low' in str(energyStandard_): energyStandard = '3-PHI Low Energy Building'
    elif '2' in str(energyStandard_) or 'EnerPHit' in str(energyStandard_): energyStandard = '2-EnerPHit'
    else: energyStandard = '1-Passive House'
else:
    energyStandard = '1-Passive House'

if class_:
    if '3' in str(class_) or 'Premium' in str(class_): certClass = '3-Premium'
    elif '2' in str(class_) or 'Plus' in str(class_): certClass = '2-Plus'
    else: certClass = '1-Classic'
else:
    certClass = '1-Classic'

if primaryEnergy_:
    if '2' in str(primaryEnergy_) or 'PER' in str(primaryEnergy_): peType = '2-PER (renewable)'
    else: peType = '1-PE (non-renewable)'
else:
    peType = '2-PER (renewable)'

if enerPHitMethod_:
    if '2' in str(enerPHitMethod_) or 'Energy' in str(enerPHitMethod_): enerPHitType = '2-Energy demand method'
    else: enerPHitType = '1-Component method'
else:
    enerPHitType = '2-Energy demand method'

if retrofit_:
    if '3' in str(retrofit_) or 'Step' in str(retrofit_): retrofit = '3-Step-by-step retrofit'
    elif '2' in str(retrofit_) or 'Retrofit' in str(retrofit_): retrofit = '2-Retrofit'
    else: retrofit = '1-New building'
else:
    retrofit = '1-New building'

# Create the Certification Object
certification_ = certification(energyStandard, certClass, peType, enerPHitType, retrofit )
preview(certification_)
