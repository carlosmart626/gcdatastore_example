from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .datastore import get_instance, create_update_instance, list_instances, delete_instance


class DataStoreTestCase(TestCase):

    def setUp(self):
        data = {
            "name": "My cool bike",
            "price": 702445.45,
            "manufacturer": "GW"
        }
        self.test_bike = create_update_instance(data)

    def tearDown(self):
        delete_instance(self.test_bike.get('id'))

    def test_detail(self):
        bike = get_instance(self.test_bike.get('id'))

        self.assertEqual(bike.get('id'), self.test_bike.get('id'))

    def test_update(self):
        data = {
            "name": "Updated my cool bike from tests",
        }
        bike = create_update_instance(data, self.test_bike.get('id'))
        self.assertEqual(bike.get('id'), self.test_bike.get('id'))
        self.assertEqual(bike.get('name'), "Updated my cool bike from tests")

    def test_create_delete(self):
        data = {
            "name": "Created other bike from tests",
        }
        bike = create_update_instance(data)
        self.assertIsNotNone(bike.get('id'))
        self.assertEqual(bike.get('name'), "Created other bike from tests")

        delete_instance(bike.get('id'))

        deleted_bike = get_instance(bike.get('id'))
        self.assertIsNone(deleted_bike)

    def test_list(self):
        results, next_cursor = list_instances()
        results_ids = [item.get('id') for item in results]
        self.assertIn(self.test_bike.get('id'), results_ids)


class BikesAPITestCase(APITestCase):

    def setUp(self):
        data = {
            "name": "FUEL EX 9.9 2018",
            "price": 22690000.00,
            "manufacturer": "TREK"
        }
        self.test_bike = create_update_instance(data)

    def tearDown(self):
        delete_instance(self.test_bike.get('id'))

    def test_list_view(self):
        url = reverse("bikes-list")
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, 200)

        content = response.data
        instance_names = [instance.get('name') for instance in content]
        self.assertIn("FUEL EX 9.9 2018", instance_names)

    def test_list_view_create(self):
        data = {
            "name": "SLASH 9.8 2018",
            "price": 15008000.00,
            "manufacturer": "TREK"
        }
        url = reverse("bikes-list")
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, 200)

        content = response.data
        self.assertIsNotNone(content.get('id'))
        self.assertEqual(content.get('name'), "SLASH 9.8 2018")
        self.assertEqual(content.get('price'), 15008000.00)
        self.assertEqual(content.get('manufacturer'), "TREK")

        # delete created instance
        delete_instance(content.get('id'))

    def test_detail_view(self):
        url = reverse("bikes-detail", kwargs={'id': self.test_bike.get('id')})
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, 200)

        content = response.data
        self.assertEqual(content.get('id'), self.test_bike.get('id'))
        self.assertEqual(content.get('name'), "FUEL EX 9.9 2018")
        self.assertEqual(content.get('price'), 22690000.00)
        self.assertEqual(content.get('manufacturer'), "TREK")

    def test_detail_view_update(self):
        data = {
            "name": "FUEL EX 9.9 2019",
            "price": 24690000.00,
            "manufacturer": "TREK"
        }
        url = reverse("bikes-detail", kwargs={'id': self.test_bike.get('id')})
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, 200)

        content = response.data
        self.assertEqual(content.get('id'), self.test_bike.get('id'))
        self.assertEqual(content.get('name'), "FUEL EX 9.9 2019")
        self.assertEqual(content.get('price'), 24690000.00)
        self.assertEqual(content.get('manufacturer'), "TREK")

    def test_detail_vew_delete(self):
        url = reverse("bikes-detail", kwargs={'id': self.test_bike.get('id')})
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, 204)
