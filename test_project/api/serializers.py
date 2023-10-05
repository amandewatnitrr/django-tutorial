from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ProfileSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerailizer(many=False)
    tags = TagSerailizer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerailizer(reviews, many=True)
        return serializer.data