from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile


class CustomUserTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@t.com',
            password='tpassword',
            age=23
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@t.com')
        self.assertEqual(self.user.age, 23)
        self.assertTrue(self.user.check_password('tpassword'))


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.profile = self.user.profile
        self.profile.date_of_birth = '2001-12-12'
        self.profile.fav_author = 'Archer'
        self.profile.save()

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(str(self.profile.date_of_birth), '2001-12-12')
        self.assertEqual(self.profile.fav_author, 'Archer')

    def test_profile_str_representation(self):
        self.assertEqual(str(self.profile), 'testuser')


class ProfileViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.profile = self.user.profile
        self.profile.date_of_birth = '2001-12-12'
        self.profile.fav_author = 'Archer'
        self.profile.save()

    def test_profile_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('accounts:show_profile', args=[self.profile.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/user_profile.html'
        )

    def test_edit_profile_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('accounts:edit_profile', args=[self.profile.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'registration/edit_profile.html'
        )