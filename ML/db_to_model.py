from pymongo import MongoClient
import pandas as pd


# MongoDB 연결
HOST = 'mydb.ldks5ty.mongodb.net'   
USER = 'pubpcs' 
PASSWORD = '0529'
DATABASE_NAME = 'my_data'   #임의로 설정가능 - DB이름
COLLECTION_NAME = 'youtube_data' #임의로 설정가능 - DB안에 입력될 데이터 이름
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# def get_wish_avg_count():
#     return int(input("목표로하는 하루당 조회수를 입력하세요:"))

def data_from_db(collection):
    for data in collection.find({},{'_id': 0}): # 조회할 필드 설정, '_id'는 제외하고 가져옴
        data
    df = pd.DataFrame(data).T
    return df

def preprocess_data(df = data_from_db(collection)):
    col = ['duration_sec', 'count','date_compare', 'good']
    new_df = df[col].reset_index().drop('index',axis=1)
    new_df['duration_sec'] = new_df['duration_sec'].astype(int)
    #하루당 조회수 평균 -> avg_count로 추가
    new_df['count'] = new_df['count'].astype(int)
    new_df['date_compare'] = new_df['date_compare'].astype(int)
    new_df['avg_count'] = new_df['count'] / new_df['date_compare']
    #트렌드 목표 조회수 설정
    #wish_avg_count = get_wish_avg_count()
    new_df['avg_count'] = new_df['avg_count'].astype(int)
    # 조건에 따라 새로운 컬럼 생성
    # new_df['trend'] = ''
    # new_df.loc[new_df['avg_count'] >= wish_avg_count, 'trend'] = 1
    # new_df.loc[new_df['avg_count'] < wish_avg_count, 'trend'] = 0
    # new_df['trend'] =new_df['trend'].astype(int)

    processed_data = new_df

    return processed_data

processed_data = preprocess_data(data_from_db(collection))