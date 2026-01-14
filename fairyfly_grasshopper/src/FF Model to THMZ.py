# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Write a fairyfly Model to an THMZ file (aka. THERM Zip file), which can then be
simulated or opened in the THERM interface.

-
    Args:
        _model: A fairyfly model object possessing all geometry and therm
            simulation properties.
        _folder_: An optional folder on this computer, into which the THMZ file
            will be written.
        _write: Set to "True" to write the THMZ file from the fairyfly Model.
        run_: Set to "True" to simulate the THMZ file in THERM once it is written.
            This will ensure that results are embedded within the output
            THMZ file such that they can be visualized with the
            "FF Read THERM Result" component.
            _
            This input can also be the integer "2", which will run the whole
            translation and simulation silently (without any batch windows).

    Returns:
        report: A detailed report of the THMZ translation and simulation.
        thmz: The file path of the SQL result file that has been generated on this
            computer. This will be None unless run_ is set to True.
"""

ghenv.Component.Name = 'FF Model to THMZ'
ghenv.Component.NickName = 'ModelToTHMZ'
ghenv.Component.Message = '1.9.1'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

import os

try:
    from fairyfly.config import folders
    from fairyfly.typing import clean_string
    from fairyfly.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:
    from fairyfly_therm.config import folders as therm_folders
    from fairyfly_therm.writer import model_to_thmz
    from fairyfly_therm.run import run_model
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_energy:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component) and _write:
    # process the simulation folder name
    assert isinstance(_model, Model), \
        'Expected Fairyfly Model for _model input. Got {}.'.format(type(_model))
    model_name = clean_string(_model.display_name)
    _folder_ = os.path.join(folders.default_simulation_folder, model_name) \
        if _folder_ is None else _folder_

    # write the model to THMZ or run it through THERM
    if not run_:
        thmz = os.path.join(_folder_, '{}.thmz'.format(model_name))
        model_to_thmz(_model, thmz)
    else:
        therm_folders.check_therm_version()
        silent = True if run_ > 1 else False
        thmz = run_model(_model, _folder_, silent)
