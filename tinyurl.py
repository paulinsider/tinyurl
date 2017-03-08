#encoding:utf-8
import urllib
import urllib2
from optparse import OptionParser
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

def check_url(url):
	pos = url.find('/')
	uurl = "http://preview.tinyurl.com" + url[pos:]
	req = urllib2.Request(uurl)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	if (res.find("Error: Unable to find site's URL to redirect to") != -1):
		return True
	else:
		poss = res.find("<blockquote><b>")
		pose = res.find("<br /></b></blockquote>")
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', res[poss+15:pose])
        return dd

def generate_url(url, alias=''):
	uurl = "http://tinyurl.com/create.php?source=indexpage&url=" + url + "&submit=Make+TinyURL%21&alias=" + alias
	req = urllib2.Request(uurl)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	poss = res.find("<div class=\"indent\"><b>")
	pose = res.find("</b><div id=\"success\">")
	return res[poss+23:pose]

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", dest="input", type="string", default="input.txt", help="输入文件，以行为单位，目标url和别名之间用空格隔开。")
    parser.add_option("-o", "--output", action="store", dest="output", type="string", default="output.txt", help="输出文件，以行为单位。")
    parser.add_option("-c", "--check", action="store_true", dest="check", help="检查所用别名是否被占用。")
    parser.add_option("-g", "--generate", action="store_true", dest="generate", help="生成短地址，如果别名被占用则使用随机生成的。")
    (option, args) = parser.parse_args()

    fin = open(option.input, "r")
    fout = open(option.output, "a")
    list = fin.readlines()
    if option.check == True:
        res = []
        num = 1
        for line in list:
            line = line.strip()
            data = line.split(' ')
            if len(data) == 1:
                tmp = data[0]
                r = check_url(data[0])
                if r == True:
                    tmp = tmp + "未被占用"
                else:
                    tmp = tmp + "被占用：" + r
            else:
                print "输入文件有误，line:" + num
                exit(0)
            res.append(tmp + "\n")
            num += 1
        fout.writelines(res)
    elif option.generate == True:
        res = []
        num = 1
        for line in list:
            line = line.strip()
            data = line.split(' ')
            if len(data) == 1:
                r = generate_url(data[0])
                tmp = data[0] + ":" + r
            elif len(data) == 2:
                rr = check_url('/' + data[1])
                if rr != True:
                    tmp = data[1] + "被占用"
                r = generate_url(data[0], data[1])
                tmp = tmp + ' ' +data[0] + ':' + r
            else:
                print "输入文件有误，line:" + num
                exit(0)
            res.append(tmp + "\n")
            num += 1
        fout.writelines(res)
