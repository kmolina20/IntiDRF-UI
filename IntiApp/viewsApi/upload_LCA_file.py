from django.db.models import query
from IntiApp.models import models
import requests
from django.shortcuts import render

from zipfile import ZipFile
import os
from xml.dom import minidom
import numpy as np
import shutil
from shutil import rmtree


#SETTING NOMBRE DIRECTORIOS
directorio = '/home/kamila/T_projects/my_env/DjangoFileUpload-1'  #PATH DEL PARCHIVO
dir_temp = '/home/kamila/T_projects/my_env/DjangoFileUpload-1/temp/' #PATH DESTINO

md = '/MasterData/'
ds = '/datasets/'

def upload_files(request):
    if request.method == "POST":
        # Fetching the form data
        file_title = request.POST["file_title"]
        uploaded_file = request.FILES["uploaded_file"]
        # Saving the information in the database
        document = models.Document(
            title=file_title,
            uploadedFile=uploaded_file
        )
        document.save()
        #UNZIP THE UPLOADED FILE INTO A DIRECTORY check
        #with ZipFile(directorio+document.uploadedFile.url, 'r') as zip:
        #    zip.extractall(directorio+'/temp')
        #    print('File is unzipped in temp folder')
        #NAME OF THE UNZIP FILE
        #a = os.path.split(document.uploadedFile.url)
        #nombre_carpeta = os.path.splitext(a[1])
        #b=nombre_carpeta[0].find('_')
        #new = nombre_carpeta[0][:b] + ' ' + nombre_carpeta[0][b+1:]
        # 
        #route = dir_temp+new+md
        route = dir_temp+'ecoinvent 3.6_apos_ecoSpold02'+md
        routeDS = dir_temp+'ecoinvent 3.6_apos_ecoSpold02'+ds
        '''post_data = {"username": "admin",
                     "password": "admin"}
        response = requests.post(
            "http://127.0.0.1:8000/inti/api_generate_token", data=post_data)
        content = response.content
        token = content.decode('utf8').split('"')
        print("\n4 %s" % token[3])'''
        #METHODS TO READ THE FILE AND ADD TO THE DATABASE
        #companies(route + 'Companies.xml')
        #sources(route + 'Sources.xml')
        #persons(route + 'Persons.xml')
        #activity_name(route + 'ActivityNames.xml')
        #geography(route + 'Geographies.xml')
        #unit(route + 'Geographies.xml')
        #intermediateExchange(route + 'IntermediateExchanges.xml')
        #system_model(route + 'SystemModels.xml')
        #property(route + 'Properties.xml')
        # cambiar el id de la version si se cambia
        id_version = search_version(document.title)
        #print("id_version %s" % id_version)
        #activityIndexEntry(route + 'ActivityIndex.xml', id_version)
        #leerActividadGenerica(routeDS, id_version)
        #rmtree(dir_temp+'ecoinvent 3.6_apos_ecoSpold02')
        #rmtree(directorio+'/media/uploaded_files')

    documents = models.Document.objects.all()

    return render(request, "Core/index.html", context={
        "files": documents
    })

def query_files(request):
    print('query_files')
    id_version = ''
    if request.method == "POST":
        # Fetching the form data
        print('post')
        version = request.POST["version"]
        int_exch_id = request.POST["int_exch_id"]
        int_exch_name = request.POST["int_exch_name"]

        # Saving the information in the database
        query = models.Query(
            version=version,
            int_exch_id=int_exch_id,
            int_exch_name = int_exch_name
        )
        #query.save()
        id_version = search_version(query.version)
        print(id_version)
        print(int_exch_id)
        print(int_exch_name)
        
    post_data = {"version": id_version}
    response = requests.post(
        #"http://127.0.0.1:8000/inti/request_ActivitiesSameName/", data=post_data)
        "https://jsonplaceholder.typicode.com/todos/", data=post_data)
    al = response.json()
    #content = al.get('response1')
    '''a = al.get('response1')
    i=0
    for e in al.get('response1'):
        i=i+1
        print(i)'''
        
    response = requests.get('https://jsonplaceholder.typicode.com/todos/')
    # transfor the response to json objects
    todos = response.json()
    for todo in todos:
        id = todo.get('id')
        # print(id)
    # return render(request, "main_app/home.html", {"todos": todos})

    '''response = requests.get('http://127.0.0.1:8000/inti/versions/50')
    a = response.json()
    #colocar validacion de si no encuentra el id, debe crear una nueva persona
    if response.status_code == 404:
        #todos = response.json()
        print("no hay el id, crea uno")
        post_data = {"synonym": "Gladys",
            "activity": "8e063bee-5d0f-4624-89e0-28a1b073c6b8"}
        response = requests.post(
            "http://127.0.0.1:8000/inti/synonyms/", data=post_data)
        content = response.content
        #insert = "insert into company(id, code, name, website, comment) values (%s,%s,%s,%s,%s)"
        #datos = (id, code, name, website, comment)
        #cursor1.execute(insert, datos)
        # conexion.commit()
    else:
        print("persona already exist")'''

    return render(request, "Core/query.html", context={
        "todos": todos, "al": al
    })

def companies(route):
    xmlReader = minidom.parse(route)
    companies = xmlReader.getElementsByTagName("company")
    for company in companies:
        id = company.getAttribute("id")
        code = company.getAttribute("code")
        website = company.getAttribute("website")
        if len(company.getElementsByTagName("name")) != 0:
            try:
                name = company.getElementsByTagName("name")[0].firstChild.data
            except AttributeError:
                name = "not name provided"
        else:
            name = "not name provided"
        if len(company.getElementsByTagName("comment")) != 0:
            try:
                comment = company.getElementsByTagName("comment")[0].firstChild.data
            except AttributeError:
                comment = "not comment provided"
        else:
            comment = "not comment provided"
        '''GET THE COMPANY ID '''
        response = requests.get('http://127.0.0.1:8000/inti/companies/'+id)
        if response.status_code == 404:
            post_data = {"id": id,
                         "code": code,
                         "name": name,
                         "website": website,
                         "comment": comment}
            response = requests.post(
                "http://127.0.0.1:8000/inti/companies/", data=post_data)
        else:
            if response.status_code == 200:
                print("already exist")
    return

def sources(route):
    print("sources")
    xmlReader = minidom.parse(route)
    sources = xmlReader.getElementsByTagName("source")
    i = 0
    for source in sources:
        source_id = source.getAttribute("id")
        source_type = source.getAttribute("sourceType")
        year = source.getAttribute("year")
        volume_no = source.getAttribute("volumeNo")
        first_author = source.getAttribute("firstAuthor")
        additional_authors = source.getAttribute("additionalAuthors")
        title = source.getAttribute("title")
        names_of_editors = source.getAttribute("namesOfEditors")
        short_name = source.getAttribute("shortName")
        page_numbers = source.getAttribute("pageNumbers")
        journal = source.getAttribute("journal")
        title_of_anthology = source.getAttribute("titleOfAnthology")
        place_of_publications = source.getAttribute("placeOfPublications")
        publisher = source.getAttribute("publisher")

        if len(source.getElementsByTagName("comment")) != 0:
            try:
                aux = ""
                comment = ""
                j = 0
                for comm in source.getElementsByTagName("comment"):
                    aux = source.getElementsByTagName(
                        "comment")[j].firstChild.nodeValue
                    comment = comment + '_' + aux
                    j += 1
            except AttributeError:
                comment = "not comment provided by the provider"
        else:
            comment = "not comment provided by the provider"
        '''obtener el id de los sources '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/sources/'+source_id)
        #print("entra al response")
        '''colocar validacion de si no encuentra el id, debe crear un nuevo sources'''
        if response.status_code == 404:
            #todos = response.json()
            i += 1
            post_data = {"id": source_id,
                         "type": source_type,
                         "year": year,
                         "volume_no": volume_no,
                         "first_author": first_author,
                         "additional_authors": additional_authors,
                         "title": title,
                         "names_of_editors": names_of_editors,
                         "short_name": short_name,
                         "page_numbers": page_numbers,
                         "journal": journal,
                         "title_of_anthology": title_of_anthology,
                         "place_of_publications": place_of_publications,
                         "publisher": publisher,
                         "comment": comment}
            response = requests.post(
                "http://127.0.0.1:8000/inti/sources/", data=post_data)
            content = response.content
        '''else :
            if response.status_code == 200:
            '''
    print("source: %s" % i)
    return

def persons(route):
    print("persons")
    xmlReader = minidom.parse(route)
    sources = xmlReader.getElementsByTagName("person")
    i = 0
    for source in sources:
        person_id = source.getAttribute("id")
        person_name = source.getAttribute("name")
        person_address = source.getAttribute("address")
        person_telephone = source.getAttribute("telephone")
        person_telefax = source.getAttribute("telefax")
        person_email = source.getAttribute("email")
        company_id = source.getAttribute("companyId")

        if len(source.getAttribute("companyId")) == 0:
            company_id = "00000000-0000-0000-0000-000000000000"
        '''obtener el id de la person '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/people/'+person_id)
        #print("entra al response")
        '''colocar validacion de si no encuentra el id, debe crear un nuevo sources'''
        if response.status_code == 404:
            #todos = response.json()
            print("algo")

            post_data = {"id": person_id,
                         "name": person_name,
                         "email": person_email,
                         "address": person_address,
                         "telephone": person_telephone,
                         "telefax": person_telefax,
                         "company_id": company_id}
            response = requests.post(
                "http://127.0.0.1:8000/inti/people/", data=post_data)
            content = response.content
        '''else :
            if response.status_code == 200:
                i += 1
    print("people: %s"%i) '''
    return

def activity_name(route):
    print("activity_name")
    xmlReader = minidom.parse(route)
    activity_names = xmlReader.getElementsByTagName("activityName")
    i = 0
    for activity_name in activity_names:
        activity_name_id = activity_name.getAttribute("id")
        #i += 1
        if len(activity_name.getElementsByTagName("name")) != 0:
            try:
                activity_name = activity_name.getElementsByTagName("name")[
                    0].firstChild.data
            except AttributeError:
                activity_name = "not name provided by the provider"
        else:
            activity_name = "not name provided by the provider"
        '''obtener el id de la activity_name '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/activities_name/'+activity_name_id)
        #print("entra al response")
        '''colocar validacion de si no encuentra el id, debe crear un nuevo activity_name'''
        if response.status_code == 404:
            #todos = response.json()
            print("algo")
            post_data = {"id": activity_name_id,
                         "activity_name": activity_name}
            response = requests.post(
                "http://127.0.0.1:8000/inti/activities_name/", data=post_data)
            content = response.content
        else:
            if response.status_code == 200:
                i += 1
    print("activities_name: %s" % i)
    return

def geography(route):
    print("geography")
    xmlReader = minidom.parse(route)
    geographies = xmlReader.getElementsByTagName("geography")
    i = 0
    for geography in geographies:
        geography_id = geography.getAttribute("id")
        longitude = geography.getAttribute("longitude")
        latitude = geography.getAttribute("latitude")
        un_code = geography.getAttribute("uNCode")
        un_region_code = geography.getAttribute("uNRegionCode")
        un_subregion_code = geography.getAttribute("uNSubregionCode")

        if len(geography.getElementsByTagName("name")) != 0:
            try:
                name = geography.getElementsByTagName(
                    "name")[0].firstChild.data
            except AttributeError:
                name = "not name provided by the provider"
        else:
            name = "not name provided by the provider"

        if len(geography.getElementsByTagName("shortname")) != 0:
            try:
                short_name = geography.getElementsByTagName("shortname")[
                    0].firstChild.data
            except AttributeError:
                short_name = "not shortname provided by the provider"
        else:
            short_name = "not shortname provided by the provider"
        '''obtener el id de la geography '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/geographies/'+geography_id)
        '''colocar validacion de si no encuentra el id, debe crear un nuevo geographies'''
        if response.status_code == 404:
            #todos = response.json()
            print("algo")
            post_data = {"id": geography_id,
                         "longitude": longitude,
                         "latitude": latitude,
                         "un_code": un_code,
                         "un_region_code": un_region_code,
                         "un_subregion_code": un_subregion_code,
                         "name": name,
                         "short_name": short_name}
            response = requests.post(
                "http://127.0.0.1:8000/inti/geographies/", data=post_data)
            content = response.content
        '''else:
            if response.status_code == 200:
                i += 1
    print("geographies: %s" % i)'''
    return

def unit(route):
    print("unit")
    xmlReader = minidom.parse(route)
    units = xmlReader.getElementsByTagName("unit")
    i = 0
    for unit in units:
        unit_id = unit.getAttribute("id")
        i += 1
        if len(unit.getElementsByTagName("name")) != 0:
            try:
                unit_name = unit.getElementsByTagName(
                    "name")[0].firstChild.data
            except AttributeError:
                unit_name = "not name provided by the provider"
        else:
            unit_name = "not name provided by the provider"
        if len(unit.getElementsByTagName("comment")) != 0:
            try:
                unit_comment = unit.getElementsByTagName("comment")[
                    0].firstChild.data
            except AttributeError:
                unit_comment = "not comment provided by the provider"
        else:
            unit_comment = "not comment provided by the provider"
        '''obtener el id de la unit '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/units/'+unit_id)
        '''colocar validacion de si no encuentra el id, debe crear un nuevo unit'''
        if response.status_code == 404:
            #todos = response.json()
            print("algo")
            post_data = {"id": unit_id,
                         "name": unit_name,
                         "comment": unit_comment}
            response = requests.post(
                "http://127.0.0.1:8000/inti/units/", data=post_data)
            content = response.content
        '''else:
            if response.status_code == 200:
                i += 1
    print("unit: %s" % i) '''
    return

def intermediateExchange(route):
    print("intermediateExchange")
    xmlReader = minidom.parse(route)
    intermediateExchanges = xmlReader.getElementsByTagName(
        "intermediateExchange")
    i = 0
    for intermediateExchange in intermediateExchanges:
        id = intermediateExchange.getAttribute("id")
        unit_id = intermediateExchange.getAttribute("unitId")
        i += 1
        if len(intermediateExchange.getElementsByTagName("name")) != 0:
            try:
                name = intermediateExchange.getElementsByTagName("name")[
                    0].firstChild.data
            except AttributeError:
                name = "not name provided by the provider"
        else:
            name = "not name provided by the provider"
        '''obtener el id de la intermediate_exchanges '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/intermediate_exchanges/'+id)
        '''colocar validacion de si no encuentra el id, debe crear un nuevo intermediate_exchanges'''
        if response.status_code == 404:
            #todos = response.json()
            print("algo")
            post_data = {"id": id,
                         "unit_id": unit_id,
                         "name": name}
            response = requests.post(
                "http://127.0.0.1:8000/inti/intermediate_exchanges/", data=post_data)
            content = response.content
        else:
            if response.status_code == 200:
                i += 1
    print("intermediate_exchanges: %s" % i)
    return

def system_model(route):
    print("system_model")
    xmlReader = minidom.parse(route)
    systemModels = xmlReader.getElementsByTagName("systemModel")
    i = 0
    s = 0
    for systemModel in systemModels:
        system_model_id = systemModel.getAttribute("id")
        if len(systemModel.getElementsByTagName("name")) != 0:
            try:
                system_model_name = systemModel.getElementsByTagName("name")[
                    0].firstChild.data
            except AttributeError:
                system_model_name = "not name provided by the provider"
        else:
            system_model_name = "not name provided by the provider"
        if len(systemModel.getElementsByTagName("shortname")) != 0:
            try:
                system_model_short_name = systemModel.getElementsByTagName("shortname")[
                    0].firstChild.data
            except AttributeError:
                system_model_short_name = "not shortname provided by the provider"
        else:
            system_model_short_name = "not shortname provided by the provider"
        '''obtener el id de la system_models '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/system_models/'+system_model_id)
        '''colocar validacion de si no encuentra el id, debe crear un nuevo system_models'''
        if response.status_code == 404:
            #todos = response.json()
            s += 1
            print("algo")
            post_data = {"id": system_model_id,
                         "name": system_model_name,
                         "short_name": system_model_short_name}
            response = requests.post(
                "http://127.0.0.1:8000/inti/system_models/", data=post_data)
            content = response.content
        else:
            if response.status_code == 200:
                i += 1
    print("intermediate_exchanges agregados: %s" % s)
    print("intermediate_exchanges habian: %s" % i)
    return

def property(route):
    print("property")
    xmlReader = minidom.parse(route)
    properties = xmlReader.getElementsByTagName("property")
    i = 0
    s = 0
    for property in properties:
        property_id = property.getAttribute("id")
        default_variable_name = property.getAttribute("defaultVariableName")
        unit_id = property.getAttribute("unitId")
        if len(property.getAttribute("unitId")) == 0:
            unit_id = "00000000-0000-0000-0000-000000000000"
        if len(property.getElementsByTagName("name")) != 0:
            try:
                property_name = property.getElementsByTagName("name")[
                    0].firstChild.data
            except AttributeError:
                property_name = "not name provided by the provider"
        else:
            property_name = "not name provided by the provider"
        '''obtener el id de la properties '''
        response = requests.get(
            'http://127.0.0.1:8000/inti/properties/'+property_id)
        '''colocar validacion de si no encuentra el id, debe crear un nuevo properties'''
        if response.status_code == 404:
            #todos = response.json()
            s += 1
            print("algo")
            post_data = {"id": property_id,
                         "unit_id": unit_id,
                         "default_variable_name": default_variable_name,
                         "name": property_name}
            response = requests.post(
                "http://127.0.0.1:8000/inti/properties/", data=post_data)
            content = response.content
        else:
            if response.status_code == 200:
                i += 1
    print("intermediate_exchanges agregados: %s" % s)
    print("intermediate_exchanges habian: %s" % i)
    return

def search_version(nombre_version):
    id_version = ""
    if nombre_version == 'ecoinvent 3.6 cut off':
        id_version = '18'
    elif nombre_version == 'ecoinvent 3.6 apos':
        id_version = '19'
    elif nombre_version == 'ecoinvent 3.6 consequential':
        id_version = '20'
    elif nombre_version == 'ecoinvent 3.7 cut off':
        id_version = '21'
    elif nombre_version == 'ecoinvent 3.7 apos':
        id_version = '22'
    elif nombre_version == 'ecoinvent 3.7 consequential':
        id_version = '23'
    elif nombre_version == 'ecoinvent 3.7.1 cut off':
        id_version = '24'
    elif nombre_version == 'ecoinvent 3.7.1 apos':
        id_version = '25'
    elif nombre_version == 'ecoinvent 3.7.1 consequential':
        id_version = '26'
    return id_version

def activityIndexEntry(route, version):
    print("activityIndexEntry")
    xmlReader = minidom.parse(route)
    activityIndexEntry = xmlReader.getElementsByTagName("activityIndexEntry")
    #version = 19
    i = 0
    for activityIndex in activityIndexEntry:
        activity_index_id = activityIndex.getAttribute("id")
        activity_name_id = activityIndex.getAttribute("activityNameId")
        geography_id = activityIndex.getAttribute("geographyId")
        start_date = activityIndex.getAttribute("startDate")
        end_date = activityIndex.getAttribute("endDate")
        special_activity_type = activityIndex.getAttribute(
            "specialActivityType")
        system_model_id = activityIndex.getAttribute("systemModelId")
        primero = 0
        segundo = 0
        cont = 1
        a = 0
        '''obtener los rows que ya han sido ingresados para comprobar que no se repita pero que si esten todos'''
        post_data = {"activity_index_id": activity_index_id,
                     "geography_id": geography_id,
                     "start_date": start_date,
                     "end_date": end_date,
                     "special_activity_type": special_activity_type,
                     "system_model_id": system_model_id}
        response = requests.post(
            "http://127.0.0.1:8000/inti/request_activityIndex/", data=post_data)
        al = response.json()
        content = al.get('response')
        #print(content)
        if content == '0':
            '''SE INGRESA EN LA TABLA activity_index'''
            post_data = {"id": activity_index_id,
                         "start_date": start_date,
                         "end_date": end_date,
                         "special_activity_type": special_activity_type,
                         "geography": geography_id,
                         "system_model": system_model_id}
            response = requests.post("http://127.0.0.1:8000/inti/activities_index/", data=post_data)
            '''SE INGRESA EN LA TABLA version_name_index'''
            post_data = {"activity_index": activity_index_id,
                         "activity_name": activity_name_id,
                         "version": version}
            response = requests.post("http://127.0.0.1:8000/inti/version_name_indexes/", data=post_data)
        else:
            post_data = {"activity_index_id": activity_index_id,
                     "activity_name_id": activity_name_id,
                     "version_id": version}
            response = requests.post(
                "http://127.0.0.1:8000/inti/request_versionNameIndex/", data=post_data)
            al = response.json()
            content = al.get('response')
            #print(content)
            if content == '0':
                '''SE INGRESA EN LA TABLA version_name_index'''
                post_data = {"activity_index": activity_index_id,
                         "activity_name": activity_name_id,
                         "version": version}
                response = requests.post("http://127.0.0.1:8000/inti/version_name_indexes/", data=post_data)
    return

def ordenamientoBurbuja(matriz,tam):
    for i in range(1,tam):
        for j in range(0,tam-i):
            if(int(matriz[j][0]) > int(matriz[j+1][0])):
                n = matriz[j+1][0]
                o = matriz[j+1][1]
                matriz[j+1][0] = matriz[j][0]
                matriz[j+1][1] = matriz[j][1]
                matriz[j][0] = n
                matriz[j][1] = o

def leerActividadGenerica(route, version):
    """data_generator_and_publication - activity - acitivity_intermediate_exchange - activity_person"""
    print("renombrando archivos")
    for archivo in os.listdir(route):
        cadena_archivo = archivo
        cortar = cadena_archivo.split('_')
        os.rename(route + cadena_archivo, route + str(cortar[0]) + ".xml")
    print("COMIENZA EL PROCESO")
    for archivo in os.listdir(route):
        print(os.path.join(archivo))
        xmlReader = minidom.parse(route + archivo)
        activityDescriptions = xmlReader.getElementsByTagName("activityDescription")
        i = 0
        general_comment = ""
        #print("for activityDescription in activityDescriptions:")
        for activityDescription in activityDescriptions:
            for activity in activityDescription.getElementsByTagName("activity"):
                activity_index_id = activity.getAttribute("id")
                '''AGREGAR SYNONYMS DE LAS ACTIVIDADES'''
                if len(activity.getElementsByTagName("synonym")) != 0:
                    try:
                        j = 0
                        for syno in activity.getElementsByTagName("synonym"):
                            aux = activity.getElementsByTagName("synonym")[j].firstChild.nodeValue
                            post_data = {"activity": activity_index_id,
                                        "synonym": aux}
                            response = requests.post("http://127.0.0.1:8000/inti/synonyms/", data=post_data)
                            j += 1
                    except AttributeError:
                        aux = "not synonym provided"
                else:
                    aux = "not synonym provided"
                '''HASTA AQUI LOS SYNONYMS'''
                if len(activity.getElementsByTagName("allocationComment")) != 0:
                    try:
                        allocation_comment = property.getElementsByTagName("allocationComment")[0].firstChild.data
                    except AttributeError:
                        allocation_comment = "not allocationComment provided by the provider"
                else:
                    allocation_comment = "not allocationComment provided by the provider"
                # included_processes = "includedActivitiesStart" +activity.getElementsByTagName("includedActivitiesStart")[0].firstChild.data
                included_processes = ""
                """VALIDAR CUANDO NO TENGA UN START -check-"""
                if len(activity.getElementsByTagName("includedActivitiesStart")) != 0:
                    try:
                        included_processes = included_processes + "includedActivitiesStart" + activity.getElementsByTagName("includedActivitiesStart")[0].firstChild.data
                    except AttributeError:
                        included_processes = included_processes + ""
                """VALIDAR CUANDO NO TENGA UN END -check-"""
                if len(activity.getElementsByTagName("includedActivitiesEnd")) != 0:
                    try:
                        included_processes = included_processes + "includedActivitiesEnd" + activity.getElementsByTagName("includedActivitiesEnd")[0].firstChild.data
                    except AttributeError:
                        included_processes = included_processes + ""
                '''ORDENAMIENTO DE generalComment -check-'''
                for generalComment in activity.getElementsByTagName("generalComment"):
                    matriz = []
                    if len(generalComment.getElementsByTagName("text")) != 0:
                        for text in generalComment.getElementsByTagName("text"):
                            filas = len(generalComment.getElementsByTagName("text"))
                            columnas = 2
                            for j in range(columnas):
                                if (j == 0):
                                    a = str(text.getAttribute("index"))
                                if (j == 1):
                                    try:
                                        b = str(generalComment.getElementsByTagName("text")[i].firstChild.data)
                                    except AttributeError:
                                        b = ""
                            i += 1
                            array = np.array([a, b])
                            matriz.append(array)
                        # print(matriz)
                        ordenamientoBurbuja(matriz, len(matriz))
                        # print(matriz)
                        for q in range(0, filas):
                            general_comment = general_comment + "\n" + matriz[q][1]
                    else:
                        general_comment = ""
        #print("administrativeInformations = xmlReader.getElementsByTagName(administrativeInformation)")
        administrativeInformations = xmlReader.getElementsByTagName("administrativeInformation")
        for administrativeInformation in administrativeInformations:
            for dataGeneratorAndPublication in administrativeInformation.getElementsByTagName("dataGeneratorAndPublication"):
                personName = dataGeneratorAndPublication.getAttribute("personName")
                source_id = dataGeneratorAndPublication.getAttribute("publishedSourceId")
                if len(dataGeneratorAndPublication.getAttribute("publishedSourceId")) == 0:
                    source_id = "00000000-0000-0000-0000-000000000000"
                is_copyright_protected = dataGeneratorAndPublication.getAttribute("isCopyrightProtected")
                '''obtener el id de la persona en base al nombre dado los diferentes id's por las versiones'''
                post_data = {"name": personName}
                response = requests.post(
                    "http://127.0.0.1:8000/inti/request_Persons/", data=post_data)
                al = response.json()
                content = al.get('response')
                content1 = al.get('response1')
                '''colocar validacion de si no encuentra el nombre, debe crear una nueva persona'''
                if content == '0':
                    print("no encuentra nombre->crear nueva 'persona' -> %s" % personName)
                post_data = {"person": content1,
                         "source": source_id,
                         "is_copyright_protected": is_copyright_protected}
                response = requests.post("http://127.0.0.1:8000/inti/data_generator_publication/", data=post_data)
            for timePeriod in activityDescription.getElementsByTagName("timePeriod"):
                is_data_valid_for_entire_period = timePeriod.getAttribute("isDataValidForEntirePeriod")
            '''VALIDAR  CIANDO NO HAYA comment_technology - check'''
            for technology in activityDescription.getElementsByTagName("technology"):
                # print(len(technology.getElementsByTagName("comment")))
                if len(technology.getElementsByTagName("comment")) != 0:
                    if len(technology.getElementsByTagName("text")) != 0:
                        try:
                            for comment in technology.getElementsByTagName("comment"):
                                comment_technology = comment.getElementsByTagName("text")[0].firstChild.data
                        except AttributeError:
                            comment_technology = comment_technology + ""
                else:
                    comment_technology = "NO COMMENT TECHNOLOGY"
            '''obtener el ultimo id de data_generator_and_publication ingresado en la base'''
            post_data = {"name": '1'}
            response = requests.post(
                    "http://127.0.0.1:8000/inti/request_DataGeneratorAndPublication/", data=post_data)
            al = response.json()
            content = al.get('response')
            content1 = al.get('response1')
            if content == '0':
                post_data = {"activity_index_id": activity_index_id,
                            "allocation_comment": allocation_comment,
                            "general_comment": general_comment,
                            "included_processes": included_processes,
                            "comment_technology": comment_technology,
                            "is_data_valid_for_entire_period": content1,
                            "data_generator_and_publication_id": version,
                            "version_id": source_id}
                response = requests.post("http://127.0.0.1:8000/inti/activities/", data=post_data)
        print("flowDatas = xmlReader.getElementsByTagName(flowData)")
        i = 0  # contador para comprabar la cantidad que se ingresa en la tabla
        flowDatas = xmlReader.getElementsByTagName("flowData")
        for flowData in flowDatas:
            for intermediateExchange in flowData.getElementsByTagName("intermediateExchange"):
                # id = intermediateExchange.getAttribute("id")
                intermediate_exchange_id = intermediateExchange.getAttribute("intermediateExchangeId")
                variable_name = intermediateExchange.getAttribute("variableName")
                if len(intermediateExchange.getElementsByTagName("inputGroup")) != 0:
                    try:
                        input_group = intermediateExchange.getElementsByTagName("inputGroup")[0].firstChild.data
                    except AttributeError:
                        input_group = "No Group"
                else:
                    input_group = "No Group"
                if len(intermediateExchange.getElementsByTagName("outputGroup")) != 0:
                    try:
                        output_group = intermediateExchange.getElementsByTagName("outputGroup")[0].firstChild.data
                    except AttributeError:
                        output_group = "No Group"
                else:
                    output_group = "No Group"
                i += 1
                '''debe buscar el ultimo id ingresado, ahora se manda el 1 pero debe buscar el ultimo id ingresado enla tabla activity'''
                post_data = {"allocation_comment": '1'}
                response = requests.post(
                        "http://127.0.0.1:8000/inti/request_Activity/", data=post_data)
                al = response.json()
                content = al.get('response')
                if content == '0':
                    content1 = al.get('response1')
                    post_data = {"activity_id": content1,
                            "intermediate_exchange_id": intermediate_exchange_id,
                            "variable_name": variable_name,
                            "input_group": input_group,
                            "output_group": output_group}
                    response = requests.post("http://127.0.0.1:8000/inti/activities_intermediate_exchange/", data=post_data)
        print("modellingAndValidations = xmlReader.getElementsByTagName(modellingAndValidation)")
        i = 0 #contador para comprabar la cantidad que se ingresa en la tabla
        modellingAndValidations = xmlReader.getElementsByTagName("modellingAndValidation")
        for modellingAndValidation in modellingAndValidations:
            for review in modellingAndValidation.getElementsByTagName("review"):
                reviewerName = review.getAttribute("reviewerName")
                '''obtener el id de la persona en base al nombre dado los diferentes id's por las versiones'''
                post_data = {"name": reviewerName}
                response = requests.post(
                        "http://127.0.0.1:8000/inti/request_ActivityPerson/", data=post_data)
                al = response.json()
                content = al.get('response')
                if content == '0':
                    content1 = al.get('response1')
                    content2 = al.get('respuesta2')
                    post_data = {"person_id": content1,
                         "activity_id": content2}
                    response = requests.post("http://127.0.0.1:8000/inti/activities_intermediate_exchange/", data=post_data)
                    
    return