from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    @action(detail=True, methods=['get'], url_path='attendance')
    def attendance(self, request, pk=None):
        employee = self.get_object()
        records = employee.attendance_records.all()

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if date_from:
            records = records.filter(date__gte=date_from)
        if date_to:
            records = records.filter(date__lte=date_to)

        total_present = records.filter(status='Present').count()
        total_absent = records.filter(status='Absent').count()

        return Response({
            'employee_id': employee.employee_id,
            'employee_name': employee.full_name,
            'total_present': total_present,
            'total_absent': total_absent,
            'records': [
                {'date': r.date, 'status': r.status}
                for r in records
            ],
        })

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        from datetime import date
        today = date.today()

        total_employees = Employee.objects.count()

        department_breakdown = list(
            Employee.objects.values('department')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        from attendance.models import Attendance
        today_records = Attendance.objects.filter(date=today)
        present = today_records.filter(status='Present').count()
        absent = today_records.filter(status='Absent').count()
        not_marked = total_employees - present - absent

        attendance_rate = round((present / total_employees * 100), 1) if total_employees > 0 else 0

        return Response({
            'total_employees': total_employees,
            'department_breakdown': department_breakdown,
            'today_attendance': {
                'date': today.isoformat(),
                'present': present,
                'absent': absent,
                'not_marked': not_marked,
            },
            'attendance_rate': attendance_rate,
        })
