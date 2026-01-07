# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>


"""
Deconstruct a material into its constituient attributes and values.
-

    Args:
        _mat: A material to be deconstructed. This can also be text for a
            material to be looked up in the material library.

    Returns:
        values: List of values for the attributes that define the material.
        attr_names: List of text that is the same length as the values, which
            notes the attribute name for each value.
"""

ghenv.Component.Name = 'FF Deconstruct Material'
ghenv.Component.NickName = 'DecnstrMat'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '3'

import re

try:  # import the fairyfly-therm dependencies
    from fairyfly_therm.lib.materials import solid_material_by_name, cavity_material_by_name
    from fairyfly_therm.material import SolidMaterial
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:  # import the fairyfly dependencies
    from fairyfly.search import get_attr_nested
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

SOLID_ATTR = (
    'display_name',
    'conductivity',
    'emissivity',
    'density',
    'porosity',
    'specific_heat',
    'vapor_diffusion_resistance'
)

CAVITY_ATTR = (
    'display_name',
    'cavity_model',
    'gas.pure_gases',
    'gas.gas_fractions'
)


if all_required_inputs(ghenv.Component):
    # check the input
    if isinstance(_mat, str):
        try:
            _mat = solid_material_by_name(_mat)
        except ValueError:
            _mat = cavity_material_by_name(_mat)

    # get the values and attribute names
    rel_attr = SOLID_ATTR if isinstance(_mat, SolidMaterial) else CAVITY_ATTR
    values, attr_names = [], []
    for r_attr in rel_attr:
        values.append(get_attr_nested(_mat, r_attr))
        attr_names.append(r_attr.split('.')[-1].replace('_', ' ').title())

