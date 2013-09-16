"""
Get Region, Section, Distribution Code
__________________________________________

This script gathers data for determining the Service Number of a consumer.
It saves the Region, Section, Distribution code in a text file in an ordered
fashion

"""
import urllib2
import re


base_url = "http://tneb.tnebnet.org/newlt/consno.php"


def match_pattern(url, pattern):
    """Matches the pattern at the URL.

    Returns a list of strings which mathces the given regex pattern in the
    response of the URL

    Args:
        url: A string containing the URL
        pattern: Regular Expression pattern

    Returns:
        A list of strings that matches the given regex pattern. For example:

        ['128,'564,'036','025','487']

    """
    response = urllib2.urlopen(url)
    html = response.read()
    match = re.findall(pattern, html)
    return match


def get_section_code(region_num):
    """Gets a list of Section codes in the Region.

    Args:
        region_num: Region code where the Section belongs

    Returns:
        A list of strings representing the Section code under the given Region
    """
    target_url = base_url + '?code=' + str(region_num)
    pattern = r'<option value=\S(\d{2,}\w*)\S'
    return match_pattern(target_url, pattern)


def get_distribution_code(region_num, section_num):
    """Gets a list of Distribution codes in the given Section.

    Args:
        region_num: Region code where the Section belongs
        section_num: Section code where the Distribution codes need to be
                     obtained

    Returns:
        A list of strings of Distribution code under the Section. For example:

        ['501CHNG', '307PORU', '568MNGR', '317TMBM']
    """
    target_url = (base_url + '?code=' +
                  str(region_num) + '&scode=' + section_num)
    pattern = r'<option value=\S(\d{3})[^\w]'
    return match_pattern(target_url, pattern)


def get_service_num_data():
    """Gets data required for forming a Service Number.

    Args:
        None

    Returns:
        None

    Output:
        The Region, Section, Distribution codes are written to a text file
        in the following format:

        Region_Code
            Section_Code
                Distribution_Code
                .....
                .....
            Section_Code
                Distribution_Code
                .....
        Region_Code
            .............
            ............
    """
    with open('code.txt', 'w') as f:
        total_regions = 1
        for region_num in range(1, total_regions + 1):
            f.write(str(region_num)+'\n')
            section_list,section_name = get_section_code(region_num)
            for section in section_list:
                distribution_list = get_distribution_code(region_num, section)
                f.write('\t' + section[:3]'\n')
                for distribution in distribution_list:
                    f.write('\t\t' + distribution + '\n')
    f.close()


if __name__ == '__main__':
    get_service_num_data()
