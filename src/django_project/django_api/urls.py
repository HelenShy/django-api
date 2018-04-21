from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('logout', views.LogoutViewSet, base_name='logout')
router.register('feed', views.UserProfileFeedViewSet)
router.register('search', views.SearchViewSet, base_name='search')
router.register('lyrics-collection', views.LyricsCollectionViewSet)
router.register('lyrics', views.LyricsViewSet)


urlpatterns = [
    url(r'', include(router.urls))
]
