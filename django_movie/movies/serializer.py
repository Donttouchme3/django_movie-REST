from rest_framework import serializers
from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'rating_user', 'middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RecursiveReview(serializers.Serializer):
    def to_representation(self, value):
        review = self.parent.parent.__class__(value, context=self.context)
        return review.data


class FilterReviewSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveReview(many=True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('name', 'text', 'children')


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating


class ActorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
