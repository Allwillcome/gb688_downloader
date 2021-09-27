# 介绍
**gb688在改版后采用了加密，现已不支持下载。具体的讨论可以参考这个[issue](https://github.com/lzghzr/TampermonkeyJS/issues/27)**

这是一个中国行业标准、地方标准、自然资源标准的下载工具
行业标准、地方标准来自[全国标准信息公共服务平台](http://std.samr.gov.cn/)
自然资源来自[自然资源标准化信息服务平台](http://www.nrsis.org.cn/portal/xxcx/std)  

# 安装
    git clone git@github.com:renmu123/gb688_downloader.git
    cd gb688_downloader
    poetry install # 如果没有安装 poerty，自行到官网进行安装

# win cli 示例
    # 去 releases (https://github.com/renmu123/gb688_downloader/releases) 下载最新命令行程序
    std_cli.exe help # 查看教程
    std_cli.exe download help  # 直接从页面下载
    std_cli.exe search help  # 搜索下载

# 源码 cli 示例
    # 进入虚拟环境
    poetry shell
    # 下载标准
    python std_cli.py download http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8DE982AF0ED306A4033F37C219E6FCF3 城乡居民基本养老保险个人账户管理规范.pdf
    # help
    python std_cli.py help
    
    # 搜索内容，默认保存在当前文件夹
    python std_cli.py search 养老

# api 示例
    from standard import HDB, NatureStd
    
    if __name__ == '__main__':
        hb = HDB('hbba')
        db = HDB('dbba')
        data = db.search('政务云工程评价指标体系及方法')
        first_record = data["records"][0]
        name = f'{first_record["code"]}({first_record["chName"]}'
        db.download(pk=first_record['pk'], name=name)
    
        std = NatureStd()
        std.search("")
        std.download("http://www.nrsis.org.cn/portal/stdDetail/211166", "乡（镇）土地利用总体规划制图规范.pdf") #行标

# 打包
    # 下面的打包方法很有可能报错，解决方法参考这个 issue(https://github.com/jazzband/prettytable/issues/82)
    pyinstaller -F std_cli.py

## 地标和行标中的一些参数
## 地方标准中的`ministry`代号

| 城市             | 代号      |
| ---------------- | --------- |
| 北京市           | bjzjj     |
| 天津市           | tjzjj     |
| 河北省           | hebeizjj  |
| 山西省           | sxzjj14   |
| 内蒙古自治区     | nmgzjj    |
| 辽宁省           | lnzjj     |
| 吉林省           | jlzjj     |
| 黑龙江省         | hljzjj    |
| 上海市           | shzjj     |
| 江苏省           | jszjj     |
| 浙江省           | zjzjj     |
| 安徽省           | ahzjj     |
| 福建省           | fjzjj     |
| 江西省           | jxzjj     |
| 山东省           | sdzjj     |
| 河南省           | henanzjj  |
| 湖北省           | hubeizjj  |
| 湖南省           | hunanzjj  |
| 广东省           | gdzjj     |
| 广西壮族自治区   | gxzjj     |
| 海南省           | hainanzjj |
| 重庆市           | cqzjj     |
| 四川省           | sczjj     |
| 贵州省           | gzzjj     |
| 云南省           | ynzjj     |
| 西藏自治区       | xzzjj     |
| 陕西省           | sxzjj61   |
| 甘肃省           | gszjj     |
| 青海省           | qhzjj     |
| 宁夏回族自治区   | nxzjj     |
| 新疆维吾尔自治区 | xjzjj     |

## 行业标准中的`ministry`代号
| 部门                 | 代号     |
|----------------------|----------|
| 工业和信息化部       | gxb      |
| 公安部               | gab      |
| 国防科工局           | gfkgj    |
| 国家档案局           | daj      |
| 国家发展和改革委员会 | fgw      |
| 国家广播电视总局     | gbdszj   |
| 国家粮食和物资储备局 | lswzcbj  |
| 国家林业和草原局     | lycyj    |
| 国家煤矿安全监察局   | mkaqjcj  |
| 国家密码管理局       | mmglj    |
| 国家能源局           | nyj      |
| 国家市场监督管理总局 | scjdglzj |
| 国家税务总局         | swj      |
| 国家体育总局         | tyzj     |
| 国家铁路局           | tlj      |
| 国家文物局           | wwj      |
| 国家新闻出版署       | xwcbs    |
| 国家烟草专卖局       | yczmj    |
| 国家药监局           | yjj      |
| 国家邮政局           | yzj      |
| 国家中医药局         | zyyj     |
| 海关总署             | hgzs     |
| 交通运输部           | jtysb    |
| 教育部               | jyb      |
| 民政部               | mzb      |
| 农业农村部           | ncnyb    |
| 人力资源和社会保障部 | rlsb     |
| 商务部               | swb      |
| 生态环境部           | sthjb    |
| 水利部               | slb      |
| 司法部               | sfb      |
| 卫生健康委员会       | wsjkwyh  |
| 文化和旅游部         | whlyb    |
| 应急管理部           | yjglb    |
| 中国地震局           | dzj      |
| 中国民用航空局       | myhkj    |
| 中国气象局           | qxj      |
| 中国人民银行         | rmyh     |
| 中华全国供销合作总社 | gxhzs    |
| 住房和城乡建设部     | zfcxjsb  |
| 自然资源部           | zrzyb    |
| 国家电影局           | gjdyj    |

## 行业标准中的`industry`代号
| 参数                     	|
|--------------------------	|
| 安全生产                 	|
| 包装                     	|
| 船舶                     	|
| 测绘                     	|
| 城镇建设                 	|
| 新闻出版                 	|
| 档案                     	|
| 地震                     	|
| 电力                     	|
| 地质矿产                 	|
| 核工业                   	|
| 纺织                     	|
| 公共安全                 	|
| 供销合作                 	|
| 国密                     	|
| 广播电影电视             	|
| 广播电影电视             	|
| 航空                     	|
| 化工                     	|
| 环境保护                 	|
| 海关                     	|
| 海洋                     	|
| 机械                     	|
| 建材                     	|
| 建筑工程                 	|
| 金融                     	|
| 交通                     	|
| 教育                     	|
| 旅游                     	|
| 劳动和劳动安全           	|
| 粮食                     	|
| 林业                     	|
| 民用航空                 	|
| 煤炭                     	|
| 民政                     	|
| 民政                     	|
| 能源                     	|
| 农业                     	|
| 轻工                     	|
| 汽车                     	|
| 航天                     	|
| 气象                     	|
| 国内贸易                 	|
| 国内贸易                 	|
| 水产                     	|
| 司法                     	|
| 石油化工                 	|
| 电子                     	|
| 水利                     	|
| 出入境检验检疫           	|
| 税务                     	|
| 石油天然气               	|
| 铁路运输                 	|
| 土地管理                 	|
| 体育                     	|
| 物资管理                 	|
| 文化                     	|
| 兵工民品                 	|
| 外经贸                   	|
| 卫生                     	|
| 文物保护                 	|
| 稀土                     	|
| 黑色冶金                 	|
| 烟草                     	|
| 通信                     	|
| 有色金属                 	|
| 医药                     	|
| 邮政                     	|
| 中医药                   	|
| 认证认可                 	|
| 消防救援                 	|
| 减灾救灾与综合性应急管理 	|


# 免责声明
**本项目仅供学习交流之用，请勿用于非法用途。**