from collections import Counter
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser, Reaction
from django.contrib.auth.models import User
from rareapi.views.reactions import ReactionSerializer


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PostRareUserSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(many=False)  # Include the UserSerializer here

    class Meta:
        model = User
        fields = ['id', 'user']  # Include the 'user' field from UserSerializer


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['label']


class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    category = PostCategorySerializer(many=False)
    reactions = ReactionSerializer(many=True)
    reactions_count = serializers.SerializerMethodField()

    def get_reactions_count(self, obj):
        # Count the occurrences of each reaction for the post
        reaction_counts = Counter(reaction['id']
                                  for reaction in obj.reactions.values())

        # Get the IDs of all reactions
        all_reaction_ids = Reaction.objects.values_list('id', flat=True)

        # Create a list of dictionaries for each reaction with or 0 if not present
        reactions_list = [{'id': reaction_id, 'count': reaction_counts[reaction_id]}
                          for reaction_id in all_reaction_ids]
        return reactions_list

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content',
                  'image_url', 'category', 'pub_date', 'approved', 'reactions', 'reactions_count']


class PostView(ViewSet):

    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        # Get the query parameter 'user' from the request
        user_param = request.query_params.get('user')

        if user_param == 'current':
            # If user_param is 'current', filter posts by the current user ID
            try:
                user_id = request.user.id
                posts = Post.objects.filter(user__user__id=user_id)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # If no 'user' parameter or 'user' is not 'current', return all posts
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):

        category = Category.objects.get(pk=request.data["category"])
        rareuser = RareUser.objects.get(pk=request.user.id)
        post = Post()
        post.user = rareuser
        post.category = category
        post.title = request.data.get('title')
        # post.pub_date = request.data.get('pub_date')
        post.image_url = request.data.get('image_url')
        post.content = request.data.get('content')
        # post.approved = request.data.get('approved')
        post.save()

        try:
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
