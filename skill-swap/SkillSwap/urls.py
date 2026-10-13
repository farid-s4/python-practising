from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('proposal/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),
    path('proposal/create/', views.proposal_create, name='proposal_create'),
    path('proposal/<int:proposal_id>/edit/', views.proposal_edit, name='proposal_edit'),
    path('lesson/<int:request_id>/review/', views.review_create, name='review_create'),
    path('myskills/', views.my_skills, name='my_skills'),
    path('my_lesson_requests/', views.my_lesson_requests, name='my_lesson_requests'),
    path('my_lesson_requests/<int:request_id>/status/', views.lesson_request_status, name='lesson_request_status'),
    path('proposal/<int:proposal_id>/lesson_request_create', views.lesson_request_create, name='lesson_request_create'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
]
