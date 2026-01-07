# Fairyfly: A Plugin for Environmental Analysis (GPL)
# This file is part of Fairyfly.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Fairyfly; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Search for available Materials within the fairyfly therm standards library.
-

    Args:
        keywords_: Optional keywords to be used to narrow down the output list of
            materials. If nothing is input here, all available materials
            will be output.
        join_words_: If False or None, this component will automatically split
            any strings of multiple keywords (spearated by spaces) into separate
            keywords for searching. This results in a greater liklihood of
            finding an item in the search but it may not be appropropriate for
            all cases. You may want to set it to True when you are searching for
            a specific phrase that includes spaces. Default: False.

    Returns:
        solid_mats: A list of solid materials within the fairyfly therm standards
            library (filtered by keywords_ if they are input).
        cavity_mats: A list of gas cavity materials within the fairyfly therm standards
            library (filtered by keywords_ if they are input).
"""

ghenv.Component.Name = 'FF Search Materials'
ghenv.Component.NickName = 'SearchMats'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'Fairyfly'
ghenv.Component.SubCategory = '1 :: THERM'
ghenv.Component.AdditionalHelpFromDocStrings = '3'

try:  # import the fairyfly-core dependencies
    from fairyfly.search import filter_array_by_keywords
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly:\n\t{}'.format(e))

try:  # import the fairyfly-therm dependencies
    from fairyfly_therm.lib.materials import SOLID_MATERIALS
    from fairyfly_therm.lib.materials import CAVITY_MATERIALS
except ImportError as e:
    raise ImportError('\nFailed to import fairyfly_therm:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import turn_off_old_tag
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))
turn_off_old_tag(ghenv.Component)


if len(keywords_) == 0:
    solid_mats = sorted(SOLID_MATERIALS)
    cavity_mats = sorted(CAVITY_MATERIALS)
else:
    split_words = True if join_words_ is None else not join_words_
    solid_mats = sorted(filter_array_by_keywords(SOLID_MATERIALS, keywords_, split_words))
    cavity_mats = sorted(filter_array_by_keywords(CAVITY_MATERIALS, keywords_, split_words))
