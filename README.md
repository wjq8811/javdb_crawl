# javdb_crawl

基于硒+铬爬取javdb工具

基本流程：

1、爬取所有演员地址

2、爬取演员下的作品地址

3、保存每个作品的html

4、根据本地html提取info

5、保存为json

exe食用条件：

1、安装chrome

2、下载对应版本的chromedriver，并将exe文件放到py文件目录下

文件夹中的chromedriver支持chrome 83.0.4103.116（正式版本）

py食用条件：

1、安装 selenium 模块

pip install selenium

2、安装chrome

3、下载对应版本的chromedriver，并将exe文件放到py文件目录下

4、安装 lxml 模块

pip install lxml

一些声明：

此工具仅用于学习交流使用，请勿用做商业用途

已知问题，请大佬斧正：

1、因为求稳，速度有点慢

2、因为懒，没有写跳过已存在的文件

3、树莓派可以跑，得替换路径斜杠




一些感谢：

感谢id:117503445大佬代码的启发


