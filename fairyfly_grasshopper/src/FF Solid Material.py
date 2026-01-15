# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create a custom solid material, which can be plugged into the "FF Shape" component
to change the properties of the material in a THERM simulation.
-

    Args:
        _name_: Text to set the name for the material.
        _conductivity: Number for the thermal conductivity of the material [W/m-K].
        _emissivity_: Number between 0 and 1 for the infrared hemispherical
            emissivity of the material. (Default: 0.9).
        density_: Number for the density of the material [kg/m3].
        porosity_: Optional number between 0 and 1 for the porosity of the material.
        spec_heat_: Number for the specific heat of the material [J/kg-K].
        vapor_resist_: Optional number for the water vapor diffusion resistance factor.
        rgb_color_: An optional color to set the color of the material when it is
            imported to THERM. If unspecified, a randomly-generated color is assigned.

    Returns:
        mat: A standard solid material that can be assigned to a Fairyfly Shape
            to change the properties of the material in a THERM simulation.
"""

ghenv.Component.Name = 'FF Solid Material'
ghenv.Component.NickName = 'SolidMat'
ghenv.Component.Message = '1.9.1'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '3'

import uuid

try:  # import the core ladybug dependencies
    from ladybug.color import Color
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:  # import the fairyfly-therm dependencies
    from fairyfly_therm.material.solid import SolidMaterial
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:  # import ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    # set the default material properties
    _emissivity_ = 0.9 if _emissivity_ is None else _emissivity_

    # create the material
    mat = SolidMaterial(
        _conductivity, _emissivity_, None,
        density_, porosity_, spec_heat_, vapor_resist_
    )
    mat.display_name = _name_ if _name_ is not None else \
        'Solid Material {}'.format(str(uuid.uuid4())[:8])
    if rgb_color_ is not None:
        mat.color = Color(rgb_color_.R, rgb_color_.G, rgb_color_.B)
