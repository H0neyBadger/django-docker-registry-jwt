from rest_framework import serializers

from django.contrib.auth.models import User

from registry.models import Registry, \
        Image, \
        Permission


class RegistrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Registry
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    registry = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Registry.objects.all(),
    )
    

    class Meta:
        model = Image
        fields = ('registry','name','comment','owner')

class ImageRegistryRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `image` `registry` relationship.
    """

    def to_representation(self, value):
        """
        Serialize objects to a simple textual representation.
        """
        return '%s/%s' % (value.registry.name, value.name)
        
    def to_internal_value(self, data):
        # FIXME: naive implementation
        registry, image = data.split('/',1)
        obj = Image.objects.get(registry__name=registry, name=image)
        return obj

class PermissionSerializer(serializers.ModelSerializer):
    image = ImageRegistryRelatedField(
        many=False,
        read_only=False,
        queryset=Image.objects.all(),
    )
    user = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Permission
        fields = '__all__'
