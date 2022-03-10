import json
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .conection import conexion
from rest_framework.views import APIView
from rest_framework.decorators import action

from IntiApp.serializersApi import general_serializer

class CorrespondenceViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.CorrespondenceSerializer
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['version','data_generator_and_publication']

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Correspondence created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            correspondence_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if correspondence_serializer.is_valid():
                correspondence_serializer.save()
                return Response(correspondence_serializer.data, status= status.HTTP_200_OK)
            return Response(correspondence_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    def destroy(self, request, pk=None):
        correspondence = self.get_queryset().filter(id = pk).first()
        if correspondence:
            correspondence.delete()
            return Response({'message':'Correspondence removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Correspondence found with this ID'}, status= status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def version(self, request):
        ai_id=request.GET.get('ai-id','') #activity_index_id=08550bca-a4c1-4373-890b-8ef2ceaae42c
        ie_name=request.GET.get('ie-name','') # ie.name='bagasse, from sugarcane'
        data = {}
        data = []
        select1_1 = ''
        cursor1 = conexion.cursor()
        select1 = "select c.activity_intermediate_exchange, c.next_activity_intermediate_exchange, a.activity_index_id from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+ai_id+"' and ie.name='"+ie_name+"';"
        cursor1.execute(select1)
        select1 = cursor1.fetchall()
        if len(select1)!=0:
            select1_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select1[0][1])+"';"
            cursor1.execute(select1_1)
            select1_1 = cursor1.fetchall()
            if len(select1_1)!=0:
                for row in select1:
                    data.append({
                        "aie_3_1": str(row[0]),
                        "aie_3_1 id": str(row[2]),
                        "aie_3_2": str(row[1]),
                        "aie_3_2 id": str(select1_1[0][1]),
                    })
        
        select2 = "select c.activity_intermediate_exchange aie_3_1, c.next_activity_intermediate_exchange aie_3_2 from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+select1_1[0][1]+"' and ie.name='"+select1_1[0][0]+"';"
        cursor1.execute(select2)
        select2 = cursor1.fetchall()
        if len(select2)!=0:
            select2_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select2[0][1])+"';"
            cursor1.execute(select2_1)
            select2_1 = cursor1.fetchall()
            if len(select2_1)!=0:
                for row in select2:
                    data.append({
                        "aie_3_3": str(row[1]),
                        "aie_3_3 id": str(select2_1[0][1]),
                    })
        
        select3 = "select c.activity_intermediate_exchange aie_3_1, c.next_activity_intermediate_exchange aie_3_2 from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+select2_1[0][1]+"' and ie.name='"+select2_1[0][0]+"';"
        cursor1.execute(select3)
        select3 = cursor1.fetchall()
        if len(select3)!=0:
            select3_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select3[0][1])+"';"
            cursor1.execute(select3_1)
            select3_1 = cursor1.fetchall()
            if len(select3_1)!=0:
                for row in select3:
                    data.append({
                        "aie_3_4": str(row[1]),
                        "aie_3_4 id": str(select3_1[0][1]),
                    })

        
        select4 = "select c.activity_intermediate_exchange aie_3_1, c.next_activity_intermediate_exchange aie_3_2 from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+select3_1[0][1]+"' and ie.name='"+select3_1[0][0]+"';"
        cursor1.execute(select4)
        select4 = cursor1.fetchall()
        if len(select4)!=0:
            select4_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select4[0][1])+"';"
            cursor1.execute(select4_1)
            select4_1 = cursor1.fetchall()
            if len(select4_1)!=0:
                for row in select4:
                    data.append({
                        "aie_3_5": str(row[1]),
                        "aie_3_5 id": str(select4_1[0][1]),
                    })

        select5 = "select c.activity_intermediate_exchange aie_3_1, c.next_activity_intermediate_exchange aie_3_2 from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+select4_1[0][1]+"' and ie.name='"+select4_1[0][0]+"';"
        cursor1.execute(select5)
        select5 = cursor1.fetchall()
        if len(select5)!=0:
            select5_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select5[0][1])+"';"
            cursor1.execute(select5_1)
            select5_1 = cursor1.fetchall()
            if len(select5_1)!=0:
                for row in select5:
                    data.append({
                        "aie_3_6": str(row[1]),
                        "aie_3_6 id": str(select5_1[0][1]),
                    })
        
        select6 = "select c.activity_intermediate_exchange aie_3_1, c.next_activity_intermediate_exchange aie_3_2 from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+select5_1[0][1]+"' and ie.name='"+select5_1[0][0]+"';"
        cursor1.execute(select6)
        select6 = cursor1.fetchall()
        if len(select6)!=0:
            select6_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select6[0][1])+"';"
            cursor1.execute(select6_1)
            select6_1 = cursor1.fetchall()
            if len(select6_1)!=0:
                for row in select6:
                    data.append({
                        "aie_3_7_1": str(row[1]),
                        "aie_3_7_1 id": str(select6_1[0][1]),
                    })

        select7 = "select c.activity_intermediate_exchange aie_3_1, c.next_activity_intermediate_exchange aie_3_2 from correspondence c, activity_intermediate_exchange aie, intermediate_exchange ie, activity a where ie.id=aie.intermediate_exchange_id and c.activity_intermediate_exchange=aie.id and aie.activity_id=a.id and a.activity_index_id='"+select6_1[0][1]+"' and ie.name='"+select6_1[0][0]+"';"
        cursor1.execute(select7)
        select7 = cursor1.fetchall()
        if len(select7)!=0:
            select7_1 = "select ie.name intermediate_exchange, a.activity_index_id from intermediate_exchange ie, activity_intermediate_exchange aie , activity a where a.id=aie.activity_id and aie.intermediate_exchange_id=ie.id and aie.id='"+str(select7[0][1])+"';"
            cursor1.execute(select7_1)
            select7_1 = cursor1.fetchall()
            if len(select7_1)!=0:
                for row in select6:
                    data.append({
                        "aie_3_8": str(row[1]),
                        "aie_3_8 id": str(select7_1[0][1]),
                    })

        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(data) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)
            