from django.urls import path

from NEMO_osticket.views import osticket

urlpatterns = [
    path("osticket/create_ticket/<int:tool_id>/", osticket.create_ticket, name="osticket_create_ticket"),
    # Override tool status to add our own osticket tab
    path("tool_status/<int:tool_id>/", osticket.tool_status, name="tool_status"),
]
