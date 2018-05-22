from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, generics, filters, permissions as prm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from . import models
from . import permissions
from . import search_functions


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating profiles.
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet, generics.GenericAPIView):
    """
    Log in using your username and password.

    **returns:** Token.
    """
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Use ObtainAuthToken APIView to validate and create token
        """
        return ObtainAuthToken().post(request)


class LogoutViewSet(viewsets.ViewSet):
    """
    Log out.
    """
    authentication_classes = (TokenAuthentication,)
    queryset = models.UserProfile.objects.all()
    permission_classes = (IsAuthenticated, )

    def create(self, request, format=None):
        """
        Log out.
        Operation deletes login token.
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of all saved users statuses.

    create:
    Save new status. 
    Authentication required.

    read:
    Get user status by id.

    update:
    Update user status. 
    Authentication required.

    partial_update:
    Partial update of user status. 
    Authentication required.

    delete:
    Delete user status. 
    Authentication required.
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """
        Sets the user profile to the logged in user
        """
        serializer.save(user_profile=self.request.user)


class SearchViewSet(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = serializers.SearchSerializer
    #queryset = models.Search.objects.all()

    def create(self, request):
        """
        Search lyrics by artist name and song title.

        **returns:** Song lyrics and video link.
        """
        #search_text = models.Search
        #resp = search_text.search(str(request))
        serializer = serializers.SearchSerializer(data=request.data)
        if serializer.is_valid():
            artist = serializer.data.get('artist')
            song_title = serializer.data.get('song_title')
            try:
                lyrics = search_functions.find_lyrics(artist, song_title)
            except Exception as e:
                lyrics = "Lyrics were not found \n" +str(e)
                #return Response({'error':"Lyrics were not found \n" +str(e)})
            try:
                video_url = search_functions.find_video_url(artist, song_title)
            except Exception as e:
                video_url = "Exception occurred when searching for video \n" +str(e)
                #return Response({'error':"Exception occurred when searching for video \n" +str(e)})

            return Response({"message": lyrics, "video": video_url})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LyricsCollectionViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    """
    list:
    Returns a list of all saved lyrics collections.

    create:
    Save new lyrics collection. 
    Authentication required.

    read:
    Get collection by id.

    update:
    Update existing collection. 
    Authentication required.

    partial_update:
    Partial update of existing collection. 
    Authentication required.

    delete:
    Delete existing collection. 
    Authentication required.
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.LyricsCollectionSerializer
    queryset = models.LyricsCollection.objects.all()
    permission_classes = (
        permissions.EditOwnLyrics, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('song_title',)

    def perform_create(self, serializer):
        """
        Sets the user profile to the logged in user
        """
        serializer.save(user_profile=self.request.user)


class LyricsViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    """
    list:
    Returns a list of all saved lyrics.

    create:
    Save new lyrics. 
    Authentication required.

    read:
    Get song lyrics by id.

    update:
    Update existing lyrics. 
    Authentication required.

    partial_update:
    Partial update of existing lyrics. 
    Authentication required.

    delete:
    Delete existing lyrics. 
    Authentication required.
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.LyricsSerializer
    queryset = models.Lyrics.objects.all()
    permission_classes = (
        permissions.EditOwnLyrics, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('song_title', )

    def perform_create(self, serializer):
        """
        Saves lyrics inctance
        """
        serializer.save(user_profile=self.request.user)

    def get_queryset(self):
        """
        Allows to filter lyrics by user that posted them and by collection they were put into
        """
        user = self.request.user

        queryset = models.Lyrics.objects.all()
        search_param = dict()
        search_param['lyrics_collection'] = self.request.query_params.get('lyrics_collection', None)
        search_param['user_profile']  = self.request.query_params.get('user_profile', None)
        if search_param['lyrics_collection']  is not None:
            queryset = queryset.filter(lyrics_collection=search_param['lyrics_collection'])
        if search_param['user_profile']  is not None:
            queryset = queryset.filter(user_profile=search_param['user_profile'])
        return queryset
