import subprocess
import json
import yaml
import time 
import os 
import pytz
from datetime import datetime
import requests  
import sys  

# yaml파일 읽어와서 CPU 사용율 X% 구하기
with open('./docker-compose.yml') as f:
    file = yaml.full_load(f)
cpus_limit = float(file['services']['blog']['deploy']['resources']['limits']['cpus'])*100
#comming soon
#mem_limit = float(file['services']['blog']['deploy']['resources']['limits']['memory'])*100
print(cpus_limit)
#print(mem_limit)
file_path = __file__
timezone = pytz.timezone("Asia/Seoul")
directory = os.path.dirname(file_path)
log_path = os.path.join(directory,"dockerlog.log")
print(directory)
print(log_path)
if not os.path.exists(directory):
    os.makedirs(directory)
# 로그 파일 있는지 체크 없으면 칼럼 넣은 파일 생성 있으면 데이터 입력
if not os.path.exists(log_path):
    with open(log_path,"w") as f:
        f.write("time, CPUuses, scaleIO\n")

# curse 함수  키입력받기 / 추후 수정 사항 scale 개수 시스템으로 받아서 처리 num = sys.argv[1]
#scale in/out 수동 조작을 위한 함수 
def scalein():
    num = sys.argv[1]
    blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
    blogcountj = json.loads(blogcount.decode("utf-8")) 
    local_time = datetime.now(timezone)
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    _,result2=checkCPU(blogcountj) 
    # 도커 감소  개수 
    cntdocker = blogcountj - num
    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}']) 
    # 환경 변수로 Line key가 있을때 Line 발송 없으면 발송안함 
    line_message("scale in")
    with open(log_path, "a", encoding="utf-8", newline='') as f:
        f.write(f"{formatted_time},{result2},I\n")
    
def scaleout():
    num = sys.argv[1]
    blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
    blogcountj = json.loads(blogcount.decode("utf-8")) 
    local_time = datetime.now(timezone)
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    _,result2=checkCPU(blogcountj) 
    # 도커 감소  개수 
    cntdocker = blogcountj + num
    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}']) 
    # 환경 변수로 Line key가 있을때 Line 발송 없으면 발송안함 
    line_message("scale out")
    with open(log_path, "a", encoding="utf-8", newline='') as f:
        f.write(f"{formatted_time},{result2},O\n")



def checkCPU(num):
    CPUchecklist = []
    statusCPU = "stable"
    # docker container cpu/mem check 
    for i in range(1,num+1):
        r = subprocess.check_output(["docker", "stats", f"samdul-blog-{i}", "--no-stream", "--format", "{{json .}}"])
        j = json.loads(r.decode("utf-8"))
        CPUchecklist.append(float(j['CPUPerc'].strip('%')))
            
    # cpu_limit 비교해서 값 보다 크면 경고 
    if sum(CPUchecklist) >= (num*(cpus_limit*0.5)):  
        statusCPU = "warn"
    print(statusCPU)
    return statusCPU,round(sum(CPUchecklist),2)


# 환경 변수로 Line key가 있을때 Line 발송 없으면 발송안함 
def line_message(scalekind): 
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_API_KEY',"None")
    if token == "None":
        print("LINE_API_KEY 환경변수에 대한 정보가 없습니다.")
        return False 
    else:
        headers = {'Authorization':'Bearer '+token}
        message = {
            "message" : f"컨테이너가 {scalekind} 되었습니다."
        }
        requests.post(api_url, headers= headers , data = message)   


try:
    warningcnt = 0
    stablecnt =0
    nomore=0 
    while True:
        # 10초마다 확인/ 문제점: 도커 컨테이너 내리면 그시간도 포함됨
        # 10초마다 확인하면 이미 잼되서 죽은 상황에서 더이상 요청을 보내지않아 stable 해짐
        #time.sleep(7)
        # check blog num
        blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
        blogcountj = json.loads(blogcount.decode("utf-8")) 
        local_time = datetime.now(timezone)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
        # check blog docker cpu
        cntdocker = blogcountj
        # warn 사인 받으면 
        result1,result2 = checkCPU(blogcountj)
        print(f"시간:{formatted_time}, cpu 총 사용량: {result2}")
        if (result1 == "warn") and (nomore == 0):
            # 경고 카운트
            warningcnt += 1 
            stablecnt=0
            print(warningcnt)
            # 운용중인 도커의 개수가 30개 이하고  1분동안 지속적으로 warn이고 warningcnt 6이상이면 운용 도커량 증가/ 증가 할때는 기존 도커개수의 2배수 +1 증가 (jam 대비)
            if (warningcnt == 6) and (blogcountj <30) :
                # 도커 증가 개수 
                cntdocker = (blogcountj * 2) + 1 
                subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}']) 
                # 환경 변수로 Line key가 있을때 Line 발송 없으면 발송안함 
                line_message("scale out")
                with open(log_path, "a", encoding="utf-8", newline='') as f:
                    f.write(f"{formatted_time},{result2},O\n")
                warningcnt = 0
       # 운용중인 도커의 개수가 30개 이상이면 시스템 주의 경고 주고 마지막으로 늘려줌 더이상 못늘어나게함    
            elif (warningcnt == 6) and (blogcountj >29) :
                print("경고! 가용 자원이 부족합니다") 
                nomore=1
                cntdocker = (blogcountj * 2) + 1 
                subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}']) 
                line_message("scale out")
                with open(log_path, "a", encoding="utf-8", newline='') as f:
                    f.write(f"{formatted_time},{result2},O\n")
                warningcnt = 0
            else:
                with open(log_path, "a", encoding="utf-8", newline='') as f:
                    f.write(f"{formatted_time},{result2},\n")
                
        elif nomore == 1 :
            print("더 이상 컨테이너를 증가 시킬 수 없습니다.")
                
        # stable 사인 받으면 warning docker cnt 초기화   
        elif (result1 == "stable") and (cntdocker>1):
            # warningcnt = 0 
            stablecnt += 1 
            print(stablecnt)
            # stablecnt 가  3이상이면 운용 도커량 1개씩 감소 
            if stablecnt == 6:
                cntdocker -= 1
                subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}']) 
                line_message("scale in")
                with open(log_path, "a", encoding="utf-8", newline='') as f:
                    f.write(f"{formatted_time},{result2},I\n")
                stablecnt = 0
                if blogcountj < 30: 
                    nomore == 0                  
            else:     
                with open(log_path, "a", encoding="utf-8", newline='') as f:
                    f.write(f"{formatted_time},{result2},\n")

except KeyboardInterrupt:
    print("Stopped by user.")

