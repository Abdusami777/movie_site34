from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS_CHOICES = (
    ('simple', 'Simple'),
    ('pro', 'Pro'),
)

TYPE_CHOICES = (
    ('360', '360p'),
    ('480', '480p'),
    ('720', '720p'),
    ('1080', '1080p'),
    ('2K', '2K'),
    ('4K', '4K'),
)


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True, region="KG")
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)],
        blank=True, null=True
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='simple')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        null=True, blank=True
    )
    image = models.ImageField(upload_to='directors/', null=True, blank=True)

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
        null=True, blank=True
    )
    image = models.ImageField(upload_to='actors/', null=True, blank=True)

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=255)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director)
    actor = models.ManyToManyField(Actor)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    types = models.CharField(max_length=20, choices=TYPE_CHOICES, default='720')
    movie_time = models.PositiveIntegerField(help_text="Minutes")
    trailer = models.URLField()
    description = models.TextField()
    movie_image = models.ImageField(upload_to='movies/')
    status_movie = models.CharField(max_length=20, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.movie_name


class MovieLanguages(models.Model):
    language = models.CharField(max_length=50)
    video = models.FileField(upload_to='movie_videos/')
    movie = models.ForeignKey(Movie, related_name='movie_languages', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.movie_name} - {self.language}"


class MovieMoments(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie_moments', on_delete=models.CASCADE)
    movie_image = models.ImageField(upload_to='movie_moments/')

    def __str__(self):
        return f"{self.movie.movie_name} moment"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.movie.movie_name} - {self.stars} stars by {self.user.username}"


class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.movie_name}"


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.movie.movie_name}"


class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} watched {self.movie.movie_name} at {self.viewed_date}"