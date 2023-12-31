from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'label']


class TagViewSet(viewsets.ViewSet):

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        #get data from JSON payload
        label = request.data.get('label')
        
        tag = Tag.objects.create(
            label=label
        )
        
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            self.check_object_permissions(request, tag)
            tag.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(data=request.data)
            if serializer.is_valid():
                tag.label = serializer.validated_data['label']
                tag.save()
                
                serializer = TagSerializer(tag, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
