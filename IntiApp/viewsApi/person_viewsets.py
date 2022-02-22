from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .conection import conexion
from rest_framework.views import APIView
from rest_framework.decorators import action

from IntiApp.serializersApi import general_serializer
from IntiApp.authentication_mixins import Authentication

#class PersonViewSet(Authentication, viewsets.ModelViewSet):
class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.PersonSerializer
    
    #permission_classes = (IsAuthenticated,) 
    #authentication_classes = (TokenAuthentication,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    '''
    def list(self, request):
        person_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(person_serializer.data, status = status.HTTP_200_OK)
    '''
    '''
    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            person_serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(person_serializer.data)
        
        person_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(person_serializer.data, status= status.HTTP_200_OK)
    '''

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Person created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            person_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if person_serializer.is_valid():
                person_serializer.save()
                return Response(person_serializer.data, status= status.HTTP_200_OK)
            return Response(person_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    def destroy(self, request, pk=None):
        person = self.get_queryset().filter(id = pk).first()
        if person:
            person.delete()
            return Response({'message':'Person removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Person found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True)
    def activities(self, request, pk=None):
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "SELECT p.name, an.id, an.activity_name ai.id FROM activity_index ai, version_name_index vni, activity_name an, activity a, person p, activity_person ap WHERE a.activity_index_id=ai.id AND vni.activity_index_id=ai.id AND an.id=vni.activity_name_id AND ap.activity_id=a.id AND ap.person_id=p.id AND p.id='"+pk+"' GROUP BY ai.id, an.id, p.id"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "person name": str(row[0]),
                #"activity name id": str(row[1]),
                "activity name": str(row[2]),
                "activity index id": str(row[3])
            })
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response({'response': data})