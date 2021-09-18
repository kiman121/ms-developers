from django.db import models
from django.db.models import Sum
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-rating', 'title']
    
    @property
    def imageUrl(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getRating(self):
        reviews = self.review_set.all()
        designRating = reviews.aggregate(Sum(design))
        usabilityRating = reviews.aggregate(Sum(usability))
        contentRating = reviews.aggregate(Sum(content))

        score = (designRating + usabilityRating + contentRating)/3
        
        # upVotes = reviews.filter(value='up').count()
        # totalVotes = reviews.count()
        
        # ratio = (upVotes/totalVotes) * 100
        # self.vote_total = totalVotes
        self.rating = round(score)
        
        self.save()

class Review(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    design = models.IntegerField(choices=list(zip(range(1, 10), range(1, 10))), unique=True)
    usability = models.IntegerField(choices=list(zip(range(1, 10), range(1, 10))), unique=True)
    content = models.IntegerField(choices=list(zip(range(1, 10), range(1, 10))), unique=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
