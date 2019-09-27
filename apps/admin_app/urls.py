from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.admin_dashboard_link, name="admin_dashboard_link"),
    url(r'^login$', views.login_route, name="login_route"),
    url(r'^logout$', views.logout_route, name="logout_route"),
    url(r'^admin$', views.admin_dashboard_link, name="admin_dashboard_link"),
    url(r'^hospital/add$', views.add_hospital_route, name="add_hospital_route"),
    # url(r'^hospital/update$', views.add_hospital_route, name="edit_hospital_route"),
    url(r'^hospital/remove$', views.remove_hospital_route, name="remove_hospital_route"),
    url(r'^drg/update$', views.update_drg_route, name="update_drg_route"),
    # url(r'^ping_sources_route$', views.ping_sources_route, name="ping_sources_route"),
]