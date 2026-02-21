import uuid
from django.db import models
from employees.models import Employee


class AttendanceStatus(models.TextChoices):
    PRESENT = 'Present', 'Present'
    ABSENT = 'Absent', 'Absent'


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='attendance_records'
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=AttendanceStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
