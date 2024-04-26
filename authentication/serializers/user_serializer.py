from rest_framework import serializers
from authentication.models import User
from reservation.models import Employee
from reservation.serializers import EmployeeSerializer


class UserSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer(required=False)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
            "employee",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def create(self):
        password = self.validated_data.pop("password")
        password2 = self.validated_data.pop("password2")

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match"})

        user = User.objects.create_user(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
            password=password,
        )

        employee_data = self.validated_data.pop("employee", {})
        Employee.objects.create(
            user=user,
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            **employee_data
        )

        return user

    def create_superuser(self):
        password = self.validated_data.pop("password")
        password2 = self.validated_data.pop("password2")

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match"})

        user = User.objects.create_superuser(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
            password=password,
        )

        employee_data = self.validated_data.pop("employee", {})
        Employee.objects.create(
            user=user,
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            **employee_data
        )

        return user
