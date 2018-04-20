from rest_framework import serializers

from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializes user profile objects.
    """

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create new user
        """
        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """
    Serializes user profile feed items.
    """

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


class SearchSerializer(serializers.Serializer):
    """
    Serializes search object.
    """
    artist = serializers.CharField(max_length=255)
    song_title = serializers.CharField(max_length=255)


class LyricsSerializer(serializers.ModelSerializer):
    """
    Serializes lyrics inctance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', None)
        if context:
            request = kwargs['context']['request']
            self.fields['lyrics_collection'] = serializers.PrimaryKeyRelatedField(
                queryset=models.LyricsCollection.objects.filter(
                    user_profile=self.context['request'].user))

    class Meta:
        model = models.Lyrics
        fields = ('id', 'user_profile', 'artist', 'song_title',
                  'song_lyrics', 'lyrics_collection', 'public', 'video_url')
        extra_kwargs = {'user_profile': {'read_only': True}}


class LyricsCollectionSerializer(serializers.ModelSerializer):
    """
    Serializes lyrics collection inctance.
    """
    lyrics_list = LyricsSerializer(read_only=True, many=True)
    class Meta:
        model = models.LyricsCollection
        fields = ('id', 'user_profile', 'title', 'lyrics_list')
        extra_kwargs = {'user_profile': {'read_only': True}}

    # def create(self, validated_data):
    #     """
    #     Create new lyrics collection
    #     """
    #     lyrics_collection = models.LyricsCollection(
    #         user_profile=validated_data['user_profile'],
    #         title=validated_data['title'],
    #         lyrics_list=validated_data['lyrics_list']
    #     )
    #
    #     lyrics_collection.save()
    #
    #     return lyrics_collection
