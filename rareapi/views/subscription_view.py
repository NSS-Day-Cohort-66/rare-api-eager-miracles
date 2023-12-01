from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Subscription, RareUser
from rareapi.views.rare_user import RareUserSerializer


class SubscriptionSerializer(serializers.ModelSerializer):

    author = RareUserSerializer(many=False)
    follower = RareUserSerializer(many=False)

    class Meta:
        model = Subscription
        fields = ['id', 'author', 'follower', 'created_on', 'ended_on']


class SubscriptionViewSet(viewsets.ViewSet):

    def list(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(
                subscription, context={'request': request})
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        author_id = request.data.get('author')
        follower_id = request.data.get('follower')

        author = RareUser.objects.get(pk=author_id)
        follower = RareUser.objects.get(pk=follower_id)

        subscription = Subscription()
        subscription.author = author
        subscription.follower = follower
        subscription.created_on = request.data.get('created_on')
        subscription.ended_on = request.data.get('ended_on')
        subscription.save()

        try:
            serializer = SubscriptionSerializer(subscription, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
