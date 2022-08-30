from rest_framework import serializers
from accounts.serializers import UserReviewSerializer
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {"stars": {"min_value": 1, "max_value": 10}}
