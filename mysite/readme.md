username:admin
password:admin

# django_class 폴더 생성
# 가상황경을 생성
- W(window) : Python -m venv myenv
- L(linux) : Python -m venv myenv
# 생성된 가상환경을 활성화
- W: myenv\Scripts\activate
- L: source myenv\bin\activate
# requirements.txt 생성 및 설치
- pip install -r requirements.txt
# 장고 프로젝트 생성
- django-admin startproject mysite .


# db 생성
- python manage.py migrate

# 관리자 계정 생성
- python manage.py createsuperuser

# 서버 실행
- python manage.py runserver
# 앱 생성
- python manage.py startapp blog
- python manage.py startapp single_pages
- settings.py에 blog 앱과 single_pages 앱 등록
# URLConf
- "URL Configuration"의 약어로, 웹 애플리케이션의 URL 패턴을 정의하고 관리하는데 사용되는 중요한 구성 요소

8. 블로그 앱 생성 : terminal - terminal - python manage.py startapp blog

9. about_me 앱 생성: terminal - python manage.py startapp about_me

10. single_pages 앱 생성: terminal - python manage.py startapp single_pages

11. 생성 후 등록 : settings.py - INSTALLED_APPS = 맨 아래
    'blog',
    'about_me',
    'single_pages',   입력 후 저장.

12. mysite - urls.py - urlpatterns - path 추가 - path('', include("single_pages.urls")), 입력 -

13. single_pages - urls.py 생성 - 후 내용 입력 - views.py - 내용 입력 - single_pages - 템플릿생성 - single_pages에 새로운 폴더 생성 templates/single_pages - landing.html 생성 - ! 작성 - python manage.py runserver