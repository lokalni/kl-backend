from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from kl_participants.models import Student
from kl_participants.serializers.student_serializer import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    permission_classes = []  # TODO

    @action(detail=True, methods=["post"], serializer_class=Serializer)
    def reset_access(self, request):
        """Create and join as moderator."""
        # check r
        student = self.get_object()
        student.reset_token()
        student.save()

        return Response(data=self.serializer_class(instance=student).data)

