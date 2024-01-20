from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.permissions import IsAdminOrReadOnly


schema_view = get_schema_view(
    openapi.Info(
        title = "Notifications ",
        default_version = "v1",
        description = "Сервис уведомлений",
        license = openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=(IsAdminOrReadOnly,),
)

urlpatterns = [
    path(
        "docs(?P(<format>\.json|\.yaml)",
        schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "docs/", schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"),
]