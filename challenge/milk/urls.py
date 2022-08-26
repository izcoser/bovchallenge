from django.urls import path
from milk import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('farmers/', views.farmer_list),
    path('farms/', views.farm_list),
    path('deliveries/', views.deliveries_list),
    path('farmer_output/', views.farmer_output),
    path('farmer_output/<str:farmer_code>', views.farmer_output),
    path('farmer_output/<str:farmer_code>/<int:month>', views.farmer_output),
]

urlpatterns = format_suffix_patterns(urlpatterns)