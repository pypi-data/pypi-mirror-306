import subprocess
import json

def checkCPU(num):
    CPUchecklist = []
    statusCPU = "stable"
    #  docker container cpu/mem check
    for i in range(1,num+1):
        r = subprocess.check_output(["docker", "stats", f"samdul-blog-{i}", "--no-stream", "--format", "{{json .}}"])
        j = json.loads(r.decode("utf-8"))
        CPUchecklist.append(float(j['CPUPerc'].strip('%')))
    print(CPUchecklist, sum(CPUchecklist))
    if sum(CPUchecklist) > (num*0.5):
        statusCPU = "warn"
    print(statusCPU)
    return statusCPU



# 컴퓨터 cpu 80이하까지 생성하는 코드 while
try:
    warningcnt = 0
    stablecnt =0
    while True:
        # check blog num
        blogcount = subprocess.check_output(["bash", "-c", "docker stats --no-stream | grep samdul-blog | wc -l"])
        blogcountj = json.loads(blogcount.decode("utf-8"))


        # check blog docker cpu
        # 경고 카운트
        # 도커 운용 개수
        cntdocker = blogcountj
        # warn 사인 받으면
        if checkCPU(blogcountj) == "warn":
            warningcnt += 1
            print(warningcnt)
            # warningcnt  5이상이면 운용 도커량 증가
            if warningcnt == 3:
                cntdocker += 1
                subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
                warningcnt = 0
        # stable 사인 받으면
        elif (checkCPU(blogcountj) == "stable") and (cntdocker>1):
            stablecnt += 1
            print(stablecnt)
            # stablecnt 가  5이상이면 운용 도커량 감소
            if stablecnt == 10:
                cntdocker -= 1
                subprocess.run(['docker', 'compose', 'up', '-d', '--scale', f'blog={cntdocker}'])
                stablecnt = 0
        # else: 갑작스럽게 올라가는 량에 대비

except KeyboardInterrupt:
    print("Stopped by user.")
