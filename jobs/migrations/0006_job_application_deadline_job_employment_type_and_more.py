from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_card_color_job_company_name_job_job_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationfield',
            name='is_required',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='applicationfield',
            name='field_type',
            field=models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('percentage', 'Percentage'), ('file', 'File'), ('multi_file', 'Multiple Files')], default='text', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='application_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='employment_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='posting_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
