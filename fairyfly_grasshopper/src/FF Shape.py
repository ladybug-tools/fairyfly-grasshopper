# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create Fairyfly Shape.
-

    Args:
        _geo: Rhino Brep or planar Polyline geometry.
        _material: Optional text for the Shape's THERM material to be looked up in the
            material library (see the "FF Search Materials" component for a
            full list of materials that ship with THERM). This input can
            also be a custom SolidMaterial or CavityMaterial object created
            from the corresponding component. Lastly, it can be text for
            the name of a HB-Energy material to be looked up in the material
            library (see the ""HB Search Materials" component for a full
            list of materials that ship with Honeybee).
        rgb_color_: An optional color to set the color of the material when it is
            imported to THERM. All materials from the Fairyfly Therm Library
            already possess colors but materials from the HB-Energy material
            lib will have a randomly-generated color if none is assigned here.

    Returns:
        report: Reports, errors, warnings, etc.
        shape: Fairyfly shapes. These can be added to Fairyfly models and used
            in THERM simulation.
"""

ghenv.Component.Name = 'FF Shape'
ghenv.Component.NickName = 'Shape'
ghenv.Component.Message = '1.9.6'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:  # import the core fairyfly dependencies
    from fairyfly.shape import Shape
    from fairyfly.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the core ladybug dependencies
    from ladybug.color import Color
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.config import units_system, current_tolerance
    from ladybug_rhino.togeometry import to_face3d
    from ladybug_rhino.grasshopper import all_required_inputs, document_counter, \
        longest_list, wrap_output, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

try:  # import the fairyfly-therm extension
    from fairyfly_therm.lib.materials import solid_material_by_name, \
        cavity_material_by_name
    from fairyfly_therm.material import SolidMaterial, CavityMaterial
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:  # import the honeybee-energy extension
    from honeybee_energy.lib.materials import opaque_material_by_identifier, \
        window_material_by_identifier
    from honeybee_energy.material.opaque import EnergyMaterial
    from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing
except ImportError as e:
    opaque_material_by_identifier = None
    EnergyMaterial = None
    EnergyWindowMaterialGlazing = None


if all_required_inputs(ghenv.Component):
    # check the model tolerance
    tol_msg = Model.check_reasonable_tolerance(units_system(), current_tolerance())
    if tol_msg is not None:
        give_warning(ghenv.Component, tol_msg)

    #prodess the inputs
    mats = {}  # dictorionary to prevent re-making materials
    shapes = []  # list of shapes that will be returned
    for j, geo in enumerate(_geo):
        mat = longest_list(_material, j)
        if isinstance(mat, str):
            if mat in mats:
                mat = mats[mat]
            else:
                try:
                    mat = solid_material_by_name(mat)
                except ValueError:
                    try:
                        mat = cavity_material_by_name(mat)
                    except ValueError:
                        msg = '"{}" was not found in any of the material ' \
                                'libraries.'.format(mat)
                        try:
                            if opaque_material_by_identifier is None:
                                raise ValueError(msg)
                            mat = opaque_material_by_identifier(mat)
                            mat = SolidMaterial.from_energy_material(mat)
                        except ValueError:
                            try:
                                if window_material_by_identifier is None:
                                    raise ValueError(msg)
                                mat = window_material_by_identifier(mat)
                                mat = SolidMaterial.from_energy_window_material_glazing(mat)
                            except ValueError:
                                raise ValueError(msg)
        else:
            if mat.display_name in mats:
                mat = mats[mat.display_name]
            if EnergyMaterial is not None and isinstance(mat, EnergyMaterial):
                mat = SolidMaterial.from_energy_material(mat)
            if EnergyWindowMaterialGlazing is not None and \
                    isinstance(mat, EnergyWindowMaterialGlazing):
                mat = SolidMaterial.from_energy_window_material_glazing(mat)
            assert isinstance(mat, (SolidMaterial, CavityMaterial)), 'Expected ' \
                'SolidMaterial or CavityMaterial. Got {}.'.format(type(mat))
        if len(rgb_color_) != 0:
            col = longest_list(rgb_color_, j)
            if not mat._locked:
                mat.color = Color(col.R, col.G, col.B)
            else:
                mat = mat.duplicate()
                mat.color = Color(col.R, col.G, col.B)
        mats[mat.display_name] = mat

        lb_faces = to_face3d(geo)
        for lb_face in lb_faces:
            ff_shape = Shape(lb_face)
            ff_shape.display_name = '{} {}'.format(
                mat.display_name, document_counter(mat.display_name))
            ff_shape.properties.therm.material = mat
            shapes.append(ff_shape)
    shapes = wrap_output(shapes)