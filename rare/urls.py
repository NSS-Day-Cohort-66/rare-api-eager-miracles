"""
URL configuration for rare project.

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
from django.conf.urls import include
from django.urls import path
from rareapi.views import register_user, login_user, PostView, TagViewSet, PostReactionView
from django.conf.urls import include
from rest_framework import routers
from rareapi.views import CategoryViewSet
from rareapi.views import ReactionViewSet, RareUserView, SubscriptionViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'posts', PostView, 'post')
router.register(r'reactions', ReactionViewSet, 'reaction')
router.register(r'tags', TagViewSet, 'tag')
router.register(r'postreactions', PostReactionView, 'postreaction')
router.register(r'rareusers', RareUserView, 'rareuser')
router.register(r'subscriptions', SubscriptionViewSet, 'subscription')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]
