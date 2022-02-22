from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


from IntiApp.serializersApi import general_serializer

class ActivityNameViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.ActivityNameSerializer
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
            return Response({'message': 'Activity Name created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            activity_name_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if activity_name_serializer.is_valid():
                activity_name_serializer.save()
                return Response(activity_name_serializer.data, status= status.HTTP_200_OK)
            return Response(activity_name_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    
    def destroy(self, request, pk=None):
        activityName = self.get_queryset().filter(id = pk).first()
        if activityName:
            activityName.delete()
            return Response({'message':'Activity Name removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Activity Name found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
        