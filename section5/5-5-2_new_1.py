# pip install -U finance-datareader 설치 후 사용
import FinanceDataReader as fdr
import pandas as pd
import datetime
import pymysql
#MySQLdb 생성
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine

#sqlalchemy 설치

try:
    #엔진 생성
    engine = create_engine("mysql+mysqldb://python123:"+"1111"+"@localhost/python_app1", encoding='utf-8')
    with engine.connect() as conn: #DB Connection
        #조회 시작 & 마감 날짜
        start = datetime.datetime(2018,2,4)
        end = datetime.datetime(2018,2,25)

        gs = fdr.DataReader('090430', start, end) #아모레퍼시픽 주가 읽기

        #데이터 출력
        print(gs)

        #인덱스 출력
        print(gs.index)

        #Column 출력
        print(gs['Open'])

        #Row 출력
        print(gs.ix['2018-02-13'])

        #상세 정보
        print(gs.describe())

        #Index To Column1
        gs['Date'] = gs.index

        #인덱스 재 설정
        gs.index = range(1,(len(gs.index)+1))

        #데이터 출력(확인)
        print(gs)

        #pandas to DataBase(to_sql)
        gs.to_sql("test", conn, if_exists="replace", index=True, index_label='Id') #fail, replace, append

        #pandas read DataBase(read_sql) 전체 조회
        df = pd.read_sql(('select * from TEST'), conn) #index_col='Id', columns=['Open', 'High'...]
        print(df)

        #pandas read DataBase(read_sql) 조건 조회
        df = pd.read_sql('select * from TEST WHERE Id = %s OR Id = %s', conn, params=(3,7), index_col='Id') #params : list, tuple or dict..
        print(df)

finally:
    #모든 커넥션을 닫는다.
    engine.dispose()
    print('Dataframe SQL Work complete!')




#검색 : how to use pandas to_sql in treasure data
#GitHub - treasure-data/pandas-td: Interactive data analysis with ...
#웹사이트 : https://github.com/treasure-data/pandas-td

import datetime
df['time'] = datetime.datetime.now()

# Set API key and start a session
Set your API key to the environment variable TD_API_KEY and run "jupyter notebook":

$ export TD_API_SERVER="https://api.treasuredata.com/"
$ export TD_API_KEY="1234/abcd..."
$ jupyter notebook

con = td.connect(apikey=os.environ['TD_API_KEY'],
                 endpoint=os.environ['TD_API_SERVER'],
                 retry_post_requests=True)
engine = td.create_engine('presto:sample_datasets', con=con)


pip install pandas-td
import pandas_td as td
engine = td.create_engine('presto:sample_datasets')

# Alternatively, initialize a connection explicitly
con = td.connect(apikey=os.environ['TD_API_KEY'], endpoint=os.environ['TD_API_SERVER'])
engine = td.create_engine('presto:sample_datasets', con=con)

# con = td.connect()
with td.connect() as con:
    td.to_td(df, 'my_db.test_table', con, if_exists='replace', index=False)


# Import it into 'tutorial.import1'
con = td.connect()
td.to_td(df, 'tutorial.import1', con, if_exists='replace', index=False)
