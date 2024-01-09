import os  # 5일차 작성 내용
from django.db import models
from django.contrib.auth.models import User   # 6일차 작성
from markdownx.models import MarkdownxField    # 8일차 작성  / markdownx 외부라이브러리
from markdownx.utils import markdown      # 8일차 작성

# 7일차 작성 내용
class Tag(models.Model):       
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    # allow_unicode=True : 영어 이외에 한글도 유효하게 처리해주는 기능
    # # SlugField : URL에 사용되는 문자열을 저장하는 필드 /  ex) http://127.0.0.1:8000/blog/category/WEB/  맨뒤에 붙는 /WEB/이 Slug

    def __str__(self):         # 이름을 문자열로 가져올 수 있게 함.
        return self.name
    
    def get_absolute_url(self):        # slug를 사용하여 url을 가져오게 함.
        return f"/blog/category/{self.slug}/"    
    
    class Meta:       # Meta : 모델 클래스의 메타데이터를 정의하는 데 사용. 모델 클래스 자체와는 직접적인 관련이 없는, 모델의 특정 속성이나 동작을 제어하기 위한 용도로 활용.
        verbose_name_plural = "categories"     # 단수를 복수형태로 변경해주는 것.
    
class Post(models.Model):    # Post 모델 정의
    title = models.CharField(max_length=30)    # 문자의 최대 길이는 30자를 정의.
    hook_text = models.CharField(max_length=100, blank=True)     ## 5일차 작성 내용
    # content = models.TextField()    # TextField : text를 여러 줄 쓸수 있는 형태. django에서 정해준 함수이고 models에서 제공해줌.
    content = MarkdownxField()   # 8일차 작성  / Markdown 형식의 텍스트를 저장하는 필드입니다. 사용자가 긴 내용을 작성하고 서식을 지정할 수 있는 용도로 사용.
    
    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d", blank=True)    ## 5일차 작성 내용    / 경로 지정
    file_upload = models.FileField(upload_to="blog/files/%Y/%m/%d", blank=True)    ## 5일차 작성 내용    / 경로 지정

    created_at = models.DateTimeField(auto_now_add=True)    # auto_now_add: 생성 시간을 자동으로 저장.
    updated_at = models.DateTimeField(auto_now=True)    # auto_now: 수정 시간을 자동으로 저장.
    # 작성자가 삭제되면 작성자명을 빈칸으로 둔다.
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    # 6일차 작성 내용   / # 하나의 카테고리와 연결될 수 있으며, 해당 카테고리가 삭제되면 해당 인스턴스의 값을 null로 처리.
    # 외래키를 사용하여 user 값을 받음

    category = models.ForeignKey(    
        Category, null=True, blank=True, on_delete=models.SET_NULL)    # 6일차 작성 내용    /  on_dele0te=models.CASCADE로 변경시 유저 완전 삭제. 지금은 유저가 없어도 null값으로 처리되게 함.
    
    tags = models.ManyToManyField(Tag, blank=True)    # 7일차 작성 내용   / 다양한 tag들을 나타내는 model? 



    def __str__(self):    # 객체를 문자열로 표현할 때 사용 /  post의 객체를 반환
        return f'[{self.pk}]{self.title}'   # pk: 객체의 고유한 번호, title: 제목. 게시물의 기본키가 대괄호로
    def get_absolute_url(self):    # get_absolute_url : 메서드 정의
        return f'/blog/{self.pk}/'   # 게시물의 상세 페이지 주소를 반환
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)    ## 5일차 작성 내용

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]     ## 5일차 작성 내용
    
    def get_content_markdown(self):    # 8일차 작성  / content 속성 값을 Markdown으로 변환, Markdown 텍스트를 HTML로 변환
        return markdown(self.content)
    # 10일차 작성,  blog post에 대한 정보들
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    
    def get_absolute_url(self):    # url 만들어주는 함수 http://127.0.0.1:8000/blog/3/#comment-2http://127.0.0.1:8000/blog/3/#comment-2
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
                  
    

