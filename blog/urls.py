from django.urls import path
from . import views

urlpatterns = [
    # path('<int:pk>/', views.single_post_page),   # pk가 정수형임을 명시
    # path('', views.index),   # 블로그 메인 페이지
    # path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    # path('create_post/', views.PostCreate.as_view()),
    path("<int:pk>/", views.PostDetail.as_view()),
    path("", views.PostList.as_view()),
    path("category/<str:slug>/", views.category_page),    # 6일차 작성  / 카테고리의 값을 str:slug으로 받는다.
    path('tag/<str:slug>/',views.tag_page),   
    path("create_post/", views.PostCreate.as_view()),    # 8일차 작성
    path("update_post/<int:pk>/", views.PostUpdate.as_view()),    # 9일차 작성   / new post와 edit post를 만들기 위해 작업
    path("<int:pk>/new_comment/", views.new_comment),    # 10일차 작성
    path("update_comment/<int:pk>/", views.CommentUpdate.as_view()),   # 10일차 작성
    path("delete_comment/<int:pk>/", views.delete_comment),    # 10일차 작성
    path('search/<str:q>/', views.PostSearch.as_view()),    # 10일차 작성
]