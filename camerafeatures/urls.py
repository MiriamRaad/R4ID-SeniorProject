from django.urls import path
from .views import FaceRecgrender, Livestreamingrender , getcloudinarypics

urlpatterns = [
    path('fr', FaceRecgrender, name='facerecognition'),
    path('ls', Livestreamingrender, name='livestreaming'),
    path('ci', getcloudinarypics, name='captureimages'),
]