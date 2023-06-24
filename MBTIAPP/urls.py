from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'MBTIAPP'

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(template_name='MBTIAPP/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mbtitest/', views.mbtitest, name='mbtitest'),
    path('result/', views.result, name='result'),
    path('blog/', views.blog, name='blog'),
    path('new/', views.new, name='new'),
    #path('postcreate/', views.postcreate, name='postcreate'),
    path('postcreate/', views.PostCreateView.as_view(), name='postcreate'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comment/<int:comment_pk>/edit/', views.comment_edit, name='comment_edit'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile-detail'),
    path('blog/<int:category_id>/posts/', views.CategoryClass.as_view(), name='category_posts_api'),
    path('profile/posts/', views.PersonalPost.as_view(), name='personal_posts_api'),
    path('profile/comments/', views.PersonalComment.as_view(), name='personal_comments_api'),
    path('profile/posts/<int:profile_id>/', views.PeoplePost.as_view(), name='people_posts_api'),

    
]
