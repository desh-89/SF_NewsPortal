from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('search/', SearchList.as_view()),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('update/<int:pk>',PostUpdate.as_view(), name='post_update'),
    path('category/<int:pk>', CategorySubscribe.as_view(), name = 'post_category'),
    path('subscribe/<int:pk>', subscribe_category, name = 'subscribe_category'),
    path('unsubscribe/<int:pk>', unsubscribe_category, name='unsubscribe_category')
]