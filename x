# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class SharingAccess(models.Model):
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    used = models.IntegerField(blank=True, null=True)
    renta = models.ForeignKey('SharingRents', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    stype = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sharing_access'


class SharingCities(models.Model):
    city_name = models.CharField(max_length=200)
    country = models.ForeignKey('SharingCountries', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sharing_cities'


class SharingCountries(models.Model):
    country_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'sharing_countries'


class SharingDistricts(models.Model):
    district_name = models.CharField(max_length=200)
    partner = models.ForeignKey('SharingPartners', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sharing_districts'


class SharingFlats(models.Model):
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    building = models.CharField(max_length=10, blank=True, null=True)
    flat_number = models.CharField(max_length=10, blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    per_hour = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    door_status = models.BooleanField(blank=True, null=True)
    cleaning_time = models.TimeField(blank=True, null=True)
    district = models.ForeignKey(SharingDistricts, models.DO_NOTHING)
    app_id = models.CharField(max_length=60, blank=True, null=True)
    app_status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharing_flats'


class SharingImages(models.Model):
    images = models.CharField(max_length=100, blank=True, null=True)
    flat = models.ForeignKey(SharingFlats, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sharing_images'


class SharingPartners(models.Model):
    account = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    city = models.ForeignKey(SharingCities, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sharing_partners'


class SharingPayments(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    status = models.BooleanField(blank=True, null=True)
    payment_type = models.IntegerField(blank=True, null=True)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    captured_at = models.DateTimeField(blank=True, null=True)
    renta = models.ForeignKey('SharingRents', models.DO_NOTHING, blank=True, null=True)
    rentor = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharing_payments'


class SharingRents(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.BooleanField(blank=True, null=True)
    paid = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    flat = models.ForeignKey(SharingFlats, models.DO_NOTHING)
    rentor = models.ForeignKey(AuthUser, models.DO_NOTHING)
    booking = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharing_rents'


class SharingSystemlogs(models.Model):
    district = models.ForeignKey(SharingDistricts, models.DO_NOTHING, blank=True, null=True)
    flat = models.ForeignKey(SharingFlats, models.DO_NOTHING, blank=True, null=True)
    partner = models.ForeignKey(SharingPartners, models.DO_NOTHING, blank=True, null=True)
    payment = models.ForeignKey(SharingPayments, models.DO_NOTHING, blank=True, null=True)
    rents = models.ForeignKey(SharingRents, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    worker = models.ForeignKey('SharingWorkers', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharing_systemlogs'


class SharingUsersdocuments(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    image_one = models.CharField(max_length=100)
    image_two = models.CharField(max_length=100)
    status = models.BooleanField()
    yakey = models.CharField(max_length=50, blank=True, null=True)
    totlal_cancelation = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    ya_card_last4 = models.CharField(max_length=4, blank=True, null=True)
    ya_card_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sharing_usersdocuments'


class SharingWorkers(models.Model):
    role = models.IntegerField()
    account = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)
    partner = models.ForeignKey(SharingPartners, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sharing_workers'
