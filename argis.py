import numpy

import arcpy

lyr = r'http://g-aset.dbkl.gov.my/gasset1/rest/services/ZAC/SEGAMBUT/MapServer/0'

nparr = arcpy.da.FeatureClassToNumPyArray(lyr, ['OBJECTID','STNAME','CNTYFIPS','Shape_Area'])

numpy.savetxt('H:\MyFeatureClass.csv', nparr, delimiter=",", fmt="%s")