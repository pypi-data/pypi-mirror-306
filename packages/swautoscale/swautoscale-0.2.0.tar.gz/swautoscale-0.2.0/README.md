# swautoscale 


# description 
docker-compose.yml 파일 실행후 사이트 부하에 따라 자동으로 운용 도커의 스케일을 늘렸다 줄였다 하는 프로그램 


## 사용법
패키지가 설치되는 곳에서 docker-compose.yml 파일을 실행 
패키지 설치 위치는 autoscale 명령어를 사용하면 출력되는 로그 생성 위치와 동일 

```
# 패키지 위치 찾기 위해 실행 
$ autoscale 
패키지 설치된 위치: ~/.pyenv/versions/3.11.9/lib/python3.11/site-packages/k1s
log 저장되는 곳 : ~/.pyenv/versions/3.11.9/lib/python3.11/site-packages/k1s/dockerlog.log

# 패키지 위치로 이동 
$ cd  ~/.pyenv/versions/3.11.9/lib/python3.11/site-packages/k1s

# 파일 실행 
$ docker compose up -d --force-recreate --build
 
```

## 기능 
자동으로 autoscale 

```
$ autoscale
```

수동으로 스케일 out 

```
# o + 늘릴 스케일 수 
$ o 1  

```

수동으로 스케일 in

```
# o + 줄일 스케일 수 
$ o 1  
```

## 내장된 부가기능 
(1) LINE_API_KEY  환경변수 설정시 스케일 인/아웃시 메세지 전송 기능 
 



