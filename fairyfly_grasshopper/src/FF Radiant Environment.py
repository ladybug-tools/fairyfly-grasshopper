# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create a custon radiant environment for Fairyfly boundary.
_
Assigning values here will create radiant conditions that are different from
stanbdard NFRC conditions (where radiant temperature equals air temperature,
the emissivity of the environment is 1, and there is no additional heat flux).
-

    Args:
        _geo: Planar Polyline or Line geometry representing the boundary.
        rad_temp_: A number for the radiant temperature at the boundary
            in degrees Celsius. If None, this will be the same as the specified
            air temperature. (Default: None).
        emissivity_: An optional number between 0 and 1 to set the emissivity
            along the boundary, which represents the emissivity of the
            environment to which the material in contact with the boundary is
            radiating to. (Default: 1).
        heat_flux_: An optional number in W/m2 that represents additional energy
            flux across the boundary. This can be used to account for solar flux
            among other forms of heat flux. (Default: 0).

    Returns:
        report: Reports, errors, warnings, etc.
        rad_env: Radiant environment properties that can be plugged into the "FF Boundary"
            component in order to customize the radiant environment within
            THERM simulation.
"""

ghenv.Component.Name = 'FF Radiant Environment'
ghenv.Component.NickName = 'RadEnv'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs, objectify_output
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    emiss = emissivity_ if emissivity_ is not None else 1.0
    heat_flux = heat_flux_ if heat_flux_ is not None else 0
    rad_env = objectify_output('Radiant Enviornment', [emiss, rad_temp_, heat_flux])
