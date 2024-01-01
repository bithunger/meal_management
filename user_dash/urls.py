"""meal_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from user_dash import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user-dashboard/manage-meal', views.manage_meal, name='manage-meal'),
    path('user-dashboard/add_or_off_meal', views.add_or_off_meal, name='add-or-off-meal'),
    path('user-dashboard/total-meal', views.total_meal, name='total-meal'),
    path('user-dashboard/add-bazar', views.add_bazar, name='add-bazar'),
    path('user-dashboard/total-bazar', views.total_bazar, name='total-bazar'),
    path('user-dashboard/partial-off-meal', views.partial_off_meal, name='partial-off-meal'),
    
    path('user-dashboard/profile', views.profile, name='profile'),
    
    path('user-dashboard/partial-delete/<int:pk>', views.partial_delete, name='partial-delete'),
    path('user-dashboard/del-all-meal', views.delete_all_meal, name='delete_all_meal'),
    path('user-dashboard/del-all-bazar', views.delete_all_bazar, name='delete_all_bazar')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
