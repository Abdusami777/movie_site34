from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from .models import (
    UserProfile, Category, Country, Director, Actor, Genre,
    Movie, MovieLanguages, MovieMoments, Rating, Review,
    Favorite, History,
)


# ---------- Movie үчүн inline'дар ----------
class MovieLanguagesInline(TranslationTabularInline):
    model = MovieLanguages
    extra = 1


class MovieMomentsInline(admin.TabularInline):
    model = MovieMoments
    extra = 1


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    fk_name = 'movie'


@admin.register(Movie)
class MovieAdmin(TabbedTranslationAdmin):
    list_display = ('movie_name', 'year', 'category', 'status_movie')
    list_filter = ('category', 'status_movie', 'year')
    search_fields = ('movie_name',)
    inlines = [MovieLanguagesInline, MovieMomentsInline, RatingInline, ReviewInline]


# ---------- UserProfile үчүн inline'дар ----------
class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0


class HistoryInline(admin.TabularInline):
    model = History
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Кошумча маалымат', {'fields': ('phone_number', 'age', 'avatar', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Кошумча маалымат', {'fields': ('phone_number', 'age', 'avatar', 'status')}),
    )
    inlines = [FavoriteInline, HistoryInline]


# ---------- Review: жооптор (replies) inline ----------
class ReplyInline(admin.TabularInline):
    model = Review
    fk_name = 'parent'
    extra = 0
    verbose_name = 'Жооп'
    verbose_name_plural = 'Жооптор'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'parent', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username', 'movie__movie_name', 'text')
    inlines = [ReplyInline]


# ---------- EN / RU / KY кнопкалары бар моделдер ----------
@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    pass


@admin.register(Country)
class CountryAdmin(TabbedTranslationAdmin):
    pass


@admin.register(Director)
class DirectorAdmin(TabbedTranslationAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(TabbedTranslationAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(TabbedTranslationAdmin):
    pass


# ---------- Rating, Favorite, History ----------
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'stars')
    list_filter = ('stars',)
    search_fields = ('movie__movie_name', 'user__username')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie')
    search_fields = ('user__username', 'movie__movie_name')


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'viewed_date')
    list_filter = ('viewed_date',)
    search_fields = ('user__username', 'movie__movie_name')