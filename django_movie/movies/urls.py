from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


# urlpatterns = [
#     path('movie/', views.MovieListView.as_view()),
#     path('movie/<int:pk>/', views.MovieDetailView.as_view()),
#     path('review/', views.ReviewCreateView.as_view()),
#     path('rating/', views.AddStarRatingView.as_view()),
#     path('actor/', views.ActorsView.as_view()),
#     path('actor/<int:pk>', views.ActorDetailView.as_view())
# ]


urlpatterns = format_suffix_patterns([
    path('movie/', views.MovieListViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', views.MovieListViewSet.as_view({'get': 'retrieve'})),
    path('review/', views.ReviewCreateView.as_view({'post': 'create'})),
    path('rating/', views.AddStarRatingView.as_view({'post': 'create'})),
    path('actor/', views.ActorsView.as_view({'get': 'list'})),
    path('actor/<int:pk>', views.ActorsView.as_view({'get': 'retrieve'}))
])
