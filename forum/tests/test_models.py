from django.test import TestCase
import factory
from factory.django import DjangoModelFactory

from forum.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = (factory.Faker("lorem", nb_words=2),)
    slug = (factory.Faker("lorem", nb_words=1),)
    description = (factory.Faker("lorem", nb_words=250),)
    url = ("https://test.test/",)
    hexcolor = factory.Faker("color")


class CategoryTest(TestCase):
    def test_category_creation(self):
        w = CategoryFactory()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__str__(), w.slug)
