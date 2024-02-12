from django.test import TestCase

from zedasignal_backend.apps.users.models import (
    Client,
    Technician,
    TechnicianType,
    User,
)


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


class TestTechnicianModel(TestCase):
    # Defining values for test data fields
    technician_type_title = "Automobile Engineer"
    professional_summary = "I'm a professional Engineer with 6+ Years of experience"
    country = "Nigeria"
    city = "Lagos"
    lga = "Victoria Island"
    work_address = "123, Lagos Island"
    services = "Cleaning Service"

    def create_technician_user(self, email):
        test_type = TechnicianType.objects.create(title="Automobile Engineer")
        user = User.user_manager.create_user(
            email=email,
            password="polymarq",
            first_name="John",
            last_name="Doe",
            phone_number="+234800000000",
            longitude=0,
            latitude=0,
            is_technician=True,
        )
        return Technician.objects.create(
            user=user,
            country=self.country,
            city=self.city,
            services=self.services,
            local_government_area=self.lga,
            job_title=test_type,
            work_address=self.work_address,
            professional_summary=self.professional_summary,
        )

    def test_model_fields(self):
        technician = self.create_technician_user("user@example.com")
        self.assertEqual(technician.job_title.title, self.technician_type_title)
        self.assertEqual(technician.professional_summary, self.professional_summary)
        self.assertEqual(technician.country, self.country)
        self.assertEqual(technician.city, self.city)
        self.assertEqual(technician.local_government_area, self.lga)
        self.assertEqual(technician.work_address, self.work_address)
        self.assertEqual(technician.services, self.services)


class TestClientModel(TestCase):
    # Defining values for test data fields
    address = "123, Lagos Island"
    email = "userClient@example.com"
    account_type = "individual"

    def create_client_user(self, email):
        user = User.user_manager.create_user(
            email=email,
            password="polymarq",
            first_name="John",
            last_name="Doe",
            phone_number="+234800000000",
            longitude=0,
            latitude=0,
            is_client=True,
        )
        return Client.objects.create(user=user, address=self.address)

    def test_model_fields(self):
        self.user = self.create_client_user(self.email)
        self.assertEqual(self.user.user.email, self.email)
        self.assertEqual(self.user.address, self.address)
        self.assertEqual(self.user.account_type, self.account_type)


class TechnicianTypeModelTest(TestCase):
    title = "Test Title"

    def test_title_field(self):
        type_test = TechnicianType.objects.create(title=self.title)
        self.assertEqual(type_test.title, self.title)
