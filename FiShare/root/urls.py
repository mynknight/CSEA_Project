from django.urls import path
from . import views
from .views import (PostListView,PostCreateView,PostDeleteView)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns =[
    path('',PostListView.as_view(),name='home'),
    path('my_files/',PostListView.as_view(),name='all_files'),
    path('my_files/new/',PostCreateView.as_view(template_name='root/add_file.html'),name='all_files_create'),
    path('my_files/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
