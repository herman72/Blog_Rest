from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as vw

from BlogApi import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('register', views.Register.as_view(), name='Register'),
    path('users', views.UserList.as_view(), name='users'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='userDetail'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('posts/<int:pk>/comment', views.AddComment.as_view(), name='comment'),
    path('users/<int:pk>/followingList', views.FollowerList.as_view(), name='FollowingList'),
    path('api-token-auth/', vw.obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)
