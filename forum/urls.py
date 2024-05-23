from django.urls import path
from . import views
app_name = 'forum'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('list', views.ForumListView.as_view(), name='forum_list'),
    path('list/<int:category_id>', views.ForumListView.as_view(), name='forum_list'),
    path('city-problems/<int:pk>/', views.CityProblemDetailView.as_view(), name='city_problem_detail'),
    path('cityproblems/', views.CityProblemListView.as_view(), name='cityproblem_list'),
    path('cityproblem/new/', views.CityProblemCreateView.as_view(), name='cityproblem_create'),
    path('cityproblem/<int:pk>/update/', views.CityProblemUpdateView.as_view(), name='cityproblem_update'),
    path('cityproblem/<int:pk>/delete/', views.CityProblemDeleteView.as_view(), name='cityproblem_delete'),
]