import os

from amadeus import Client, ResponseError
from django.shortcuts import get_object_or_404, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.flight.serializer import FlightSerializer
from flight.models import Flight


class FlightList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flights = Flight.objects.filter(owner=request.user)
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["owner"] = request.user.id
        serializer = FlightSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class FlightDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Flight.objects.get(id=id)
        except Flight.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        flight = self.get_object(pk)
        if flight.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = FlightSerializer(flight)
        return Response(serializer.data)

    def delete(self, request, id):
        flight = self.get_object(id)
        if flight.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
