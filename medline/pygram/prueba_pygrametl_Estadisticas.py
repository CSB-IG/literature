# -*- coding: utf-8 -*-

import datetime
import sys
import time

sys.path.append('/home/Documents') #donde está ubicado pygrametl

import pygrametl
from pygrametl.datasources import CSVSource, MergeJoiningSource
from pygrametl.tables import CachedDimension, SnowflakedDimension,BulkFactTable

# Connection to target DW:
import MySQLdb
myconn = MySQLdb.connect(user='pygram', passwd='hola',db='Estadisticas')
connection=pygrametl.ConnectionWrapper(myconn)
connection.setasdefault()


def loader(name,atts,fieldsep,rowsep,nullval,filehandle):
	curs=MySQLConnection.cursor()
	curs.copy_from(file=filehandle,table=name,sep=fieldsep, null=str(nullval),columns=atts)

#base de datos
sgbstdn = CachedDimension(
	name='SGBSTDN',
	key = 'matricula',
	attributes = ['nombre','paterno', 'materno', 'degc_code','class_code'],
	lookupatts = ['matricula']
)

scbcrse = CachedDimension(
	name='SCBCRSE',	
	key = 'cvemat',
	attributes = ['nommat','clase','lab','unidades'],
	lookupatts = ['cvemat']
)


ssbsect_algo = CachedDimension(
	name = 'SSBSECT',
	key = 'crn',
	attributes = ['cvemat', 'grupo', 'levl_code', 'coll_code', 'dept_code']
)

#merge tablas que utiliza fk 
ssbsect = SnowflakedDimension(
	[(ssbsect_algo,(scbcrse))]

)

facttabl= BulkFactTable(
	name='aaa',
	keyrefs=['matricula','cvemat','crn'],
	measures=['errors'],
	bulkloader=loader
)


#de donde se baja la info  // cambiar path al de bd
resSGBSTDN = CSVSource(file('./vistaSGBSTDN.csv','r',16384), delimiter='\t')
resSCBCRSE = CSVSource(file('./vistaSCBCRSE.csv','r',16384), delimiter='\t')	    
resSSBSECT = CSVSource(file('./vistaSSBSECT.csv','r',16384), delimiter='\t')

inputdata=MergeJoiningSource(resSCBCRSE, 'cvemat',resSSBSECT, 'cvemat')

def main():
	for row in inputdata:
	        print row
		row['cvemat']=scbcrse.ensure(row,'nommat':'hola')
		row['crn']=ssbsect.sfdensure(row)
		facttbl.insert(row)
	connection.commit() #cargar cambios a base de datos

if __name__ == '__main__':
    main()


