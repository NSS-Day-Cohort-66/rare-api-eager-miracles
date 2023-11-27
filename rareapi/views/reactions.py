from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Reaction

class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ['id', 'label', 'image_url']

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
        
    def create(self, request):
        label = request.data.get('label')
        image_url = request.data.get('image_url')

        reaction = Reaction.objects.create(
            label=label,
            image_url=image_url
        )

        serializer = ReactionSerializer(reaction, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)

            serializer = ReactionSerializer(data=request.data)
            if serializer.is_valid():
                reaction.label = serializer.validated_data['label']
                reaction.image_url = serializer.validated_data['image_url']
                reaction.save()

                serializer = ReactionSerializer(reaction, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Reaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)