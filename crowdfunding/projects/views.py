from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from django.http import Http404
from rest_framework import status

# Get request
class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all()
        # convert to jason
        serializer = ProjectSerializer(projects, many=True)   #can be accessable by manyprojects
        # return jason, send response to who do the request
        return Response(serializer.data)

    # Post request,put data into database
    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        # check that user inputs are valid in formatting
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# Details view of specific project
class ProjectDetail(APIView):
    # get record form database, equals the primary key that pass in
    def get_object(self,pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        project = self.get_object(pk)
        # get_object function can be here as well, but put it indepedently other delete/update class can use it as well
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    





