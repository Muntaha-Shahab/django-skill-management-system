
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Skill


class SkillManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!"
        )
        self.client.login(
            username="testuser",
            password="TestPassword123!"
        )

    def test_login_page_loads(self):
        self.client.logout()
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        self.client.logout()
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_logged_in_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_add_skill(self):
        response = self.client.post(
            reverse("add_skill"),
            {
                "skill_name": "Python",
                "proficiency_level": "Intermediate",
                "years_of_experience": 2,
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(
            Skill.objects.filter(
                user=self.user,
                skill_name="Python",
            ).exists()
        )

    def test_user_can_delete_own_skill(self):
        skill = Skill.objects.create(
            user=self.user,
            skill_name="Django",
            proficiency_level="Beginner",
            years_of_experience=1,
        )

        response = self.client.get(
            reverse("delete_skill", args=[skill.id])
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertFalse(Skill.objects.filter(id=skill.id).exists())

    def test_user_cannot_delete_another_users_skill(self):
        another_user = User.objects.create_user(
            username="anotheruser",
            password="AnotherPassword123!",
        )
        skill = Skill.objects.create(
            user=another_user,
            skill_name="Java",
            proficiency_level="Advanced",
            years_of_experience=3,
        )

        self.client.get(reverse("delete_skill", args=[skill.id]))

        self.assertTrue(Skill.objects.filter(id=skill.id).exists())

    def test_signup_creates_user(self):
        self.client.logout()

        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "NewPassword123!",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_invalid_login_shows_error(self):
        self.client.logout()

        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "WrongPassword!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")
