from flask import Flask, request

app = Flask(__name__)

@app.route('/ex', methods=['POST'])
def example():
    data = request.get_json()  # JSON 데이터 파싱

    # 파싱된 JSON 데이터에 접근
    value = data['key']

    # 처리 로직 작성

    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)