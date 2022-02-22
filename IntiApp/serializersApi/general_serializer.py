from IntiApp.models import Version, Activity, Company, Person, Geography, Unit, ActivityIntermediateExchange, ActivityIndex, ActivityName, ActivityPerson, DataGeneratorAndPublication, IntermediateExchange, Property, Source, Synonym, SystemModel, VersionNameIndex, RequestActivityIndex, RequestIdName, RequestName, RequestId, RequestVersionNameIndex
from rest_framework import serializers

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
    
class PersonSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Person
        fields = '__all__'

class GeographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Geography
        fields = '__all__'
    
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
    
class ActivityIntermediateExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityIntermediateExchange
        fields = '__all__'

class ActivityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityName
        fields = '__all__'

class IntermediateExchangeSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model = IntermediateExchange
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    unit = UnitSerializer()

    class Meta:
        model = Property
        fields = '__all__'

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class DataGeneratorAndPublicationSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    source = SourceSerializer()
    
    class Meta:
        model = DataGeneratorAndPublication
        fields = '__all__'

class SystemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemModel
        fields = '__all__'
 
class ActivityIndexSerializer(serializers.ModelSerializer):
    
    geography = GeographySerializer()
    system_model = SystemModelSerializer()

    class Meta:
        model = ActivityIndex
        fields = '__all__'
    
class VersionNameIndexSerializer(serializers.ModelSerializer):
    activity_index = ActivityIndexSerializer()
    activity_name = ActivityNameSerializer()
    version = VersionSerializer()

    class Meta:
        model = VersionNameIndex
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer): 
    activity_index = ActivityIndexSerializer()
    data_generator_and_publication = DataGeneratorAndPublicationSerializer()
    version = VersionSerializer()
    
    class Meta:
        model = Activity
        fields = '__all__'

class ActivityPersonSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = ActivityPerson
        fields = '__all__'

class SynonymSerializer(serializers.ModelSerializer):
    activity = ActivityIndexSerializer()
    
    class Meta:
        model = Synonym
        fields = '__all__'


#UPLOAD FILE PETITIONS (only for the client)
class RequestActivityIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestActivityIndex
        fields = '__all__'

class RequestVersionNameIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestVersionNameIndex
        fields = '__all__'

#PERSONALIZED PETITIONS
class RequestIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestId
        fields = '__all__'

class RequestNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestName
        fields = '__all__'

class RequestIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestIdName
        fields = '__all__'