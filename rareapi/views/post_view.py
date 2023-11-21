from django.http import HttpResponseServerError
from collections import Counter
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser, Reaction
from django.contrib.auth.models import User
from rareapi.views.reactions import ReactionSerializer
from datetime import datetime


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
        user_id = self.request.query_params.get('user')

        if user_id:
            # If user_id is provided, filter posts by user ID
            try:
                user_id = int(user_id)
                posts = Post.objects.filter(user__user__id=user_id)
            except ValueError:
                raise Http404("Invalid user ID provided.")
        else:
            # If no user_id provided, return all posts
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

