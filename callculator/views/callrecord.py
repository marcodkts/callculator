from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from callculator.serializers import CallRecordSerializer


@extend_schema(
    summary="Call Records",
    description="Call Records Operations.",
    tags=["call record"],
    responses={
        200: CallRecordSerializer,
    },
    auth=[],
)
class CallRecordViewSet(viewsets.GenericViewSet):
    serializer_class = CallRecordSerializer

    @extend_schema(
        request=CallRecordSerializer,
    )
    @action(methods=["post"], detail=False)
    def callrecord(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
