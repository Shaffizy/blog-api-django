from django.urls import path
from .views import UserCreateView, PostListCreateView, PostDetailView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
