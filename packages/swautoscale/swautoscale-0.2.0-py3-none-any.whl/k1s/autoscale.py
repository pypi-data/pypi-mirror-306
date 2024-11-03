import subprocess
import json
import yaml
import time
import os
import pytz
from datetime import datetime
import requests
import sys

# scale in/out 수동 조작을 위한 함수
def scalein():
    num = int(sys.argv[1])
    blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
    blogcountj = int(blogcount.decode("utf-8").strip())
    local_time = datetime.now(timezone)
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    _, result2 = checkCPU(blogcountj)
    cntdocker = blogcountj - num
    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
    line_message("scale in")
    with open(log_path, "a", encoding="utf-8", newline='') as f:
        f.write(f"{formatted_time},{result2},I\n")

def scaleout():
    num = int(sys.argv[1])
    blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
    blogcountj = int(blogcount.decode("utf-8").strip())
    local_time = datetime.now(timezone)
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    _, result2 = checkCPU(blogcountj)
    cntdocker = blogcountj + num
    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
    line_message("scale out")
    with open(log_path, "a", encoding="utf-8", newline='') as f:
        f.write(f"{formatted_time},{result2},O\n")


# yaml파일 읽어와서 CPU 사용율 X% 구하기
def readlimit():
    with open('./docker-compose.yml') as f:
        file = yaml.full_load(f)
    cpus_limit = float(file['services']['blog']['deploy']['resources']['limits']['cpus']) * 100
    print(cpus_limit)
    return cpus_limit

def checkCPU(num):
    cpus_limit = readlimit()
    CPUchecklist = []
    statusCPU = "stable"
    for i in range(1, num + 1):
        r = subprocess.check_output(["docker", "stats", f"samdul-blog-{i}", "--no-stream", "--format", "{{json .}}"])
        j = json.loads(r.decode("utf-8"))
        CPUchecklist.append(float(j['CPUPerc'].strip('%')))

    if sum(CPUchecklist) >= (num * (cpus_limit * 0.5)):
        statusCPU = "warn"
    print(statusCPU)
    return statusCPU, round(sum(CPUchecklist), 2)

def line_message(scalekind):
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_API_KEY', "None")
    if token == "None":
        print("LINE_API_KEY 환경변수에 대한 정보가 없습니다.")
        return False
    else:
        headers = {'Authorization': 'Bearer ' + token}
        message = {
            "message": f"컨테이너가 {scalekind} 되었습니다."
        }
        requests.post(api_url, headers=headers, data=message)

file_path = __file__
timezone = pytz.timezone("Asia/Seoul")
directory = os.path.dirname(file_path)
log_path = os.path.join(directory, "dockerlog.log")
print(f"패키지 설치된 위치: {directory}")
print(f"log 저장되는 곳 : {log_path}")

if not os.path.exists(directory):
    os.makedirs(directory)

# 로그 파일 있는지 체크 없으면 칼럼 넣은 파일 생성 있으면 데이터 입력
if not os.path.exists(log_path):
    with open(log_path, "w") as f:
        f.write("time, CPUuses, scaleIO\n")


def main():
    try:
        warningcnt = 0
        stablecnt = 0
        nomore = 0
        while True:
            blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
            blogcountj = int(blogcount.decode("utf-8").strip())
            local_time = datetime.now(timezone)
            formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
            cntdocker = blogcountj
            result1, result2 = checkCPU(blogcountj)
            print(f"시간:{formatted_time}, cpu 총 사용량: {result2}, 상태: {result1}")

            if (result1 == "warn") and (nomore == 0):
                warningcnt += 1
                stablecnt = 0
                print(warningcnt)

                if (warningcnt == 6) and (blogcountj < 30):
                    cntdocker = (blogcountj * 2) + 1
                    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
                    line_message("scale out")
                    with open(log_path, "a", encoding="utf-8", newline='') as f:
                        f.write(f"{formatted_time},{result2},O\n")
                    warningcnt = 0

                elif (warningcnt == 6) and (blogcountj > 29):
                    print("경고! 가용 자원이 부족합니다")
                    nomore = 1
                    cntdocker = (blogcountj * 2) + 1
                    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
                    line_message("scale out")
                    with open(log_path, "a", encoding="utf-8", newline='') as f:
                        f.write(f"{formatted_time},{result2},O\n")
                    warningcnt = 0
                else:
                    with open(log_path, "a", encoding="utf-8", newline='') as f:
                        f.write(f"{formatted_time},{result2},\n")

            elif nomore == 1:
                print("더 이상 컨테이너를 증가 시킬 수 없습니다.")

            elif (result1 == "stable") and (cntdocker > 1):
                stablecnt += 1
                print(stablecnt)

                if stablecnt == 6:
                    cntdocker -= 1
                    subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
                    line_message("scale in")
                    with open(log_path, "a", encoding="utf-8", newline='') as f:
                        f.write(f"{formatted_time},{result2},I\n")
                    stablecnt = 0
                    if blogcountj < 30:
                        nomore = 0
                else:
                    with open(log_path, "a", encoding="utf-8", newline='') as f:
                        f.write(f"{formatted_time},{result2},\n")

    except KeyboardInterrupt:
        print("Stopped by user.")
