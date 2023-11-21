from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser, PostTag
from django.contrib.auth.models import User


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PostRareUserSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(many=False)  # Include the UserSerializer here

    class Meta:
        model = RareUser
        fields = ['id', 'user']  # Include the 'user' field from UserSerializer


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    category = PostCategorySerializer(many=False)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content',
                  'image_url', 'category', 'pub_date', 'approved']


class PostView(ViewSet):

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):

        title = request.data.get('title')
        pub_date = request.data.get('pub_date')
        image_url = request.data.get('image_url')
        content = request.data.get('content')
        approved = request.data.get('approved')

        post = Post.objects.create(
            title=title,
            pub_date=pub_date,
            image_url=image_url,
            content=content,
            approved=approved
        )

        try:
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
