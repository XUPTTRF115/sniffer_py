
#import pcap
#import dpkt
#devs = pcap.findalldevs()
#for dev in devs:
#    print(dev)
#pc = pcap.pcap()
#pc.setfilter('tcp port 80')
#for ptime,pdata in pc:
#    print(ptime, pdata)

#########################################################

import pcap
import dpkt
import argparse
import requests
from lxml import etree

#参数处理
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--run", help="start listening on a device, and you can use `all` for all device you can find ")
parser.add_argument("-s", "--scraw", help="scraw the page's html content ")
parser.add_argument("-x", "--xpath", help="xpath of the lxml, sort the result of scraw page ")
parser.add_argument("-st", "--save", help="save to file, require a param for file path")
parser.add_argument("-c", "--count", help="the max of package number, default 10 ")
parser.add_argument("-l", "--list", help="list all devices", action="store_true")
# parser.add_argument("-compare", "--compare", help="",nargs="+")
args = parser.parse_args()
#print(args)

#列出设备
def listdevs():
    #通过pcap查找所有可用设备
    devs = pcap.findalldevs()
    if (args.list != False):
        print("list the devices:")
        if(len(devs) == 0):
            print("no device is avaliable")
        else:
            for dev in devs:
                print(dev)
    return devs

#选择启用设备
def devstart():
    #获取设备信息列表
    devs = listdevs()
    dev = ''

    #根据不同的用户输入参数run选择设备
    if(len(devs) == 0):
        print("start error , no device found.")
        return dev
    
    if (args.run != None):
        if (args.run in devs):
            print("start listening on " + args.run)
            dev = pcap.pcap(args.run)
        elif (args.run == 'all'):
            print("start listening on all")
            dev = pcap.pcap()
        else:
            print("can not find the device of " + args.run)
            print("quit")
    return dev

# pc.setfilter('tcp port 80')

#主要监听程序
def runlisten():
    try:
        #定义计数器
        count = 0
        #查找设备，如果没有找到则返回
        dev = devstart()
        if(dev == ''):
            print("[-- quit --]")
            return False
        #默认给予10个有效包长度
        if(args.count == None):
            args.count = 10        
        #打开指定路径文件
        if(args.save != None):
            f = open(args.save,"w")
        for ptime, pdata in dev:
            #解析数据包
            p = dpkt.ethernet.Ethernet(pdata)
            if p.data.__class__.__name__ == 'IP':
                ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
                if p.data.data.__class__.__name__ == 'TCP':
                    if p.data.data.dport == 80:
                        #如果监听到的数据长度不为0则打印出数据
                        if(len(p.data.data.data) != 0):
                            print(p.data.data.data)
                            print("\n\n\n\n")
                            print("-------------------------------------------------------------")
                        #如果在规定请求次数内，并且数据长度大于0 save参数不为空 将内容写入文件
                        if((args.count != None) and (int(args.count) > count) and (len(p.data.data.data)!=0)):
                            count += 1
                            if(args.save != None):
                                f.write("count:" + str(count) + "\t\n" + p.data.data.data + "\t\n\t\n\t\n")
                        elif(int(args.count) <= count):
                            if(args.save != None):
                                f.close()
                            print(str(args.count) + " results at above.")
                            break
    #当用户键盘打断
    except KeyboardInterrupt:
        print("KeyboardInterrupt Exception .... ")
    #当存储文件打开或文件路径出错
    except IOError:
        print("Please check your input path.")
        print("Can not find the path :" + args.save)
    #其他意外的异常情况
    except Exception as e:
        print("Some error message : ")
        print(e)
    # nrecv,ndrop,nifdrop=pc.stats()

#开始爬取网站内容
def doscraw(url):
    try:
        #设置请求头
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "referer": url
        }
        
        #发起请求得到响应
        response = requests.get(url, headers=headers)
        #设置响应编码格式
        response.encoding='utf-8'

        #转成xml文档
        xml = etree.HTML(response.text)
        result = response.text
        if(args.xpath != None):
            #筛选响应内容
            result = xml.xpath(args.xpath)
            #如果xpath没有匹配到内容
            if(len(result) == 0):
                print("the result is empty . please check your xpath")
                return False
            #如果匹配到了将Unicode编码文字转成utf-8格式输出
            for item in result: 
                print(item.encode('utf-8'))
            return True
        print(result)
        return True
    #当出错情况，打印出错信息
    except Exception as e:
        print("error occoured:")
        print(e)

if __name__ == "__main__":
    #如果抓取页面则不进行监听
    if(args.scraw == None):
        runlisten()
    else:
        doscraw(args.scraw)
    
        
