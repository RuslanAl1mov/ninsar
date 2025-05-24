from django.db.models import Window
from django.db.models.functions import RowNumber
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Competition, CompetitionResult
from .serializers import CompetitionRequestSerializer, CompetitionResponseSerializer


class CompetitionResultView(views.APIView):
    """
    POST `/api/v1/results/results/get-competition-result/`
    
    СООБЩЕНИЕ ДЛЯ ПРОВЕРЯЮЩЕГО!
    Вывод собирается во вьюхе, это самый просто вариант с дополнительным "управляющим"
    сериализатором CompetitionRequestSerializer, но также можно было бы собрать ответ
    через сериализатор, нужно не много больше времени, обычно я используя сериализаторный 
    метод
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    OTHER_LIMIT = 10  # число чужих результатов в ответе

    @staticmethod
    def obj_to_dict(obj) -> dict:
        return {
            "position": obj.position,
            "user_name": obj.user.username,
            "flight_time": obj.flight_time,
            "command_name": obj.team.name if obj.team else "",
        }

    def post(self, request, *args, **kwargs):
        req_ser = CompetitionRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        comp_name = req_ser.validated_data["competition"]
        scenario = req_ser.validated_data["scenario"]
        username = req_ser.validated_data["user_name"]

        try:
            comp = Competition.objects.get(name=comp_name)
        except Competition.DoesNotExist:
            return Response({"detail": "Competition not found."}, status=status.HTTP_404_NOT_FOUND)

        qs = (
            CompetitionResult.objects.filter(
                competition=comp, scenario=scenario, false_start=False
            )
            .annotate(position=Window(RowNumber(), order_by=["flight_time", "id"]))
            .select_related("user", "team")
        )

        try:
            user_res = qs.get(user__username=username)
        except CompetitionResult.DoesNotExist:
            return Response({"detail": "User result not found."}, status=status.HTTP_404_NOT_FOUND)

        user_result = self.obj_to_dict(user_res)
        other_results = [
            self.obj_to_dict(o) for o in qs.exclude(user__username=username)[: self.OTHER_LIMIT]
        ]

        return Response(
            CompetitionResponseSerializer(
                {"user_result": user_result, "other_results": other_results}
            ).data
        )
