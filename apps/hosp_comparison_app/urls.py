from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.comparison_link, name="comparison_link"),
    url(r'^gencomparison$', views.comparison_route, name="comparison_route"),
    url(r'^specific_hospital$', views.spec_hosp_link, name="spec_hosp_link"),
    url(r'^genspecific$', views.spec_hosp_route, name="spec_hosp_route"),
    url(r'^about$', views.about_link, name="about_link"),
    # url(r'^specific_drg$', views.spec_drg_link, name="spec_drg_link"),
]