# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create a Fairyfly Model, which can be used for simulation.
-

    Args:
        rooms_: A list of fairyfly Shapes to be added to the Model. Note that at
            least one Shape is necessary to make a simulate-able THERM model.
        boundaries_: A list of fairyfly Boundary objects to be added to the Model.
            Note that at least two distinct boundary conditions are necessary
            to make a simulate-able THERM model.
        _name_: Text to be used for the Model name. If no name is provided, it
            will be "unnamed".

    Returns:
        report: Reports, errors, warnings, etc.
        model: A Fairyfly Model object possessing all of the input geometry
            objects.
"""

ghenv.Component.Name = 'FF Model'
ghenv.Component.NickName = 'Model'
ghenv.Component.Message = '1.9.1'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:  # import the core fairyfly dependencies
    from fairyfly.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
    from ladybug_rhino.config import units_system, current_tolerance, angle_tolerance
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


def check_all_geo_none():
    """Check whether all of the geometry inputs to this component are None."""
    return all(obj_list == [] or obj_list == [None] for obj_list in
               (shapes_, boundaries_))


if all_required_inputs(ghenv.Component) and not check_all_geo_none():
    # check the Rhino Model units
    units, tolerance = units_system(), current_tolerance()
    tol_msg = Model.check_reasonable_tolerance(units, tolerance)
    if tol_msg is not None:
        give_warning(ghenv.Component, tol_msg)

    # create the model
    model = Model(
        shapes_, boundaries_,
        units=units, tolerance=tolerance, angle_tolerance=angle_tolerance)
    model.display_name = _name_ if _name_ is not None else 'unnamed'
