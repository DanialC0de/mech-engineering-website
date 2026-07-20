from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class ProfessorPanelAccessTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student-access-test',
            phone_number='09120000002',
            password='test-password',
            role='student',
        )

    def test_student_receives_403_for_professor_panel(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse('professor:panel'))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
