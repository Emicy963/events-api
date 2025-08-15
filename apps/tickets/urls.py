from django.urls import path
from . import views

urlpatterns = [
    path("order/create/", views.create_order, name="create_order"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("<uuid:ticket_id>/validate/", views.validate_ticket, name="validate_ticket"),
    path("event/<int:event_id>/ticket-types/", views.TicketTypeListView.as_view(), name="ticket_type_list"),
]

