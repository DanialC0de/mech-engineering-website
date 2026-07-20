from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class StudentPanelAccessTests(TestCase):
    def setUp(self):
        self.professor = CustomUser.objects.create_user(
            username='professor-access-test',
            phone_number='09120000001',
            password='test-password',
            role='professor',
        )

    def test_professor_receives_403_for_student_panel(self):
        self.client.force_login(self.professor)

        response = self.client.get(reverse('students:panel'))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertContains(
            response,
            'اجازه ورود به این بخش را ندارید',
            status_code=403,
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('students:panel'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_wrong_role_api_request_returns_json_403(self):
        self.client.force_login(self.professor)

        response = self.client.get(
            reverse('students:dashboard_data'),
            HTTP_ACCEPT='application/json',
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'error': 'دسترسی غیرمجاز'})
