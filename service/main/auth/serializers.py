from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["is_employee"] = user.is_employee

        if user.is_employee and hasattr(user, "employee"):
            token["position"] = user.employee.position.code.name
        elif user.is_patient and hasattr(user, "patient"):
            token["position"] = "patient"

        return token

