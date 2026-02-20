# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create parameters for THERM model exposure, that describes the model's location
within a larger building.
-

    Args:
        _model_type_: Text to indicate the type of construction detail or the purpose
            of the model. Chose from the following. (Default: Other).
            * Window
            * Opaque Wall
            * Opaque Roof
            * Other
        _cross_section_: Text to indicate the type of cross section that the model represents.
            The acceptable fields here depend upon the model_type. If unspecified,
            the default is set to the top of each list below for each model_type.
            _
            For the Window model_type, choose from the following.
            * Sill
            * Jamb
            * Head
            * Horizontal Divider
            * Vertical Divider
            * Horizontal Meeting Rail
            * Vertical Meeting Rail
            * Common Frame
            * Spacer
            _
            For the Opaque Wall and Roof model_type, choose from the following.
            * Sill Plate
            * Header
            * End Section
            * Middle Section
            * Thermal Bridge
            * Window Framing - Sill
            * Rough Opening - Header
            * Rough Opening - Jamb
            _
            For the Other model_type, choose from the following.
            * General Cross Section
            * Common Thermal Bridge
        _gravity_orient_: Text to indicate the direction of gravity for the model. If unspecified, 
            this will be computed from the orientation of the model's plane
            in the 3D scene.
            * Down
            * Up
            * Left
            * Right
            * Into Screen
            * Out Of Screen
        _wind_orient_: A number between 0 and 360 for the direction the exterior surface
            of the model faces. This orientation of the exterior surface
            is used to determine the wind direction for the simulation. (Default: 0).
            For reference, 0 = North, 90 = East, 180 = South, 270 = West.

    Returns:
        exposure: Parameters for THERM model exposure, that describes the model's
            location within a larger building. These can be connected to the
            "FF Model to THMZ" component in order to specify settings for
            the THERM simulation.
"""

ghenv.Component.Name = 'FF Model Exposure'
ghenv.Component.NickName = 'Exposure'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '0'

try:
    from fairyfly_therm.simulation.exposure import ModelExposure
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import turn_off_old_tag
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))
turn_off_old_tag(ghenv.Component)

# set default sizing factors
_model_type_ = 'Other' if _model_type_ is None else _model_type_
_wind_orient_ = 0 if _wind_orient_ is None else _wind_orient_

# create the object
exposure = ModelExposure(_model_type_, _cross_section_, _gravity_orient_, _wind_orient_)
