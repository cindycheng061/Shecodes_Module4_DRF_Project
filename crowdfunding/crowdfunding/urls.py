"""
URL configuration for crowdfunding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
# from rest_framework.authtoken.views import obtain_auth_token
from users.views import CustomAuthToken #import custom token view
from projects.views import UserProjectList, UserPledgeList
urlpatterns = [  
    path('admin/', admin.site.urls),
    path('',include ('projects.urls')),
    path('', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('api-token-auth/', obtain_auth_token,name='api_token_auth'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),  # use custom token view
    path('api/user-projects/', UserProjectList.as_view(), name='user-projects'), # request user's projects
    path('api/user-pledges/', UserPledgeList.as_view(), name='user-pledges'), 
]
