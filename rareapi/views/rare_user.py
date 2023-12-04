from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser, Subscription
from rareapi.views.subscription_view import SubscriptionSerializer
from django.contrib.auth.models import User

# class RareUserSubscriptionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Subscription
#         fields = ['id', 'author_id', 'follower_id']

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
    created_on = serializers.SerializerMethodField()
    current_user_is_subscribed = serializers.SerializerMethodField()
    # subscriptions_as_followers = RareUserSubscriptionSerializer(many=True)
    
    def get_current_user_is_subscribed(self, obj):
        # Get the user id of the current user from the request
        current_user_id = self.context['request'].user.id

        # Get all the subscriptions of the current RareUser where it is an author
        rare_user_subscriptions_as_author = obj.subscriptions_as_author.values()

        # Loop through all subscriptions where RareUser is an author
        for subscription in rare_user_subscriptions_as_author:
            current_is_subscribed = False
            # Conditional to see if current user is subscribed to RareUser and if it is still current
            if subscription['follower_id'] == current_user_id and subscription['ended_on'] is None:
                return True
            
        return current_is_subscribed
   
    def get_created_on(self, obj):
        return f'{obj.created_on.month}/{obj.created_on.day}/{obj.created_on.year}'
    
    def get_image_avatar(self, obj):
        if obj.image_url:
            return obj.image_url
        return 'https://cdn1.iconfinder.com/data/icons/user-pictures/100/unknown-512.png'

    class Meta:
        model = RareUser
        fields = ['id', 'user', 'image_avatar',
                  'created_on', 'current_user_is_subscribed']


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
