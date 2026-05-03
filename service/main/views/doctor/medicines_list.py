from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Medicine_Guide
from main.serializers.doctor.medicines_list.serializers import MedicinesListSerializers


class MedicinesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        medicines = Medicine_Guide.objects.all()
        serializer = MedicinesListSerializers(medicines, many=True)
        return Response(serializer.data)
