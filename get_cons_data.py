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



def get_cons_data(cons_no):
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
    url = "http://tneb.tnebnet.org/newlt/consumerwise_gmc_report.php"
    cons_det = {'cons_no','type','ass_date','units_cons'}
    val = "TANGEDCO||" + cons_no[2:5]+"||" + cons_no[5:8]+"||"+cons_no[8:]
    data = {'encserno': base64.b64encode(val),
            'rsno': base64.b64encode(cons_no[:2])}
    params = urllib.urlencode(data)
    response = urllib2.urlopen(url, params)
    html = response.read()
    response.close()
    match = re.search(r'</span>(\d+)', html)
    cons_det['cons_no'] = match.group(1)
    match = re.search(r'(L\w\d\w)', html)
    cons_det['type'] =match.group(1)
    html = html[html.find('Collection'+100) :]
    html = html[: html.find('/table')]
    


def print_cons_data(dict):
    print "Service Number: %s\t Type: %s" % (dict['cons_no'], dict['type'])
    print "Assesment Date\tUnits Consumed"
    for i in range(len(dict['units_cons'])):
        print "%s\t%s" % (dict['ass_date'][i], dict['units_cons'][i])
    
    
def  main():
    args = sys.argv[1:]
    if not args:
        print "\nusage:[--range] serv_num [serv_num_end]"
        sys.exit(0)
    if args[0] == '--range':
        for num in range(args[1],args[2]):
            d = get_cons_data(num)
            print_cons_data(d)
            print ""
    d=get_cons_data(args[0])
    #print_cons_data(d)
    
    
if __name__=='__main__':
    main()
