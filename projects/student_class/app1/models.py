from django.db import models


class Grade(models.Model):
    title = models.CharField(max_length=20)


class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=20, default='male')
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)


class User(models.Model):
    username = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)


class Goods(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
