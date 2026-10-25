from django.urls import path
from . import views

urlpatterns = [
    path('dealers/', views.get_dealers, name='get_dealers'),
    path('dealers/<int:id>/', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('dealers/state/<str:state>/', views.get_dealers_by_state, name='get_dealers_by_state'),
    path('dealers/<int:id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('cars/', views.get_cars, name='get_cars'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('get_csrftoken/', views.get_csrftoken, name='get_csrftoken'),
    path('analyze-review/', views.analyze_review, name='analyze_review'),
    path('current/', views.current_user, name='current_user'),
]
