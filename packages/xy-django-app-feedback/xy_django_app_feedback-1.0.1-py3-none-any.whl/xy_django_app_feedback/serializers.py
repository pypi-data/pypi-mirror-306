from .models import MFeedback
from rest_framework import viewsets
from xy_django_serializer.Serializer import Serializer


class SFeedback(Serializer):

    default_value = ""

    class Meta:
        model = MFeedback
        fields = "__all__"


# ViewSets define the view behavior.
class VSFeedback(viewsets.ModelViewSet):
    queryset = MFeedback.objects.all()
    serializer_class = SFeedback
