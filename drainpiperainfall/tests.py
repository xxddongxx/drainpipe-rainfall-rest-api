from rest_framework import status
from rest_framework.test import APITestCase


PATH = "/api/v1/drainpiperainfall/"


class TestDrainPipeRainfallAPI(APITestCase):
    def setUp(self):
        self.gu_name = "종로구"

    def test_latest_api_fail(self):
        """
        최신 데이터 조회 실패 테스트
        """
        latest_url = f"{PATH}latest/?gu_name=제주도"
        response = self.client.get(latest_url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response_data, dict)
        self.assertIn("message", response_data)
        self.assertIn("status", response_data)
        self.assertIn("result", response_data)

    def test_latest_api_success(self):
        """
        최신 데이터 조회 테스트
        """
        latest_url = f"{PATH}latest/?gu_name={self.gu_name}"
        response = self.client.get(latest_url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)
        self.assertIn("message", response_data)
        self.assertIn("status", response_data)
        self.assertIn("result", response_data)
