from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage

from vote.models import VoteModel

from authors.apps.profiles.models import Profile
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import get_comments

User = get_user_model()


class Tag(models.Model):
    """
    Model for for tags
    """
    tag_name = models.CharField(max_length=100)

    class Meta:
        ordering = ('tag_name',)

    def __str__(self):
        return self.tag_name

    @property
    def articles(self):
        """
        gets all articles associated with the tag
        """
        queryset = Article.objects.filter(tags__pk=self.pk)
        return queryset


class Article(VoteModel, models.Model):
    """
    Model for articles
    """
    slug = AutoSlugField(populate_from='title', always_update=True,
                         blank=True, null=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.PositiveSmallIntegerField(default=0)
    image = CloudinaryField('image')

    class Meta:
        ordering = ['created_at', ]

    def get_image(self):
        """
        Retrieve article image
        """
        image_url = CloudinaryImage(str(self.image)).build_url(crop='fill')
        return image_url

    def get_author_details(self):
        """
        Fetch author's Profile
        """
        return {
            "username": self.author.username,
            "bio": self.author.profile.bio,
            "image": self.author.profile.fetch_image,
            "following": self.author.profile.following.reverse
        }

    @property
    def average_ratings(self):
        import math
        ratings = RatingModel.objects.filter(article__pk=self.pk)
        average = 0
        if ratings:
            total = sum([rating.rate for rating in ratings])
            average = total/ratings.count()
        return average

    @property
    def my_ratings(self):
        rates = RatingModel.objects.filter(article__pk=self.pk)
        my_ratings = [rates.rate for rating in rates]
        return my_ratings

    @property
    def tagList(self):
        """
        Gets all tags on an article
        """
        tags = [tag.tag_name for tag in self.tags.all()]
        return tags

    def clear_tags(self):
        """
        Clears all tags for an article
        """
        for tag in self.tags.all():
            self.tags.remove(tag)
            if not tag.articles:
                tag.delete()

    @property
    def comments(self):
        """
        Gets all comments on a specific article
        """
        comments = Comment.objects.filter(article__slug=self.slug)
        return get_comments(comments)


class Comment(models.Model):
    """
    model for  comments
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # def __str__(self):
    #     return self.body

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def comments(self):
        """
        Returns a serializable format of children
        """
        comments = Comment.objects.all()
        return get_comments(comments)

    @property
    def representation(self):
        """
        Representation of a comment in a JSON serializable format
        """

        response = {
            "id": self.pk,
            "article": {
                "author": self.article.author.username,
                "body": self.article.body
            },
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "body": self.body,
            "author": self.get_profile_details()
        }
        return response

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_profile_details(self):
        """
        get author's Profile
        """
        return Article.get_author_details(self)


class Favorite(models.Model):
    """
    A class model for storing user fovorites and articles
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def is_favorited(self, user, article):
        """
        Get all articles that are favorited by user
        """
        try:
            article = self.article
            user = self.user
        except Article.DoesNotExist:
            pass

        queryset = Favorite.objects.filter(article_id=article, user_id=user)

        if queryset:
            return True
        return False


class RatingModel(models.Model):
    """
    Models for rating an article (0 - 5)
    """
    article = models.ForeignKey(
        Article, related_name='rated_article', on_delete=models.CASCADE)
    rated_by = models.ForeignKey(
        User, related_name='rated_by', on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def get_articles_details(self):
        """
        Fetch relevant articles details
        """
        return {
            "slug": self.article.slug,
            "title": self.article.title,
            "description": self.article.description,
            "body": self.article.body,
            "created_at": self.article.created_at,
            "updated_at": self.article.updated_at
        }

    def my_ratings(self, article, user):
        """
        Model to display rating for users in an articles
        """

        try:
            article = self.article
            user = self.rated_by
        except Article.DoesNotExist:
            pass
        

        queryset = RatingModel.objects.filter(article_id=article, rated_by_id=user).first()

  

        if queryset:
            return queryset.rate
        return False