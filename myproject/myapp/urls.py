from .views import PassListCreateView
from django.urls import path
from . import views


urlpatterns = [
    path('api/pass/', PassListCreateView.as_view(), name='pass-list-create'),
    path('api/pass/submitData', PassListCreateView.as_view(), name='pass-submit-data'),
    path('submitData/<int:id>/', views.get_submit_data, name='get_submit_data'),
    path('submitData/<int:id>/', views.edit_submit_data, name='edit_submit_data'),
    path('submitData/', views.get_submit_data_by_email, name='get_submit_data_by_email'),
]