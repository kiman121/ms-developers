from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import ProjectSerializer, ProfileSerializer
from projects.models import Project, Review
from users.models import Profile

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getUserProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data)