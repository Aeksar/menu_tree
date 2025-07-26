from django.test import TestCase, RequestFactory
from django.template import Template, Context
from menu_app.models import MenuItem
from menu_app.templatetags.menu_tags import draw_menu
import json

class MenuItemModelTests(TestCase):
    def setUp(self):
        self.parent = MenuItem.objects.create(
            name="Главная", menu_name="main_menu", url="/", position=1
        )
        self.child1 = MenuItem.objects.create(
            name="Профиль", menu_name="main_menu", url="/profile/", parent=self.parent, position=1
        )
        self.child2 = MenuItem.objects.create(
            name="Портфолио", menu_name="main_menu", url="/portfolio/", parent=self.child1, position=1
        )
        self.sibling = MenuItem.objects.create(
            name="О нас", menu_name="main_menu", url="/about/", position=2
        )

    def test_menu_item_creation(self):
        self.assertEqual(MenuItem.objects.count(), 4)
        self.assertEqual(self.parent.name, "Главная")
        self.assertEqual(self.child1.parent, self.parent)
        self.assertEqual(self.child2.parent, self.child1)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            MenuItem.objects.create(name="Главная", menu_name="main_menu", url="/test/", position=3)
