import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from .conection import conexion
from IntiApp.serializersApi import general_serializer
    
class GeographyViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.GeographySerializer
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
            return Response({'message': 'Geography created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            geography_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if geography_serializer.is_valid():
                geography_serializer.save()
                return Response(geography_serializer.data, status= status.HTTP_200_OK)
            return Response(geography_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    def destroy(self, request, pk=None):
        geography = self.get_queryset().filter(id = pk).first()
        if geography:
            geography.delete()
            return Response({'message':'Geography removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Geography found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True)
    def activities(self, request, pk=None):
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "select an.id, an.activity_name, ai.id, g.name from activity_name an, version_name_index vni, activity_index ai, geography g where an.id=vni.activity_name_id and vni.activity_index_id=ai.id and ai.geography_id=g.id and g.id='"+pk+"'"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                #"activity name id": str(row[0]),
                "activity name": str(row[1]),
                "activity index id": str(row[2]),
                "geography name": str(row[3])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response({'response': d2})