# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>


"""
Load any fairyfly object from a fairyfly JSON file
-
Fairyfly objects include any Model, Shape, or Boundary.
-
It also includes any fairyfly Material or Simulation object.
-

    Args:
        _ff_file: A file path to a fairyfly JSON from which objects will be loaded
            back into Grasshopper. The objects in the file must be non-abridged
            in order to be loaded back correctly.
        _load: Set to "True" to load the objects from the _ff_file.

    Returns:
        report: Reports, errors, warnings, etc.
        ff_objs: A list of fairyfly objects that have been re-serialized from
            the input file.
"""

ghenv.Component.Name = 'FF Load Objects'
ghenv.Component.NickName = 'LoadObjects'
ghenv.Component.Message = '1.9.1'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '4'

import io

try:  # import the core fairyfly dependencies
    import fairyfly.dictutil as ff_dict_util
    from fairyfly.model import Model
    from fairyfly.config import folders
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the core fairyfly_energy dependencies
    import fairyfly_therm.material.dictutil as therm_dict_util
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_energy:\n\t{}'.format(e))

try:  # import the core ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
    from ladybug_rhino.config import units_system, current_tolerance
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

import json


def model_units_tolerance_check(model):
    """Convert a model to the current Rhino units and check the tolerance.

    Args:
        model: A fairyfly Model, which will have its units checked.
    """
    # check the model units
    if model.units != units_system():
        print('Imported model units "{}" do not match that of the current Rhino '
            'model units "{}"\nThe model is being automatically converted '
            'to the Rhino doc units.'.format(model.units, units_system()))
        model.convert_to_units(units_system())

    # check that the model tolerance is not too far from the Rhino tolerance
    if model.tolerance / current_tolerance() >= 100:
        msg = 'Imported Model tolerance "{}" is significantly coarser than the ' \
            'current Rhino model tolerance "{}".\nIt is recommended that the ' \
            'Rhino document tolerance be changed to be coarser and this ' \
            'component is re-run.'.format(model.tolerance, current_tolerance())
        print msg
        give_warning(ghenv.Component, msg)


if all_required_inputs(ghenv.Component) and _load:
    with io.open(_ff_file, encoding='utf-8') as inf:
        first_char = inf.read(1)
        second_char = inf.read(1)
    with io.open(_ff_file, encoding='utf-8') as inf:
        if second_char == '{':
            inf.read(1)
        data = json.load(inf)

    if 'type' in data:
        ff_objs = ff_dict_util.dict_to_object(data, False)  # re-serialize as a core object
        if ff_objs is None:  # try to re-serialize it as an energy object
            ff_objs = therm_dict_util.dict_to_object(data, False)
        elif isinstance(ff_objs, Model):
            model_units_tolerance_check(ff_objs)
    else:  # no 'type' key; assume that its a group of objects
        ff_objs = []
        for hb_dict in data.values():
            ff_obj = ff_dict_util.dict_to_object(hb_dict, False)  # re-serialize as a core object
            if ff_obj is None:  # try to re-serialize it as an energy object
                ff_obj = therm_dict_util.dict_to_object(hb_dict, False)
            ff_objs.append(ff_obj)