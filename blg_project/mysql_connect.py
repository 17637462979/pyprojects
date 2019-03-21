#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/7
# @Author  : zhang

import pymysql


class MysqlConnection(object):
    # 初始化函数，初始化连接列表
    def __init__(self, host, user, pwd, dbname):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbname = dbname

    # 获取数据库游标对象cursor
    # 游标对象：用于执行查询和获取结果
    def getCursor(self):

        # 建立数据库连接
        self.db = pymysql.connect(self.host, self.user, self.pwd, self.dbname)

        # 创建游标对象
        cur = self.db.cursor()

        # 返回
        return cur

    # 查询操作
    def queryOperation(self, sql):
        cur = self.getCursor()
        cur.execute(sql)
        row = cur.rowcount
        # fetch*
        dataList = cur.fetchall()
        cur.close()
        self.db.close()
        print('查询成功')
        return dataList, row

    # 删除操作
    def deleteOperation(self, sql):

        cur = self.getCursor()
        try:
            cur.execute(sql)

            self.db.commit()
            print('删除成功')

        except Exception as e:
            print(e)
            self.db.rollback()
        cur.close()
        self.db.close()
    # 数据更新

    def updateOperation(self, sql):
        cur = self.getCursor()
        try:
            cur.execute(sql)
            self.db.commit()
            print('修改成功')
        except Exception as e:
            print(e)
            self.db.rollback()

        cur.close()
        self.db.close()

    # 添加数据
    def insertOperation(self, sql):

        cur = self.getCursor()
        try:
            cur.execute(sql)
            self.db.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            self.db.rollback()

        cur.close()
        self.db.close()


if __name__ == '__main__':
    pass
    # mm = MysqlConnection('127.0.0.1', 'root', '123456', 'ydwl_data')
    # cc = mm.queryOperation('select * from skypy_personnel')
    # mm.insertOperation("""insert into skypy_personnel(registration_category,registration_number,registration_major,href,comp_name,identity_number,name) values('{}','{}','{}','{}','{}','{}','{}')""".format('test','test','test','test','test','test','test'))
    # mm.updateOperation("""UPDATE skypy_personnel SET comp_name = '{}' WHERE href = '{}' """.format('test999999','test'))
    # mm.deleteOperation("""DELETE FROM skypy_personnel WHERE comp_name='{}'""".format('test999999'))
    # print(list(cc))
    # for c in cc[0]:
    #     print(c)
