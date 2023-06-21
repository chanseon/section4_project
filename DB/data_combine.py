###데이터 합치기 및 전처리 진행
#list JSON 파일을 리스트로 읽기
import pandas as pd
from datetime import datetime
import json

with open('../data/data_output_duration.json', 'r') as f:
    url_duration = json.load(f)
with open('../data/data_output_others.json', 'r') as f:
    other = json.load(f)

data1 = {'url': [url[0] for url in url_duration],
         'duration': [url[1] for url in url_duration]}
data1_df = pd.DataFrame(data1)

data2 = {'count': [datas[0] for datas in other[1:]],
         'date': [datas[1] for datas in other[1:]],
         'hashtag': [datas[2] for datas in other[1:]],
         'good': [datas[3] for datas in other[1:]],
         'game': [datas[4] for datas in other[1:]]}
data2_df = pd.DataFrame(data2)

data_df = pd.concat([data1_df,data2_df],axis=1)

##하면서 에러 걸리는 부분 추가 작업 후 저장된 데이터 셋
with open('../data/data_all_raw.json', 'r') as f:
    data_df = json.load(f)
data_df = pd.DataFrame(data_df)

#데이터 전처리
##duration
duration_sec=[]
##date
date_compare =[]
data_df.date = data_df.date.str.replace('최초 공개: ',"")
##game
game_name = []
game_release_date = []

#duration,date,hashtag
for i in range(len(data_df)):
      ##duration
      if len(data_df.duration.iloc[i]) <= 5:
            data_df.duration.iloc[i] = '0:'+ data_df.duration.iloc[i]
      else:
            pass
      target = data_df.duration.iloc[i].split(":")
      duration_sec.append((int(target[0])*3600) + (int(target[1])*60) + (int(target[2])))
      ##date
      today = datetime.now()
      date_to_compare = datetime.strptime(data_df.date.iloc[i], "%Y. %m. %d.")
      date_diff = today - date_to_compare
      date_compare.append(date_diff.days)
      ##hashtag
      data_df.hashtag.iloc[i] = ','.join(s for s in data_df.hashtag.iloc[i])
      ##game
      data_df.game.iloc[i] = data_df.game.iloc[i].split('\n')
      try:
            game_name.append(data_df.game.iloc[i][0])
            game_release_date.append(data_df.game.iloc[i][1])
      except IndexError:
            game_release_date.append(data_df.game.iloc[i][0])


data_df.insert(2,'duration_sec',duration_sec)
data_df.insert(5,'date_compare',date_compare)
data_df.insert(9,'game_name',game_name)
data_df.insert(10,'game_release_date',game_release_date)

##count 
data_df['count'] = data_df['count'].str.replace(",","")
data_df['count'] = data_df['count'].astype(int)
##hashtag plus+
data_df.hashtag = data_df.hashtag.str.replace("#",'')
#해쉬태그가 없는 경우가 있음! 이번데이터는 1160 부터.
data_df.hashtag.iloc[1160:] = data_df.hashtag.iloc[1160:].str.replace(',',"")
data_df.hashtag.iloc[1160:] = data_df.hashtag.iloc[1160:].str.replace(r'[^a-zA-Z가-힣]',",",regex=True)
##good
data_df.good = data_df.good.str.replace('천','00')
data_df.good = data_df.good.str.replace('만','000')
data_df.good = data_df.good.str.replace('.','')
data_df.good = data_df.good.str.replace('좋아요','0')
data_df.good = data_df.good.astype(int)

#dataframe json으로 저장
data_df.to_json("../data/data_final.json", orient = 'records')