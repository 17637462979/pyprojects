#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/6
# @Author  : zhang
import os
import re
from urllib.parse import unquote

import pymysql
import requests
from fake_useragent import UserAgent
import wget
from lxml import etree
from pyquery import PyQuery as pq
from mysql_connect import MysqlConnection


class BLG(object):
    base_url = 'http://bryant.bitzh.edu.cn'  #中文版
    start_url = 'http://bryant.bitzh.edu.cn/en' #英文版
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36',
    }
    ms = MysqlConnection('127.0.0.1', 'root', '123456', 'blg_data')


class home_page(BLG):
    # res = requests.get(url=BLG.base_url,headers=BLG.headers)
    def hots(self):
        doc = pq(url=BLG.start_url, headers=BLG.headers)
        # home_video = wget.download('http://bryant.bitzh.edu.cn/home.mp4', out='H:\\blg')
        # BLG.ms.insertOperation("""insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}',)""".format('首页','首页',home_video,'','','H:\\blg\\blg_english_file\\\\home.mp4',))
        hot_hrefs = pq(doc)('.news_top .c_width a').items()
        titles = pq(doc)('.news_top .c_width a img').items()
        up_dates = pq(doc)('.news_top .c_width a span').items()
        # print(up_dates)
        # hot_hrefs = [href.get('href') for href in hot_hrefs]
        # titles = [title.text() for title in up_dates]
        # print(titles)
        for href, title, up_date in zip(hot_hrefs, titles, up_dates):
            href = href.attr('href')
            title = title.attr('alt')
            up_date = up_date.text()
            # print(up_date)
            resp = requests.get(BLG.base_url + href, headers=BLG.headers)
            print(BLG.base_url + href)
            print(resp.text)
            content = pq(resp.text)('.news')
            img1 = pq(resp.text)('.news p img')
            img1 = [img.get('src') for img in img1]
            img2 = pq(resp.text)('.news div img')
            img2 = [img.get('src') for img in img2]
            imgs = img1 + img2
            # print(imgs)
            images = []
            for img in imgs:
                # img = wget.download(BLG.base_url + img, out='H:\blg')
                # print(img)
                r = requests.get(BLG.base_url + img)
                img = img.split('/')[-1]
                img = 'H:\\blg\\blg_english_file\\' + img
                with open(img,'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                    'home', 'news', title, up_date, content, images))
            # print(title, up_date, content, imgs)

            # BLG.ms.insertOperation(
            #     """insert into bblg_englishlg(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}',)""".format(
            #         '首页', 'hots', title, up_date, content, imgs, ))

    def teach_mod(self):
        doc = pq(url=BLG.start_url, headers=BLG.headers)
        teach_hrefs = pq(doc)('.techbox ul li a').items()
        teach_titles = pq(doc)('.techbox ul li a').items()
        for href,title in zip(teach_hrefs,teach_titles):
            # print(href.get('href'))
            if href.attr('href') == '/list/?57_1.html':
                continue
            href = href.attr('href')
            title = title.text()
            # print(BLG.base_url)
            # print('href:' + str(href))
            # print("asdasdasd" + str(BLG.start_url + href))
            html = pq(url=BLG.start_url + href, headers=BLG.headers)
            content = pq(html)('table')
            img1 = pq(html)('p img')
            img1 = [img.get('src') for img in img1]
            # img2 = pq(html)('td img')
            # img2 = [img.get('src') for img in img2]
            # imgs = img1 + img2
            images = []
            for img in img1:
                # img = wget.download(BLG.base_url + img, out='H:\blg')
                # print(img)
                r = requests.get(BLG.start_url + img)
                img = img.split('/')[-1]
                img = 'H:\\blg\\blg_english_file\\' + img
                with open(img, 'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,content,img) values('{}','{}','{}','{}','{}')""".format(
                    'home', 'Educational philosophy', title,content, images))


class for_us(BLG):
    # http://bryant.bitzh.edu.cn/about/?11.html
    def xmjj(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?11.html',
            headers=BLG.headers)
        content = pq(doc)('.desc')
        # print(content)

        img1 = pq(doc)('.leadership p img')
        imgs = [img.get('src') for img in img1]
        images = []
        for img in imgs:
            r = requests.get(BLG.base_url + img)
            img = img.split('/')[-1]
            img = 'H:\\blg\\blg_english_file\\\\' + img
            with open(img, 'wb') as f:
                f.write(r.content)
            images.append(img)
        images = ','.join(images)
        images = pymysql.escape_string(images)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,title,content,img) values('{}','{}','{}','{}','{}')""".format(
                '关于我们', '项目简介', '项目简介', content, images))

    def szdw(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?12.html',
            hreders=BLG.headers)
        trs = pq(doc)('#table1 tbody tr')
        for tr in trs:
            img_head = pq(tr)('td img').attr('src')
            if img_head is None:
                continue
            r = requests.get(BLG.base_url + img_head)
            img = img_head.split('/')[-1]
            img = 'H:\\blg\\blg_english_file\\' + img
            with open(img, 'wb') as f:
                f.write(r.content)
            # images.append(img)
            brief = pq(tr)('td p').text()
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,content,img) values('{}','{}','{}','{}')""".format(
                    '关于我们', '师资队伍',brief, img))
        # http://bryant.bitzh.edu.cn/about/?13.html

    def q_a(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?13.html',
            headers=BLG.headers)
        q_a_c = pq(doc)('.desc')
        imgs = pq(doc)('p img').items()
        images = []
        for img in imgs:
            # img = wget.download(BLG.base_url + img, out='H:\blg')
            img = img.attr('src')
            r = requests.get(BLG.base_url + img)
            img = img.split('/')[-1]
            img = 'H:\\blg\\blg_english_file\\' + img
            with open(img, 'wb') as f:
                f.write(r.content)
            images.append(img)
        images = ','.join(images)
        images = pymysql.escape_string(images)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,content,img) values('{}','{}','{}','{}')""".format(
                '关于我们', 'Q&A', q_a_c, images))

    def yxcg(self):
        # http://bryant.bitzh.edu.cn/list/?161_1.html
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?161_1.html',
            headers=BLG.headers)
        cg_hrefs = pq(doc)('.newslist li a').items()
        cg_hrefs = [cg_href.attr('href') for cg_href in cg_hrefs]
        # print(cg_hrefs)
        for cg_href in cg_hrefs:
            html = pq(BLG.base_url + cg_href, headers=BLG.headers)
            imgs = pq(html)('.news p img')
            name = pq(html)('.news h1').text()
            up_date = pq(html)('.date').text()
            # print(name,up_date)

            # print(imgs)
            # if imgs :
            #     if name == 'Kyung-Taek Lim':
            #         print(name,up_date,imgs)
            imgs = [img.get('src') for img in imgs]
            print(imgs)
            content = pq(html)('.news')
            images = []
            for img in imgs:
                # img = wget.download(BLG.base_url + img, out='H:\blg')
                # img = img.attr('src')
                r = requests.get(BLG.base_url + img)
                img = img.split('/')[-1]
                img = 'H:\\blg\\blg_english_file\\' + img
                with open(img, 'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,content,img) values('{}','{}','{}','{}','{}')""".format(
                    '关于我们', '教师研究成果', name, content,images))

    # 规章制度更新中...
    def gzzd(self):
        # http://bryant.bitzh.edu.cn/list/?160_1.html
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?160_1.html',
            headers=BLG.headers)
        content = pq(doc)('.newslist')
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,content) values('{}','{}','{}')""".format(
                '关于我们', '规章制度',content))


class zs(BLG):
    def zszc(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?110.html',
            headers=BLG.headers)
        zszc = pq(doc)('.desc')
        zszc_video = pq(doc)('embed').attr('src')
        zszc_name = wget.download(zszc_video,
            out='H:\\blg')
        zszc_name = pymysql.escape_string(zszc_name)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,content,img) values('{}','{}','{}','{}')""".format(
                '招生', '招生政策', zszc,zszc_name))

    def xf_jj(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?121.html',
            headers=BLG.headers)
        content = pq(doc)('.desc')
        img = pq(doc)('.desc p img').attr('src')
        img = wget.download(BLG.base_url + img, out='H:\\blg')
        img = pymysql.escape_string(img)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,content,img) values('{}','{}','{}','{}')""".format(
                '招生', '联系我们', content, img))
    def lxwm(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?111.html',
            headers=BLG.headers)
        content = pq(doc)('.desc')
        imgs = pq(doc)('.desc p img')
        imgs = [img.get('src') for img in imgs]
        images = []
        for img in imgs:
            # img = wget.download(BLG.base_url + img, out='H:\blg')
            # img = img.attr('src')
            r = requests.get(BLG.base_url + img)
            img = img.split('/')[-1]
            img = 'H:\\blg\\blg_english_file\\' + img
            with open(img, 'wb') as f:
                f.write(r.content)
            images.append(img)
        images = ','.join(images)
        images = pymysql.escape_string(images)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,content,img) values('{}','{}','{}','{}')""".format(
                '招生', '联系我们',content, images))


class jyjx(BLG):
    def zysz(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?18.html',
            headers=BLG.headers)
        content = pq(doc)('.desc')
        img = pq(doc)('.desc p img').attr('src')
        img = wget.download(BLG.base_url + img, out='H:\\blg')
        img = pymysql.escape_string(img)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,content,img) values('{}','{}','{}','{}')""".format(
                '教育教学', '专业设置', content, img))

    def kcsz(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?55_1.html',
            headers=BLG.headers)
        href = pq(doc)('.newslist li a').attr('href')
        print(href)
        html = pq(url=BLG.base_url + href, headers=BLG.headers)
        imgs = pq(html)('.news p img')
        name = pq(html)('.news h1').text()
        up_date = pq(html)('.date').text()
        imgs = [img.get('src') for img in imgs]
        # if imgs == []:
        content = pq(html)('.news')
        images = []
        for img in imgs:
            # img = wget.download(BLG.base_url + img, out='H:\blg')
            # img = img.attr('src')
            r = requests.get(BLG.base_url + img)
            img = img.split('/')[-1]
            img = 'H:\\blg\\blg_english_file\\' + img
            with open(img, 'wb') as f:
                f.write(r.content)
            images.append(img)
        images = ','.join(images)
        images = pymysql.escape_string(images)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                '教育教学', '课程设置', name, up_date,content, images))

    def jwc(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?138.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.desc a').items()
        hrefs = [href.attr('href') for href in hrefs]

        html1 = pq(
            url='http://bryant.bitzh.edu.cn/about/' +
            hrefs[0],
            headers=BLG.headers)
        ksap = pq(html1)('.desc').text()
        # BLG.ms.insertOperation(
        #     """insert into blg(fir_column,sec_column,title,content) values('{}','{}','{}','{}')""".format(
        #         '教育教学', '教务处', '考试安排',ksap))
        html2 = pq(
            url='http://bryant.bitzh.edu.cn/about/' +
            hrefs[1],
            headers=BLG.headers)
        names = pq(html2)('.desc').items()
        names = [name.text() for name in names][0].split('\n')
        # print(names)
        hrefs_biapge = pq(html2)('.desc p a')
        # Bryant Zhuhai Course Withdrawal form.pdf
        for name, href in zip(names, hrefs_biapge):
            # name = name.text
            href = href.get('href')
            # print(name,href)
            new_name = unquote(href.split('/')[-1])
            r = requests.get(url=BLG.base_url + href, headers=BLG.headers)
            # with open('H:\\blg\\blg_english_file\\' + new_name, 'wb') as f:
            #     f.write(r.content)
            # images = pymysql.escape_string('H:\\blg\\blg_english_file\\' + new_name)
            # BLG.ms.insertOperation(
            #     """insert into blg(fir_column,sec_column,title,img) values('{}','{}','{}','{}')""".format(
            #         '教育教学', '教务处', '学生常用表格', images))
        html3 = pq(
            url='http://bryant.bitzh.edu.cn/about/' +
            hrefs[2],
            headers=BLG.headers)
        imgs = pq(html3)('p img').items()
        imgs = [img.attr('src') for img in imgs]
        # print(imgs)
        # for img in imgs:
            # img = img.split('/')[-1]
            # print(img)
            # r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
            # with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
            #     f.write(r.content)
            #     images = pymysql.escape_string('H:\\blg\\blg_english_file\\' + img.split('/')[-1])
            #     BLG.ms.insertOperation(
            #         """insert into blg(fir_column,sec_column,title,img) values('{}','{}','{}','{}')""".format(
            #             '教育教学', '教务处', '课表', images))
        html4 = pq(
            url='http://bryant.bitzh.edu.cn/about/' +
            hrefs[3],
            headers=BLG.headers)
        imgs = pq(html4)('p img').items()
        imgs = [img.attr('src') for img in imgs]
        for img in imgs:
            pass
            # img = img.split('/')[-1]
            # print(img)
            # r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
            # with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
            #     f.write(r.content)
            #     images = pymysql.escape_string('H:\\blg\\blg_english_file\\' + img.split('/')[-1])
            #     BLG.ms.insertOperation(
            #         """insert into blg(fir_column,sec_column,title,img) values('{}','{}','{}','{}')""".format(
            #             '教育教学', '教务处', '校历', images))
        html5 = pq(
            url='http://bryant.bitzh.edu.cn/about/' +
            hrefs[4],
            headers=BLG.headers)
        total = pq(html5)('.desc').items()
        total = [title.text() for title in total][0].split('\n')
        total .pop(0)
        total = str(total).replace(': ', ':')
        # re.search()
        # print(total)
        #['Bryant Academic Policy:http://catalog.bryant.edu/undergraduate/academicregulationsandpolicies','Bryant BSBA Accounting Catalog:http://catalog.bryant.edu/undergraduate/collegeofbusiness/accountingdepartment/accountingconcentration/', 'BITZH Student Forms:http://jwc.zhbit.com/fuwuxiangmu/xscybg']
        # 等待插入######################################http://bryant.bitzh.edu.cn/list/?57_1.html
        images = "'Bryant Academic Policy:http://catalog.bryant.edu/undergraduate/academicregulationsandpolicies','Bryant BSBA Accounting Catalog:http://catalog.bryant.edu/undergraduate/collegeofbusiness/accountingdepartment/accountingconcentration/', 'BITZH Student Forms:http://jwc.zhbit.com/fuwuxiangmu/xscybg'"
        images = pymysql.escape_string(images)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,title,img) values('{}','{}','{}','{}')""".format(
                '教育教学', '教务处', '常用链接', images))


    def xscy(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?57_1.html',
            headers=BLG.headers)
        cy_hrefs = pq(doc)('.newslist li a').items()
        cy_titles = pq(doc)('.newslist li a h2').items()
        cy_dates = pq(doc)('.newslist li p').items()
        cy_hrefs = [href.attr('href') for href in cy_hrefs]
        cy_titles = [href.text() for href in cy_titles]
        cy_dates = [href.text() for href in cy_dates]

        for cy,cy_title,cy_date in zip(cy_hrefs,cy_titles,cy_dates):
            cy = cy
            cy_title = cy_title
            cy_date = cy_date
            print(cy,cy_title,cy_date)
            html = pq(url=BLG.base_url + cy, headers=BLG.headers)
            content = pq(html)('.news')
            imgs = pq(html)('p img')
            # imgs = [img.get('src') for img in content.items()]
            images = []
            # for img in imgs:
            #     r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
            #     img = img.split('/')[-1]
            #     with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
            #         f.write(r.content)
            #     images.append(img)
            # images = ','.join(images)
            # images = pymysql.escape_string(images)
            if cy_title == 'ACE职员表':
                content = pymysql.escape_string("""<div class="news">
<h1>ACE职员表</h1>
<div class="date">2018-04-26&#160;&#160;&#160;&#160;布莱恩特学院</div>
<p>
	<b><span><span style="font-size:16px;">Director:&nbsp;</span></span><span><span style="font-size:16px;"></span><b><span style="font-size:16px;">Corey Larsen</span></b></span></b>
</p>
<p>
	<b><span><b><span style="font-size:16px;background-color:#FFF1BC;"><img width="199" height="231" alt="" src="/upload/image/20180426/20180426150215841584.jpg" /></span></b></span></b>
</p>
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(188, 241, 255, 0.298039);">
	<strong>&nbsp;&nbsp;&nbsp;&nbsp;Hello, I am Corey Larsen and I am the Director of ACE. I also teach Writing, Global Foundations of Character and Leadership. I am also in charge of the Bryant Zhuhai IDEA Program. I can help students improve their English and study skills.</strong>
</p>
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(188, 241, 255, 0.298039);">
	<strong>Email :&nbsp;corey.larsen@zhuhai.bryant.edu</strong>
</p>
<p>
	<b><span><br />
</span></b>
</p>
<p>
	<b><span style="font-size:16px;">Academic Services Coordinator: </span><span style="font-size:16px;"><b><span>Nicole Ann&nbsp;Krupski&nbsp;</span></b></span></b><b><span style="font-size:16px;"></span></b>
</p>
<p>
	<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;">Study Strategies, Academic Support, Speaking, Marketing</span></span></b>
</p>
<p>
	<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;"><img alt="" src="/upload/image/20180426/20180426150569606960.jpg" /></span></span></b>
</p>
<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;">
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(153, 210, 200, 0.298039);">
	<strong>&nbsp;&nbsp;&nbsp;&nbsp;Hello, I’m Nicole Ann Krupski! Feel free to come by ACE (QA103) to make an appointment with me to learn different studying strategies, English, or Marketing.</strong><strong><br />
</strong>
</p>
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(153, 210, 200, 0.298039);">
	<strong>Email:nicole.krupski@zhuhai.bryant.edu</strong>
</p>
</span></span></b>
<p>
	<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;"><br />
</span></span></b>
</p>
<p>
	<span><span style="font-size:16px;"><strong>Learning Specialist: Tina Nakova</strong></span></span>
</p>
<p>
	<span><span style="font-size:16px;"><b><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#59BFBA;">Speaking,Writing, Reading, Study Skills</span></b></span></span>
</p>
<span><span style="font-size:16px;"></span></span>
<p>
	<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;"><img width="199" height="149" alt="" src="/upload/image/20180426/20180426150637603760.jpg" /></span></span></b><b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;"></span></span></b>
</p>
<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;">
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(253, 184, 219, 0.298039);">
	<strong>&nbsp;&nbsp;&nbsp;&nbsp;Hello, </strong><strong>I am Tina and I am available to help students with their English language skills.&nbsp;</strong>
</p>
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(253, 184, 219, 0.298039);">
	<strong>Please come by ACE to say hello! &nbsp;</strong><strong><br />
</strong>
</p>
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(253, 184, 219, 0.298039);">
	<strong>Email: tina.nakova@Zhuhai.bryant.edu</strong>
</p>
</span></span></b>
<p>
	<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;"></span></span></b>
</p>
<p>
	<b><span><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#FF7DBB;"></span><span style="font-size:16px;"><br />
</span></span></b>
</p>
<p>
	<b><span><span style="font-size:16px;">Learning Specialist: Jing Gong</span></span></b>
</p>
<p>
	<b><span><span style="font-size:16px;"><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:14px;font-style:normal;font-weight:normal;line-height:22.3999996185303px;background-color:#F96E57;">English Learning, Self Management, Presentation Skills</span></span></span></b>
</p>
<p>
	<b><span><span style="font-size:16px;"><img width="199" height="199" alt="" src="/upload/image/20180426/20180426150866876687.jpg" /></span></span></b>
</p>
<b><span><span style="font-size:16px;">
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(153, 210, 200, 0.298039);">
	<strong>&nbsp;&nbsp;&nbsp;&nbsp;Greeting from Jing! Nice meeting you. I can provide you with suggestions on English learning, Self management and Presentation skills.<br />
</strong>
</p>
<p style="color:#2D4257;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:15px;font-style:normal;font-weight:normal;text-align:justify;text-indent:0px;background-color:rgba(153, 210, 200, 0.298039);">
	<strong>Email: jing.gong@zhuhai.bryant.edu</strong>
</p>
</span></span></b>
<p>
	<b><span><span style="font-size:16px;"><br />
</span></span></b>
</p>
<p>
	<b><span><span style="font-size:16px;"><span><b>Learning Specialist: </b></span>Yuan Jiang</span></span></b>
</p>
<p>
	<b><span><span style="font-size:16px;"><span style="color:#FFFFFF;font-family:'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;font-size:16px;font-style:normal;font-weight:normal;line-height:25.6000003814697px;background-color:#59BFBA;">Economics, Accounting</span></span></span></b>
</p>
<p>
	<b><span><span style="font-size:16px;"><img width="199" height="265" alt="" src="/upload/image/20180426/20180426151040804080.jpg" /></span></span></b>
</p>
<p>
	<b><span style="background-color:#0FCDFB;">&nbsp;&nbsp;&nbsp;&nbsp;<span style="font-size:14px;">Hello, my name is Rebecca. I am able to help you with Economics and Accounting. Feel Free to make an appointment with me and come to ACE if you have any questions about these two subjects.</span></span></b>
</p>
<p>
	<b><span style="background-color:#0FCDFB;"><span style="font-size:14px;">Email: yuan.jiang@zhuhai.bryant.edu</span></span></b>
</p>
<p>
	<b><span style="background-color:#0FCDFB;"><span style="font-size:14px;"><br />
</span></span></b>
</p>
<p>
	<b><span style="background-color:#0FCDFB;"><span style="font-size:14px;"></span></span></b><b><span><span style="font-size:16px;"><br />
</span></span></b>
</p>
<p>
	<b><span></span></b>
</p><script src="/inc/Bomiw_VisitsAdd.asp?id=299"></script>
</div>

</div>

<div class="foot">
  <!--[if IE]><link href="/templates/cn/css/ie-fix.css" rel="stylesheet" type="text/css"><![endif]-->
</div>
""")
                # print('教育教学', '学生创优中心',cy,cy_title,cy_date,images)
                BLG.ms.insertOperation(
                    """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                        '教育教学', '学生创优中心', cy_title, cy_date,content,images))


class dxsh(BLG):
    def xsst(self):
        urls = ['http://bryant.bitzh.edu.cn/list/?65_1.html',
                'http://bryant.bitzh.edu.cn/list/?65_2.html']
        for url in urls:
            doc = pq(url=url, headers=BLG.headers)
            st_hrefs = pq(doc)('.newslist li a').items()
            st_names = pq(doc)('.newslist li a h2').items()
            st_dates = pq(doc)('.newslist li p').items()
            for st,st_name,st_date in zip(st_hrefs,st_names,st_dates):
                st = st.attr('href')
                st_name = st_name.text()
                st_date = st_date.text()
                html = pq(url=BLG.base_url + st, headers=BLG.headers)
                content = pq(html)('.news')
                imgs = pq(html)('p img')
                imgs = [img.get('src') for img in imgs]
                images = []
                for img in imgs:
                    r = requests.get(
                        url=BLG.base_url + img, headers=BLG.headers)
                    img = img.split('/')[-1]
                    with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
                        f.write(r.content)
                    images.append(img)
                images = ','.join(images)
                images = pymysql.escape_string(images)
                BLG.ms.insertOperation(
                    """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                        '大学生活', '学生社团', st_name, st_date, content, images))

    def hwyx(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?66_1.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.newslist li a').items()
        names = pq(doc)('.newslist li a h2').items()
        dates = pq(doc)('.newslist li p').items()
        for href, name, date in zip(hrefs, names, dates):
            href = href.attr('href')
            name = name.text()
            date = date.text()
            html = pq(url=BLG.base_url + href, headers=BLG.headers)
            content = pq(html)('.news')
            imgs = pq(html)('p img')
            imgs = [img.get('src') for img in imgs]

            images = []
            for img in imgs:
                # print(img)
                r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
                img = img.split('/')[-1]
                with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                    '大学生活', '海外资讯', name, date, content, images))

    def sjkc(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?67_1.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.newslist li a').items()
        names = pq(doc)('.newslist li a h2').items()
        dates = pq(doc)('.newslist li p').items()
        for href, name, date in zip(hrefs, names, dates):
            href = href.attr('href')
            name = name.text()
            date = date.text()
            html = pq(url=BLG.base_url + href, headers=BLG.headers)
            content = pq(html)('.news')
            imgs = pq(html)('p img')
            imgs = [img.get('src') for img in imgs]
            for img in imgs:
                # print(img)
                r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
                img = img.split('/')[-1]
                with open('H:\\blg\\blg_english_file\\' + img.split('/')[-c1], 'wb') as f:
                    f.write(r.content)
            images = []
            for img in imgs:
                # print(img)
                r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
                img = img.split('/')[-1]
                with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                    '大学生活', '暑假课程', name, date, content, images))

    def xssw(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/about/?68.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.desc p a img').parents()
        hrefs = [href.get('href') for href in hrefs]
        hrefs = list(filter(None, hrefs))
        # # print(hrefs)
        # html1 = pq(url=BLG.base_url + hrefs[0], headers=BLG.headers)
        # content1 = pq(html1)('.desc')
        # BLG.ms.insertOperation(
        #     """insert into blg(fir_column,sec_column,title,content) values('{}','{}','{}','{}')""".format(
        #         '大学生活', '学生事务', '学生事务处人员职责',  content1))
        # html2 = pq(url=BLG.base_url + hrefs[1], headers=BLG.headers)
        # hrefs = pq(doc)('.newslist li a').items()
        # names = pq(doc)('.newslist li a h2').items()
        # dates = pq(doc)('.newslist li p').items()
        # for href, name, date in zip(hrefs, names, dates):
        #     href = href.attr('href')
        #     name = name.text()
        #     date = date.text()
        #     # print(href)
        #     root = pq(url=BLG.base_url + href, headers=BLG.headers)
        #     content2 = pq(root)('.news')
        #     imgs1 = pq(root)('p img')
        #     imgs2 = pq(root)('.news img')
        #     imgs1 = [img.get('src') for img in imgs1]
        #     imgs2 = [img.get('src') for img in imgs2]
        #     imgs = imgs1 + imgs2
        #     images = []
        #     # for img in imgs:
        #         # print(img)
        #         # r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
        #         # img = img.split('/')[-1]
        #     #     with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
        #     #         f.write(r.content)
        #     #     images.append(img)
        #     # images = ','.join(images)
        #     # images = pymysql.escape_string(images)
        #     # BLG.ms.insertOperation(
        #     #     """insert into blg(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
        #     #         '大学生活', '暑假课程', name, date, content2, images))
        #     # print(content2)
        html3 = pq(url=BLG.base_url + hrefs[2], headers=BLG.headers)
        hrefs = pq(html3)('.desc p a').items()
        names = pq(html3)('.desc p a h2').items()
        images = []
        for href, name in zip(hrefs, names):
            href = href.attr('href')
            name = name.text()
            r = requests.get(url=BLG.base_url + href, headers=BLG.headers)
            bg_href = href.split('/')[-1]
            img = 'H:\\blg\\blg_english_file\\' + bg_href.split('/')[-1]
            with open(img, 'wb') as f:
                f.write(r.content)
            images.append(img)
        images = ','.join(images)
        images = pymysql.escape_string(images)
        BLG.ms.insertOperation(
            """insert into blg_english(fir_column,sec_column,title,img) values('{}','{}','{}','{}')""".format(
                '大学生活', '学生事务', '表格下载',images))


class jysx(BLG):
    def jyzd(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?157_1.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.newslist li a').items()
        names = pq(doc)('.newslist li a h2').items()
        dates = pq(doc)('.newslist li p').items()
        for href, name, date in zip(hrefs, names, dates):
            href = href.attr('href')
            name = name.text()
            date = date.text()
            html = pq(url=BLG.base_url + href, headers=BLG.headers)
            content = pq(html)('.news')
            imgs1 = pq(html)('p img')
            imgs2 = pq(html)('.news img')
            imgs1 = [img.get('src') for img in imgs1]
            imgs2 = [img.get('src') for img in imgs2]
            imgs = imgs1 + imgs2
            images = []
            for img in imgs:
                # print(img)
                r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
                img = img.split('/')[-1]
                with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            content = pymysql.escape_string("""<div class="news">
<h1>How to Use LinkedIn to Job Search</h1>
<div class="date">2018-04-25&#160;&#160;&#160;&#160;布莱恩特学院</div>
<p align="center" style="text-align:center;text-indent:2em;">
	<span style="font-size:18px;">Building Your Connections Along With Your Profile</span> 
</p>
<p align="center" style="text-align:center;text-indent:2em;">
	<br />
</p>
<p style="text-indent:2em;">
	<span>There are so many ways for job seekers to
use&nbsp;LinkedIn&nbsp;to improve their job search. For example, more and more
employers are using LinkedIn to post job listings, as well as to reach out to
possible job candidates. At the same time, many LinkedIn users are going on to
the site to connect and network with people in their industry. </span> 
</p>
<p style="text-indent:2em;">
	<span>How can you ensure that you're using the full power of
LinkedIn to assist with your search for a new job?</span> 
</p>
<p style="text-indent:2em;">
	<span>It is critical to take the time
to build your LinkedIn profile, add to your connections, and effectively use
them to aid in your job search. It is also important to give back and help your
connections too when they need advice and referrals. After all, networking is
about building relationships rather than just asking for assistance.</span> 
</p>
<p style="text-indent:2em;">
	<span>Read below for advice on how to best use LinkedIn to
enhance your job search.</span> 
</p>
<p style="text-indent:2em;">
	<span><br />
</span> 
</p>
<h3 style="text-indent:2em;">
	Tips for Using LinkedIn
for Your Job Search
</h3>
<p style="text-indent:2em;">
	<span><strong><span> Complete and Update Your
Profile</span></strong><br />
The more complete your LinkedIn profile, the more chances that you will be
found and contacted by an employer. Use your LinkedIn profile like a resume and
provide prospective employers with detailed information about your skills and
experiences. Creating a catchy headline and detailed summary, including a
professional photo, and listing your skills and accomplishments are all ways to
enhance your profile.</span> 
</p>
<p style="text-indent:2em;">
	<span>You can also strengthen your profile by adding links, such as a link to
your professional website or online portfolio.</span> 
</p>
<p style="text-indent:2em;">
	<span><br />
</span> 
</p>
<p style="text-indent:2em;">
	<span><strong><span>Find and Use Connections</span></strong><br />
The more connections you have, the better your chances of finding someone who
can help with your job search. Employers look for referrals from their own employees
to fill positions before opening up a job to the masses, so someone who is
employed at the company or has connections there will have a leg up in
referring you as an applicant.</span> 
</p>
<p style="text-indent:2em;">
	<span>While you want to have a number of connections, make sure you only connect
with people who you know, or whom you are planning to reach out to. You do not
want to connect with everyone on LinkedIn - the goal is to maintain or
establish relationships with people who are in your field or whom you are
already connected with.</span> 
</p>
<p style="text-indent:2em;">
	<span><br />
</span> 
</p>
<p style="text-indent:2em;">
	<span><strong><span>Check Out Job Search
Options</span></strong><br />
You can search for jobs on LinkedIn under the "Jobs" tab. Search for
jobs by keyword, country, and zip code. Use the Advanced Search Option to
refine your search and to search by date posted, experience level, specific
location, job function, company, and industry. You can save job searches, and
even receive emails about new job listings.</span> 
</p>
<p style="text-indent:2em;">
	<span>You can also find job openings by searching for and clicking on specific
companies. Many companies post job openings on their LinkedIn pages. Here's how
to search for and apply for jobs on LinkedIn.</span> 
</p>
<p style="text-indent:2em;">
	<span><br />
</span> 
</p>
<p style="text-indent:2em;">
	<span><strong><span>Use Recommendations and
Referrals</span></strong><br />
If a&nbsp;job is listed directly on LinkedIn, you'll see how you're connected
to the hiring manager and you can request a LinkedIn recommendation from
someone you know at the company. If you request a recommendation, LinkedIn will
provide you with a template you can use for your message that&nbsp;you can edit
and personalize.</span> 
</p>
<p style="text-indent:2em;">
	<span>These recommendations will help boost your credibility in
the eyes of employers.</span> 
</p>
<p style="text-indent:2em;">
	<span>You can also receive endorsements from network contacts for various skills
that you have. An endorsement emphasizes that you do, in fact, have a certain
skill that you listed on your LinkedIn profile. The best way to receive
endorsements is to give some to your contacts first. They will then be more
likely to do the same for you in return.</span> 
</p>
<p style="text-indent:2em;">
	<span><br />
</span> 
</p>
<p style="text-indent:2em;">
	<span><strong><span>Use LinkedIn Company
Profiles to Learn About Employers</span></strong><br />
LinkedIn company profiles are a good way to find more information on a company
you're interested in at a glance. You'll be able to see your connections at the
company, new hires, promotions, jobs posted, related companies, and company
statistics. </span> 
</p>
<p style="text-indent:2em;">
	<span>Consider following your dream companies on LinkedIn. This will allow you to
keep up with their achievements (which will be useful to bring up in a cover
letter or interview), and will help you spot any job openings. </span> 
</p>
<p style="text-indent:2em;">
	<span><br />
</span> 
</p>
<p style="text-indent:2em;">
	<span>Source: <a href="https://www.thebalance.com/how-to-use-linkedin-to-job-search-2062600"><span>https://www.thebalance.com/how-to-use-linkedin-to-job-search-2062600</span></a> </span> 
</p>
<p style="text-indent:2em;">
	<br />
</p><script src="/inc/Bomiw_VisitsAdd.asp?id=293"></script>
</div>

</div>
""")
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                    '就业升学', '就业指导', name, date, content, images))


    def sxzd(self):
        # http://bryant.bitzh.edu.cn/list/?156_1.html
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?156_1.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.newslist li a').items()
        names = pq(doc)('.newslist li a h2').items()
        dates = pq(doc)('.newslist li p').items()
        for href, name, date in zip(hrefs, names, dates):
            href = href.attr('href')
            name = name.text()
            date = date.text()
            html = pq(url=BLG.base_url + href, headers=BLG.headers)
            content = pq(html)('.news')
            imgs1 = pq(html)('p img')
            imgs2 = pq(html)('.news img')
            imgs1 = [img.get('src') for img in imgs1]
            imgs2 = [img.get('src') for img in imgs2]
            imgs = imgs1 + imgs2
            if imgs == []:
                continue
            images = []
            for img in imgs:
                # print(img)
                r = requests.get(url=BLG.base_url + img, headers=BLG.headers)
                img = img.split('/')[-1]
                with open('H:\\blg\\blg_english_file\\' + img.split('/')[-1], 'wb') as f:
                    f.write(r.content)
                images.append(img)
            images = ','.join(images)
            images = pymysql.escape_string(images)
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,up_date,content,img) values('{}','{}','{}','{}','{}','{}')""".format(
                    '就业升学', '工作实习', name, date, content, images))

    def gzsx(self):
        urls = ['http://bryant.bitzh.edu.cn/list/?155_1.html',
                'http://bryant.bitzh.edu.cn/list/?155_2.html']
        for url in urls:
            doc = pq(url=url, headers=BLG.headers)
            hrefs = pq(doc)('.newslist li a').items()
            names = pq(doc)('.newslist li a h2').items()
            dates = pq(doc)('.newslist li p').items()
            for href, name, date in zip(hrefs, names, dates):
                href = href.attr('href')
                name = name.text()
                date = date.text()
                html = pq(url=BLG.base_url + href, headers=BLG.headers)
                content = pq(html)('.news')
                BLG.ms.insertOperation(
                    """insert into blg_english(fir_column,sec_column,title,up_date,content) values('{}','{}','{}','{}','{}')""".format(
                        '就业升学', '工作实习', name, date, content))

    def hdgg(self):
        doc = pq(
            url='http://bryant.bitzh.edu.cn/list/?158_1.html',
            headers=BLG.headers)
        hrefs = pq(doc)('.newslist li a').items()
        names = pq(doc)('.newslist li a h2').items()
        dates = pq(doc)('.newslist li p').items()
        for href, name, date in zip(hrefs, names, dates):
            href = href.attr('href')
            name = name.text()
            date = date.text()
            html = pq(url=BLG.base_url + href, headers=BLG.headers)
            content = pq(html)('.news')
            BLG.ms.insertOperation(
                """insert into blg_english(fir_column,sec_column,title,up_date,content) values('{}','{}','{}','{}','{}')""".format(
                    '就业升学', '活动公告', name, date, content))
# def start():
#     home_page = home_page()


if __name__ == '__main__':
    blg1 = home_page()
    blg1.hots()
    blg1.teach_mod()
    # blg2 = for_us()
    # blg2.xmjj()
    # blg2.szdw()
    # blg2.yxcg()
    # blg2.q_a()
    # blg2.gzzd()

    # blg = jysx()
    # blg.gzsx()
    # blg.hdgg()
    # blg.teach_mod()
