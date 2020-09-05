from django.urls import path
from .views import homeview, create, delete, get_svg

urlpatterns = [
    path('', homeview, name='home'),
    path('create/', create, name='create'),
    path('<int:id>/delete', delete, name='delete'),
    path('plot/', get_svg, name='plot'),
]

