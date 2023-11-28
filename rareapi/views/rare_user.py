from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser
from django.contrib.auth.models import User

class RareUserUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    user_profile_type = serializers.SerializerMethodField()

    def get_user_profile_type(self, obj):
        if obj.is_staff:
            return 'admin'
        return 'author'

    class Meta:
        model = User
        fields = ['full_name', 'email', 'user_profile_type', 'date_joined']

class RareUserSerializer(serializers.ModelSerializer):
    user = RareUserUserSerializer(many=False)
    image_avatar = serializers.SerializerMethodField()

    def get_image_avatar(self, obj):
        if obj.image_url:
            return obj.image_url
        return 'https://cdn1.iconfinder.com/data/icons/user-pictures/100/unknown-512.png'
    
    class Meta:
        model = RareUser
        fields = ['id', 'user', 'image_avatar']


class RareUserView(ViewSet):

    def list(self, request):
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(rare_users, many=True, context={'request': request})
        return Response(serializer.data)