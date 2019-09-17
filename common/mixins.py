from datetime import datetime

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from common.decorators import login_not_required
from common.decorators import required_params


class LoginNotRequiredMixin:

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return login_not_required(view_func=view)


class SyncMixin:

    @required_params
    @action(methods=['post'], detail=False)
    def sync(self, request, date_time, *args, **kwargs):
        try:
            dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            result = self.queryset.model.get_ids_for_sync(self.get_queryset(), dt)
            return Response(data=result)
        except Exception as e:
            return Response(data={'error': str(e)}, status=HTTP_400_BAD_REQUEST)

    def _get_meta_result(self, ids):
        queryset = self.get_queryset().filter(pk__in=ids)
        serializer = self.get_serializer(queryset, many=True)
        result = serializer.data
        return result

    @action(methods=['post'], detail=False)
    def meta(self, request, *args, **kwargs):
        ids = set(request.data.get('ids', []))
        result = self._get_meta_result(ids)
        return Response(result, status=HTTP_200_OK)
