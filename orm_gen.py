
import os

dbname = 'lis.db'
orm_py_file = 'orm.py'

os.system(fr"conda activate sqlacodegen && sqlacodegen sqlite:///{dbname} --outfile {orm_py_file}")
print('ORM ok')