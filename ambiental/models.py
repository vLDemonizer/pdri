from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

WD = (      # Weighting Designation Options
    ('H', 'High-Priority'),
    ('P', 'Pro-Rated'),
)

MV = (      # Maturity Value Options
    ('1', 'Slow'),
    ('2', 'Kinda Slow'),
    ('3', 'Okay'),
    ('4', 'Fastish'),
    ('5', 'Fast'),
)
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default="Nothing here yet")
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CD(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)
    score_a = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    score_b = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    score_c = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    score_d = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    score_e = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    total_score = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.total_score = self.score_a + self.score_b + self.score_c + self.score_d + self.score_e
        super(CD, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class RatingElement(models.Model):
    cd = models.ForeignKey(CD, on_delete=models.CASCADE)
    group = models.CharField(max_length=50, blank=True)  # Group Name example Cost
    index = models.CharField(max_length=4, blank=True)  # Index of the group 'A1'
    name = models.CharField(max_length=100, blank=True)  # Rating Element name
    wd = models.CharField(max_length=100, default='H/P', blank=True)   # Weighting Designation
    wf = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)    # Weighting Factor
    mv = models.CharField(max_length=1, default='N/A', choices=MV, blank=True) # Maturity Value
    score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0) # Target Score
    comment = models.CharField(max_length=300, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.index)
        super(RatingElement, self).save(*args, **kwargs)

    def __str__(self):
        return self.cd.project.name + ' / ' + self.cd.name + ' | ' + self.index + ' - ' + self.name
