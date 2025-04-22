from django.utils import timezone
from rest_framework import serializers
from authentication.models import User

DEFAULT_PASSWORD = 'pnMGgxsG1P3MKGk'


class UserSerializer(serializers.ModelSerializer):
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
            'is_staff', 'is_superuser',
            "password",
            "password2",
        )
        read_only_fields = ['is_staff', 'is_superuser']
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
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_staff=False,
            is_superuser=False
        )
        return user


class StaffRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=['Admin', 'Officer'], write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_staff=role in ['Admin', 'Officer'],
            is_superuser=(role == 'Admin')
        )
        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name', 'is_staff', 'is_superuser']
        # read_only_fields = ['email', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
        }

    def validate(self, attrs):
        if self.instance == self.context['request'].user:
            raise serializers.ValidationError(
                "You cannot modify your own permissions")
        return attrs

    # def update(self, instance, validated_data):
    #     residence_data = validated_data.pop('residence', {})

    #     # Update user permissions
    #     instance = super().update(instance, validated_data)

    #     # Update residence information
    #     residence = instance.residence
    #     for key, value in residence_data.items():
    #         setattr(residence, key, value)
    #     residence.save()

    #     return instance


class UserWithResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                  'is_staff', 'is_superuser']


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
