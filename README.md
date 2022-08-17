# hwp2odt

### 실행방법
config file에 외부 ip adress 와 cloudconvert_api 키를 추가
```
# cloudconvert server에 dataset을 url로 넘겨주기 위한 flask server실행
python source/server.py

# file 변환 코드 hwp to odt 
python source/hwp2odt.py --file_name="test.hwp" --output_dir="output" 
# 동시에 실행시키고 싶을 경우
sh run.sh
```
