from rest_framework import serializers
from projects.models import Project, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_projects(self, obj):
        projects = obj.project_set.all()
        serializer = ProjectSerializer(projects, many=True)
        return serializer.data

class ProjectSerializer(serializers.ModelSerializer):
    # owner = ProfileSerializer(many=False)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data