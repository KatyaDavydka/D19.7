from django.urls import path
from .views import IndexView, ConfirmUser

urlpatterns = [
    path('', IndexView.as_view(), name="profile"),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),

]