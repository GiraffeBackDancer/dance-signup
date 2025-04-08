from flask import Flask, request, render_template
import os

app = Flask(__name__)
LIMITS = {'male': 6, 'female': 6, 'group': None}
FILES = {'male': 'male.txt', 'female': 'female.txt', 'group': 'group.txt'}

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

    # 제한 인원 확인
    if LIMITS[song_type] is not None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                applicants = f.read().splitlines()
        except FileNotFoundError:
            applicants = []

        if len(applicants) >= LIMITS[song_type]:
            return f"<h2>{song_type} 곡 신청은 마감되었습니다.</h2>"

    # 신청 저장
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(name + '\n')

    return f"<h2>{name}님, {song_type} 곡 신청 완료!</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

