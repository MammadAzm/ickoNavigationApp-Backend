from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from ickoNavigator.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token),

    path('getAssets/', GetAssetsApiView.as_view()),
    path('call/<int:moduleID>', PassPhone_and_MakeCallQuery.as_view()),  # It Adds the Query too.

    path('sendGPS/', GPSDataApiView.as_view()),
    path('sendStatus/', StatusApiView.as_view()),
    path('getPhone/', GetPhoneApiView.as_view()),

    path('activityHistory/', ActivityHistoryAPIView.as_view()),
    path('loadHistory/', LoadHistoryAPIView.as_view()),
    path('history/raw/<int:moduleID>/<str:startTimeStamp>to<str:tillTimeStamp>', RawHistoryAPIView.as_view()),
    path('history/raw/<int:moduleID>/', rawHistory_redirect),


    # path('callLog/', CallLogApiView.as_view()),  # In Case that the Module is gonna Post the Call Log Details.

    # path("", include("django.contrib.auth.urls")),
]

