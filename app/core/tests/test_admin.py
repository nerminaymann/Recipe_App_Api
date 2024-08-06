from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.admin_user = User.objects.create_superuser('admin@example.com','12345')

        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user('user@example.com','12345','Test User')

    def test_users_list(self):
        #test that users are listed on the admin page

        url = reverse('admin:core_user_changeList')
        res = self.client.get(url)

        self.assertContains(res,self.user.email)
        self.assertContains(res,self.user.name)


