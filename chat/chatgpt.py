import openai
import requests
from flask import Flask, request, jsonify, send_file, render_template,Blueprint
# from infer_zh import main as generate_melody
import subprocess
import re
from lyrics_to_phone import convert_to_phonemes

# app = Flask(__name__)


app1 = Blueprint('app1', __name__)


# 设置你的ChatGPT API密钥
openai.api_key = '  '

is_en = 1


def has_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            return True
    return False


@app1.route('/app1')
def serve_html():
    return send_file("templates/chatgpt.html")
# @app1.route('/app1')
# def index():
#     return render_template('homepage.html')

@app1.route('/get_answer', methods=['POST'])
def get_answer():
    user_input = request.json['input']

    # 调用 ChatGPT API 进行回答
    response = openai.Completion.create(
        engine='gpt-3.5-turbo-instruct',  # 使用 ChatGPT 引擎
        prompt=user_input,
        max_tokens=500  # 设置生成回答的最大长度
    )

    answer = response.choices[0].text.strip()

    if has_chinese(user_input):
        answer_re = answer.replace(',', ' ').replace('.', ' ').replace('，', ' ').replace('。', ' ')
        answer_re = re.sub(r'[^\u4e00-\u9fff\s]', '', answer_re)  # 去除非中文字符
        answer_re = answer_re.strip() # 去除开头结尾的换行符
        answer_re = answer_re.replace('\n', ' ')  # 将换行符替换为空格
        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格
        # 将空格替换为[sep]
        answer_re = answer_re.replace(' ', '[sep] ')
        # 使用正则表达式，在每个单词之间添加空格
        answer_re = ' '.join(answer_re)

        answer_re = answer_re.replace('[ s e p ]', '[sep]')

        # 在末尾添加 [sep]
        answer_re += ' [sep]'

        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格

        # 将处理后的回答写入 lyric.txt 文件中
        with open('data/zh/test/lyric.txt', 'w') as f:
            f.write(answer_re)

        return jsonify({'answer': answer})

    else:  # 英文

        # 去除数字
        answer_re = re.sub(r'\d+', '', answer)
        # 去除 ":" 和特定词汇
        words_to_remove = ['Verse', 'Chorus', 'Bridge', 'Outro']
        for word in words_to_remove:
            answer_re = answer_re.replace(word, '')
        # 将标点符号给去掉
        answer_re = answer_re.replace(',', '').replace('.', '').replace(':','')
        # 将开头结尾的空格给去掉
        answer_re = answer_re.strip()
        # 将多个换行符换成一个换行符
        answer_re = re.sub(r'\n+', '\n', answer_re)
        answer_re = answer_re.replace('\n', ' [sep] ')
        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格

        # 在末尾添加 [sep]
        answer_re += ' [sep]'

        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格
        phone = convert_to_phonemes(answer_re)
        with open('data/en/test/syllable.txt', 'w') as f:
            f.write(phone)
        # 将处理后的回答写入 lyric.txt 文件中
        with open('data/en/test/lyric.txt', 'w') as f:
            f.write(answer_re)

        global is_en
        is_en = 0

        return jsonify({'answer': answer})


@app1.route('/update_answer', methods=['POST'])
def update_answer():
    new_input = request.json['input']
    answer = request.json['answer']

    # 更新回答
    updated_answer = answer.replace('原来的回答', new_input)  # 替换原来的回答

    if has_chinese(new_input):
        answer_re = update_answer.replace(',', ' ').replace('.', ' ').replace('，', ' ').replace('。', ' ')
        answer_re = re.sub(r'[^\u4e00-\u9fff\s]', '', answer_re)  # 去除非中文字符
        answer_re = answer_re.strip()
        answer_re = answer_re.replace('\n', ' ')  # 将换行符替换为空格
        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格
        # 将空格替换为[sep]
        answer_re = answer_re.replace(' ', '[sep] ')
        # 使用正则表达式，在每个单词之间添加空格
        answer_re = ' '.join(answer_re)

        answer_re = answer_re.replace('[ s e p ]', '[sep]')

        # 在末尾添加 [sep]
        answer_re += ' [sep]'

        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格

        # 将处理后的回答写入 lyric.txt 文件中
        with open('data/zh/test/lyric.txt', 'w') as f:
            f.write(answer_re)

    else:
        # 去除数字
        answer_re = re.sub(r'\d+', '', answer)
        # 去除 ":" 和特定词汇
        words_to_remove = ['Verse', 'Chorus', 'Bridge', 'Outro']
        for word in words_to_remove:
            answer_re = answer_re.replace(word, '')
        answer_re = answer_re.replace(',', '').replace('.', '').replace(':', '')
        answer_re = answer_re.strip()

        answer_re = re.sub(r'\n+', '\n', answer_re)
        answer_re = answer_re.replace('\n', ' [sep] ')
        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格
        # # 将空格替换为[sep]
        # answer_re = answer_re.replace(' ', '[sep] ')
        # # 使用正则表达式，在每个单词之间添加空格
        # answer_re = ' '.join(answer_re)
        #
        # answer_re = answer_re.replace('[ s e p ]', '[sep]')

        # 在末尾添加 [sep]
        answer_re += ' [sep]'

        answer_re = re.sub(r'\s+', ' ', answer_re)  # 多个连续空格替换为单个空格
        phone = convert_to_phonemes(answer_re)
        with open('data/en/test/syllable.txt', 'w') as f:
            f.write(phone)
        # 将处理后的回答写入 lyric.txt 文件中
        with open('data/en/test/lyric.txt', 'w') as f:
            f.write(answer_re)

        global is_en
        is_en = 0
    return jsonify({'updatedAnswer': updated_answer})


@app1.route('/generate_music', methods=['POST'])
def generate_music():
    # 获取前端传来的和弦数据
    chords = request.json['chords']
    if is_en == 1:
        # 将和弦保存到 chord.txt 文件中
        with open('data/zh/test/chord.txt', 'w') as f:
            f.write(chords)

        # 调用生成音乐的 Python 文件（假设为 generate_music.py）
        # 运行生成音乐的代码，并生成 0.mid 文件
        # 这里只是一个示例，您需要根据实际情况调用相应的代码
        subprocess.run(['python', 'infer_zh.py'])

        # 构建生成的音乐文件路径和下载链接
        file_name = '0.mid'
        file_path = f'results/zh/midi/{file_name}'
        download_link = f"/download_music?file={file_name}"

        # 返回生成的音乐文件路径和下载链接
        return jsonify({'file_path': file_path, 'download_link': download_link})
    if is_en == 0:
        # 将和弦保存到 chord.txt 文件中
        with open('data/en/test/chord.txt', 'w') as f:
            f.write(chords)

        # 调用生成音乐的 Python 文件（假设为 generate_music.py）
        # 运行生成音乐的代码，并生成 0.mid 文件
        # 这里只是一个示例，您需要根据实际情况调用相应的代码
        subprocess.run(['python', 'infer_en.py'])

        # 构建生成的音乐文件路径和下载链接
        file_name = '0.mid'
        file_path = f'results/en/midi/{file_name}'
        download_link = f"/download_music?file={file_name}"

        # 返回生成的音乐文件路径和下载链接
        return jsonify({'file_path': file_path, 'download_link': download_link})


@app1.route('/download_music', methods=['GET'])
def download_music():
    if is_en == 1:
        # 获取下载文件的路径
        file_name = request.args.get('file')
        file_path = f'results/zh/midi/{file_name}'

        # 返回生成的音乐文件，并添加 CORS 头部
        response = send_file(file_path, mimetype='audio/midi')
        response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有域访问，可以根据需求进行调整

        return response
    elif is_en == 0:
        # 获取下载文件的路径
        file_name = request.args.get('file')
        file_path = f'results/en/midi/{file_name}'

        # 返回生成的音乐文件，并添加 CORS 头部
        response = send_file(file_path, mimetype='audio/midi')
        response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有域访问，可以根据需求进行调整

        return response

#
# if __name__ == '__main__':
#     app.run()
