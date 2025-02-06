import pymongo 

Myclient = pymongo.MongoClient('mongodb://localhost:27017/')
Mydb = Myclient['ghanadb']
Mycol = Mydb['information_of_site'] 