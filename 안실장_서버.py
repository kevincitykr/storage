# -*- coding: utf-8 -*-
"""
안실장_서버.py
대시보드(HTML)와 자동화 봇(Python)을 연결하는 통합 컨트롤러
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import subprocess
import os
import sys
import threading
import socket
import json
from datetime import datetime

app = Flask(__name__, template_folder='.')
CORS(app) # CORS 허용 추가

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 대시보드 파일 경로 명시적 설정
LATAM_HUB = os.path.join(BASE_DIR, "YouTube_Factory_Hub_20260429_0020.html")
ECONOMY_HUB = os.path.join(BASE_DIR, "Economy_Factory_Hub_20260419.html")
PSYCHOLOGY_HUB = os.path.join(BASE_DIR, "Psychology_Factory_Hub_20260419.html")
WINDLY_HUB = os.path.join(BASE_DIR, "..", "500.윈들리", "Windly_Factory_Hub.html")
OLD_DASHBOARD = os.path.join(BASE_DIR, "..", "003_onhwa_mindnote", "dashboard_005.html")


def get_best_dashboard():
    if os.path.exists(LATAM_HUB): return LATAM_HUB
    if os.path.exists(ECONOMY_HUB): return ECONOMY_HUB
    if os.path.exists(PSYCHOLOGY_HUB): return PSYCHOLOGY_HUB
    return OLD_DASHBOARD


DASHBOARD_PATH = get_best_dashboard()

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# 봇 스크립트 매핑
BOT_SCRIPTS = {
    "psychology": os.path.join(BASE_DIR, "안실장_심리자동봇.py"),
    "economy": os.path.join(BASE_DIR, "안실장_경제자동봇.py"),
    "latam_music": os.path.join(BASE_DIR, "안실장_라틴음악봇.py")
}


# 상태 저장용 변수
status = {
    "is_running": False,
    "current_type": "",
    "current_topic": "",
    "progress": 0,
    "status_text": "대기 중",
    "last_result": "아직 실행 결과가 없습니다.",
    "logs": ["서버가 가동되었습니다. 안실장님의 명령을 기다리는 중..."],
    "log_file": os.path.join(BASE_DIR, "output", "bot_runtime.log")
}

def add_log(msg):
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    status["logs"].append(log_msg)
    print(f"[*] {log_msg}")
    try:
        with open(status["log_file"], "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    except:
        pass

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 연결하지 않고 소켓의 주소를 알아냄
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

LOCAL_IP = get_local_ip()

# 로그 파일 초기화
if not os.path.exists(os.path.dirname(status["log_file"])):
    os.makedirs(os.path.dirname(status["log_file"]), exist_ok=True)
with open(status["log_file"], "w", encoding="utf-8") as f:
    f.write(f"--- SERVER STARTED AT {datetime.now()} ---\n")

@app.route('/')
def index():
    # 명시적으로 경제 허브 우선 서빙
    if os.path.exists(LATAM_HUB):
        path = LATAM_HUB
    elif os.path.exists(ECONOMY_HUB):
        path = ECONOMY_HUB
    elif os.path.exists(PSYCHOLOGY_HUB):
        path = PSYCHOLOGY_HUB
    else:
        path = OLD_DASHBOARD

        
    print(f"[*] Serving Dashboard: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.route('/economy')
def economy():
    print(f"[*] Serving Economy Dashboard: {ECONOMY_HUB}")
    with open(ECONOMY_HUB, "r", encoding="utf-8") as f:
        return f.read()

@app.route('/psychology')
def psychology():
    print(f"[*] Serving Psychology Dashboard: {PSYCHOLOGY_HUB}")
    with open(PSYCHOLOGY_HUB, "r", encoding="utf-8") as f:
        return f.read()

@app.route('/windly')
def windly():
    print(f"[*] Serving Windly Dashboard: {WINDLY_HUB}")
    if not os.path.exists(WINDLY_HUB):
        return "Windly Dashboard file not found. Please create it first.", 404
    with open(WINDLY_HUB, "r", encoding="utf-8") as f:
        return f.read()

@app.route('/api/run_bot', methods=['POST'])
def run_bot():
    if status["is_running"]:
        return jsonify({"ok": False, "msg": "이미 봇이 가동 중입니다."})
    
    topic = request.args.get('topic', '일반')
    bot_type = request.args.get('type', 'psychology')
    
    if bot_type not in BOT_SCRIPTS:
        return jsonify({"ok": False, "msg": f"알 수 없는 봇 타입입니다: {bot_type}"})
    
    bot_script = BOT_SCRIPTS[bot_type]
    
    # 별도 스레드에서 봇 실행
    def execute():
        status["is_running"] = True
        status["current_type"] = bot_type
        status["current_topic"] = topic
        status["progress"] = 5
        status["status_text"] = "봇 초기화 중..."
        
        start_msg = f"▶ [{datetime.now().strftime('%H:%M:%S')}] '{bot_type}' 가동 (주제: {topic})..."
        status["logs"].append(start_msg)
        
        try:
            # 봇 스크립트 실행 (로그를 파일과 상태 객체에 동시 기록)
            with open(status["log_file"], "a", encoding="utf-8") as lf:
                lf.write(f"\n{start_msg}\n")
                
                process = subprocess.Popen(
                    [sys.executable, bot_script], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True, 
                    encoding='utf-8',
                    bufsize=1,
                    universal_newlines=True
                )
                
                for line in process.stdout:
                    clean_line = line.strip()
                    if clean_line:
                        status["logs"].append(clean_line)
                        lf.write(f"{clean_line}\n")
                        lf.flush()
                        
                        # 진행률 파싱 (봇 스크립트의 [STEP X] 패턴 매칭)
                        if "[STEP 0]" in clean_line: 
                            status["progress"] = 10
                            status["status_text"] = "새 노트북 생성 중..."
                        elif "[STEP 1]" in clean_line: 
                            status["progress"] = 25
                            status["status_text"] = "마중물 소스 주입 중..."
                        elif "[STEP 2]" in clean_line: 
                            status["progress"] = 45
                            status["status_text"] = "트렌드 주제 분석 중..."
                        elif "[STEP 3]" in clean_line: 
                            status["progress"] = 65
                            status["status_text"] = "대본 및 시각 묘사 생성 중..."
                        elif "[STEP 4]" in clean_line: 
                            status["progress"] = 85
                            status["status_text"] = "LM Studio 프롬프트 최적화 중..."
                        elif "[FINISH]" in clean_line:
                            status["progress"] = 100
                            status["status_text"] = "작업 완료!"
                
                process.wait()
            
            if process.returncode == 0:
                status["progress"] = 100
                status["status_text"] = "완료"
                status["logs"].append(f"✅ [성공] {bot_type} 제작 파이프라인 완료!")
                status["last_result"] = "제작된 파일을 확인해 주세요."
            else:
                status["status_text"] = "오류 발생"
                status["logs"].append(f"❌ [오류] 봇 실행 중 문제가 발생했습니다. (Exit Code: {process.returncode})")
        
        except Exception as e:
            status["status_text"] = "시스템 에러"
            status["logs"].append(f"❌ [에러] 시스템 예외 발생: {str(e)}")
        
        status["is_running"] = False

    threading.Thread(target=execute).start()
    return jsonify({"ok": True, "msg": "봇 가동 명령 접수 완료"})

@app.route('/api/status')
def get_status():
    return jsonify({
        "is_running": status["is_running"],
        "current_type": status["current_type"],
        "current_topic": status["current_topic"],
        "progress": status["progress"],
        "status_text": status["status_text"],
        "logs": status["logs"][-50:], # 최근 50줄 전송
        "last_result": status["last_result"]
    })

@app.route('/api/forbidden_keywords')
def get_forbidden_keywords():
    master_list_path = os.path.join(BASE_DIR, "..", "500.윈들리", "forbidden_master_list.json")
    if os.path.exists(master_list_path):
        with open(master_list_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/forbidden_keywords/add', methods=['POST'])
def add_forbidden_keyword():
    data = request.json
    keyword = data.get('keyword')
    reason = data.get('reason', '수동 추가')
    if not keyword:
        return jsonify({"ok": False, "msg": "키워드를 입력해주세요."})
    
    master_list_path = os.path.join(BASE_DIR, "..", "500.윈들리", "forbidden_master_list.json")
    master_list = {}
    if os.path.exists(master_list_path):
        with open(master_list_path, "r", encoding="utf-8") as f:
            master_list = json.load(f)
            
    master_list[keyword] = reason
    
    with open(master_list_path, "w", encoding="utf-8") as f:
        json.dump(master_list, f, ensure_ascii=False, indent=4)
        
    return jsonify({"ok": True, "msg": f"'{keyword}' 추가 완료"})

@app.route('/api/forbidden_keywords/delete', methods=['POST'])
def delete_forbidden_keyword():
    data = request.json
    keyword = data.get('keyword')
    
    if not keyword:
        return jsonify({"ok": False, "msg": "삭제할 키워드가 없습니다."})
        
    master_list_path = os.path.join(BASE_DIR, "..", "500.윈들리", "forbidden_master_list.json")
    if os.path.exists(master_list_path):
        with open(master_list_path, "r", encoding="utf-8") as f:
            master_list = json.load(f)
            
        if keyword in master_list:
            del master_list[keyword]
            with open(master_list_path, "w", encoding="utf-8") as f:
                json.dump(master_list, f, ensure_ascii=False, indent=4)
            return jsonify({"ok": True, "msg": f"'{keyword}' 삭제 완료"})
            
    return jsonify({"ok": False, "msg": "키워드를 찾을 수 없습니다."})

@app.route('/api/sync_legal', methods=['POST'])
def sync_legal():
    # ... (기존 코드 생략)
    pass

@app.route('/api/launch_kvenue', methods=['POST'])
def launch_kvenue():
    script_path = os.path.join(BASE_DIR, "..", "500.윈들리", "kvenue_auto.py")
    def run_bot():
        subprocess.run([sys.executable, script_path])
    threading.Thread(target=run_bot).start()
    return jsonify({"ok": True, "msg": "K-Venue 브라우저를 실행했습니다."})

@app.route('/api/launch_debug_chrome', methods=['POST'])
def launch_debug_chrome():
    add_log("🚀 디버그 웨일 실행 요청 수신")
    whale_path = r"C:\Program Files\Naver\Naver Whale\Application\whale.exe"
    user_data_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Naver", "Naver Whale", "User Data")
    
    def run_whale():
        try:
            add_log("⏳ 기존 웨일 프로세스 종료 중...")
            subprocess.run(["taskkill", "/f", "/im", "whale.exe"], capture_output=True)
            import time; time.sleep(2)
            
            add_log(f"🚀 웨일 실행: {whale_path}")
            cmd = [
                whale_path,
                f"--user-data-dir={user_data_dir}",
                "--profile-directory=Default",
                "--remote-debugging-port=9222",
                "--no-first-run",
                "--no-default-browser-check",
                "https://www.aliexpress.com/ssr/300001014/kvenue-update"
            ]
            subprocess.Popen(cmd)
            add_log("✅ 웨일 실행 완료 (윈들리 확장 포함)")
        except Exception as e:
            add_log(f"❌ 웨일 실행 중 오류: {str(e)}")
    
    threading.Thread(target=run_whale).start()
    return jsonify({"ok": True, "msg": "디버그 모드 웨일이 실행되었습니다. 로그인을 확인해 주세요."})


@app.route('/api/run_windly_clicker', methods=['POST'])
def run_windly_clicker():
    add_log("🤖 윈들리 클릭커 실행 요청 수신")
    script_path = os.path.join(BASE_DIR, "..", "500.윈들리", "windly_clicker.py")
    def run_bot():
        try:
            # 결과 로그를 실시간으로 status["logs"]에 추가하기 위해 subprocess.Popen 사용
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )
            for line in process.stdout:
                clean_line = line.strip()
                if clean_line:
                    add_log(f"[CLICKER] {clean_line}")
            process.wait()
            add_log("🏁 윈들리 클릭커 작업 종료")
        except Exception as e:
            add_log(f"❌ 클릭커 실행 중 오류: {str(e)}")
    
    threading.Thread(target=run_bot).start()
    return jsonify({"ok": True, "msg": "윈들리 자동 클릭커가 시작되었습니다."})

@app.route('/api/generate_excel', methods=['POST'])
def api_generate_excel():
    try:
        import subprocess
        result = subprocess.run(['python', os.path.join(BASE_DIR, "..", "500.윈들리", "generate_excel.py")], 
                              capture_output=True, text=True, encoding='utf-8')
        if "성공" in result.stdout:
            add_log("📊 엑셀 파일 생성 성공! (알리수집 폴더)")
            return jsonify({"status": "success", "message": result.stdout})
        else:
            add_log(f"❌ 엑셀 생성 실패: {result.stdout}")
            return jsonify({"status": "error", "message": result.stdout})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/trigger_scrape', methods=['POST'])
def trigger_scrape():
    signal_path = os.path.join(BASE_DIR, "..", "500.윈들리", "scrape_signal.txt")
    with open(signal_path, "w") as f:
        f.write("START")
    return jsonify({"ok": True, "msg": "수집 명령을 전달했습니다."})

@app.route('/api/collected_results')
def get_collected_results():
    results_path = os.path.join(BASE_DIR, "..", "500.윈들리", "collected_results.json")
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])

if __name__ == '__main__':
    print("\n" + "="*50)
    print("   안실장 심리 자동화 통합 서버 가동 중")
    print(f"   로컬 접속: http://127.0.0.1:5000")
    print(f"   외부 접속 (B노트북): http://{LOCAL_IP}:5000")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
