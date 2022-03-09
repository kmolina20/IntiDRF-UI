# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    activity_index = models.ForeignKey('ActivityIndex', models.DO_NOTHING)
    allocation_comment = models.CharField(max_length=-1, blank=True, null=True)
    general_comment = models.CharField(max_length=-1, blank=True, null=True)
    comment_technology = models.CharField(max_length=-1, blank=True, null=True)
    included_processes = models.CharField(max_length=-1, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    is_data_valid_for_entire_period = models.BooleanField(blank=True, null=True)
    data_generator_and_publication = models.ForeignKey('DataGeneratorAndPublication', models.DO_NOTHING, blank=True, null=True)
    version = models.ForeignKey('Version', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'activity'


class ActivityIndex(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    geography = models.ForeignKey('Geography', models.DO_NOTHING, blank=True, null=True)
    system_model = models.ForeignKey('SystemModel', models.DO_NOTHING, blank=True, null=True)
    start_date = models.CharField(max_length=-1, blank=True, null=True)
    end_date = models.CharField(max_length=-1, blank=True, null=True)
    special_activity_type = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_index'


class ActivityIntermediateExchange(models.Model):
    activity = models.ForeignKey(Activity, models.DO_NOTHING)
    intermediate_exchange = models.ForeignKey('IntermediateExchange', models.DO_NOTHING)
    variable_name = models.CharField(max_length=-1, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    input_group = models.CharField(max_length=-1, blank=True, null=True)
    output_group = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_intermediate_exchange'


class ActivityName(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    activity_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_name'


class ActivityPerson(models.Model):
    person = models.OneToOneField('Person', models.DO_NOTHING, primary_key=True)
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'activity_person'
        unique_together = (('person', 'activity'),)


class Company(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    code = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)
    website = models.CharField(max_length=-1, blank=True, null=True)
    comment = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class Correspondence(models.Model):
    id = models.BigAutoField(primary_key=True)
    activity_intermediate_exchange = models.ForeignKey(ActivityIntermediateExchange, models.DO_NOTHING, db_column='activity_intermediate_exchange')
    next_activity_intermediate_exchange = models.ForeignKey(ActivityIntermediateExchange, models.DO_NOTHING, db_column='next_activity_intermediate_exchange')
    differences = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'correspondence'


class DataGeneratorAndPublication(models.Model):
    person = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    source = models.ForeignKey('Source', models.DO_NOTHING, blank=True, null=True)
    is_copyright_protected = models.BooleanField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'data_generator_and_publication'


class Geography(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    longitude = models.CharField(max_length=-1, blank=True, null=True)
    latitude = models.CharField(max_length=-1, blank=True, null=True)
    un_code = models.CharField(max_length=-1, blank=True, null=True)
    un_region_code = models.CharField(max_length=-1, blank=True, null=True)
    un_subregion_code = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)
    short_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geography'


class IntermediateExchange(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    unit = models.ForeignKey('Unit', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intermediate_exchange'


class Person(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    company = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)
    email = models.CharField(max_length=-1, blank=True, null=True)
    address = models.CharField(max_length=-1, blank=True, null=True)
    telephone = models.CharField(max_length=-1, blank=True, null=True)
    telefax = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Property(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    unit = models.ForeignKey('Unit', models.DO_NOTHING, blank=True, null=True)
    default_variable_name = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property'


class Source(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(max_length=-1, blank=True, null=True)
    volume_no = models.CharField(max_length=-1, blank=True, null=True)
    first_author = models.CharField(max_length=-1, blank=True, null=True)
    additional_authors = models.CharField(max_length=-1, blank=True, null=True)
    title = models.CharField(max_length=-1, blank=True, null=True)
    names_of_editors = models.CharField(max_length=-1, blank=True, null=True)
    page_numbers = models.CharField(max_length=-1, blank=True, null=True)
    journal = models.CharField(max_length=-1, blank=True, null=True)
    title_of_anthology = models.CharField(max_length=-1, blank=True, null=True)
    place_of_publications = models.CharField(max_length=-1, blank=True, null=True)
    publisher = models.CharField(max_length=-1, blank=True, null=True)
    comment = models.CharField(max_length=-1, blank=True, null=True)
    year = models.CharField(max_length=-1, blank=True, null=True)
    short_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source'


class Synonym(models.Model):
    activity = models.ForeignKey(ActivityIndex, models.DO_NOTHING, blank=True, null=True)
    synonym = models.CharField(max_length=-1, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'synonym'


class SystemModel(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=-1, blank=True, null=True)
    short_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_model'


class Unit(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=-1, blank=True, null=True)
    comment = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit'


class Version(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'version'


class VersionNameIndex(models.Model):
    id = models.BigAutoField(primary_key=True)
    activity_index = models.ForeignKey(ActivityIndex, models.DO_NOTHING, blank=True, null=True)
    activity_name = models.ForeignKey(ActivityName, models.DO_NOTHING, blank=True, null=True)
    version = models.ForeignKey(Version, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'version_name_index'

# Create the models for upload a file

class Document(models.Model):
    title = models.CharField(max_length = 200, blank=True, null=False)
    uploadedFile = models.FileField(upload_to = "uploaded_files/", blank=True, null=False)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)

class Query(models.Model):
    version = models.CharField(max_length = 200)
    int_exch_id = models.CharField(max_length = 200)
    int_exch_name = models.CharField(max_length = 200)

# Create models for correspondence files

class Correspondence(models.Model):
    id = models.BigAutoField(primary_key=True)
    activity_intermediate_exchange = models.ForeignKey('ActivityIntermediateExchange', models.DO_NOTHING)
    #next_activity_intermediate_exchange = models.ForeignKey('ActivityIntermediateExchange', models.DO_NOTHING)
    differences = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'correspondence'