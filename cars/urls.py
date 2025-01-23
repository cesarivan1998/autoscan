from django.urls import path, include
from rest_framework import routers
from cars import views
from rest_framework.documentation import include_docs_urls
#api versioning
router = routers.DefaultRouter()
router.register(r'cars',views.CarsView, 'cars')
router.register(r'brands',views.BrandsView, 'brands')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="Cars API"))
]