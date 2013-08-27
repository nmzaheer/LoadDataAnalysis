import urllib2
import re


url = "http://tneb.tnebnet.org/newlt/consno.php"

def pat_match(url, pattern):
    response = urllib2.urlopen(url)
    html = response.read()
    match = re.findall(pattern, html)
    return match

def extract_sec_code(reg):
    target = url + '?code=' + str(reg)
    pattern = r'<option value=\S(\d{2,}\w*)\S'
    return pat_match(target, pattern)

def extract_dist_code(reg, sec):
    target = url + '?code=' + str(reg) + '&scode=' + sec
    pattern = r'<option value=\S(\d{3})[^\w]'
    return pat_match(target, pattern)

def extract_servcode():
    f = open('servcode.txt','w')
    dist_num = 0
    for reg_no in range(1,10):
        f.write(str(reg_no)+'\n')
        sec_list = extract_sec_code(reg_no)
        for section in sec_list:
            dist_list = extract_dist_code(reg_no, section)
            f.write('\t' + section[:3]+'\n')
            for distribution in dist_list:
                f.write('\t\t' + distribution + '\n')
            dist_num +=len(dist_list)
    print "Done"
    print dist_num


if __name__ == '__main__':
    extract_servcode()
