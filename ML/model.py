import db_to_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

df = db_to_model.processed_data

# 머신러닝 모델에 데이터 입력
X = df[['duration_sec','date_compare','good','avg_count']]  # 영상길이,영상업로드날짜차이,좋아요 수
y = df['count']  # 예시로 target 값 사용

# 데이터 전처리
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 특성 선택
selector = SelectKBest(score_func=f_regression, k=3)  # 선택할 특성의 개수를 조정할 수 있습니다.
X_selected = selector.fit_transform(X_scaled, y)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.3, random_state=42)

# 선형 회귀 모델 학습
model = LinearRegression()
model.fit(X_train, y_train)

#예측 결과 평가
score = model.score(X_test, y_test)
print("R^2 Score:", score)

######################################################################

# 모델 피클로 저장
def save_model(model):
    with open("./flask_app/model.pkl", 'wb') as file:
        pickle.dump(model, file)

save_model(model)