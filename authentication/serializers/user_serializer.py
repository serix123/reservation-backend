from rest_framework import serializers
from authentication.models import User
from reservation.models import Employee
from reservation.serializers import EmployeeSerializer

DEFAULT_PASSWORD = 'pnMGgxsG1P3MKGk'


class UserSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer(required=False)
    password = serializers.CharField(required=False, allow_null=True,
                                     style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(required=False, allow_null=True,
                                      style={"input_type": "password"}, write_only=True)

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
            "password": {"required": False, "write_only": True},
            "password2": {"required": False, "write_only": True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def create(self):
        password = self.validated_data.pop("password")
        password2 = self.validated_data.pop("password2")

        if password is not None or password2 is not None:
            if password != password2:
                raise serializers.ValidationError(
                    {"password": "Passwords must match"})
        else:
            password = DEFAULT_PASSWORD

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
            raise serializers.ValidationError(
                {"password": "Passwords must match"})

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

    def create_employee_and_assign(self):
        password = self.validated_data.pop("password")
        password2 = self.validated_data.pop("password2")

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords must match"})

        user = User.objects.create_user(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
            password=password,
        )
        # Access the requesting user from the serializer context
        registering_user = self.context['request'].user.employee
        employee_data = self.validated_data.pop("employee", {})
        Employee.objects.create(
            user=user,
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            immediate_head=registering_user,
            department=registering_user.department,
            **employee_data
        )

        return user


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
