from django.urls import include, path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('tours/', views.TourListView.as_view(), name='tours'),
    path('tour/<int:pk>', views.TourDetailView.as_view(), name='tour-detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
