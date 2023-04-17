from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
# html 내부에 파이썬 코드가 있으면 결과값을 실행시켜서 브라우저로 쏴주기 위해 render_template

from ..models import Question

bp = Blueprint('main', __name__, url_prefix='/')
# 블루프린트에 대한 구별 이름(별칭) , __name__(파이썬에서 제공해주는 이름 수정불가!!), url에 대한 기본경로
# __name__ 에 모듈명인 main_views가 전달(하나의 파일이 모듈이야)


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('question._list'))
    # _list 함수명을 가지고 url_for 함수를 통해 url 뽑아내 redirect 함수를 통해 url로 넘어가기


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)