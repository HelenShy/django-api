from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('feed', views.UserProfileFeedViewSet)
router.register('search', views.SearchViewSet, base_name='search')
router.register('lyrics-collection', views.LyricsCollectionViewSet)
router.register('lyrics', views.LyricsViewSet)
#router.register('lyrics', views.LyricsViewSet, base_name='lyrics-viewset')


urlpatterns = [
    url(r'^hello-view/', views.HelloAPIView.as_view()),
    url(r'', include(router.urls))
]
