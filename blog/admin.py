from django.contrib import admin
from .models import Post, Category, Tag, Comment #Post 모델을 불러옴

admin.site.register(Post) # Post 모델을 관리자 페이지에서 볼 수 잇도록 등록

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}      #  웹admin - ADD category - Name생성시 Slug에도 같은 이름으로 생성하게 해주는 기능.
    
admin.site.register(Category, CategoryAdmin)      # admin에서 Category, CategoryAdmin 을 관리함.

class TagAdmin(admin.ModelAdmin):     # 7일차 작성
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag, TagAdmin)    # 7일차 작성



