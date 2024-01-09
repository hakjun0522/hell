# from typing import Any
# from django.http import HttpRequest
# from django.http.response import HttpResponse
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect   # redirect 8일차 작성  / 조건이 안맞으면 다시 돌아가라는 뜻.
from .models import Post, Category, Tag, Comment  # Comment 10일차 추가 작성
from django.views.generic import ListView, DetailView, CreateView, UpdateView   # 장고 generic에서  import 한다는 뜻.  / # CreateView, UpdateView 8일차 작성
from django.utils.text import slugify   # 8일차 작성   / slugify 함수는 문자열을 URL에 적합한 형태로 변환
from django.shortcuts import get_object_or_404   # 8일차 작성     # 해당 객체가 존재하지 않을 경우 404 오류 페이지를 반환
from django.core.exceptions import PermissionDenied   # 8일차 작성  /# 권한이 없는 경우 파일 쓰기 시도 시 거부되었을때 나오는 오류
from django.db.models import Q   # 8일차 작성  /  # db에서 데이터를 검색, 필터링 할 때, 다양한 조건을 조합하고 동적으로 쿼리를 작성하는 상황에서 유용 , Q 객체는 filter() 메서드와 함께 사용됨.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   # 8일차 작성
# from django.views.generic.edit import CreateView, UpdateView   # 8일차 작성
from .forms import CommentForm   # 10일차 작성



# CBV: Class Based View
class PostList(ListView):
    model = Post
    ordering = "-pk"      # 역순 정렬 넣어줘야함.
    paginate_by = 5     # 10일차 작성

    def get_context_data(self, **kwargs):    # 6일차 작성
        context = super(PostList, self).get_context_data()    # 부모 클래스 super 의 get_context_data() 호출
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        return context
    
class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()    # 10일차 생성 
        return context
    

# 8일차 작성
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):   # form_valid 메서드는 폼 데이터가 유효할 때 호출되는 메서드
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)   # 사용자로부터 제출된 폼이 유효한지 여부를 확인하고, 유효할 경우에는 해당 데이터를 저장하거나 추가적인 처리를 수행하는 역할

            tags_str = self.request.POST.get("tags_str")   # tags_str은 태그를 입력하는 폼에서 전달받은 데이터

            if tags_str:
                tags_str = tags_str.strip()  # strip:좌우 공백처리

                tags_str = tags_str.replace(",", ";")   # ,은 db에서 사용되는 구분자이어서 오해의 문제가 될 수 있음.
                tags_list = tags_str.split(";")

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)

                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
            
        else:
            return redirect("/blog/")
# 9일차 작성
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "hook_text", "content", "head_image", "file_upload", "category"]

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context
    
    def dispatch(self, request, *args, **kwargs):  # 부모 클래스의 dispatch 메서드를 호출
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',',';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

            return response
# slug는 일반적으로 이미 얻은 데이터를 사용하여 유효한 url을 생성하는 방법
def category_page(request, slug):    
    if slug == "no_category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(            # 렌더링 시 아래 해당 카테고리로 들어감.
        request,
        "blog/post_list.html",      # 아래 내용을 "blog/post_list.html" 으로 처리한다.
        {
            "post_list": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category,   # 현재 선택된 카테고리
        },
    )
# 7일차 작성 - import tag 추가
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)     # 해당 슬러그와 일치하는 Tag 객체를 가져옴
    post_list = tag.post_set.all()     # tag에 속한 모든 post 객체를 가져옴

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,     # 게시물 목록을 템플릿에 전달하여 해당 태그에 속한 게시물만 출력
            'tag': tag,      # 현재 선택된 태그
            'categories': Category.objects.all(),    # 모든 카테고리 정보를 가져와 템플릿에 전달
            'no_category_post_count': Post.objects.filter(Category=None).count(),
        }
    )

# 10일차 작성
def new_comment(request, pk):     #  comment 작성시 주소에 http://127.0.0.1:8000/blog/3/#comment-3 뒤에 #comment-3 가 생성 
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)    # pk에 해당하는 Post 객체를 가져옴.

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)    # CommentForm(request.POST)를 사용하여 제출된 데이터로 댓글 폼의 인스턴스를 생성
            if comment_form.is_valid():    # 폼의 데이터가 유효한지 검사
                comment = comment_form.save(commit=False)    # comment_form.save(commit=False)를 사용하여 Comment 객체를 생성하되, 데이터베이스에는 저장하지 않음
                comment.post = post    # 댓글 객체에 post 속성을 할당
                comment.author = request.user    # 댓글 객체에 author 속성을 할당
                comment.save()
                return redirect(comment.get_absolute_url())    # 댓글 객체의 get_absolute_url 메서드를 호출하여 댓글 상세 페이지로 이동
        else:
            return redirect(post.get_absolute_url())   # 댓글 폼이 유효하지 않으면 post.get_absolute_url()로 이동
    else:
        raise PermissionDenied   # 로그인하지 않은 사용자가 댓글을 작성하려고 하면 PermissionDenied 예외를 발생시킴
    
class CommentUpdate(LoginRequiredMixin, UpdateView):  # CommentUpdate 클래스는 LoginRequiredMixin을 상속받는다.
    model = Comment   # Comment 모델을 사용
    form_class = CommentForm   # 사용할 폼으로 CommentForm을 지정

    def dispatch(self, request, *args, **kwargs): 
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)    # 부모 클래스의 dispatch 메서드를 호출
        else:
            raise PermissionDenied          # 권한이 없으면 허가 거부
        
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    
# 10일차 작성
class PostSearch(PostList):
    paginate_by = None
    
    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context

# 처음에 적었던 내용
# # FBS: Fuction Based View
# def index(request):
#     posts = Post.objects.all().order_by('-pk')    # 모든 post 객체를 가져와서 pk 역순으로 정렬  / post는 .models에서 가져 옴.

#     return render(    # render 함수는 세 번째 인수로 전달된 딕셔너리 데이터를 템플릿 파일에 적용하여 HTML 코드로 변환.
#         request,    # 첫 번째 인수는 반드시 request
#         'blog/index.html',    # 두 번째 인수는 템플릿 파일의 경로
#         {
#             'posts':posts,    # posts 키에 posts 변수를 할당
#         }
#     )

# def single_post_page(request, pk):    # pk는 URL에서 추출한 게시물의 고유 번호
#     post = Post.objects.get(pk=pk)    # pk가 매개변수 pk와 같은 Post 객체를 post 변수에 할당

#     return render(
#         request,
#         'blog/single_post_page.html',    # 템플릿 파일의 경로
#         {
#             'post': post,
#         }
#     )
