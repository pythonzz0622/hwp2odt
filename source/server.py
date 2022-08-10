# importing flask
from flask import Flask, request, send_file
import os
from glob import glob

data = glob('../dataset/*.hwp')
data_name = [os.path.basename(data) for data in data ]

app = Flask(__name__)

@app.route('/')
@app.route('/get_hwp')
def get_hwp():
    '''

    :return: query형식으로 받음
    '''
    hwp_dir = "../dataset/"
    hwp_file = request.args['data']
    hwp_path = os.path.join(hwp_dir, hwp_file)

    # Also make sure the requested hwp file does exist
    if not os.path.isfile(hwp_path):
        return "ERROR: file %s was not found on the server" % hwp_file
    # Send the file back to the client
    return send_file(hwp_path, as_attachment=True, attachment_filename=hwp_file)

app.run(host='0.0.0.0', port=int("9000"))