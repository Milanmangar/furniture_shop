from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status

from table.models import Table,  Leg, Feet
from table.serializers_table import serializers as table_serializer


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_table_feet_leg(user):
    # creating 1st table
    Feet.objects.create(name="rounded")
    feet_instance = Feet.objects.get(name__iexact="rounded")
    Leg.objects.create(name="tall flat", feet=feet_instance)
    leg_instance = Leg.objects.get(name__iexact="tall flat")
    Table.objects.create(name="brown iron", description="round top",
                         price=2500, created_by=user, legs=leg_instance)

    # creating 2nd table
    Feet.objects.create(name="flat")
    feet_instance = Feet.objects.get(name__iexact="flat")
    Leg.objects.create(name="rectangle", feet=feet_instance)
    leg_instance = Leg.objects.get(name__iexact="rectangle")
    Table.objects.create(name="steel", description="square top",
                         price=8700, created_by=user, legs=leg_instance)
    # creating extra leg
    Leg.objects.create(name="toy leg", feet=feet_instance)
    return Leg.objects.get(name__iexact="toy leg")


class TestTableApiLoginRequiredTests(TestCase):
    """ Test case for TableViewset login required"""

    def setUp(self):
        self.client = APIClient()
        self.post_data = {
                            "name": "wooden table",
                            "description": "wooden table with rounded top",
                            "price": 2000,
                            "legs": "tall legs"

                        }

    def test_login_required(self):
        """ test to give unauthorized error, if the user is not logged in"""
        url = reverse("table:table_viewset-list")
        res = self.client.post(url, self.post_data , format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTableApiTests(TestCase):
    """ Test case for TableViewset """

    def setUp(self):
        self.data = {
                            "name": "post table",
                            "description": "big wooden table with rounded top",
                            "price": 2000,
                            "legs": "toy leg"
                        }
        self.user = create_user(
            username='test1',
            password='Test1@123',
            email='test1@gmail.com',
            first_name='test1_first',
            last_name='test1_last'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        """ test to create new table, requires authentication"""
        url = reverse("table:table_viewset-list")
        self.data["legs"] = create_table_feet_leg(self.user)
        res = self.client.post(url, self.data)
        table = Table.objects.get(name__iexact="post table")
        serializer = table_serializer.TableSerializer(table)
        expected_data = {"result": serializer.data, "success_message": "'Post Table' Table created successfully",
                         'status': 'success'}
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, expected_data)

    def test_list(self):
        """ test to list all tables, doesn't require authentication """
        create_table_feet_leg(self.user)
        url = reverse("table:table_viewset-list")
        res = self.client.get(url)
        tables = Table.objects.all().order_by("-created_date")
        serializer = table_serializer.TableSerializer(tables, many=True)
        expected_data = {"result": serializer.data, 'status': 'success'}
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_retreive(self):
        """ test to list one tables, doesn't require authentication  """
        create_table_feet_leg(self.user)
        url = reverse("table:table_viewset-detail", kwargs={'pk': 'steel'})
        res = self.client.get(url)
        table = Table.objects.get(name__iexact="steel")
        serializer = table_serializer.TableSerializer(table)
        expected_data = {"result": serializer.data, 'status': 'success'}
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_update(self):
        """ test to update exisiting table, requires authentication"""
        create_table_feet_leg(self.user)
        del self.data["name"]
        self.data["description"] = "from update test case"
        url = reverse("table:table_viewset-detail", kwargs={'pk': 'steel'})
        res = self.client.put(url, self.data)
        table = Table.objects.get(name__iexact="steel")
        serializer = table_serializer.TableSerializer(table)
        expected_data = {"result": serializer.data, "success_message": "'Steel' Table updated successfully",
                         'status': 'success'}
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_partial_update(self):
        """ test to partial update exisiting table, requires authentication"""
        create_table_feet_leg(self.user)
        del self.data["name"]
        del self.data["legs"]
        self.data["description"] = "from partial update test case"
        url = reverse("table:table_viewset-detail", kwargs={'pk': 'steel'})
        res = self.client.patch(url, self.data)
        table = Table.objects.get(name__iexact="steel")
        serializer = table_serializer.TableSerializer(table)
        expected_data = {"result": serializer.data, "success_message": "'Steel' Table partially updated successfully",
                         'status': 'success'}
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, expected_data)

    def test_destroy(self):
        """ test to delete exisiting table, requires authentication"""
        create_table_feet_leg(self.user)
        self.data["description"] = "from partial update test case"
        url = reverse("table:table_viewset-detail", kwargs={'pk': 'steel'})
        res = self.client.delete(url)
        table = Table.objects.all()
        serializer = table_serializer.TableSerializer(table)
        expected_data = {"message": "'steel' deleted successfully", "status": "success"}
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.data, expected_data)
