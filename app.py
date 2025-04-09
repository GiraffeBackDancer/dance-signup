from flask import Flask, request, render_template, redirect, url_for
import os
from datetime import datetime
from pytz import timezone  # 한국 시간대 설정

app = Flask(__name__)

FILES = {
    'male': 'male.txt',
    'female': 'female.txt',
    'group': 'group.txt'
}

LIMITS = {
    'male': 6,
    'female': 6,
    'group': 999
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    song_type = request.form['song']
    file_path = FILES[song_type]

    # 중복 신청 확인
    for path in FILES.values():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                if name in f.read():
                    return render_template('result.html', message=f"{name}님은 이미 신청하셨습니다!", image=None)

    # 인원 제한 확인
    with open(file_path, 'r', encoding='utf-8') if os.path.exists(file_path) else open(os.devnull, 'r') as f:
        current = f.read().splitlines()
        if len(current) >= LIMITS[song_type]:
            return render_template('result.html', message=f"{song_type} 곡은 이미 인원이 마감되었습니다.", image=None)

    # 신청 시간 (한국 시간 기준)
    kst = timezone('Asia/Seoul')
    timestamp = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{name} ({timestamp})\n")

    # 신청 완료 메시지
    message = f"{name}님, {song_type} 곡 신청 완료!"
    return render_template('result.html', message=message, image=None)

@app.route('/status')
def status():
    status_data = {}
    for key, path in FILES.items():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                names = f.read().splitlines()
        except FileNotFoundError:
            names = []
        status_data[key] = names
    return render_template('status.html', status_data=status_data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    status_data = {}
    for key, path in FILES.items():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                names = f.read().splitlines()
        except FileNotFoundError:
            names = []
        status_data[key] = names

    if request.method == 'POST':
        for path in FILES.values():
            if os.path.exists(path):
                os.remove(path)
        return redirect(url_for('admin'))

    return render_template('admin.html', status_data=status_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
