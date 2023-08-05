from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project,Pledge
from .serializers import ProjectDetailSerializer,PledgeSerializer,ProjectSerializer
from django.http import Http404
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly

# Get request
class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
            serializer.save(owner = request.user)
            # return Response(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# Details view of specific project
class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    # get record form database, equals the primary key that pass in
    def get_object(self,pk):
        try:
            # return Project.objects.get(pk=pk)
            project = Project.objects.get(pk=pk)
            self.check_object_perssions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        project = self.get_object(pk)
        # get_object function can be here as well, but put it indepedently other delete/update class can use it as well
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    # lateron add status code on my own????
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project,
            data=request.data,         
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            #   addddddddd in class
            return Response(serializer.data)


 
class PledgeList(APIView):
    def get(self, request):
        pledges =Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    





