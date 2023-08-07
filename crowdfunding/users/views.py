
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAdminUser
from .models import CustomUser
from .serializers import CustomUserSerializer
class CustomUserList(APIView):
    def get(self, request):
        #from db
        users = CustomUser.objects.all() 
        #to json   
        serializer = CustomUserSerializer(users, many=True)
        #returning json files of all users
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    #post-created a user
    def post(self, request):
        # converting user's input to something suits db
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #serializer.data is a json data, otherthings else serializer.**** is might not a json data
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated, AllowAny


class CustomUserList(APIView):
    permission_classes = [IsAdminUser | AllowAny]

    def get(self, request):
        # Admin can see all users' information
        if request.user.is_authenticated and request.user.is_staff:
            users = CustomUser.objects.all()
        else:
            # For non-admin users, return an empty queryset (hide other users' information)
            users = CustomUser.objects.none()

        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        # Allow anyone to create a new user
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetail(APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            # Ensure non-admin user can only update their own profile
            if not request.user.is_superuser and request.user != user:
                return Response({"error": "You don't have permission to update this profile."},
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


