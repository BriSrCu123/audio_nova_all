from flask import Flask, request, send_file, jsonify
import os
from flask_cors import CORS  # 导入 CORS
from pydub import AudioSegment
from werkzeug.debug import console

app = Flask(__name__)
# 允许跨域请求
CORS(app)

# 指定音频文件保存路径
SAVE_PATH = './raw'
RESULT_PATH = './result_wav'

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'wav'}


# 检查文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 检查上传保存路径是否存在，如果不存在就创建
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
# 检查结果保存路径是否存在，如果不存在就创建
if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)


@app.route('/api/optimization', methods=['POST'])
def optimization():
    # 参数接收
    files = request.files.getlist('audio')  # 接收多个音频文件
    if len(files) == 0:
        return jsonify({'error': 'No files uploaded'}), 400
    tones = request.form.getlist('tone')  # 接受音色序列
    if len(tones) == 0:
        return jsonify({'error': 'No tone selected'}), 400
    style = request.form.get('style')  # 获取风格
    if not style:
        return jsonify({'error': 'No style selected'}), 400

    # 优化算法，暂时放一个音轨合成代码
    audio_segments = []
    saved_file_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            try:
                # 保存文件到指定路径
                file_path = SAVE_PATH + "/" + file.filename
                file.save(file_path)
                saved_file_paths.append(file_path)

                # 使用 pydub 加载音频文件
                audio = AudioSegment.from_file(file_path)
                audio_segments.append(audio)
            except Exception as e:
                return jsonify({'error': f'Error loading audio file: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Invalid file format'}), 400

        if len(audio_segments) > 0:
            merged_audio = AudioSegment.silent(
                duration=max(audio.duration_seconds for audio in audio_segments) * 1000)  # 创建一个静音轨道，持续时间为最长音频的时长

            for i, audio in enumerate(audio_segments):
                merged_audio = merged_audio.overlay(audio, position=0)  # 所有音频在相同的时间位置重合

    if not merged_audio:
        print("merge successful")
    # 保存合并后的音频到指定路径
    merged_audio_path = RESULT_PATH + '/merged_audio.wav'
    merged_audio.export(merged_audio_path, format="wav")  # 保存为 WAV 格式

    # 返回合并后的音频文件给前端
    return send_file(
        merged_audio_path,
        mimetype='audio/wav',  # 设置文件的类型
        as_attachment=True,  # 使文件作为附件下载
        download_name='merged_audio.wav'  # 设置下载文件名
    )


if __name__ == '__main__':
    app.run(debug=True)

