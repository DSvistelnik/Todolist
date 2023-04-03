from django.urls import path
from core.views import main_page

# -----------------------------------------------------------------------

urlpatterns = [
    path("", main_page),
]