from flask import Flask, request, render_template
import os

app = Flask(__name__)

# 신청 유형별 파일 경로
FILES = {
    'male': 'male.txt',
    'female': 'female.txt',
    'group': 'group.txt'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    song_type = request.form['song']
    file_path = FILES[song_type]

    # 중복 신청 방지
    for path in FILES.values():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                if name in f.read().splitlines():
                    return f"<h2>{name}님은 이미 신청하셨습니다!</h2>"

    # 이름 저장
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(name + '\n')

    return f"<h2>{name}님, {song_type} 곡 신청 완료!</h2>"

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

if __name__ == '__main__':
    app.run(debug=True)
