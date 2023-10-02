from django.db import models
from django.db.models import Q, F, Count
from django.shortcuts import get_object_or_404


class EmployeeQuerySet(models.query.QuerySet):

    def employee_age(self):
        return self.count()


class EmployeeManager(models.Manager):

    def get_queryset(self):
        return EmployeeQuerySet(self.model, self._db)

    def employee_age(self):
        return self.get_queryset().employee_age()

