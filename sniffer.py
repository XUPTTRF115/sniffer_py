
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


def listdevs():
    devs = pcap.findalldevs()
    if (args.list != False):
        print("list the devices:")
        if(len(devs) == 0):
            print("no device is avaliable")
        else:
            for dev in devs:
                print(dev)
    return devs


def devstart():
    devs = listdevs()
    dev = ''
    
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

def runlisten():
    try:
        count = 0
        dev = devstart()
        if(dev == ''):
            print("[-- quit --]")
            return False
        if(args.count == None):
            args.count = 10        
        if(args.save != None):
            f = open(args.save,"w")
        for ptime, pdata in dev:
            p = dpkt.ethernet.Ethernet(pdata)
            if p.data.__class__.__name__ == 'IP':
                ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
                if p.data.data.__class__.__name__ == 'TCP':
                    if p.data.data.dport == 80:
                        if(len(p.data.data.data) != 0):
                            print(p.data.data.data)
                            print("\n\n\n\n")
                            print("-------------------------------------------------------------")
                        if((args.count != None) and (int(args.count) > count) and (len(p.data.data.data)!=0)):
                            count += 1
                            f.write("count:" + str(count) + "\t\n" + p.data.data.data + "\t\n\t\n\t\n")
                        elif(int(args.count) <= count):
                            f.close()
                            print(str(args.count) + " results at above.")
                            break
    except KeyboardInterrupt:
        print("KeyboardInterrupt Exception .... ")
    except IOError:
        print("Please check your input path.")
        print("Can not find the path :" + args.save)
    except Exception as e:
        print("Some error message : ")
        print(e)
    # nrecv,ndrop,nifdrop=pc.stats()


def doscraw(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "referer": url
    }
    
    responsePart = requests.get(url, headers=headers)
    responsePart.encoding='utf-8'

    #xml = etree.HTML(responsePart.text)
    print(responsePart.text)

if __name__ == "__main__":
    if(args.scraw == None):
        runlisten()
    else:
        doscraw(args.scraw)
    
        
