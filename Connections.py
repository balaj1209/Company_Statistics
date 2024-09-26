from sqlalchemy import create_engine
import oracledb

user = 'system'
password = 'arich'
host = 'localhost'
sid = 'xe'

dsn = oracledb.makedsn(host=host, port=1521, sid=sid)

conn_str = f'oracle+oracledb://{user}:{password}@{dsn}'

engine = create_engine(conn_str)