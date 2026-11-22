from .models import Category, Genre, Country, Director, Actor, Movie, MovieLanguages
from modeltranslation.translator import translator, TranslationOptions


class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


class GenreTranslationOptions(TranslationOptions):
    fields = ('genre_name',)


class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


class DirectorTranslationOptions(TranslationOptions):
    fields = ('director_name', 'bio')


class ActorTranslationOptions(TranslationOptions):
    fields = ('actor_name', 'bio')


class MovieTranslationOptions(TranslationOptions):
    fields = ('movie_name', 'description')


class MovieLanguagesTranslationOptions(TranslationOptions):
    fields = ('language',)


translator.register(Category, CategoryTranslationOptions)
translator.register(Genre, GenreTranslationOptions)
translator.register(Country, CountryTranslationOptions)
translator.register(Director, DirectorTranslationOptions)
translator.register(Actor, ActorTranslationOptions)
translator.register(Movie, MovieTranslationOptions)
translator.register(MovieLanguages, MovieLanguagesTranslationOptions)