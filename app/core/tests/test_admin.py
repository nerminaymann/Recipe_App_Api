from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.admin_user = User.objects.create_superuser(email='admin@example.com',password='12345')

        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(email='user@example.com',password='12345',name='Test User')

    def test_users_list(self):
        #test that users are listed on the admin page

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res,self.user.email)
        self.assertContains(res,self.user.name)

    def test_edit_user_page(self):
        #test the edit user page works
        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        #test the create user page works
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

