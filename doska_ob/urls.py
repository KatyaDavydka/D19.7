from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostList, PostDetail, PostSearch, PostDelete, PostCreate, PostUpdate, accept)

urlpatterns = [

   path('', PostList.as_view(), name='post'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('accept/<int:pk>', accept, name='accept'),
   path('reject/<int:pk>', accept, name='reject'),
]