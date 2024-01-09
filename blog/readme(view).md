## Generic view
- 장고(Django)의 제네릭 뷰(Generic Views)는 일반적인 웹 개발 작업을 위한 미리 정의된 뷰 클래스들을 제공
- 제네릭 뷰를 사용하면 표준적인 CRUD(Create, Read, Update, Delete) 작업을 처리하는 데 필요한 코드 양을 크게 줄일 수 있다.

#### ListView
- 목적: 모델의 객체 목록을 표시하기 위한 뷰
- 특징: 지정된 모델의 모든 레코드(또는 쿼리셋을 통해 필터링된 레코드)를 가져와서 템플릿에 전달
- Django는 클래스 기반 뷰에 대한 기본 템플릿 이름을 자동으로 생성합니다. 이 이름은 {app_name}/{model_name}_list.html 형식을 따릅니다. 예를 들어, Book 모델을 가진 library 앱에 대한 ListView를 생성한다고 가정하면 library/templates/library/book_list.html

#### DetailView 
- 목적: 특정 객체의 상세 정보를 표시하기 위한 뷰. 특징: URL에서 전달된 키(보통 기본 키)를 기반으로 특정 모델 인스턴스를 검색하여 템플릿에 전달. 
- Book 모델에 대한 DetailView를 구현하면 book_detail.html 파일을 생성.
library/templates/library/book_detail.html

## 로그인

#### 라이브러리 설치 : pip install django-allauth
#### INSTALLED_APPS 추가
- "django.contrib.sites", # 사이트 관리
- "allauth", # allauth 앱
- "allauth.account", # 계정 관리
- "allauth.socialaccount", # 소셜 계정 관리
- "allauth.socialaccount.providers.google", # 구글 로그인

#### AUTHENTICATION_BACKENDS 설정
""" AUTHENTICATION_BACKENDS = [ # Needed to login by username in Django admin, regardless of allauth "django.contrib.auth.backends.ModelBackend", # allauth specific authentication methods, such as login by e-mail "allauth.account.auth_backends.AuthenticationBackend", ] """ SITE_ID = 2 # 사이트 아이디

- ACCOUNT_EMAIL_REQUIRED = True # 회원가입시 이메일 필수 
- ACCOUNT_EMAIL_VERIFICATION = "none" # 이메일 인증 필요없음 
- LOGIN_REDIRECT_URL = "/blog/" # 로그인 후 이동 페이지

#### 구글 개발자 콘솔
- 새 프로젝트와 클라이언트 만들기 - console.developers.google.com 에 접속
- 새 프로젝트 생성 > 만들기 > OAuth 동의화면 외부 선택 > 앱이름
- 사용자 인증 정보 > 사용자 인증 정보 만들기 > OAuth 클라이언트 ID > 만들기 (유형, 이름, URL, URI 입력)
- 승인된 자바스크립트 원본 : http://127.0.0.1:8000
- 승인된 리디렉션 URI : http://127.0.0.1:8000/accounts/google/login/callback/

#### navbar {% load socialaccount %}