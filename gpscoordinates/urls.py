from django.urls import path
from .views import locationstreamingrender

urlpatterns = [
    path('ps', locationstreamingrender, name='locationstreaming'),

]