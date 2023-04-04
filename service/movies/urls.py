# yapf: disable
from django.urls import path
from movies.login import Login, Registration
from movies.views import index

urlpatterns = [
    path('', index),
    path("logout", Login.logout),
    # path("login/", login.urls),
]
