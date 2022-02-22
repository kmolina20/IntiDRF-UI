from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


from IntiApp.serializersApi import general_serializer
    
class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.UnitSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Unit created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            unit_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if unit_serializer.is_valid():
                unit_serializer.save()
                return Response(unit_serializer.data, status= status.HTTP_200_OK)
            return Response(unit_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    
    def destroy(self, request, pk=None):
        unit = self.get_queryset().filter(id = pk).first()
        if unit:
            unit.delete()
            return Response({'message':'Unit removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Unit found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
        