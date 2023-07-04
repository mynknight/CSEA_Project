from django.urls import path
from .views import (PostCreateView,download_file,
                    PostDeleteView,create_folder,
                    MyFileFolderView)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns =[
    path('',MyFileFolderView.as_view(),name='home'),
    path('my_files/',MyFileFolderView.as_view(),name='all_files'),
    path('my_files/new/',PostCreateView.as_view(template_name='root/add_file.html'),name='all_files_create'),
    path('my_files/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_file'),
    path('my_files/folder/create', create_folder,name='create_folder'),
    path('my_files/folder/create/<int:parent_folder_id>/',PostCreateView.as_view(template_name='root/add_file.html'),name='create_file_in_folder'),
    path('my_files/folder/create/folder/<int:parent_folder_id>/',create_folder,name='create_folder_in_folder'),
    path('my_files/<int:parent_folder_id>/',MyFileFolderView.as_view(template_name='root/subfolder.html'),name='subfolder'),
    path('download/<str:file_path>/', download_file, name='download_file'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
