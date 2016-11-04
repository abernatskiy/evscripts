import sqlite3

def _sqlType(var):
	types = {int: 'INT', float: 'FLOAT', str: 'TEXT'}
	try:
		return types[type(var)]
	except:
		raise ValueError('Conversion of an unsuitable variable type to SQL type attempted. Suitable types: ' + str(types.keys()))

def _sqlStr(var):
	if(type(var) == int or type(var) == float):
		return str(var)
	elif(type(var) == str):
		# TODO Validate the string here
		return '\'' + var + '\''
	else:
		raise ValueError('Conversion of a variable of unsuitable type to SQL converted')

def makeGridTable(grid, dbfilename):
	with sqlite3.connect(dbfilename) as con:
		cur = con.cursor()

		tableDesc = 'Grid(id INT PRIMARY KEY'
		examplePoint = grid[0]
		paramNames = examplePoint.keys()
		for paramName in paramNames:
			tableDesc += ', ' + paramName + ' ' + _sqlType(examplePoint[paramName]) # TODO paramName is not validated!
		tableDesc += ')'
		cur.execute('CREATE TABLE ' + tableDesc + ';')

		for i,point in enumerate(grid):
			vstrs = [ str(i) ] + [ _sqlStr(point[paramName]) for paramName in paramNames ]
			cur.execute('INSERT INTO Grid VALUES (' + ', '.join(vstrs) + ');')

def gridIdsFromSqlite(dbfilename):
	with sqlite3.connect(dbfilename) as con:
		cur = con.cursor()
		cur.execute('SELECT id FROM Grid;')
		idTuples = cur.fetchall()
	return [ id for id, in idTuples ]

def makeGridQueueTable(dbfilename):
	ids = gridIdsFromSqlite(dbfilename)
	with sqlite3.connect(dbfilename) as con:
		cur = con.cursor()
		cur.execute('PRAGMA foreign_keys=ON;')
		cur.execute('CREATE TABLE GridQueue(id INT, inWorks BOOL, done BOOL, FOREIGN KEY(id) REFERENCES Grid(id));')
		for id in ids:
			cur.execute('INSERT INTO GridQueue VALUES (' + str(id) + ', 0, 0);')

def requestPointFromGridQueue(dbfilename):
	'''Finds a point that is neither worked upon nor done, marks it as worked upon
	   and returns the parameter dictionary. If the point is not found, None is
	   returned.
	'''
	with sqlite3.connect(dbfilename) as con:
		con.text_factory = str
		cur = con.cursor()
		cur.execute('SELECT id FROM GridQueue WHERE NOT inWorks AND NOT done LIMIT 1;')
		pointIdList = cur.fetchall()
		if len(pointIdList) == 1: # If there is still a point that hasn't been processed
			pointId, = pointIdList[0]
			# mark it as being in works
			cur.execute('UPDATE GridQueue SET inWorks=1 WHERE id=' + str(pointId) + ';')
			# fetch and return the grid parameters
			cur.execute('SELECT * FROM Grid WHERE id=' + str(pointId) + ';')
			vals = cur.fetchall()
			dict = {}
			for idx, col in enumerate(cur.description):
				dict[col[0]] = vals[0][idx]
			id = dict.pop('id')
			return id, dict
		elif len(pointIdList) == 0:
			return None
		else:
			raise ValueError('SELECT query with LIMIT 1 returned more than one result')

def reportSuccessOnPoint(dbfilename, id):
	with sqlite3.connect(dbfilename) as con:
		cur = con.cursor()
		cur.execute('UPDATE GridQueue SET inWorks=0, done=1 WHERE id=' + str(id) + ';')

def reportFailureOnPoint(dbfilename, id):
	with sqlite3.connect(dbfilename) as con:
		cur = con.cursor()
		cur.execute('UPDATE GridQueue SET inWorks=0 WHERE id=' + str(id) + ';')
