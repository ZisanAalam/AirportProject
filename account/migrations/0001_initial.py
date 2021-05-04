# Generated by Django 3.2 on 2021-05-04 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='FaultLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Runway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runway', models.CharField(max_length=20)),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.make')),
            ],
        ),
        migrations.CreateModel(
            name='FaultLocationPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('faultlocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.faultlocation')),
            ],
        ),
        migrations.CreateModel(
            name='FaultEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('period', models.CharField(max_length=255)),
                ('down_time', models.CharField(max_length=255)),
                ('fault_discription', models.CharField(max_length=255)),
                ('action_taken', models.CharField(max_length=255)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.equipment')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.faultlocation')),
                ('locationpart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.faultlocationpart')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.make')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.model')),
                ('runway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.runway')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='runway',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.runway'),
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('middle_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=150)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, default='default.png', upload_to='profile')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.airport')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
