from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
from . import permissions
from . import search_functions


class HelloAPIView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """
        Returns a list of APIView features
        """
        an_apiview = [
            'Uses HTTP methods as function',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """
        Create a hello message with name
        """
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Updates an object
        """
        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """
        Updates only fields provided in request.
        """
        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """
        Deletes an object.
        """
        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """
    Test API ViewSet.
    """

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """
        Return a hello messages
        """
        a_viewset = [
            'Uses actions',
            'Automatically maps to URLs using routers',
            'Provides more functionality with less code'
        ]
        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """
        Create a new hello message
        """
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Handles getting an object by its ID.
        """
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """
        Updates an object
        """
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """
        Updates part of an object
        """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """
        Removes an object
        """
        return Response({'http_method': 'DELETE'})


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


class LoginViewSet(viewsets.ViewSet):
    """
    Checks email and password, returns an auth token
    """
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Use ObtainAuthToken APIView to validate and create token
        """
        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating profile feed items.
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


class SearchViewSet(viewsets.ViewSet):
    serializer_class = serializers.SearchSerializer
    #queryset = models.Search.objects.all()

    def create(self, request):
        """
        Handles lyrics search by artist name and song title
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
                return Response({'error':"Lyrics were not found \n" +str(e)})
            try:
                video_url = search_functions.find_video_url(artist, song_title)
            except Exception as e:
                return Response({'error':"Exception occurred when searching for video \n" +str(e)})

            return Response({"message": lyrics, "video": video_url})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LyricsCollectionViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating lyrics collections.
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.LyricsCollectionSerializer
    queryset = models.LyricsCollection.objects.all()
    permission_classes = (
        permissions.EditOwnLyrics , IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('song_title',)

    def perform_create(self, serializer):
        """
        Sets the user profile to the logged in user
        """
        serializer.save(user_profile=self.request.user)


class LyricsViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating lyrics instances.
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.LyricsSerializer
    queryset = models.Lyrics.objects.all()
    permission_classes = (
        permissions.EditOwnLyrics , IsAuthenticatedOrReadOnly)
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
        search_param = {}
        search_param['lyrics_collection'] = self.request.query_params.get('lyrics_collection', None)
        search_param['user_profile']  = self.request.query_params.get('user_profile', None)
        if search_param['lyrics_collection']  is not None:
            queryset = queryset.filter(lyrics_collection=search_param['lyrics_collection'])
        if search_param['user_profile']  is not None:
            queryset = queryset.filter(user_profile=search_param['user_profile'])
        return queryset

    # def get_serializer_class(self):
    #     user = self.request.user
    #
    #     import rest_framework
    #
    #     class LyricsSerializer(rest_framework.serializers.ModelSerializer):
    #         """
    #         Serializes lyrics collection inctance.
    #         """
    #         #user_profile =  serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    #
    #         lyrics_collection =  rest_framework.serializers.PrimaryKeyRelatedField(queryset=models.LyricsCollection.objects.filter(user_profile=user))
    #         class Meta:
    #             model = models.Lyrics
    #             fields = ('id', 'user_profile', 'artist', 'song_title', 'song_lyrics', 'lyrics_collection')
    #             extra_kwargs = {'user_profile': {'read_only': True}}
    #     return LyricsSerializer
