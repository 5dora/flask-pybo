# 현재 내 폴더 구조를 꺼내기 위해
import os

BASE_DIR = os.path.dirname(__file__)
# 내파일에 대한 경로

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'osy.db'))
# URI 주로 로컬쪽에서 쓰는 객체 / URL은 웹쪽에서
# pybo.db myproject에 만들어져
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 이벤트 처리에 관련된 옵션

SECRET_KEY = "dev"