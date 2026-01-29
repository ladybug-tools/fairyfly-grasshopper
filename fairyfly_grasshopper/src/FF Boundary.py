# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Create Fairyfly Boundary.
-

    Args:
        _geo: Planar Polyline or Line geometry representing the boundary.
        _name_: Optional text for the name of the boundary. If unspecified,
            a generic one will be automatically assigned.
        _temperature: A number for the temperature at the boundary in degrees Celsius.
            For NFRC conditions, this temperature should be 21C for interior
            boundary conditions and -18 C for winter exterior boundary conditions.
        _film_coeff: A number in W/m2-K that represents the convective resistance of
            the air film at the boundary condition. Typical film coefficient
            values range from 36 W/m2-K (for an exterior condition where
            outdoor wind strips away most convective resistance) to 2.5 W/m2-K
            (for a vertically-oriented interior wood/vinyl surface). For NFRC
            conditions, this should be 26 for exterior boundary conditions and
            around 3 for interior boundary conditions.
        rad_env_: The optional output of the "FF Radiant Environment" component,
            which can be used to customize the radiant properties of the
            boundary (if they differ from the input _temperature and standard
            emissivity of 1 or if there is additional solar heat flux along
            the boundary).
        u_factor_tag_: An optional text string for to define a U-Factor tag along
            the boundary condition. This tag is used tell THERM the boundary on
            which a net U-Value shall be computed. Typical values to input here,
            which are recognizable in LBNL WINDOW include the following.
                * Frame
                * Edge
                * Spacer
                * ShadeInETag
                * ShadeOutETag
                * SHGC Exterior
        rgb_color_: An optional color to set the color of the material when it is
            imported to THERM. All materials from the Fairyfly Therm Library
            already possess colors but materials from the HB-Energy material
            lib will have a randomly-generated color if none is assigned here.

    Returns:
        report: Reports, errors, warnings, etc.
        boundaries: Fairyfly boundaries. These can added to Fairyfly models and
            used in THERM simulation.
"""

ghenv.Component.Name = 'FF Boundary'
ghenv.Component.NickName = 'Boundary'
ghenv.Component.Message = '1.9.3'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '0 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = '1'

try:  # import the core fairyfly dependencies
    from fairyfly.boundary import Boundary
    from fairyfly.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the fairyfly-therm extension
    from fairyfly_therm.condition.steadystate import SteadyState
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:  # import the core ladybug dependencies
    from ladybug.color import Color
    from ladybug_geometry.geometry3d import Polyline3D
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.config import units_system, current_tolerance
    from ladybug_rhino.togeometry import to_polyline3d
    from ladybug_rhino.grasshopper import all_required_inputs, document_counter, \
        longest_list, wrap_output, de_objectify_output, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    # check the model tolerance
    tol_msg = Model.check_reasonable_tolerance(units_system(), current_tolerance())
    if tol_msg is not None:
        give_warning(ghenv.Component, tol_msg)

    # create the boundary objects
    boundaries = []  # list of boundaries that will be returned
    for j, geo in enumerate(_geo):
        # translate the geometry
        lb_geo = to_polyline3d(geo)
        lb_segs = lb_geo.segments if isinstance(lb_geo, Polyline3D) else [lb_geo]
        ff_boundary = Boundary(lb_segs)

        # create the SteadyState condition object
        name = 'Condition {}'.format(document_counter('condition')) \
            if len(_name_) == 0 else longest_list(_name_, j)
        name = '{} {}'.format(name, j) \
            if len(_name_) != 0 and len(_name_) != len(_geo) else name
        condition = SteadyState(longest_list(_temperature, j), longest_list(_film_coeff, j))
        condition.display_name = name
        if len(rad_env_) != 0:
            rad_env = longest_list(rad_env_, j)
            emiss, rad_temp, heat_flux = de_objectify_output(rad_env)
            condition.emissivity = emiss
            condition.radiant_temperature = rad_temp
            condition.heat_flux = heat_flux
        if len(rgb_color_) != 0:
            rgb_color = longest_list(rgb_color_, j)
            condition.color = Color(rgb_color.R, rgb_color.G, rgb_color.B)

        # assign properties to the boundary
        ff_boundary.display_name = name
        ff_boundary.properties.therm.condition = condition
        if len(u_factor_tag_) != 0:
            ff_boundary.properties.therm.u_factor_tag = longest_list(u_factor_tag_, j)
        boundaries.append(ff_boundary)
    boundaries = wrap_output(boundaries)
