from django.db import models

# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


class PfAirline(models.Model):
    id = models.IntegerField(primary_key=True)
    flight_date = models.DateField(db_column='Flight Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airline = models.CharField(db_column='Airline', max_length=50, blank=True, null=True)  # Field name made lowercase.
    start_time = models.TimeField(db_column='Start Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    start_airport = models.CharField(db_column='Start airport', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    arrival_time = models.TimeField(db_column='Arrival Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    arrival_airport = models.CharField(db_column='Arrival airport', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    direct1 = models.CharField(db_column='Direct1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direct2 = models.CharField(db_column='Direct2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pf_airline'


# class PfHotel(models.Model):
#     id = models.IntegerField(primary_key=True)
#     day = models.CharField(db_column='Day', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     checkin = models.DateField(db_column='Checkin', blank=True, null=True)  # Field name made lowercase.
#     checkout = models.DateField(db_column='Checkout', blank=True, null=True)  # Field name made lowercase.
#     location = models.CharField(db_column='Location', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     hotelname = models.CharField(db_column='HotelName', max_length=200, blank=True, null=True)  # Field name made lowercase.        
#     locationname = models.CharField(db_column='LocationName', max_length=50, blank=True, null=True)  # Field name made lowercase.   
#     grade = models.FloatField(db_column='Grade', blank=True, null=True)  # Field name made lowercase.
#     star = models.IntegerField(db_column='Star', blank=True, null=True)  # Field name made lowercase.
#     characte = models.CharField(db_column='Characte', max_length=200, blank=True, null=True)  # Field name made lowercase.
#     price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
#     etcprice = models.IntegerField(db_column='etcPrice', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'pf_hotel'


# class TravelloDestination(models.Model):
#     name = models.CharField(max_length=100)
#     img = models.CharField(max_length=100)
#     desc = models.TextField()
#     offer = models.BooleanField()
#     price = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'travello_destination'