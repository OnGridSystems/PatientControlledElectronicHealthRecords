# Generated by Django 2.1.2 on 2018-10-25 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delegated_at', models.DateTimeField(auto_now_add=True)),
                ('recepient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='users.Recepient')),
            ],
        ),
        migrations.CreateModel(
            name='KeyFragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('delegation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_fragments', to='re_encryption.Delegation')),
            ],
        ),
        migrations.CreateModel(
            name='RecordsSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('data', models.TextField()),
                ('capsule', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records_sets', to='users.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='delegation',
            name='records_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='re_encryption.RecordsSet'),
        ),
    ]
