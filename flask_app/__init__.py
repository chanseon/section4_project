from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# 피클로 저장된 모델 로드
def load_model():
    with open("flask_app/model.pkl", 'rb') as file:
        model = pickle.load(file)
    return model


def predict(model=load_model()):
    # 모델로 예측 수행
    prediction = model.predict([[36000,10,100]])
    # 영상길이,영상업로드날짜차이,좋아요 수
    prediction = prediction.tolist()
    # 예측 결과 반환
    return jsonify({'predicted count': prediction})

@app.route('/predict')
def index():
    return predict(),200


if __name__ == '__main__':
    app.run(debug=True)


#FLASK_APP=flask_app flask run






















# import pickle
# import pandas as pd
# from flask import Flask, request, jsonify

# # 피클로 저장된 모델 로드
# def load_model():
#     with open("API/model.pkl", 'rb') as file:
#         model = pickle.load(file)
#     return model

# # # #새로운 데이터로 예측
# # # def predict(model):
# # #           input_data = []
# # #           for i in ['duration_sec','date_compare','good']:
# # #                     input_data.append(int(input(i+":")))
# # #           new_data = pd.DataFrame([input_data])  # 예시로 새로운 데이터 생성
# # #           prediction = model.predict(new_data)

# # #           return prediction

# # # model = load_model()

# # # app = Flask(__name__)

# # # # 예측 엔드포인트
# # # @app.route('/')
# # # def index():
# # #     request.get_json()
# # #     return 'Hello World!'

# # # @app.route('/predict', methods=['POST'])
# # # def predict():
# # #         if request.method == 'POST':
# # #                     data = request.get_json()
# # #                     duration_sec = data['duration_sec']
# # #                     date_compare = data['date_compare']
# # #                     good = data['good']
# # #         new_data = pd.DataFrame([[duration_sec, date_compare, good]])

# # #         # 모델로 예측 수행
# # #         prediction = model.predict(new_data)
# # #         # 예측 결과 반환
# # #         return jsonify({'prediction': prediction})

# # # if __name__ == '__main__':
# # #     app.run(debug=True)
# # ####################################################################################
# # from flask import Flask, request

# # app = Flask(__name__)

# # @app.route('/ex', methods=['POST'])
# # def example():
# #     data = request.get_json()  # JSON 데이터 파싱

# #     # 파싱된 JSON 데이터에 접근
# #     value = data['key']

# #     # 처리 로직 작성

# #     return 'Success'

# # if __name__ == '__main__':
# #     app.run(debug=True)a

