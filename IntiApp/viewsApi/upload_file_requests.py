from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from IntiApp.serializersApi import general_serializer
from rest_framework.views import APIView
from IntiApp.models import ActivityIndex
from .conection import conexion

class RequestActivityIndex(APIView):
    serializer_class = general_serializer.RequestActivityIndexSerializer
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        peticion = self.serializer_class(data=request.data)
        if peticion.is_valid():
            activity_index_id = peticion.validated_data.get('activity_index_id')        #f7e93a25-56e4-4268-a603-3bfd57c79eff
            geography_id = peticion.validated_data.get('geography_id')                  #34dbbff8-88ce-11de-ad60-0019e336be3a 
            start_date = peticion.validated_data.get('start_date')                      #1981-01-01
            end_date = peticion.validated_data.get('end_date')                          #2005-12-31
            special_activity_type = peticion.validated_data.get('special_activity_type')   #0
            system_model_id = peticion.validated_data.get('system_model_id')            #8b738ea0-f89e-4627-8679-433616064e82
            cursor1 = conexion.cursor()
            select = "SELECT * FROM activity_index where id='" + activity_index_id + "' and geography_id='"+geography_id+"' and start_date='"+start_date+"' and end_date='"+end_date+"' and special_activity_type='"+special_activity_type+"' and system_model_id='"+system_model_id+"';"
            cursor1.execute(select)
            select_activity_index = cursor1.fetchall()
            if len(select_activity_index) == 0:
                return Response({'response':'0'})
            else:
                return Response({'response':'1'})
        else:
            return Response({'response':'invalid'})

class RequestActivityPerson(APIView):
    serializer_class = general_serializer.RequestNameSerializer
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        peticion = self.serializer_class(data=request.data)
        if peticion.is_valid():
            personName = peticion.validated_data.get('name')        # Charlotte Petiot
            cursor1 = conexion.cursor()
            select = "SELECT id FROM person where name='"+personName+"';"
            cursor1.execute(select)
            person_id = cursor1.fetchall()
            '''if of validate if the person exists'''
            if len(person_id) == 0:
                person_id2= ""
            else:
                person_id2 = "".join(map(str, person_id[0]))
            print(person_id2)
            '''search the last id from activity'''
            select = "SELECT MAX(id) AS id FROM activity"
            cursor1.execute(select)
            activity_id = cursor1.fetchall()
            activity_id2 = "".join(map(str, activity_id[0]))
            select = "SELECT person_id, activity_id FROM activity_person where person_id='"+person_id2+"' and activity_id='"+activity_id2+"';"
            cursor1.execute(select)
            verifica = cursor1.fetchall()
            if len(verifica) == 0:
                return Response({'response':'0','respuesta1':person_id2, 'respuesta2':activity_id2})
            else:
                return Response({'response':'1'})
        else:
            return Response({'response':'invalid'})

class RequestActivity(APIView):
    serializer_class = general_serializer.RequestNameSerializer
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        peticion = self.serializer_class(data=request.data)
        if peticion.is_valid():
            personName = peticion.validated_data.get('name')        #any string
            cursor1 = conexion.cursor()
            select = "SELECT MAX(id) AS id FROM activity;"
            cursor1.execute(select)
            select_activity = cursor1.fetchall()
            return Response({'response':'0','respuesta1':select_activity[0]})
        else:
            return Response({'response':'invalid'})

class RequestDataGeneratorAndPublication(APIView):
    serializer_class = general_serializer.RequestNameSerializer
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        peticion = self.serializer_class(data=request.data)
        if peticion.is_valid():
            personName = peticion.validated_data.get('name')        #any string
            cursor1 = conexion.cursor()
            select = "SELECT MAX(id) AS id FROM data_generator_and_publication;"
            cursor1.execute(select)
            select_data_generator_and_publication = cursor1.fetchall()
            return Response({'response':'0','respuesta1':select_data_generator_and_publication[0]})
        else:
            return Response({'response':'invalid'})

class RequestPersons(APIView):
    serializer_class = general_serializer.RequestNameSerializer
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        peticion = self.serializer_class(data=request.data)
        if peticion.is_valid():
            personName = peticion.validated_data.get('name')        #Charlotte Petiot
            cursor1 = conexion.cursor()
            select = "SELECT id FROM person where name='" + personName + "';"
            cursor1.execute(select)
            select_person_id = cursor1.fetchall()
            if len(select_person_id) == 0:
                return Response({'response':'0'})
            else:
                return Response({'response':'0','respuesta1':select_person_id[0]})
        else:
            return Response({'response':'invalid'})

class RequestVersionNameIndex(APIView):
    serializer_class = general_serializer.RequestVersionNameIndexSerializer
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        peticion = self.serializer_class(data=request.data)
        if peticion.is_valid():
            activity_index_id = peticion.validated_data.get('activity_index_id')        # f7e93a25-56e4-4268-a603-3bfd57c79eff
            activity_name_id = peticion.validated_data.get('activity_name_id')        # c2d58788-238b-464b-89c5-6b075d323033
            version_id = peticion.validated_data.get('version_id')              # 24
            cursor1 = conexion.cursor()
            select = "SELECT * FROM version_name_index where activity_index_id='" + activity_index_id + \
                "' and activity_name_id='" + activity_name_id + \
                "' and version_id='"+version_id+"';"
            cursor1.execute(select)
            select_version_name_index = cursor1.fetchall()
            if len(select_version_name_index) == 0:
                return Response({'response':'0'})
            else:
                return Response({'response':'1'})
            # return Response(h)
        else:
            return Response({'response':'invalid'})