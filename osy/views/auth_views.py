from flask import Blueprint, url_for, render_template, flash, request, session, g
# g는 어플리케이션 영역이 아닌 환경변수 쪽에서 실행됨.
# html을 감싸고 있는 거 app , app 감싸고 있는 게 flask라는 framework
# 요청했을 때 g라는 변수가 만들어지고 요청 끝나면 g사라져
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash 비밀번호를 암호화 시켜서 저장하기
# 비밀번호 암호화 되어있기 때문에 그냥 비교하면 안돼check_password_hash
from werkzeug.utils import redirect

from .. import db
from ..forms import UserCreateForm, UserLoginForm
from ..models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): #사용자가 입력한 데이터를 암호화한 다음 암호화된 데이터와 비교
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear() #flask server 내의 session / db.session과 달라
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


# 가장 먼저 실행됨!
@bp.before_app_request # 라우팅 함수보다 항상 먼저 실행됨
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view