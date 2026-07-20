from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from students.models import StudentProfile


User = get_user_model()


class StudentRegistrationTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["register_phone"] = "09123456789"
        session.save()

    def test_registration_creates_student_and_redirects_to_student_panel(self):
        response = self.client.post(reverse("register_user"), {
            "first_name": "علی",
            "last_name": "رضایی",
            "student_id": "40123456",
            "major": "مهندسی مکانیک",
            "level": "کارشناسی",
            "entry_year": "1401",
            "term": "ترم ۶",
            "interest": "طراحی جامدات",
            "bio": "دانشجوی مهندسی مکانیک",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["redirect"], reverse("students:panel"))

        user = User.objects.get(phone_number="09123456789")
        self.assertEqual(user.role, "student")
        self.assertEqual(user.username, "40123456")
        self.assertTrue(self.client.session.get("_auth_user_id"))

        profile = StudentProfile.objects.get(user=user)
        self.assertEqual(profile.student_id, "40123456")
        self.assertEqual(profile.entry_year, 1401)

    def test_registration_requires_verified_phone_session(self):
        self.client.session.flush()

        response = self.client.post(reverse("register_user"), {
            "first_name": "علی",
            "last_name": "رضایی",
            "student_id": "40123456",
            "major": "مهندسی مکانیک",
            "level": "کارشناسی",
            "entry_year": "1401",
        })

        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.exists())
