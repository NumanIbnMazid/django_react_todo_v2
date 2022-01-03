from django.urls import path
from todos.api.views import TodoViewSet

urlpatterns = [
    # ==============================*** Todo URLS ***==============================
    path("create/", TodoViewSet.as_view({'post': 'create'}, name='create_todo')),
    path("create-or-update/multiple/", TodoViewSet.as_view({'post': 'create_or_update_multitodo'}, name='create_or_update_multitodo')),
    path("retrieve/<slug>/", TodoViewSet.as_view({"get": "retrieve"}, name="retrieve_todo")),
    path("update/<slug>/", TodoViewSet.as_view({"put": "update"}, name="update_todo")),
    path("partial/update/<slug>/", TodoViewSet.as_view({"patch": "partial_update"}, name="partial_update_todo")),
    path("delete/<slug>/", TodoViewSet.as_view({"delete": "destroy"}, name="delete_todo")),
    path("delete-multiple/", TodoViewSet.as_view({'post': 'destroy_multitodo'}, name='destroy_multitodo')),
    path("list/", TodoViewSet.as_view({"get": "list"}, name="list_todo")),
]