from django.contrib import admin
from django.urls import path,include

from Pages import views as Pages
from API.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('staff/admin/panel/', admin.site.urls,name='admin_pannel'),
    path('',Pages.home_page,name='home_page'),
    path('posts/tagged/<str:tag>/',Pages.tag_page,name='tag_page'),
    path('posts/category/<str:category>/',Pages.catogory_page,name='category_page'),
    path('contact',Pages.contact_page,name='contact_page'),
    path('search/posts/<str:search_query>/',Pages.search_page,name='search_page'),
    path('view_blog/<slug:slug>',Pages.view_blog,name='view_blog'),
    path('auth/login',Pages.login_user,name='login'),
    path('auth/register',Pages.register_user,name='register'),
    path('auth/logout',Pages.logout_user,name='logout'),
    path('my-posts',Pages.my_posts,name='my_posts'),
    path('view/author/<str:username>/',Pages.staff_profile,name='staff_profile'),
    path('edit_profile',Pages.update_user,name='update_user'),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    
    path('api/home/get/trending',YouMayLikeAPI.as_view()),
    path('api/home/get/reccomended',RecommendedPostsAPI.as_view()),
    path('api/home/get/all_posts',AllBlogsAPI.as_view()),
    path('api/create/cookie-model/history',Pages.edit_history),
    path('api/get/query/',FilteredBlogsAPI.as_view()),
    path('api/get/comments',CommentAPI.as_view()),
    path('api/post/comment',post_comment),
    path('api/get/posts/my-uploads',MyPostsAPI.as_view()),
    path('api/blog/post/user/follow',follow_author),
    path('api/blog/post/user/unfollow',unfollow_user),
    path('api/blog/post/stars/like',like_post),
    path('api/blog/post/stars/unlike',unlike_post),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
