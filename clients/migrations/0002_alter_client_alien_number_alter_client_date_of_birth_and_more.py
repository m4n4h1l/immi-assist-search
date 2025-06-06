# Generated by Django 5.2.1 on 2025-06-01 00:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='alien_number',
            field=models.CharField(blank=True, help_text='A-Number (if available)', max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_of_birth',
            field=models.DateField(help_text='Format: YYYY-MM-DD'),
        ),
        migrations.CreateModel(
            name='ImmigrationCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_name', models.CharField(help_text="e.g., 'I-485 Application - 2025' or 'Asylum Case'", max_length=200)),
                ('date_opened', models.DateField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='clients.client')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(default=django.utils.timezone.now, help_text='The date you are entering this information.')),
                ('form_type', models.CharField(help_text='e.g., I-485, I-765, Account Access Notice', max_length=50)),
                ('i765_category', models.CharField(blank=True, help_text='e.g., C11, C5. Only for I-765 forms.', max_length=10)),
                ('receipt_number', models.CharField(blank=True, max_length=50)),
                ('received_date', models.DateField(blank=True, help_text="The 'Received Date' on the notice from USCIS.", null=True)),
                ('processing_center', models.CharField(blank=True, help_text='e.g., California Service Center', max_length=100)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notices', to='clients.immigrationcase')),
            ],
        ),
    ]
