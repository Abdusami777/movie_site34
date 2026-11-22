from django.urls import path, include
from rest_framework import routers
from .views import (
    RegisterView, LoginView, LogoutView,
    UserProfileListAPIView, UserProfileDetailAPIView,
    CategoryListAPIView, CategoryDetailAPIView,
    GenreListAPIView, GenreDetailAPIView,
    MovieListAPIView, MovieDetailAPIView,
    CountryListAPIView, CountryDetailAPIView,
    DirectorListAPIView, DirectorDetailAPIView,
    ActorListAPIView, ActorDetailAPIView,
    RatingViewSet, ReviewCreateAPIView, ReviewEditAPIView,
    FavoriteViewSet, HistoryAPIView
)

router = routers.SimpleRouter()
router.register(r'rating', RatingViewSet)
router.register(r'favorite', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # JWT Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),

    # Category & Genre
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('genre/', GenreListAPIView.as_view(), name='genre_list'),
    path('genre/<int:pk>/', GenreDetailAPIView.as_view(), name='genre_detail'),

    # Movie
    path('movie/', MovieListAPIView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailAPIView.as_view(), name='movie_detail'),

    # Country, Director, Actor
    path('country/', CountryListAPIView.as_view(), name='country_list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country_detail'),
    path('director/', DirectorListAPIView.as_view(), name='director_list'),
    path('director/<int:pk>/', DirectorDetailAPIView.as_view(), name='director_detail'),
    path('actor/', ActorListAPIView.as_view(), name='actor_list'),
    path('actor/<int:pk>/', ActorDetailAPIView.as_view(), name='actor_detail'),

    # Review & History
    path('review/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('review/<int:pk>/', ReviewEditAPIView.as_view(), name='review_edit'),
    path('history/', HistoryAPIView.as_view(), name='movie_history'),
]