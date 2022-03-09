import json
import csv
import requests

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .conection import conexion
from rest_framework.views import APIView
from rest_framework.decorators import action

from IntiApp.serializersApi import general_serializer


class IntermediateExchangeViewSet(viewsets.ModelViewSet):
    serializer_class = general_serializer.IntermediateExchangeSerializer
    serializer_class2 = general_serializer.RequestIdSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Intermediate Exchange created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            intermediate_exchange_serializer = self.serializer_class(
                self.get_queryset(pk), data=request.data)
            if intermediate_exchange_serializer.is_valid():
                intermediate_exchange_serializer.save()
                return Response(intermediate_exchange_serializer.data, status=status.HTTP_200_OK)
            return Response(intermediate_exchange_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        intermediateExchange = self.get_queryset().filter(id=pk).first()
        if intermediateExchange:
            intermediateExchange.delete()
            return Response({'message': 'Intermediate Exchange removed successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'No Intermediate Exchange found with this ID'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def producers(self, request, pk=None):
        data = {}
        data = []
        cursor1 = conexion.cursor()
        select = "SELECT DISTINCT ie.id, ie.name, an.id, an.activity_name, ai.id, p.name , v.version FROM version v, activity_index ai, version_name_index vni, activity_name an, activity_intermediate_exchange aie, intermediate_exchange ie, activity a, data_generator_and_publication dgap, person p WHERE ie.id=aie.intermediate_exchange_id AND aie.activity_id=a.id AND a.data_generator_and_publication_id=dgap.id AND dgap.person_id=p.id AND a.activity_index_id=ai.id AND vni.activity_index_id=ai.id AND an.id=vni.activity_name_id AND vni.version_id=v.id AND ie.id='" +pk+"' AND aie.output_group = '0' GROUP BY v.id, ie.id, ai.id, an.id, p.id"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "intermediate exchange id": str(row[0]),
                "intermediate exchange name": str(row[1]),
                #"activity name id": str(row[2]),
                "activity name": str(row[3]),
                "activity index id": str(row[4]),
                "data generator and publication person name": str(row[5]),
                "version": str(row[6]),
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response({'response': d2})
    
    @action(detail=True)
    def activities(self, request, pk=None):
        v_id=request.GET.get('version','') #Version name = ecoinvent 3.6 cut off
        data = {}
        data = []
        cursor1 = conexion.cursor()
        if len(v_id)==0:
            select = "SELECT IE.ID, IE.NAME, v.version, an.id, an.ACTIVITY_NAME, ai.id FROM ACTIVITY_INTERMEDIATE_EXCHANGE AIE, INTERMEDIATE_EXCHANGE IE, ACTIVITY A, ACTIVITY_NAME AN, VERSION_NAME_INDEX VNI, ACTIVITY_INDEX AI, VERSION V WHERE AIE.OUTPUT_GROUP = '0' AND AIE.INTERMEDIATE_EXCHANGE_ID = IE.ID AND AIE.ACTIVITY_ID = A.ID AND A.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_NAME_ID = AN.ID AND VNI.VERSION_ID = V.ID AND IE.id='"+pk+"'"
        else:
            select = "SELECT IE.ID, IE.NAME, v.version, an.id, an.ACTIVITY_NAME, ai.id FROM ACTIVITY_INTERMEDIATE_EXCHANGE AIE, INTERMEDIATE_EXCHANGE IE, ACTIVITY A, ACTIVITY_NAME AN, VERSION_NAME_INDEX VNI, ACTIVITY_INDEX AI, VERSION V WHERE AIE.OUTPUT_GROUP = '0' AND AIE.INTERMEDIATE_EXCHANGE_ID = IE.ID AND AIE.ACTIVITY_ID = A.ID AND A.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_INDEX_ID = AI.ID AND VNI.ACTIVITY_NAME_ID = AN.ID AND VNI.VERSION_ID = V.ID AND V.version = '"+v_id+"' AND IE.id='"+pk+"'"
        cursor1.execute(select)
        select = cursor1.fetchall()
        for row in select:
            data.append({
                "intermediate exchange id": str(row[0]),
                "intermediate exchange name": str(row[1]),
                "version": str(row[2]),
                # "activity name id": str(row[3]),
                "activity name": str(row[4]),
                "activity index id": str(row[5]),
            })
        s1 = json.dumps(data)
        d1 = json.loads(s1)
        d2=self.paginate_queryset(d1)
        if len(select) == 0:
            return Response({'response': 'no data found'})
        else:
            return Response({'response': d2})

@csrf_exempt
def export_intermediate_exchange(request,intermediate_exchange,Version):
    index = 1
    responseUsuarioCSV = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(responseUsuarioCSV,delimiter=';')
    writer.writerow(['Intermediate Exchange Id','Intermediate Exchange Name','Activity Index Id','Activity Name','Version Name'])
    
    url = 'http://127.0.0.1:8000/inti/intermediate_exchanges/{0}/activities/?page=1&version={1}'.format(intermediate_exchange,Version) 
    r = requests.get(url)
    
    while r.status_code != 404:
        url = 'http://127.0.0.1:8000/inti/intermediate_exchanges/{0}/activities/?page={2}&version={1}'.format(intermediate_exchange,Version,index) 
        r = requests.get(url)
        if r.status_code != 404:
            activities = r.json()

            for row in activities['response']:
                activity = []
                activity.append(row['intermediate exchange id'])
                activity.append(row['intermediate exchange name']) 
                activity.append(row['activity index id'])
                activity.append(row['activity name'])
                activity.append(row['version'])
                writer.writerow(activity)
            
            index = index+1
            print(url)

    responseUsuarioCSV['Content-Disposition'] = 'attachment;filename="Activities_by_Intermediate_Exchanges&Versions.csv"'

    return responseUsuarioCSV