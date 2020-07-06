# javdb_crawl

基requests爬取javdb工具

基本流程：

1、爬取所有演员地址

2、爬取演员下的作品地址

3、保存每个作品的html

4、根据本地html提取info

5、保存为json

6、用json_to_xlsx 转为excel


py食用条件：

1、安装 python3

2、安装 requests 模块

pip install requests

3、安装 lxml 模块

pip install lxml

4 安装 cfscrape 模块

pip install cfscrape

一些声明：

此工具仅用于学习交流使用，请勿用做商业用途

已知问题，请大佬斧正：

1、因为求稳，速度有点慢，求大佬帮搞一下并发

2、树莓派可以跑，得替换路径斜杠




一些感谢：

感谢id:117503445大佬代码的启发

