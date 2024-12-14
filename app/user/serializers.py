"""
Serilizers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serilizers for the user object"""
    class Meta:
        model = get_user_model() # Every serializer must have some unique model
        fields = ['email', 'password', 'name'] # required fields for this serializer
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)  # Fixed indentation

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        return user


# Serializer is just taking data from url - views - validation -> Again returning to views.py
class AuthTokenSerializer(serializers.Serializer):
    """Serilizers for the user auth token""" 
    ## Defining here field - Two Field email and password
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs): # Passing Data to Views -> it will go to Serializers -> validate method will validate the data.
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user # After validation done, views.py will except this user
        return attrs