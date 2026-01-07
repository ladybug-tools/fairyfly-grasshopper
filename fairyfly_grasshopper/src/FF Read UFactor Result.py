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
        _thmz: Path to a THMZ file that has been simulated in THERM. This can be the
            direct output of the "FF Model to THMZ" component as long as
            run_ has been set to True.
        _u_type_: Optional text or an integer to set the type of U-Factor to import from
            the THMZ file if something other than the U-Factor along the total
            boundary length is desired. Choose from the following options. (Default: Total)
                0 - Total
                1 - Projected X
                2 - Projected Y
                3 - Projected in Glass Plane
                4 - Custom Rotation
        ip_: Set to True to have all data imported with IP Units (Btu/h-ft2-F and in)
            instead of the default SI units of W/m2-K and mm.

    Returns:
        report: Reports, errors, warnings, etc.
        tags: The names of each of the U-Factor tags in the THMZ file.
        u_factors: The U-Factors accross each boundary that was labeled with a U-Factor tag.
            This will be in W/m2-K by default unless ip_ is set to True in which
            case it will be in Btu/h-ft2-F.
        lengths: The proejcted lengths of each boundary that was labeled with a U-Factor tag.
            This will be the total length of the boundary if the default u_type
            of "Total" has been used and will account for the length only in the
            projection plane if a different u_type is used. Values are in mm by
            default unless ip_ is set to True, in which case it will be in inches.
"""

ghenv.Component.Name = 'FF Read UFactor Result'
ghenv.Component.NickName = 'UFactorResult'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '2'

try:  # import the core fairyfly dependencies
    from fairyfly_therm.result import THMZResult
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))


try:  # import the core ladybug dependencies
    from ladybug.datatype.uvalue import UValue
    from ladybug.datatype.distance import Distance
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

try:  # import the ladybug_rhino dependencies
    from ladybug_rhino.config import conversion_to_meters
    from ladybug_rhino.fromgeometry import from_mesh3d, from_point3d
    from ladybug_rhino.fromobjects import legend_objects
    from ladybug_rhino.text import text_objects
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

U_TYPES = {
    'total': 'total',
    '0': 'total',
    'projected x': 'projected_x',
    '1': 'projected_x',
    'projected y': 'projected_y',
    '2': 'projected_y',
    'projected in glass plane': 'projected_in_glass_plane',
    '3': 'projected_in_glass_plane',
    'custom rotation': 'custom_rotation',
    '4': 'custom_rotation'
}


if all_required_inputs(ghenv.Component):
    # create the THMZResult object and check to be sure that it has been simulated
    result_obj = THMZResult(_thmz)
    uf_objs = result_obj.u_factors
    if uf_objs is None:
        msg = 'No U-Factor data was found within the THMZ file.\nMake sure that the THMZ ' \
            'file has been successfully simulated in THERM.'
        print(msg)
        give_warning(ghenv.Component, msg)

    elif len(uf_objs) == 0:
        msg = 'U-Factor tags were not assigned to any boundaries.\nMake sure that ' \
            'a u_factor_tag_ has been input to one of the "FF Boundary" components.'
        print(msg)
        give_warning(ghenv.Component, msg)

    else:
        # figure out the right attributes to get from the UFactor objects
        if _u_type_ is None:
            b_attr = 'total'
        else:
            b_attr = U_TYPES[_u_type_.lower()]
        u_attr = '{}_u_factor'.format(b_attr)
        l_attr = '{}_length'.format(b_attr)
        
        # extract all of the U-Factor information
        tags, u_factors, lengths = [], [], []
        for uf_obj in uf_objs:
            tags.append(uf_obj.name)
            u_factors.append(getattr(uf_obj, u_attr))
            lengths.append(getattr(uf_obj, l_attr))

        # if IP units are requested, convert them
        if ip_:
            u_factors = UValue().to_ip(u_factors, 'W/m2-K')[0]
            lengths = Distance().to_ip(lengths, 'mm')[0]
