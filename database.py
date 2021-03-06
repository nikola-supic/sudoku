"""
Created on Wed Mar 3 21:34:15 2021

@author: Sule
@name: database.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

import mysql.connector
import json
import random

try:
	mydb = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='',
		database='sudoku'
		)
	mycursor = mydb.cursor(buffered=True)
	print('[ + ] Successfully connected to database.')
except mysql.connector.errors.InterfaceError: 
	print('[ - ] Can not connect to database.')

def new_grid(creator, start_pos, finish_pos):
	start = json.dumps(start_pos)
	finish = json.dumps(finish_pos)

	sql = "INSERT INTO levels (creator, start, finish) VALUES (%s, %s, %s) LIMIT 1"
	val = (creator, start, finish, )

	mycursor.execute(sql, val)
	mydb.commit()
	return True

def get_random():
	mycursor.execute("SELECT id FROM levels")
	result = mycursor.fetchall()
	levels = [row[0] for row in result]
	random.shuffle(levels)
	return levels[0]

def get_level_grid(id):
	sql = "SELECT start, finish FROM levels WHERE id=%s LIMIT 1"
	val = (id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	if result is not None:
		start = json.loads(result[0])
		finish = json.loads(result[1])
		return start, finish
	return False

def get_level(id):
	sql = "SELECT creator, record, recorder FROM levels WHERE id=%s LIMIT 1"
	val = (id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	if result is not None:
		return result[0], result[1], result[2]
	return False

def update_record(id, record, recorder):
	sql = "UPDATE levels SET record=%s, recorder=%s WHERE id=%s"
	val = (record, recorder, id, )
	mycursor.execute(sql, val)
	mydb.commit()
	return True


