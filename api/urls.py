from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from teacher_app.models import Paper


class PaperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paper
        fields = ["id", "name", "description", "is_published", "user_id"]


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer


router = routers.DefaultRouter()
router.register("papers", PaperViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
