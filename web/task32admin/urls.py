"""setting32admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import application.views as avrora


urlpatterns = [
    path('', avrora.index),
    path('admin/', admin.site.urls),
    path('avrora_leave/user_<int:pk>/<int:vv>/', avrora.avrora),
    path('avrora_leave/new_leave/', avrora.new_avrora),
    path('revenue_calculation/<str:id_project>', avrora.revenue_calculation)
]

#handler404 = "application.views.page_not_found_view_400"
#handler500 = "application.views.page_not_found_view_500"