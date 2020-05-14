# for consumers routing

# as we can have multiple consumers, same as we may have multiple views

from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/gallery/$', consumers.CoordConsumer),
]