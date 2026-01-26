# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Color Fairyfly Boundaries in the Rhino scene using their attributes.
_
This can be used as a means to check that correct properties are assigned to
different boundaries.
-

    Args:
        _ff_objs: An array of fairyfly Boundaries to be colored with their attributes
            in the Rhino scene. This can also be an entire Model to be colored.
        _attribute_: Text for the name of the attribute with which the boundaries should
            be colored. The "FF Boundary Attributes" component lists all of the
            attributes of the boundary. (Default: THERM Condition).
        legend_par_: An optional LegendParameter object to change the display
            of the colored boundaries (Default: None).

    Returns:
        wire_frame: A list of lines representing the outlines of the _ff_objs.
        legend: Geometry representing the legend for colored lines.
        lines: Line segments of the boundaries colored according to their attributes.
        values: A list of values noting the attribute assigned to each boundary.
        colors: A list of colors noting the color of each boundary in the Rhino scene.
            This can be used in conjunction with the native Grasshopper
            "Custom Preview" component to create custom visualizations in
            the Rhino scene.
        vis_set: An object containing VisualizationSet arguments for drawing a detailed
            version of the ColorRoom in the Rhino scene. This can be connected to
            the "LB Preview Visualization Set" component to display this version
            of the visualization in Rhino.
"""

ghenv.Component.Name = 'FF Color Boundary Attributes'
ghenv.Component.NickName = 'ColorBoundaryAttr'
ghenv.Component.Message = '1.9.2'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '3'

try:  # import the core fairyfly dependencies
    from fairyfly.model import Model
    from fairyfly.boundary import Boundary
    from fairyfly.shape import Shape
    from fairyfly.colorobj import ColorBoundary
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.colorize import ColoredLine
    from ladybug_rhino.fromgeometry import from_linesegment3d, from_face3d_to_wireframe
    from ladybug_rhino.fromobjects import legend_objects
    from ladybug_rhino.color import color_to_color
    from ladybug_rhino.grasshopper import all_required_inputs, schedule_solution
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

DEFAULT_PROP = 'properties.therm.condition.display_name'


if all_required_inputs(ghenv.Component):
    # extract any boundaries from input Models
    _attribute_ = DEFAULT_PROP if _attribute_ is None else _attribute_
    boundaries, shapes = [], []
    for ff_obj in _ff_objs:
        if isinstance(ff_obj, Model):
            boundaries.extend(ff_obj.boundaries)
            shapes.extend(ff_obj.shapes)
        elif isinstance(ff_obj, Boundary):
            boundaries.append(ff_obj)
        elif isinstance(ff_obj, Shape):
            shapes.append(ff_obj)

    # create the ColorBoundary visualization object
    color_obj = ColorBoundary(boundaries, _attribute_, legend_par_)
    # assign condition colors if this is what is being used for coloring
    if _attribute_ == DEFAULT_PROP and color_obj.legend_parameters.are_colors_default:
        color_model = Model(boundaries=boundaries)
        color_dict = {con.display_name: con.color
                      for con in color_model.properties.therm.conditions}
        leg_colors = [color_dict[m_name] for m_name in color_obj.attributes_unique]
        if len(leg_colors) == 1:
            leg_colors = [leg_colors[0]] * 2
        color_obj.legend_parameters.colors = leg_colors

    # output the visualization geometry
    graphic = color_obj.graphic_container
    values = color_obj.attributes_original
    flat_geo = color_obj.flat_geometry
    wire_frame = []
    for shape in shapes:
        wire_frame.extend(from_face3d_to_wireframe(shape.geometry))
    legend = legend_objects(graphic.legend)
    colors = [color_to_color(col) for col in graphic.value_colors]
    lines = []
    for lin, col in zip(flat_geo, colors):
        col_line = ColoredLine(from_linesegment3d(lin))
        col_line.color = col
        col_line.thickness = 3
        lines.append(col_line)
    # CWM: I don't know why we have to re-schedule the solution but this is the
    # only way I found to get the colored polylines to appear (redraw did not work).
    schedule_solution(ghenv.Component, 2)
    vis_set = color_obj
