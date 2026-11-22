from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import (
    UserProfile, Category, Country, Director, Actor, Genre,
    Movie, MovieLanguages, MovieMoments, Rating, Review,
    Favorite, History
)


# --- ҮЙ ТАПШЫРМАСЫ: REGISTER & LOGIN SERIALIZERS ---
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


# --- ПРОЕКТТИН НЕГИЗГИ SERIALIZER-ЛЕРИ ---
class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'avatar']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['id', 'language', 'video']


class MovieMomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieMoments
        fields = ['id', 'movie_image']


class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_name']


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y')
    country = CountrySerializer(many=True)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'year', 'country', 'genre', 'movie_image', 'status_movie']


class CategoryDetailSerializer(serializers.ModelSerializer):
    movie_set = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'movie_set']


class CountryDetailSerializer(serializers.ModelSerializer):
    movie_set = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['country_name', 'movie_set']


class DirectorDetailSerializer(serializers.ModelSerializer):
    movie_set = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Director
        fields = ['director_name', 'bio', 'age', 'image', 'movie_set']


class ActorDetailSerializer(serializers.ModelSerializer):
    movie_set = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['actor_name', 'bio', 'age', 'image', 'movie_set']


class GenreDetailSerializer(serializers.ModelSerializer):
    movie_set = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['genre_name', 'movie_set']


class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    user = UserProfileListSerializer()

    class Meta:
        model = Review
        fields = ['id', 'user', 'created_date', 'text', 'parent']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%d-%m-%Y')
    country = CountrySerializer(many=True)
    director = DirectorSerializer(many=True)
    actor = ActorSerializer(many=True)
    genre = GenreSerializer(many=True)
    movie_languages = MovieLanguagesSerializer(many=True, read_only=True)
    movie_moments = MovieMomentsSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'movie_name', 'movie_image', 'year', 'country', 'director',
            'genre', 'types', 'movie_time', 'actor', 'trailer',
            'description', 'status_movie', 'movie_languages',
            'movie_moments', 'reviews'
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    movie = MovieNameSerializer()
    viewed_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = History
        fields = ['id', 'movie', 'viewed_date']