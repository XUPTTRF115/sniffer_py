# sniffer_py
python - 网络嗅探器

## 用法
    python sniffer.py 参数列表
    参数列表:
      -r   --run"    指定接口开始运行，可以使用all指定所有网卡接口
      -s   --scraw   爬取html内容，供分析参考
      -x   --xpath   指定xpath规则匹配指定爬取内容
      -st  --save    将结果保存到文件，需指定路径
      -c   --count   最大嗅探包数目，默认为10
      -l   --list    列出所有可用的网卡接口

## 依赖
    pypcap : 安装参考[Python之pypcap库的安装及简单抓包工具的实现]
    dpkt   : pip install dpkt
    lxml   : pip install lxml
+ [Python之pypcap库的安装及简单抓包工具的实现](https://blog.csdn.net/weixin_34342992/article/details/88004374?utm_source=app/)

## 参考
```python
import pcap
import dpkt
devs = pcap.findalldevs()
for dev in devs:
    print(dev)
pc = pcap.pcap()
pc.setfilter('tcp port 80')
for ptime,pdata in pc:
    print(ptime, pdata)
```

## 说明
本嗅探器使用python实现，在监听基础上加以扩展，仅供学习和参考使用。