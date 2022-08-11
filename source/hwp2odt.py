import os
import cloudconvert
import argparse
import json

with open('config.json', 'r') as f:
    json_data = json.load(f)


# set key & ip_address
api_key = json_data['api_key']
cloudconvert.configure(api_key = api_key , sandbox = False)
ip_address = json_data['ip_address']

parser = argparse.ArgumentParser(description='get config')
parser.add_argument('--file_name', type=str, help='file_name')
parser.add_argument('--output_dir', type=str, help='output_dir')

args = parser.parse_args()
file_name = args.file_name
output_dir = args.output_dir

def hwp2odt(file_name , output_dir):
    '''
    Description:
        hwp파일을 odt파일로 변환하는 함수입니다.

    Args:
        file_path (str): hwp파일의 base이름 입력 ex) test.hwp
        output_dir (str): 결과 저장 경로 입력 ex) output/

    Return: 성공 여부와 저장된 경로를 반환합니다.
   '''

    url_path = f'http://{ip_address}:9000/get_hwp?data='
    file_path = url_path + file_name
    print(file_path)
    # hwp파일을 불러오고, 전환하고, 내보내는 3가지 task에 대한 job을 정의
    job = cloudconvert.Job.create(payload={
        "tasks": {
             'import-my-file': {
                  'operation': 'import/url',
                  'url': file_path
             },
            'convert-my-file': {
                'operation': 'convert',
                'input': 'import-my-file',
                'input_format' : "hwp" ,
                'output_format': 'odt',
                'some_other_option': 'value'
            },
            'export-my-file': {
                'operation': 'export/url',
                'input': 'convert-my-file'
            }
        }
    })
    print(job)
    # 변환 다 될때 까지 기다리기
    job = cloudconvert.Job.wait(id=job['id'])

    # export 작업이 완료된 파일에 대해서 뽑기
    for task in job["tasks"]:
        if task.get("name") == "export-my-file" and task.get("status") == "finished":
            export_task = task

    # 변환된 odt file return 받기 url형태로 받음
    file = export_task.get("result").get("files")[0]
    # file download
    cloudconvert.download(filename= os.path.join( output_dir ,file['filename']), url=file['url'])

    return None

if __name__ == "__main__":
    hwp2odt(file_name , output_dir)