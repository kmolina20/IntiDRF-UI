from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from IntiApp.serializersApi import general_serializer
    
class VersionViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.VersionSerializer
    authentication_classes = (TokenAuthentication,)
    #version
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['version',]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()
            
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Version created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            version_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if version_serializer.is_valid():
                version_serializer.save()
                return Response(version_serializer.data, status= status.HTTP_200_OK)
            return Response(version_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    
    def destroy(self, request, pk=None):
        version = self.get_queryset().filter(id = pk).first()
        if version:
            version.delete()
            return Response({'message':'Version removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Version found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
        