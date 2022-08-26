from django.urls import path
from milk import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('costs/', views.costs),
    path('farmers/', views.farmer_list),
    path('farms/', views.farm_list),
    path('deliveries/', views.deliveries_list),
    path('farmer_output/<str:farmer_code>/<int:month>/<int:year>', views.farmer_output),
    path('farmer_monthly_price/<str:farmer_code>/<int:month>/<int:year>', views.farmer_monthly_price),
    path('farmer_yearly_price/<str:farmer_code>/<int:year>', views.farmer_yearly_price),
]

urlpatterns = format_suffix_patterns(urlpatterns)