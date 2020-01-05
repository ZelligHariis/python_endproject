from flask import Flask,render_template,request,escape
import csv
import pandas as pd

app = Flask(__name__)

csvdata = []

df = pd.read_excel('data/museum.csv', encoding='gbk', delimiter="\t")
regions_available_loaded = list(df.地区.dropna().unique())

@app.route('/')
def first() -> 'html':
    title = "数据故事"
    return render_template('first.html',
                           the_title = title)

@app.route('/gdp')
def base() -> 'html':
    title = "城市GDP数据"
    with open('data/GDP.csv') as csv1:
        for line in csv1:
            csvdata.append([])
            for item in line.split(','):
                csvdata[-1].append(item)
    return render_template('yutingjiejie.html',
                           the_title = title,
                           the_data = csvdata)


@app.route('/option' , methods=['POST'])
def result() -> 'html':
    return_shengfen = ["全部","北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省","吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省","福建省","山东省","江西省","湖北省","河南省","湖南省","广东省","广西壮族自治区","海南省","重庆市","四川省","贵州省","云南省","西藏自治区","陕西省","甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区"]
    return_nianfen = ["全部","2018年","2017年","2016年","2015年","2014年","2013年","2012年","2011年","2010年","2009年","2008年","2007年","2006年","2005年","2004年","2003年","2002年","2001年","2000年","1999年"]
    shengfen = request.form['shengfen']
    nianfen = request.form['nianfen']
    title = "这是筛选后的结果："
    if shengfen == "全部" and nianfen =="全部":
        return render_template('yutingjiejie.html',
                               the_title=title,
                               the_data=csvdata)
    elif shengfen != "全部" and nianfen == "全部":
        return render_template('result.html',
                               the_title = title,
                               the_nianfen = nianfen,
                               the_shengfen = shengfen,
                               the_data1 =csvdata[return_shengfen.index(shengfen)],
                               the_data2 = csvdata[0])
    elif shengfen == "全部" and nianfen != "全部":
        option1 = []
        option2 = []
        acout = 0
        while True:
            option1.append(csvdata[acout][return_nianfen.index(nianfen)])
            option2.append(csvdata[acout][0])
            acout += 1
            if acout == 32:
                break
            else:
                continue
        return render_template('result1.html',
                               the_title = title,
                               the_nianfen = nianfen,
                               the_shengfen = shengfen,
                               the_data1 = option1,
                               the_data2 = option2)
    else:
        data = csvdata[return_shengfen.index(shengfen)][return_nianfen.index(nianfen)]
        return render_template('result2.html',
                               the_title = title,
                               the_nianfen = nianfen,
                               the_shengfen = shengfen,
                               the_data = data)

@app.route('/hurun', methods=['GET'])
def hu_run_2019() -> 'html':
    data_str = df.to_html()
    regions_available = regions_available_loaded  # 下拉选单有内容
    return render_template('museum.html',
                           the_res=data_str,  # 表
                           the_select_region=regions_available)

@app.route('/hurun1', methods=['POST'])
def hu_run_select() -> 'html':
    the_region = request.form["the_region_selected"]  ## 取得用户交互输入
    print(the_region)  ## 检查用户输入, 在后台
    dfs = df.query("地区=='{}'".format(the_region))  ## 使用df.query()方法. 按用户交互输入the_region过滤
    data_str = dfs.to_html()  # <------------------数据产出dfs, 完成互动过滤呢
    regions_available = regions_available_loaded  # 下拉选单有内容
    return render_template('museum.html',
                           the_res=data_str,
                           the_select_region=regions_available)

@app.route('/number')
def shijie1() -> 'html':
    title = "各省博物馆数量与旅客数的关系"
    return render_template('trop.html',
                           the_title = title)

@app.route('/art')
def shijie2() -> 'html':
    title = "各省艺术表演场馆出场数与旅客数的关系"
    return render_template('art.html',
                           the_title = title)

@app.route('/start',methods=['POST'])
def start() -> 'html':
    title = "数据故事"
    return render_template('first.html',
                           the_title = title)

if __name__ == '__main__':
    app.run()
