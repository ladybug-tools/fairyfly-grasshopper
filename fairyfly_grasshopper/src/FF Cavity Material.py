# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create a custom cavity material, which can be plugged into the "FF Shape" component
to change the properties of the material in a THERM simulation.
-

    Args:
        _name_: Text to set the name for the material.
        _cavity_model_: Text for the type of cavity model to be used to determine
            the thermal resistance of the material. (Default: CEN). Choose from
            the following.
                * CEN
                * NFRC
                * ISO15099
                * ISO15099Ventilated
        _gas_type_: Text describing the types of gas in the gap. (Default: Air).
            Text must be one of the following: 'Air', 'Argon', 'Krypton', 'Xenon'.
        _gas_ratios_: A list of text describing the volumetric fractions of gas
            types in the mixture.  This list must align with the gas_types
            input list. Default: Equal amout of gases for each type.
        rgb_color_: An optional color to set the color of the material when it is
            imported to THERM. If unspecified, a randomly-generated color is assigned.

    Returns:
        mat: A cavity material that can be assigned to a Fairyfly Shape to change the
            properties of the material in a THERM simulation.
"""

ghenv.Component.Name = 'FF Cavity Material'
ghenv.Component.NickName = 'CavityMat'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '3'

import uuid

try:  # import the core ladybug dependencies
    from ladybug.color import Color
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:  # import the fairyfly-energy dependencies
    from fairyfly_therm.material import CavityMaterial, Gas
    from fairyfly_therm.lib.gases import gas_by_name
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_energy:\n\t{}'.format(e))

try:  # import ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import turn_off_old_tag
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))
turn_off_old_tag(ghenv.Component)


# set the default material properties
_cavity_model_ = 'CEN' if _cavity_model_ is None else _cavity_model_
_gas_type_ = 'Air' if _gas_type_ is None else _gas_type_

# get the Gas material to fill the cavity
cavity_gas = gas_by_name(_gas_type_.title())

# create the material
mat = CavityMaterial(cavity_gas, _cavity_model_)
mat.display_name = _name_ if _name_ is not None else \
    'Cavity Material {}'.format(str(uuid.uuid4())[:8])
if rgb_color_ is not None:
    mat.color = Color(rgb_color_.R, rgb_color_.G, rgb_color_.B)
