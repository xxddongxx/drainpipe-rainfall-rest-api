from requests.exceptions import MissingSchema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drainpiperainfall import serializers
from utils.drainpipecontroller import DrainPipeController
from utils.rainfallcontroller import RainFallController


class Least(APIView):
    def get(self, request):
        """
        GET /api/v1/drainpiperainfall/latest/?gu_name="용산구" or "용산"
        """
        gu_name = request.GET["gu_name"]
        try:
            drain = DrainPipeController(gu_name)
            drain_url = drain.get_latest_url()
            drain_datas, drain_set_len = drain.get_datas_set_len(drain_url)
            drain_result = drain.get_result(drain_datas, drain_set_len)

            rainfall = RainFallController(gu_name)
            rainfall_url = rainfall.get_url()
            rainfall_datas, rainfall_set_len = rainfall.get_datas_set_len(rainfall_url)
            rainfall_result = rainfall.get_result(rainfall_datas, rainfall_set_len)

            drain_serializer = serializers.DrainPipeSerializer(drain_result, many=True)
            rainfall_serializer = serializers.RainFallSerializer(
                rainfall_result, many=True
            )

            return Response(
                {
                    "message": "Success",
                    "status": status.HTTP_200_OK,
                    "result": {
                        "Drain_Pipe": drain_serializer.data,
                        "RainFall": rainfall_serializer.data,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {
                    "message": "데이터를 찾을 수 없습니다.",
                    "status": status.HTTP_404_NOT_FOUND,
                    "result": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class RainFallToday(APIView):
    def get(self, request):
        """
        오늘 데이터 조회
        GET /api/v1/drainpiperainfall/rainfall/today/?gu_name="용산구" or "용산"
        """
        gu_name = request.GET["gu_name"]
        try:
            rainfall = RainFallController(gu_name)
            rainfall_url = rainfall.get_url()
            datas, set_len = rainfall.get_datas_set_len(rainfall_url)
            rainfall_result = rainfall.get_today_result(datas, set_len)
            rainfall_total_count = len(rainfall_result)

            rainfall_serializer = serializers.RainFallSerializer(
                rainfall_result, many=True
            )

            return Response(
                {
                    "message": "Success",
                    "status": status.HTTP_200_OK,
                    "result": {
                        "now_total_count": rainfall_total_count,
                        "RainFall": rainfall_serializer.data,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {
                    "message": "데이터를 찾을 수 없습니다.",
                    "status": status.HTTP_404_NOT_FOUND,
                    "result": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class DrainPipeToday(APIView):
    def get(self, request):
        """
        오늘 데이터 조회
        GET /api/v1/drainpiperainfall/drainpipe/today/?gu_name="용산구" or "용산"
        """
        gu_name = request.GET["gu_name"]
        try:
            drain = DrainPipeController(gu_name)
            drain_url = drain.get_latest_url()
            drain_today_url_list = drain.make_today_url_list(drain_url)
            drain_today_result = drain.thread_executor_method(drain_today_url_list)
            drain_total_count = len(drain_today_result)

            drain_serializer = serializers.DrainPipeSerializer(
                drain_today_result, many=True
            )
            return Response(
                {
                    "message": "Success",
                    "status": status.HTTP_200_OK,
                    "result": {
                        "now_total_count": drain_total_count,
                        "Drain_Pipe": drain_serializer.data,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                {
                    "message": "데이터를 찾을 수 없습니다.",
                    "status": status.HTTP_404_NOT_FOUND,
                    "result": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )
