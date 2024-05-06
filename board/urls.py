from django.urls import path

from board.views import *

app_name = 'board'

urlpatterns = [
    path('', get_post_list),
    path('post/create/', post_post),
    path('post/detail/<int:post_id>/', get_post_detail),
    path('post/update/<int:post_id>/', update_post),
    path('post/delete/<int:post_id>/', delete_post),
    path('comment/create/<int:post_id>/', create_comment),
    path('comment/list/<int:post_id>/', get_comments)
]