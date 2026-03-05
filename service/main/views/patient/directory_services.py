from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ...models import Service_Guide
from ...serializers.patient.directory_services.serializers import DirectoryOfServicesSerializers

class DirectoryOfServicesView (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sort_by = request.query_params.get("sort", "id")
        services = Service_Guide.objects.all().order_by(sort_by)
        serializer = DirectoryOfServicesSerializers(services, many=True)
        return Response(serializer.data)










