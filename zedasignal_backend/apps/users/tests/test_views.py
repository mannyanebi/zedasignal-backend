import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from zedasignal_backend.apps.users.forms import UserAdminChangeForm
from zedasignal_backend.apps.users.models import (
    Client,
    Technician,
    TechnicianType,
    User,
)
from zedasignal_backend.apps.users.tests.factories import BaseTestCase, UserFactory
from zedasignal_backend.apps.users.views import (
    UserRedirectView,
    UserUpdateView,
    user_detail_view,
)
from zedasignal_backend.core.utils.base64_samples import image1

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request
        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        form = UserAdminChangeForm()
        form.cleaned_data = {}
        form.instance = user
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [_("Information successfully updated")]


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request
        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()
        response = user_detail_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"


class TestTechnicianView(BaseTestCase):
    # Defining values for test data fields
    technician_type_title = "Automobile Engineer"
    professional_summary = "I'm a professional Engineer with 6+ Years of experience"
    address = "123, Lagos Island"
    email = "user@example.com"
    username = "userTech"

    @classmethod
    def setUpTestData(cls):
        cls.test_type = TechnicianType.objects.create(title="Automobile Engineer")
        cls.technician_data = {
            "user": {
                "email": "userTech@example.com",
                "username": "userTech2",
                "first_name": "Tech",
                "last_name": "1",
                "password": "12345678",
                "phone_number": "08080000000",
                "longitude": 0,
                "latitude": 0,
            },
            "professional_summary": cls.professional_summary,
            "country": "Nigeria",
            "city": "Lagos",
            "local_government_area": "Alimosho",
            "work_address": "Ikotun",
            "services": "Home Maintenance",
            "years_of_experience": 9,
            "job_title": cls.test_type.pk,
        }
        cls.user = cls.create_technician_user(cls, cls.email)

    def create_technician_user(self, email):
        user = User.user_manager.create_user(
            email=email,
            username=self.username,
            password="polymarq",
            first_name="John",
            last_name="Doe",
            phone_number="+234800000000",
            longitude=0,
            latitude=0,
            is_technician=True,
            is_active=True,
        )
        technician_data = self.technician_data.copy()
        technician_data.pop("user")
        technician_data.pop("job_title")
        return Technician.objects.create(
            user=user, **technician_data, job_title=self.test_type
        )

    def test_register_technician(self):
        url = reverse("auth-api:technician-user-register")
        self.technician_data["user"]["password"] = "polymarq33"
        response = self.client.post(
            url, self.technician_data, content_type="application/json"
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json.get("message"), "Technician registered successfully"
        )

    def test_register_technician_with_certificate(self):
        url = reverse("auth-api:technician-user-register")
        self.technician_data["user"]["password"] = "polymarqCert33"
        self.technician_data["certificate"] = image1
        response = self.client.post(
            url, self.technician_data, content_type="application/json"
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_json.get("message"), "Technician registered successfully"
        )

    def test_get_technicians_list(self):
        url = reverse("api:technician-profiles-list")
        response = self.client.get(url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["count"], 1)
        self.assertEqual(
            response_json["result"]["data"][0]["uuid"], str(self.user.uuid)
        )
        self.assertEqual(
            response_json["result"]["data"][0]["professionalSummary"],
            self.professional_summary,
        )

    def test_get_single_technician(self):
        url = reverse("api:technician-user-profile", args=[self.user.uuid])
        response = self.client.get(url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["uuid"], str(self.user.uuid))
        self.assertEqual(
            response_json["result"]["professionalSummary"], self.professional_summary
        )

    def test_update_single_technician(self):
        url = reverse("api:technician-user-profile", args=[self.user.uuid])
        work_address = "456, Lagos Island"

        response = self.client.patch(
            url,
            data=dict(work_address=work_address),
            headers=self.headers,
            content_type="application/json",
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 202)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["workAddress"], work_address)

    def test_delete_single_technician(self):
        url = reverse("api:technician-user-profile", args=[self.user.uuid])
        response = self.client.delete(url, headers=self.headers)
        technicians = Technician.objects.filter(uuid=self.user.uuid, is_deleted=False)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(technicians.count(), 0)


class TechnicianTypeView(BaseTestCase):
    title = "Automobile engineer"
    email = "userType@example.com"
    username = "userType"

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_technician_user(cls, cls.email)
        cls.technician_type = TechnicianType.objects.create(title=cls.title)

    def create_technician_user(self, email):
        return User.user_manager.create_user(
            email=email,
            username=self.username,
            password="polymarq",
            first_name="John",
            last_name="Doe",
            phone_number="+234800000000",
            longitude=0,
            latitude=0,
            is_technician=True,
            is_active=True,
        )

    def test_create_technician_type(self):
        url = reverse("api:technician-types")
        title = "Home Maintenance"
        response = self.client.post(
            url,
            data=dict(title=title),
            headers=self.headers,
            content_type="application/json",
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response_json["result"], dict)
        self.assertEqual(response_json["result"]["title"], title)

    def test_technician_types_list(self):
        url = reverse("api:technician-types")
        response = self.client.get(url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json["result"], dict)
        self.assertEqual(response_json["result"]["count"], 1)

    def test_get_single_technician_type(self):
        test_title = "Test Title 3"
        test_type = TechnicianType.objects.create(title=test_title)
        url = reverse("api:technician-types-detail", args=[test_type.uuid])
        response = self.client.get(url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json["result"], dict)
        self.assertEqual(response_json["result"]["title"], test_title)

    def test_update_single_technician_type(self):
        test_title = "Test Title 4"
        test_type = TechnicianType.objects.create(title=test_title)
        url = reverse("api:technician-types-detail", args=[test_type.uuid])
        title = "Home automations"

        response = self.client.patch(
            url,
            data=dict(title=title),
            headers=self.headers,
            content_type="application/json",
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 202)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["title"], title)

    def test_delete_single_technician_type(self):
        test_type = TechnicianType.objects.create(title="IT Technician")
        url = reverse("api:technician-types-detail", args=[test_type.uuid])
        response = self.client.delete(url, headers=self.headers)
        types = TechnicianType.objects.filter(id=test_type.id)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(types.count(), 0)


class TestClientView(BaseTestCase):
    # Defining values for test data fields
    address = "123, Lagos Island"
    email = "userClient@example.com"
    username = "userClient"

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_client_user(cls, cls.email)
        cls.client_data = {
            "user": {
                "email": "polymarqClient@example.com",
                "username": "polymarqClient",
                "first_name": "polymarq",
                "last_name": "client",
                "password": "polymarqClient",
                "phone_number": "0808000000",
                "longitude": 0,
                "latitude": 0,
            },
            "account_type": "individual",
            "address": cls.address,
        }

    def create_client_user(self, email):
        user = User.user_manager.create_user(
            email=email,
            username=self.username,
            password="polymarq",
            first_name="John",
            last_name="Doe",
            phone_number="+234800000000",
            longitude=0,
            latitude=0,
            is_client=True,
            is_active=True,
        )
        return Client.objects.create(
            user=user,
            address=self.address,
        )

    def test_register_client(self):
        url = reverse("auth-api:client-user-register")
        response = self.client.post(
            url, self.client_data, content_type="application/json"
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json.get("message"), "Client registered successfully")

    def test_get_clients_list(self):
        url = reverse("api:client-profiles-list")
        response = self.client.get(url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["count"], 1)
        self.assertEqual(
            response_json["result"]["data"][0]["uuid"], str(self.user.uuid)
        )
        self.assertEqual(response_json["result"]["data"][0]["address"], self.address)

    def test_get_single_client(self):
        url = reverse("api:client-user-profile", args=[self.user.uuid])
        response = self.client.get(url, headers=self.headers)
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["uuid"], str(self.user.uuid))
        self.assertEqual(response_json["result"]["address"], self.address)

    def test_update_single_client(self):
        url = reverse("api:client-user-profile", args=[self.user.uuid])
        address = "456, Lagos Island"

        response = self.client.patch(
            url,
            data=dict(address=address),
            headers=self.headers,
            content_type="application/json",
        )
        response_json = response.json()

        self.assertEqual(response.status_code, 202)
        self.assertIsInstance(response_json, dict)
        self.assertEqual(response_json["result"]["address"], address)

    def test_delete_single_client(self):
        url = reverse("api:client-user-profile", args=[self.user.uuid])
        response = self.client.delete(url, headers=self.headers)
        clients = Technician.objects.filter(uuid=self.user.uuid, is_deleted=False)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(clients.count(), 0)
