from rest_framework import serializers

from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for getting user profile
    """
    username = serializers.ReadOnlyField(source='fetch_username')
    img_url = serializers.ReadOnlyField(source='fetch_image')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Profile
        fields = (
            'username', 'first_name', 'last_name', 'bio', 'img_url', 'created_at'
        )

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for updating user profile
    """
    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name', 'bio', 'image'
        )