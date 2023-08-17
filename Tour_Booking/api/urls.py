from django.urls import path
from . import api_views

urlpatterns = [
    path('login/', api_views.login_view, name='api-login'),
    path('toggle-favorite/<int:tour_id>/', api_views.toggle_favorite_tour, name='toggle-favorite-tour'),
    path('favorite-tours/', api_views.FavoriteToursListView.as_view(), name='favorite-tours-list'),
]
