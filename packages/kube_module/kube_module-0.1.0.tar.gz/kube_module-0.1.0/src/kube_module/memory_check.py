import subprocess
import json
import time
from datetime import datetime
import os
import requests

global a_count
global b_count

def linux_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )
    return result

def check_ab(a,b):
    global a_count 
    global b_count
    if a:
        a_count = a_count + 1
        b_count = 0
    if b:
        b_count = b_count + 1
        a_count = 0
    return a_count,b_count

def log_scale_change(action):
    # 로그 디렉토리 생성
    log_dir = './log/scaletime/'
    os.makedirs(log_dir, exist_ok=True)  # 디렉토리가 없으면 생성
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    log_message = f"{current_time} - {action}\n"
    with open(os.path.join(log_dir, 'scale_changes.log'), 'a') as f:
        f.write(log_message)

def admin_scale(num):
    linux_command(['docker', 'compose', 'up', '-d', '--scale', f'blog={num}'])

def send_line(messages):
    token = os.getenv('LINE_NOTI_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    info = {'message': f'scale 알림 : {messages}'}
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data = info)

a_count = 0
b_count = 0

while True:

    try:
        result = linux_command(['docker', 'stats', 'samdul-blog-1', '--no-stream', '--format', '{{ json . }}'])

        # 결과를 JSON 형식으로 로드
        stats = json.loads(result.stdout)

        # CPU 사용량을 출력
        print(f"Current CPU Usage: {stats['CPUPerc']}")  # 예: '0.00%'
        
        CPU_usage = float(stats['CPUPerc'][:-1])  # 문자열에서 '%' 제거하고 float로 변환
        #scale,count = adjust_scale_based_on_cpu(CPU_usage, current_scale)
        if CPU_usage < 6:
            a = True; b = False
        else:
            a = False; b = True

        check_ab(a,b) 
        
        print(f"현재 scale 2의 지속시간 {a_count * 10}")
        print(f"현재 sacle 3의 지속시간 {b_count * 10}")
        
        if a_count == 6:
            linux_command(['docker', 'compose', 'up', '-d', '--scale', 'blog=2'])
            print("scale-in 완료")
            log_scale_change("scale-in 완료")  
            send_line("sacle-in 완료")

        if b_count == 6:
            linux_command(['docker', 'compose', 'up', '-d', '--scale', 'blog=3'])
            print("scale_out 완료")
            log_scale_change("scale-in 완료")
            send_line("scale-out 완료")

        # 1초 간 대기 
        time.sleep(1)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        break  # 오류 발생 시 루프 종료
    except json.JSONDecodeError:
        print("Failed to decode JSON from output.")
        break  # JSON 디코드 오류 발생 시 루프 종료
