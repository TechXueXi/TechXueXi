#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @FileName: 强国题库.py
 @Date: 2021/10/5 11:30
 @Description:
 使用方法：因为调用了`techXueXi`中的`pdlearn`
 使用时需要将`challengeAnswerBank.py`和`QuestionBank.db`放到`/techXueXi/SourcePackages/`目录下
"""
import json
import time
from pdlearn import color
# import requests
from bottle import route, run, static_file, request
import sqlite3


class DbTool:
	def __init__(self):
		self.db = sqlite3.connect('QuestionBank.db')
		self.c = self.db.cursor()

	def close(self):
		"""
		关闭数据库
		"""
		self.c.close()
		self.db.close()

	def execute(self, sql, param=None):
		"""
		执行数据库的增、删、改
		sql：sql语句
		param：数据，可以是list或tuple，亦可是None
		retutn：成功返回True
		"""
		# print('sql=', sql, 'param=', param)
		try:
			if param is None:
				self.c.execute(sql)
			else:
				if type(param) is list:
					self.c.executemany(sql, param)
				else:
					self.c.execute(sql, param)
			count = self.db.total_changes
			self.db.commit()
		except Exception as e:
			print('Exception:', e)
			return False
		if count > 0:
			return True
		else:
			print('删除了0行')
			return False

	def query(self, sql, param=None):
		"""
		查询语句
		sql：sql语句
		param：参数,可为None
		retutn：成功返回True
		"""
		# print('sql=', sql, 'param=', param)
		if param is None:
			self.c.execute(sql)
		else:
			self.c.execute(sql, param)
		return self.c.fetchall()

def search(keyword='', tableName='tiku', page=1, rows=10):
	limit = (page - 1) * rows
	db = DbTool()
	total = db.query(
		'select count(*) from ' + tableName + ' where question like ' + '"%' + keyword + '%"' + 'or answer like ' + '"%' + keyword + '%"')
	result = db.query(
		'select question,answer,datetime from ' + tableName + ' where question like ' + '"%' + keyword + '%"' + 'or answer like ' + '"%' + keyword + '%" LIMIT ' +
		str(limit) + ',' + str(rows))
	data = {'total': total[0][0], 'rows': []}
	for r in result:
		# data['rows'].append({'id': r[0], 'question': r[1], 'answer': r[2], 'datetime': 0})
		data['rows'].append({'id': 0, 'question': r[0], 'answer': r[1], 'datetime': r[2]})
	###################################将tikuNet表中的题库，插入到tiku表中###############
	# question = r[1]
	# answer = r[2]
	# db = DbTool()
	# q = db.query('select * from ' + 'tiku' + ' where question = "' + question + '" and answer = "' + answer + '"')
	# if not len(q):
	# 	result = db.execute('insert into ' + 'tiku' + '(question,answer) values (?,?)', (question, answer))
	# 	print(result)
	###################################将tikuNet表中的题库，插入到tiku表中###############

	# return json.dumps(data, ensure_ascii=False)
	return data

if __name__ == '__main__':
	count = 0
	while True:
		count = count + 1
		question = input("开始第{}次挑战答题，请输入题目(输入`exit`退出答题)：".format(count))
		if question == 'exit':
			break
		data = search(keyword = question)
		print(color.yellow("共查询到{}条数据如下：".format(data['total'])))
		for i in range(len(data['rows'])):
			print("Question{}：{}\nAnswer：{}\n".format(i+1, data['rows'][i]['question'], color.green(data['rows'][i]['answer'])))


