from django.urls import path
from .views import TicketListCreateAPIView, TicketDetailUpdateAPIView, EstadisticasAPIView
from .views_auth import RegistroAPIView, LoginApiView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('tickets/', TicketListCreateAPIView.as_view(), name='tickets-list-create'),
    path('tickets/estadisticas/', EstadisticasAPIView.as_view(), name='tickets-estadisticas'),
    path('tickets/<str:ticket_id>/', TicketDetailUpdateAPIView.as_view(), name='ticket-detail-update'),

    path('registro/', RegistroAPIView.as_view(), name='registro-usuario'),
    path('login/', LoginApiView.as_view(), name='login-usuario'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]