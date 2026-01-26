# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Color Fairyfly Shapes in the Rhino scene using their attributes.
_
This can be used as a means to check that correct properties are assigned to
different shapes.
-

    Args:
        _ff_objs: An array of fairyfly Shapes to be colored with their attributes
            in the Rhino scene. This can also be an entire Model to be colored.
        _attribute_: Text for the name of the attribute with which the shapes should
            be colored. The "FF Shape Attributes" component lists all of the
            attributes of the shape. (Default: THERM Material).
        legend_par_: An optional LegendParameter object to change the display
            of the colored shapes. (Default: None).

    Returns:
        wire_frame: A list of lines representing the outlines of the _ff_objs.
        legend: Geometry representing the legend for colored meshes.
        mesh: Meshes of the shapes colored according to their attributes.
        values: A list of values noting the attribute assigned to each shape.
        colors: A list of colors noting the color of each shape in the Rhino scene.
            This can be used in conjunction with the native Grasshopper
            "Custom Preview" component to create custom visualizations in
            the Rhino scene.
        vis_set: An object containing VisualizationSet arguments for drawing a detailed
            version of the ColorRoom in the Rhino scene. This can be connected to
            the "LB Preview Visualization Set" component to display this version
            of the visualization in Rhino.
"""

ghenv.Component.Name = 'FF Color Shape Attributes'
ghenv.Component.NickName = 'ColorShapeAttr'
ghenv.Component.Message = '1.9.2'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '3'

try:  # import the core fairyfly dependencies
    from fairyfly.model import Model
    from fairyfly.shape import Shape
    from fairyfly.colorobj import ColorShape
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.fromgeometry import from_face3ds_to_colored_mesh, \
        from_face3d_to_wireframe
    from ladybug_rhino.fromobjects import legend_objects
    from ladybug_rhino.color import color_to_color
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

DEFAULT_PROP = 'properties.therm.material.display_name'


if all_required_inputs(ghenv.Component):
    # extract any shapes from input Models
    _attribute_ = DEFAULT_PROP if _attribute_ is None else _attribute_
    shapes = []
    for ff_obj in _ff_objs:
        if isinstance(ff_obj, Model):
            shapes.extend(ff_obj.shapes)
        elif isinstance(ff_obj, Shape):
            shapes.append(ff_obj)

    # create the ColorShape visualization object
    color_obj = ColorShape(shapes, _attribute_, legend_par_)
    # assign material colors if this is what is being used for coloring
    if _attribute_ == DEFAULT_PROP and color_obj.legend_parameters.are_colors_default:
        color_model = Model(shapes)
        color_dict = {mat.display_name: mat.color
                      for mat in color_model.properties.therm.materials}
        leg_colors = [color_dict[m_name] for m_name in color_obj.attributes_unique]
        if len(leg_colors) == 1:
            leg_colors = [leg_colors[0]] * 2
        color_obj.legend_parameters.colors = leg_colors

    # output the visualization geometry
    graphic = color_obj.graphic_container
    values = color_obj.attributes_original
    flat_geo = color_obj.geometry
    mesh = []
    for fc, col in zip(flat_geo, graphic.value_colors):
        mesh.append(from_face3ds_to_colored_mesh([fc], col))
    wire_frame = []
    for face in flat_geo:
        wire_frame.extend(from_face3d_to_wireframe(face))
    legend = legend_objects(graphic.legend)
    colors = [color_to_color(col) for col in graphic.value_colors]
    vis_set = color_obj
