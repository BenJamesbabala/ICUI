# ICUI
一句话介绍：硕士毕业论文和ICUI论文的代码，包括了网络爬虫、数据清洗、回归分析三部分。按数据类型分为监测站基本信息(GIS)、百度地图兴趣点、空气污染数据。

语言：Python
软件：Spyder(Python 3.6)

#####################兴趣点（POI）数据的爬取和整理#######################
bounds：
利用百度地图API示例，得到上海市行政边界经纬度（http://lbsyun.baidu.com/jsdemo.htm#c1_10） ，作为划分小矩形的依据。

POI_crawler：
利用百度地图API的地点检索功能，爬取了上海市四种兴趣点（饭店、工厂、公交站、加油站）的基本信息。由于一次请求最多只能爬取400条数据，按上海市范围无法爬取所有的数据。利用矩形区域检索，将上海市划分成15 * 15 = 225个小矩形，循环爬取。保存为CSV文件，编码格式为'utf_8_sig'

POI_merge：
可能是由于电脑性能的原因，无法连续爬取225个矩形内的兴趣点。此次按0-75，75-150，150-225的顺序分批次爬取，最后合并在一起。

POI_jingweidu:
用百度地图API爬取的数据都是字符串格式，且经纬度包含在一个元素中，需要进行整理和转化。另外根据网络博主处理百度地图数据的经验，如果百度地图的经纬度是（x,y）实际的应该是（x,y）+（-0.01185，-0.00328）=（x-0.01185，y-0.00328）

在ArcGIS中做Buffer处理，导出100m\300m\500m\1000m\3000m范围内的信息

#####################监测站信息与GIS信息的拼接#######################
points_jingweidu
从"上海环境监测-非国控站.xlsx"获得监测站的经纬度信息。

points_huizong_100：
统计Buffer = 100m的兴趣点个数、道路长度、人口数量、土地利用类型，merge到监测站经纬度信息表中，保存为CSV格式。以此类推，统计300m\500m\1000m\3000m内的信息，merge在"监测点信息汇总_3000.csv"中。

#####################污染物数据的清洗与回归##########################
pollution_preprocess_week：
读入"上海环境监测-非国控站.xlsx"。删除缺失数据；为PM2.5、二氧化氮、风速、气温、气压设置阈值；删除少于8小时的数据；增加工作日/非工作日变量；按周统计工作日/非工作日平均；产生日平均数据库、周平均数据库和月平均数据库.csv。

pollution_merge：
将监测站信息和污染物数据库合并，产生用于回归的最终数据库。

pollution_regression_stepwise：
排除共线性变量后，运用stepwise策略，挑选进入多元线性回归的变量，分别对日平均数据（含/不含月份虚拟变量）、周平均数据和月平均数据（含/不含月份虚拟变量）进行回归。

pollution_regression_RF：
调用python中sklearn的随机森林包，分别对日平均数据（含/不含月份虚拟变量）、周平均数据和月平均数据（含/不含月份虚拟变量）进行回归。

####################图形绘制#########################
plot_figure_line:
绘制日均、月均数据的折线图。

plot_figure_scatter:
绘制自变量与因变量的散点图。

U-shape:
绘制标准U型曲线。

####################回归映射###########################
mapping_database:
确定挑选某一天的数据。

mapping_huizong:
将监测点信息、污染物数据、GIS中整理得到的数据合并。

pollution_prediction_stepwise:
利用stepwise，根据挑选出的重要变量，预测上海市1km✖1km的污染地图。

pollution_prediction_RF:
利用RF，根据挑选出的重要变量，预测上海市1km✖1km的污染地图。


