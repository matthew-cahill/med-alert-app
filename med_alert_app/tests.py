# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'med_alert_project.settings'

import django
# django.setup()
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from med_alert_app.models import Document, SiteAdmin
from django.test import Client, TestCase

@pytest.mark.django_db
class TestUserAccess(TestCase):
    def test_home_page_for_anonymous_user(self):
        client = Client()
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'login.html' in [t.name for t in response.templates]

    def test_home_page_for_common_user(self):
        client = Client()
        user = User.objects.create_user(username='user', password='password')
        client.force_login(user)
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'userpage.html' in [t.name for t in response.templates]

    def test_home_page_for_admin_user(self):
        client = Client()
        user = User.objects.create_user(username='regularuser', password='regularpass')
        admin_user = SiteAdmin.objects.create(user=user)  # Assuming this is how you link a user to a site admin
        client.force_login(user)
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminpage.html')
'''
@pytest.mark.django_db
class TestFileUpload:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='testpass')
        self.client.force_login(self.user)

    def test_upload_file(self):
        upload_file = SimpleUploadedFile("testfile.txt", b"abc", content_type="text/plain")
        response = self.client.post(reverse('uploadfiles'), {'file': upload_file}, follow=True)
        assert response.status_code == 200
        assert Document.objects.count() == 1
        assert Document.objects.first().upload.name.endswith('testfile.txt')
'''
@pytest.mark.django_db
class TestLogout:
    def test_logout_view(self):
        client = Client()
        response = client.get(reverse('logout'), follow=True)
        assert response.status_code == 200
        assert not response.context['user'].is_authenticated
'''
@pytest.mark.django_db
class TestViewFiles:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='testpass')
        self.client.force_login(self.user)
        # Create a dummy file
        Document.objects.create(upload="dummyfile.txt")

    def test_view_files_page(self):
        response = self.client.get(reverse('viewfiles'))
        assert response.status_code == 200
        assert 'viewfiles.html' in [t.name for t in response.templates]
        documents = response.context['documents']
        assert len(documents) == 1
        assert documents[0].upload == "dummyfile.txt"
'''