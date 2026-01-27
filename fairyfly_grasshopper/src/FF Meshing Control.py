# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create parameters with criteria for meshing THERM geometry.
-

    Args:
        _mesh_type_: Text to indicate the type of meshing algorithm to use. Choose from
            the following. Simmetrix is generally more flexible and capable of
            handling more complex geometry when compared with the QuatTree. However,
            the structure of QuadTree meshes is more predictable. (Default: Simmetrix).
            * Simmetrix
            * QuadTree
        _parameter_: A positive integer for the minimum number of subdivisions to
            be performed while meshing the input geometry. The higher the mesh
            control parameter, the smaller the maximum size of finite elements
            in the model and the smoother the results will appear. However, higher
            mesh parameters will also require more time to run. (Default: 20).
        _check_error_: Boolean to note whether the error estimator should
            be run as part of the finite element analysis. If the global error
            is above a specified value, then the error estimator signals the mes
            generator, and the mesh is refined in areas where the potential
            for error is high.  The refined mesh is sent back to the finite
            element solver, and a new solution is obtained. (Default: True).
        _max_error_: A number between 0 and 100 for the percent error energy
            norm used by the error estimator. This is the maximum value
            of the error energy divided by the energy of the sum of the
            recovered fluxes and the error, multiplied by 100. (Default: 10).
        _max_iter_: A positive integer for the number of iterations between the error
            estimator and the solver to be performed before the finding
            a solution is abandoned and the program exits. (Default: 5).

    Returns:
        meshing: Parameters with criteria for creating the finite element mesh.
            These can be connected to the "FF Model to THMZ" component in
            order to specify settings for the THERM simulation.
"""

ghenv.Component.Name = 'FF Meshing Control'
ghenv.Component.NickName = 'Meshing'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:
    from fairyfly_therm.simulation.mesh import MeshControl
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import turn_off_old_tag
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))
turn_off_old_tag(ghenv.Component)

# set default sizing factors
_mesh_type_ = 'Simmetrix' if _mesh_type_ is None else _mesh_type_
_parameter_ = 20 if _parameter_ is None else _parameter_
_check_error_ = True if _check_error_ is None else _check_error_
_max_error_ = 10 if _max_error_ is None else _max_error_
_max_iter_ = 5 if _max_iter_ is None else _max_iter_

# create the object
meshing = MeshControl(_mesh_type_, _parameter_, _check_error_, _max_error_, _max_iter_)
