from django.urls import path
from .views import login_view, signup_view, logout_view, dashboard, add_skill, delete_skill

urlpatterns = [
    path('', login_view, name='login'),      # first page = login
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-skill/', add_skill, name='add_skill'),
    path('delete-skill/<int:skill_id>/', delete_skill, name='delete_skill'),
]
