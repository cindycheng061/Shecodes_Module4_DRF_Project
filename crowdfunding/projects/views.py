from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project,Pledge
from .serializers import ProjectDetailSerializer,PledgeSerializer,PledgeDetailSerializer,ProjectSerializer
from django.http import Http404
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
from rest_framework.permissions import IsAdminUser

# Get request
class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        # get queryset
        projects = Project.objects.all()
        # convert to jason
        serializer = ProjectSerializer(projects, many=True)   #can be accessable by manyprojects
        # return jason, send response to who do the request
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

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
        # permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly|IsAdminUser
    ]
    # get record form database, equals the primary key that pass in
    def get_object(self,pk):
        try:
            # return Project.objects.get(pk=pk)
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        project = self.get_object(pk)
        # get_object function can be here as well, but put it indepedently other delete/update class can use it as well
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
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
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_200_OK)

    

class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        pledges =Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter = request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class PledgeDetail(APIView):
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly|IsAdminUser
        
    ]
    # get record form database, equals the primary key that pass in
    def get_object(self,pk):
        try:
            # return Pledge.objects.get(pk=pk)
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        pledge = self.get_object(pk)
        # get_object function can be here as well, but put it indepedently other delete/update class can use it as well
        serializer = PledgeDetailSerializer(pledge)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    # lateron add status code on my own????
    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=request.data,         
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            #   addddddddd in class
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_200_OK)
    

# add two views to return all projects and pledges that request user owned/supported
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer

class UserProjectList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # use filter to get request.user projects
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPledgeList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        pledges = Pledge.objects.filter(supporter= request.user)
        serializer = PledgeSerializer(pledges,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





