from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser, Subscription
from django.contrib.auth.models import User


class RareUserSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['id', 'author_id', 'follower_id', 'created_on']


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
    subscriptions_as_author = RareUserSubscriptionSerializer(
        many=True, read_only=True)
    subscriptions_as_follower = RareUserSubscriptionSerializer(
        many=True, read_only=True)

    def get_image_avatar(self, obj):
        if obj.image_url:
            return obj.image_url
        return 'https://cdn1.iconfinder.com/data/icons/user-pictures/100/unknown-512.png'

    class Meta:
        model = RareUser
        fields = ['id', 'user', 'image_avatar',
                  'subscriptions_as_author', 'subscriptions_as_follower']


class RareUserView(ViewSet):

    def list(self, request):
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(
            rare_users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            rare_user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(
                rare_user, context={'request': request})
            return Response(serializer.data)
        except RareUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
