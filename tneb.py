import urllib2
import urllib
import base64
import re


def main():
    url = 'http://tneb.tnebnet.org/newlt/consumerwise_gmc_report.php'
    cons_db = {}
    f=open('shenoy.txt','a')
    for num in range(166,450):
        val = 'TANGEDCO||171||065||' + str(num)
        data = {'encserno': base64.b64encode(val), 'rsno': base64.b64encode('9')}
        params = urllib.urlencode(data)
        response = urllib2.urlopen(url, params)
        html = response.read()
        response.close()
        if re.search(r'NOT A', html):
            print "Not valid"
        else:
            match = re.search(r'</span>(\d+)',html)
            cons_id = match.group(1)
            print cons_id + ' '
            if re.search(r'METER REMOVED', html):
                pass
                #print "Meter removed"
            elif re.search(r'DISCONNECTED', html):
                pass
                #print "Disconnected"
            elif re.search(r'Collection Details', html):# and re.search(r'LA1A', html) :
                html = html[html.find('Collection')+100:]
                html = html[:html.find('/table')]
                entry_match = re.findall(r'size=2>[&a-z;]*([\d/]*)', html)
                num_entry_match = re.findall(r'<tr', html) 
                cons_unit = [int(entry_match[i*16 +3]) for i in range(len(num_entry_match)-1)]
                f.write(cons_id+' ')
                for reading in cons_unit:
                    f.write(str(reading)+' ')
                f.write('\n')
                

if __name__ == '__main__':
    main()
