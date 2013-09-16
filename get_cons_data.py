"""
Consumer Data Extraction
_ _ _ _ _ _ _ _ _ _ _ _ _
- - - - - - - - - - - - -

This script will extract consumer data like Consumer ID, Type of Consumer
and Consumption details from the URL given
"""

import base64
import re
import sys
import urllib
import urllib2



def get_cons_data(html):
    """Returns data of the given Consumer Number

    Args:
        cons_no: A string containing the Consumer Number

    Returns:
        A dict containing Consumer Number, Type of Consumer. Assessment Date
        and Reading details is written to a database. For example

        cons_data = {'cons_no':'0842411563', 'type':'LA1A',
                     'ass_date':['22/07/2013','20/05/2013','23/03/2013'],
                     'units_cons':[500,645,458]}
    """
    cons_det = {}
    match = re.search(r'>:([\w\s.]+)\b', html)
    cons_det['name'] = match.group(1)
    html = html[match.end():]
    match = re.search(r'(\d{11})', html)
    cons_det['cons_no'] = match.group(1)
    html = html[match.end():]
    match = re.search(r'(L\w\d\w)', html)
    cons_det['tariff'] =match.group(1)
    html = html[match.end():]
    cons_det['address'] = extract_address(html)
    html = html[html.find('Collection')+100 :]
    html = html[: html.find('/table')]
    entry_match = re.findall(r'size=2>[&a-z;]*([\d/]*)', html)
    num_entry_match = len(re.findall(r'<tr', html))
    cons_unit = [int(entry_match[i*16 + 3]) for i in range(num_entry_match-1)]
    cons_det['units_cons'] = cons_unit
    ass_date = [entry_match[i*16] for i in range(num_entry_match-1)]
    cons_det['ass_date'] = ass_date
    return cons_det

def valid_consumer(cons_no):
    if len(cons_no) == 11:
        response = get_response(cons_no)
    else:
        print "Invalid Service Number"
        sys.exit(0)
    if re.search(r'(Not valid | METER REMOVED | DISCONNECTED)', response):
        print "No details available for the given service number"
        sys.exit(0)
    elif re.search(r'Collection Details', response):
        return get_cons_data(response)

def get_response(cons_no):
    url = "http://tneb.tnebnet.org/newlt/consumerwise_gmc_report.php"
    cons_det = {}
    val = "TANGEDCO||" + cons_no[2:5]+"||" + cons_no[5:8]+"||"+cons_no[8:]
    data = {'encserno': base64.b64encode(val),
            'rsno': base64.b64encode(cons_no[:2])}
    params = urllib.urlencode(data)
    response = urllib2.urlopen(url, params)
    html = response.read()
    response.close()
    return html


def extract_address(src):
    start = src.find('ADDRESS')
    end = src.find('SERVICE STATUS')
    a = re.search(r';([A-Z\d.,]+)<', src[start:end])
    return a


def print_cons_data(dict):
    print "\nConsumer Name: %s\t Service Number: %s\t Type: %s" % (dict['name'], dict['cons_no'], dict['tariff'])
    print "Assessment Date\t\tUnits Consumed"
    for i in range(len(dict['units_cons'])):
        print "%s\t\t%s" % (dict['ass_date'][i], dict['units_cons'][i])
    
    
def  main():
    args = sys.argv[1:]
    if not args:
        print "\nusage:[--range] serv_num [serv_num_end]"
        sys.exit(0)
    if args[0] == '--range':
        for num in range(args[1],args[2]):
            d = valid_consumer(num)
            print_cons_data(d)
            print ""
    d = valid_consumer(args[0])
    print_cons_data(d)
    
    
if __name__=='__main__':
    main()
