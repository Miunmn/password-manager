from django.db import models

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=100, null=False, blank=False, unique=True)
	password = models.CharField(max_length=50, null=False, blank=False)
	salt = models.CharField(max_length=50, null=False, blank=False)

	class Meta:
		db_table = 'user'
		verbose_name_plural = 'users'

class StoredPasswords(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	passwords = models.CharField(max_length=5000, null=False, blank=False)

	class Meta:
		db_table = 'stored_passwords'
		verbose_name_plural = 'stored passwords'