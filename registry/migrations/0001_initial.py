# Generated by Django 2.1.7 on 2019-03-05 09:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[a-z0-9]+([/a-z0-9_-])*+$(?<!\\/)', 'Docker compatible image name only', 'Invalid Entry')])),
                ('comment', models.TextField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('push', models.BooleanField(default=False)),
                ('pull', models.BooleanField(default=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator('^[a-z0-9]+\\.[a-z0-9]{1,4}(:[0-9]{1,5})?$', 'Domain name only', 'Invalid Entry')])),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='registry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Registry'),
        ),
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together={('user', 'image')},
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('registry', 'name')},
        ),
    ]