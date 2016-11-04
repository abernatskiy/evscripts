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

def grid2sqlite(grid, dbfilename):
	with sqlite3.connect(dbfilename) as con:
		cur = con.cursor()

		tableDesc = 'Grid(id INT'
		examplePoint = grid[0]
		paramNames = examplePoint.keys()
		for paramName in paramNames:
			tableDesc += ', ' + paramName + ' ' + _sqlType(examplePoint[paramName]) # TODO paramName is not validated!
		tableDesc += ')'
		cur.execute('CREATE TABLE ' + tableDesc + ';')

		for i,point in enumerate(grid):
			vstrs = [ str(i) ] + [ _sqlStr(point[paramName]) for paramName in paramNames ]
			cur.execute('INSERT INTO Grid VALUES (' + ', '.join(vstrs) + ');')

def makeGridQueueTable(dbfilename):
	#with sqlite3.connect(dbfilename) as con:
	#	cur = con.cursor()
	#	cur.execute('CREATE TABLE GridCoverage(FOREIGN KEY(id) REFERENCES Grid(id), ')
	pass
