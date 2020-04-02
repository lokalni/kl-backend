from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from kl_participants.models import Student
from kl_participants.serializers.student_serializer import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    filterset_fields = ['group']
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], serializer_class=Serializer)
    def reset_access(self, request, pk):
        """Create and join as moderator."""
        student = self.get_object()
        student.reset_token()
        student.save()
        student.refresh_from_db()
        return Response(data=StudentSerializer(instance=student).data)

