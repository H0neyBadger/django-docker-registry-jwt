from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group

class Registry(models.Model):
    '''
    Api token consumer (docker registry)
    '''
    name = models.CharField(
        validators=[ RegexValidator('^[a-z0-9]+(\.[a-z0-9]+){0,4}(:[0-9]{1,5})?$','[domain|IP][:port number]','Invalid Entry') ],
        max_length=200, 
        blank=False, 
        null=False,
        unique=False
    )
    
    
    def __str__(self):
        return '%s' % (self.name)

class Image(models.Model):
    '''
    Docker registry images
    '''
    name = models.CharField(
        validators=[ RegexValidator('^[a-z0-9]+[\/a-z0-9_-]*$(?<!\/)','Docker compatible image name only','Invalid Entry') ],
        max_length=100
    )
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE)
    # keep image in database
    # only staff is now able to change the owner
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    class Meta:
        unique_together = (
            ("registry", "name"),
        )

    def __str__(self):
        return '%s/%s' % (self.registry, self.name)


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    push = models.BooleanField(default=False)
    pull = models.BooleanField(default=True)
    # custom right to allow 
    # visible = models.BooleanField(default=False)
    
    class Meta:
        unique_together = (
            ("user", "image"),
        )

