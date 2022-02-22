from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend



from IntiApp.serializersApi import general_serializer

class ActivityIntermediateExchangeViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.ActivityIntermediateExchangeSerializer
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['activity',]


    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(output_group = 0)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Activity Intermediate Exchange created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            activityIntermediateExchange_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if activityIntermediateExchange_serializer.is_valid():
                activityIntermediateExchange_serializer.save()
                return Response(activityIntermediateExchange_serializer.data, status= status.HTTP_200_OK)
            return Response(activityIntermediateExchange_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    
    def destroy(self, request, pk=None):
        activityIntermediateExchange = self.get_queryset().filter(id = pk).first()
        if activityIntermediateExchange:
            activityIntermediateExchange.delete()
            return Response({'message':'Activity Intermediate Exchange removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Activity Intermediate Exchange found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
        