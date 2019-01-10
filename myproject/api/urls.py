from django.urls import path
from .views import ItemsView, ItemView

app_name = 'api'

urlpatterns = [
    path('items/', ItemsView.as_view(), name = 'items'),
    path('item/<int:pk>', ItemView.as_view(), name = 'item'),
]