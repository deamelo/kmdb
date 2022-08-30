from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException

from accounts.permissions import IsAdminOrReadOnly, IsCriticOwnerOrReadOnly, IsCriticOrReadOnly
from movies.models import Movie

from .models import Review
from .serializers import ReviewSerializer


class OwnerOnlyError(APIException):
    status_code = 403


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly | IsCriticOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie, user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id: int) -> Response:
        review = Review.objects.filter(movie_id=movie_id)
        result_page = self.paginate_queryset(review, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly | IsCriticOwnerOrReadOnly]

    def get(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)
        serializer = ReviewSerializer(review)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)
        self.check_object_permissions(request, review)

        if request.user.is_critic and request.user != review.user:
            raise OwnerOnlyError({"detail": "You do not have permission to perform this action."})

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
