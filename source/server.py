# importing flask
from flask import Flask, request, send_file
import os
from glob import glob
from urllib import parse

# 데이터 모두 불러 오기
data = glob('dataset/*.hwp')
data_name = [os.path.basename(data) for data in data ]
print(data_name)
app = Flask(__name__)

@app.route('/')
@app.route('/get_hwp')

def get_hwp() :
    '''
    Description:
        hwp file을 url로 넘겨주기 위한 함수
    '''

    # hwp file path 지정
    hwp_dir = "dataset/"
    hwp_file = request.args['data']
    enc_name = parse.quote(hwp_file)
    hwp_path = os.path.join(hwp_dir, hwp_file)

    # 절대 경로로 변경
    full_path = os.getcwd()
    full_path = os.path.join(full_path , hwp_path)
    # Also make sure the requested hwp file does exist
    if not os.path.isfile(hwp_path):
        return "ERROR: file %s was not found on the server" % hwp_file
    # Send the file back to the client
    return send_file(full_path, as_attachment=True, attachment_filename=enc_name)

# 서버 실행
app.run(host='0.0.0.0', port=int("9000"))