from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Prescribed_Service, Patient


class VisitDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)

        try:
            visit = Prescribed_Service.objects.get(id=pk, patient=patient)
        except Prescribed_Service.DoesNotExist:
            return Response({"error": "Запис не знайдено"}, status=404)

        if visit.status == "Підтверджено":
            return Response(
                {"error": "Не можна видалити запис якщо він підтверджений"}, status=400
            )
        visit.delete()
        return Response({"message": "Запис видалено"}, status=204)
