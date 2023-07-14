from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Movie, Actor
from .service import get_client_ip, MovieFilter, Pagination
from .serializer import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorsListSerializer,
    ActorDetailSerializer

)


# class MovieListView(APIView):

#     def get(self, request):
        # movies = Movie.objects.filter(draft=False).annotate(
        #     rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
        # ).annotate(
        #     middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        # )
        # serializer = MovieListSerializer(movies, many=True)
        # return Response(serializer.data)


# class MovieDetailView(APIView):
#     def get(self, request, pk):
#         movie = Movie.objects.get(pk=pk, draft=False)
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)



# class ReviewCreateView(APIView):

#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


# class AddStarRatingView(APIView):

#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)


# class ActorsView(generics.ListAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorsListSerializer


# class ActorDetailView(generics.RetrieveAPIView):
#     queryset = Actor.objects.filter()
#     serializer_class = ActorDetailSerializer


# # ##################### GENERICS
# class MovieListView(generics.ListAPIView):
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter

#     # permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return movies


# class MovieDetailView(generics.RetrieveAPIView):
#     serializer_class = MovieDetailSerializer

#     def get_queryset(self):
#         movie = Movie.objects.filter(draft=False)
#         return movie


# class ReviewCreateView(generics.CreateAPIView):
#     serializer_class = ReviewCreateSerializer


# class AddStarRatingView(generics.CreateAPIView):
#     serializer_class = CreateRatingSerializer

#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))


# #######################VIEWSETS
class MovieListViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateView(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(viewsets.ModelViewSet):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsView(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorsListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer

