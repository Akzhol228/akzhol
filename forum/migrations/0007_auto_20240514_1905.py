# Generated by Django 3.2.4 on 2024-05-14 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0006_alter_cityproblem_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cityproblem',
            options={'verbose_name': 'IT проект', 'verbose_name_plural': 'IT проекты'},
        ),
        migrations.AlterModelOptions(
            name='solutionproposal',
            options={'verbose_name': 'Предложение идеи', 'verbose_name_plural': 'Предложения идей'},
        ),
        migrations.AddField(
            model_name='cityproblem',
            name='collected_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Собранная сумма'),
        ),
        migrations.AlterField(
            model_name='cityproblem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='solutionproposal',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to=settings.AUTH_USER_MODEL, verbose_name='Автор идеи'),
        ),
        migrations.AlterField(
            model_name='solutionproposal',
            name='description',
            field=models.TextField(verbose_name='Описание идеи'),
        ),
        migrations.AlterField(
            model_name='solutionproposal',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='forum.cityproblem', verbose_name='IT проект'),
        ),
    ]
