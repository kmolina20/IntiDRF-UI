import json

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.decorators import action

from .conection import conexion


from IntiApp.serializersApi import general_serializer

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.ActivitySerializer
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
            return Response({'message': 'Activity created successfully'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            activity_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if activity_serializer.is_valid():
                activity_serializer.save()
                return Response(activity_serializer.data, status= status.HTTP_200_OK)
            return Response(activity_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
   
    def destroy(self, request, pk=None):
        activity = self.get_queryset().filter(id = pk).first()
        if activity:
            activity.delete()
            return Response({'message':'Activity removed successfully'}, status= status.HTTP_200_OK) 
        return Response({'message':'No Activity found with this ID'}, status= status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True)
    def people(self, request, pk=None):
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "SELECT an.id, an.activity_name, ai.id, p.id, p.name FROM activity_index ai, version_name_index vni, activity_name an, activity a, person p, activity_person ap WHERE a.activity_index_id=ai.id AND vni.activity_index_id=ai.id AND an.id=vni.activity_name_id AND ap.activity_id=a.id AND ap.person_id=p.id AND a.id='"+pk+"' GROUP BY ai.id, an.id, p.id;"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                #"activity name id": str(row[0]),
                "activity name": str(row[1]),
                "activity index id": str(row[2]),
                "person id": str(row[3]),
                "person name": str(row[4])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)

    @action(detail=True)
    def references(self, request, pk=None):
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "SELECT aie.id, ie.id, ie.name from activity_intermediate_exchange aie, intermediate_exchange ie WHERE ie.id=aie.intermediate_exchange_id and aie.activity_id = '"+pk+"' AND aie.output_group = '0'"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "activity intermediate exchange id": str(row[0]),
                "intermediate exchange id": str(row[1]),
                "intermediate exchange name": str(row[2])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)
    
    @action(detail=True)
    def flows(self, request, pk=None):
        v_id = request.GET.get('version', '') # version = ecoinvent 3.6 cut off
        data = {}
        data = []
        cursor1 = conexion.cursor()
        if len(v_id)==0:
            select = "SELECT IE.ID, IE.NAME, v.version, an.id, an.ACTIVITY_NAME, ai.id FROM ACTIVITY_INTERMEDIATE_EXCHANGE AIE, INTERMEDIATE_EXCHANGE IE, ACTIVITY A, ACTIVITY_NAME AN, VERSION_NAME_INDEX VNI, ACTIVITY_INDEX AI, VERSION V WHERE AIE.OUTPUT_GROUP = '0' AND AIE.INTERMEDIATE_EXCHANGE_ID = IE.ID AND AIE.ACTIVITY_ID = A.ID AND A.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_NAME_ID = AN.ID AND VNI.VERSION_ID = V.ID AND a.id='"+pk+"'"
        else:
            select = "SELECT IE.ID, IE.NAME, v.version, an.id, an.ACTIVITY_NAME ai.id FROM ACTIVITY_INTERMEDIATE_EXCHANGE AIE, INTERMEDIATE_EXCHANGE IE, ACTIVITY A, ACTIVITY_NAME AN, VERSION_NAME_INDEX VNI, ACTIVITY_INDEX AI, VERSION V WHERE AIE.OUTPUT_GROUP = '0' AND AIE.INTERMEDIATE_EXCHANGE_ID = IE.ID AND AIE.ACTIVITY_ID = A.ID AND A.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_NAME_ID = AN.ID AND VNI.VERSION_ID = V.ID AND V.version = '"+v_id+"' and a.id='"+pk+"'"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "intermediate exchange id": str(row[0]),
                "intermediate exchange name": str(row[1]),
                "version": str(row[2]),
                #"activity name id": str(row[3]),
                "activity name": str(row[4]),
                "activity index id": str(row[5])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)

    @action(detail=False)
    def same_names(self, request):
        version=request.GET.get('version','') #Version name = ecoinvent 3.6 cut off
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "select DISTINCT an.id, vni.activity_index_id, S1.activity_name, S1.version from (select activity_name.activity_name, version.version, count(*) from activity_name, version_name_index, version where activity_name.id=version_name_index.activity_name_id and version.id=version_name_index.version_id and version.version='"+version+"' group by activity_name.activity_name, version.id) S1, activity_name an, version_name_index vni where an.id=vni.activity_name_id and an.activity_name=S1.activity_name and vni.activity_name_id=an.id"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                #"activity name id": str(row[0]),
                "activity index id": str(row[1]),
                "activity name": str(row[2]),
                "version": str(row[2])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)

    @action(detail=False)
    def similar_names(self, request):
        name=request.GET.get('name','')
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "select DISTINCT an.activity_name, an.id, vni.activity_index_id from activity_name an, version_name_index vni where an.activity_name like '%"+name+"%' AND vni.activity_name_id=an.id"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "activity name": str(row[0]),
                #"activity name id": str(row[1]),
                "activity index id": str(row[2])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)

    @action(detail=False)
    def alike_flows(self, request):
        v_id=request.GET.get('version','') #Version Id = ecoinvent 3.6 cut off
        ie_name=request.GET.get('name','') # IE part of a name = trawler
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "SELECT IE.ID, IE.NAME, v.version FROM ACTIVITY_INTERMEDIATE_EXCHANGE AIE, INTERMEDIATE_EXCHANGE IE, ACTIVITY A, ACTIVITY_NAME AN, VERSION_NAME_INDEX VNI, ACTIVITY_INDEX AI, VERSION V WHERE AIE.OUTPUT_GROUP = '0' AND AIE.INTERMEDIATE_EXCHANGE_ID = IE.ID AND AIE.ACTIVITY_ID = A.ID AND A.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_NAME_ID = AN.ID AND VNI.VERSION_ID = V.ID AND V.version = '"+v_id+"' AND IE.NAME LIKE '%"+ie_name+"%'"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "intermediate exchange id": str(row[0]),
                "intermediate exchange name": str(row[1]),
                "version": str(row[2])
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response(d2)
