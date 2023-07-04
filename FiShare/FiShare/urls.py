from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from users import views as users_view
from django.conf.urls.static import static
from django.conf import settings
from root.views import PostListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', users_view.register, name='register'),
    path('profile/', users_view.profile, name='profile'),
    path('all_users/', users_view.user_list, name='all_users'),
    path('all_users/<int:user_id>', PostListView.as_view(template_name='root/user_repo.html'),name='user_repo'),
    path('', include('root.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
