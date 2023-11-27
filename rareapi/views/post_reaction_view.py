from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import PostReaction, RareUser, Post, Reaction

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ['id', 'user_id', 'post_id', 'reaction_id']

class PostReactionView(ViewSet):
    def list(self, request):
        post_reactions = PostReaction.objects.all()
        serializer = PostReactionSerializer(post_reactions, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        user = RareUser.objects.get(pk=request.user.id)
        post = Post.objects.get(pk=request.data['post'])
        reaction = Reaction.objects.get(pk=request.data['reaction'])

        post_reaction = PostReaction.objects.create(
            user = user,
            post = post,
            reaction = reaction
            
        )
        post_reaction.save()

        try:
            serializer = PostReactionSerializer(post_reaction, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)  