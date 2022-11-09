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
        GET /api/v1/drainpiperainfall/latest/
        """
        gu_name = request.GET["gu_name"]
        try:

            drain = DrainPipeController(gu_name)
            drain_url = drain.get_url()
            drain_result = drain.get_result(drain_url)

            rainfall = RainFallController(gu_name)
            rainfall_url = rainfall.get_url()
            rainfall_result = rainfall.get_result(rainfall_url)

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
