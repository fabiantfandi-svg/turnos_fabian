from django.urls import path
from .views import TicketListCreateAPIView, TicketDetailUpdateAPIView, EstadisticasAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('tickets/', TicketListCreateAPIView.as_view(), name='tickets-list-create'),
    path('tickets/estadisticas/', EstadisticasAPIView.as_view(), name='tickets-estadisticas'),
    path('tickets/<str:ticket_id>/', TicketDetailUpdateAPIView.as_view(), name='ticket-detail-update'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]