from flask import Flask, request
import json
from question_classifyer import QuestionClassifier
from question_parser import QuestionPaser
from answer_search import AnswerSearcher
from flask_cors import CORS

# 创建一个FLASK应用实例
server = Flask(__name__)
# 使用CORS允许所有跨域请求
CORS(server, resources=r'/*')


# 定义路由“index”处理get请求
@server.route('/index', methods=['get'])
def index():
    res = {}
    classifier = QuestionClassifier()
    parser = QuestionPaser()
    searcher = AnswerSearcher()
    answer = """您好，我是小珞，希望可以帮您解决一些心理方面的问题。
    如果没有得到满意答案，欢迎反馈意见，祝您身体健康，天天开心！"""

    if request.args is None:
        res['code'] = '5004'
        res['info'] = '请求参数为空'
        return json.dumps(res, ensure_ascii=False)

    param = request.args.to_dict()
    # 获取用户输入的问题参数
    sent = param.get('sent')

    res_classify = classifier.classify(sent)
    if not res_classify:
        res['answer'] = answer
        return json.dumps(res, ensure_ascii=False)
        # return render_template('home.html')
    res_sql = parser.parser_main(res_classify)
    final_answers = searcher.search_main(res_sql)
    if not final_answers:
        return json.dumps(res, ensure_ascii=False)
    else:
        str = '\n'.join(final_answers)
        res['answer'] = str
        return json.dumps(res, ensure_ascii=False)


if __name__ == '__main__':
    server.config['JSON_AS_ASCII'] = False
    server.run(port=5001, debug=True)
