from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, MeView, FolderViewSet, FileViewSet, login_view, logout_view

router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', login_view),
    path('auth/logout/', logout_view),
    path('auth/me/', MeView.as_view()),
    path('files/<int:pk>/download/', FileViewSet.as_view({'get': 'download'})),
    path('', include(router.urls)),
]
