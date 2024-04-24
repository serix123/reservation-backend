from rest_framework import serializers
from authentication.models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'} ,write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'} ,write_only=True)

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password', 'password2')
        # extra_kwargs = {
        #     'password' : {'write_only': True}
        # }

    def create(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password' : 'Passwords must match'})

        user = User.objects.create_user(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            password=password
        )

        return user
