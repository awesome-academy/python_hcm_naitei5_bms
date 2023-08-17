from django.urls import include, path
from . import views
from django.conf.urls.static import static
from .views import  BookTourView

urlpatterns = [
    path('', views.index, name='index'),
    path('tour/<int:tour_id>/book/', BookTourView.as_view(), name='book-tour'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour-detail'),
    path('tour/<int:pk>/submit-reply/', views.submit_reply_comment, name='submit-reply-comment'),
    path('tour/<int:tour_id>/submit-rating/', views.submit_rating, name='submit-rating'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('bookings/', views.list_bookings, name='list-bookings'),
    path("signup/", views.sign_up, name="signup"),
    path("signup/send-mail-success/", views.send_mail_success, name="send-mail-success"),
    # path('tour/<int:pk>/rate-comment/', views.tour_rating_comment, name='tour-rating-comment'),
    # path('tour/<int:pk>/submit-comment/', views.submit_comment, name='submit-comment'),
    path('tour/<int:pk>/submit-reply-comment/', views.submit_reply_comment, name='submit-reply-comment'),
    path('approve-tours/', views.approve_tours, name='approve-tours'),
    path('toggle-favorite/<int:tour_id>/', views.toggle_favorite_tour, name='toggle-favorite-tour'),
    path('favorite-tours/', views.favorite_tours_list, name='favorite-tours-list'),
    path('upload-tour-data/', views.upload_tour_data, name='upload_tour_data'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
]
