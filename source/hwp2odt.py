import os
import cloudconvert
import argparse

# set api key
cloudconvert.configure(api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZmEzNzYwYWIxZjA1NDM2N2FhY2IwZWQ5NjU3OGViZjEyZjcxZmViYTJjYzYyNzA2ODM5NGRmMzMzNjJhYmJiZDhlZTFiNjkyNTliZDYzOGYiLCJpYXQiOjE2NjAwNDQ4MjguNzI2NjQsIm5iZiI6MTY2MDA0NDgyOC43MjY2NDIsImV4cCI6NDgxNTcxODQyOC43MTQzMiwic3ViIjoiNTkyMjI1MjMiLCJzY29wZXMiOlsidXNlci5yZWFkIiwidGFzay5yZWFkIiwidXNlci53cml0ZSIsInRhc2sud3JpdGUiLCJ3ZWJob29rLnJlYWQiLCJ3ZWJob29rLndyaXRlIiwicHJlc2V0LnJlYWQiLCJwcmVzZXQud3JpdGUiXX0.A05yFRwzrZWLFFoEIDcNQLqzQrwy4PTfG-X46ZShDrtden_VzgSaXJqCdrP0Ep_E-2Yihgdv90b-bNbP8J2AfJwsibf-L4CcSfAZaU9e7fXDQYfjg6jTTstAbkBAk5ewIKEA3xa-srVt518vs_Ngkc3RMYnWycNP5fM7IMnqL7MB5yfkXSkCPC1hq6Rtf9B9VbmG4bFy7F8Y-VqMtYLrqZHN0D4FV3AfHBC6HUyVEX997eV4StMKaINNvieSSNrPIkUM5dWmktD7NgZZ4iUpUorlFuTPZhxaFotFid37-v6r4N68wj6If3-hnzADe4zrV7l6Eku9wYSt4CxTqIjeQPnvtCq9dlPTYom-OjrjPIczjD0woHbm1dS1Jw3VMaU4j5blVii2EYBtLLxRw6D16quI__Xd6vYWCbPucaEI-d4eaQSr42BRTEtohSbwefEVwYAugYj3JYkQxjHmgVXGiMWM8EhX0FbFjuxmgo5J6iz3jngX_gn8CqBv-Rrec7m0J-ef1zywpSpemW0iRdaFiDcuJpzrGtmSjgR8_ZAA_vTH2P-HFzGyh9zOF1TTL6uLs_oEPMQewrJvScaZLxJCOILWZKW-V86vSfaI-saXoAt0mLpgZ893F4J8E-np5_wOIy32VFOnh7Ce64_eG48IeW-Ojftu0_Hx_prmE76MPxs' , sandbox = False)
ip_address = '218.48.227.56'

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
        :param str file_path: hwp파일의 base이름 입력 ex) test.hwp
               str output_dir: 결과 저장 경로 입력 ex) output/

    :return 성공 여부와 저장된 경로를 반환합니다.
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
    # 변환 다 될때 까지 기다리기
    job = cloudconvert.Job.wait(id=job['id'])

    # export 작업이 완료된 파일에 대해서 뽑기
    for task in job["tasks"]:
        if task.get("name") == "export-my-file" and task.get("status") == "finished":
            export_task = task

    # 변환된 odt file return 받기 url형태로 받음
    file = export_task.get("result").get("files")[0]
    # file download
    cloudconvert.download(filename= os.path.join('..' , output_dir ,file['filename']), url=file['url'])

    return None

if __name__ == "__main__":
    hwp2odt(file_name , output_dir)