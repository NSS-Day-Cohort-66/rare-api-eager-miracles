from django.http import HttpResponseServerError
from collections import Counter
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser, Reaction
from django.contrib.auth.models import User
<<<<<<< HEAD
=======
from rareapi.views.reactions import ReactionSerializer
from datetime import datetime
>>>>>>> main


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
    reactions = ReactionSerializer(many=True)
    reactions_count = serializers.SerializerMethodField()
   
    def get_reactions_count(self, obj):
        # Count the occurrences of each reaction for the post
        reaction_counts = Counter(reaction['id'] for reaction in obj.reactions.values())

        # Get the IDs of all reactions
        all_reaction_ids = Reaction.objects.values_list('id', flat=True)

        # Create a list of dictionaries for each reaction with or 0 if not present
        reactions_list = [{'id' : reaction_id, 'count': reaction_counts[reaction_id]} for reaction_id in all_reaction_ids]
        return reactions_list    
       

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content',
                  'image_url', 'category', 'pub_date', 'approved', 'reactions', 'reactions_count']


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

        category = Category.objects.get(pk=request.data["category"])
        user = RareUser.objects.get(pk=request.data["rareuser"])

        post = Post()
        post.user = user
        post.category = category
        post.title = request.data.get('title')
        post.pub_date = request.data.get('pub_date')
        post.image_url = request.data.get('image_url')
        post.content = request.data.get('content')
        post.approved = request.data.get('approved')
        post.save()

        try:
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
