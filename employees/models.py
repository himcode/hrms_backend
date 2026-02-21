import uuid
from django.db import models


class Department(models.TextChoices):
    HR = 'HR', 'Human Resources'
    ENGINEERING = 'Engineering', 'Engineering'
    FINANCE = 'Finance', 'Finance'
    MARKETING = 'Marketing', 'Marketing'
    SALES = 'Sales', 'Sales'
    OPERATIONS = 'Operations', 'Operations'
    IT = 'IT', 'Information Technology'
    LEGAL = 'Legal', 'Legal'


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.CharField(max_length=10, unique=True, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=20, choices=Department.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last = Employee.objects.order_by('-employee_id').first()
            if last and last.employee_id:
                num = int(last.employee_id.split('-')[1]) + 1
            else:
                num = 1
            self.employee_id = f"EMP-{num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
