from rest_framework.pagination import PageNumberPagination
from rest_framework.routers import DefaultRouter

from IntiApp.viewsApi import version_viewsets, company_viewsets, geography_viewsets, person_viewsets, unit_viewsets, activity_viewsets, activity_intermediate_exchange_viewsets, activity_index_viewsets, activity_name_viewsets, activity_person_viewsets, data_generator_publication_viewsets, intermediate_exchange_viewsets, property_viewsets, source_viewsets, synonym_viewsets, system_model_viewsets, version_name_index_viewsets


router = DefaultRouter()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 25

router.register(r'activities',activity_viewsets.ActivityViewSet, basename= 'activity')
router.register(r'versions',version_viewsets.VersionViewSet, basename= 'version')
router.register(r'companies',company_viewsets.CompanyViewSet, basename='company')
router.register(r'people',person_viewsets.PersonViewSet, basename='person')
router.register(r'geographies',geography_viewsets.GeographyViewSet, basename='geography')
router.register(r'units',unit_viewsets.UnitViewSet, basename='unit')
router.register(r'activities_intermediate_exchange',activity_intermediate_exchange_viewsets.ActivityIntermediateExchangeViewSet, basename= 'activity intermediate exchange')
router.register(r'activities_index',activity_index_viewsets.ActivityIndexViewSet, basename= 'activity index')
router.register(r'activities_name',activity_name_viewsets.ActivityNameViewSet, basename= 'activity name')
router.register(r'activities_person',activity_person_viewsets.ActivityPersonViewSet, basename= 'activity person')
router.register(r'data_generator_publications',data_generator_publication_viewsets.DataGeneratorAndPublicationViewSet, basename= 'data generator and publications')
router.register(r'intermediate_exchanges',intermediate_exchange_viewsets.IntermediateExchangeViewSet, basename= 'intermediate exchange')
router.register(r'properties',property_viewsets.PropertyViewSet, basename= 'property')
router.register(r'sources',source_viewsets.SourceViewSet, basename= 'source')
router.register(r'synonyms',synonym_viewsets.SynonymViewSet, basename= 'synonym')
router.register(r'system_models',system_model_viewsets.SystemModelViewSet, basename= 'system model')
router.register(r'version_name_indexes',version_name_index_viewsets.VersionNameIndexViewSet, basename= 'version name index')


urlpatterns = router.urls