from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class CreateListDeleteMixinSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        GenericViewSet):

    permission_classes = (IsAdminOrReadOnly,)
