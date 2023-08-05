
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
class CustomUserList(APIView):
    def get(self, request):
        #from db
        users = CustomUser.objects.all() 
        #to json   
        serializer = CustomUserSerializer(users, many=True)
        #returning json files of all users
        return Response(serializer.data)
    #post-created a user
    def post(self, request):
        # converting user's input to something suits db
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #serializer.data is a json data, otherthings else serializer.**** is might not a json data
            return Response(serializer.data)
        return Response(serializer.errors)
class CustomUserDetail(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
