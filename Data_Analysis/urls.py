from django.urls import path 
from . import views


urlpatterns = [
    path("", views.import_and_preprocess_data, name="import_data"),
    path(
        "success_page/<path:processed_data_html>/<str:data_name>/", 
        views.success_page, 
        name="success_page"
    ),
    path(
        "my_data/",
        views.my_data,
        name="my_data"
    ),
    ]