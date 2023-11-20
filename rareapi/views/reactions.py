from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Reaction

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['label', 'image_url']

class ReactionViewSet(viewsets.ViewSet):

    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)