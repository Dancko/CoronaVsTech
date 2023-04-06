from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.mail import send_mail
from companies.dynamic import dynamic_fib_v2
from companies.serializers import CompanySerializer
from companies.models import Company


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_email(request: Request) -> Response:
    """Sends email to the user."""

    send_mail(
        subject=request.data.get("subject"),
        message=request.data.get("message"),
        from_email="sandboxsandbox77@gmail.com",
        recipient_list=["dchestnyh21@gmail.com"],
    )

    return Response(
        {"status": "success", "info": "email sent successfully"}, status=200
    )


@api_view(http_method_names=["GET"])
def fibonacci(request: Request) -> Response:
    n = request.GET.get("n")

    if n:
        try:
            n = int(n)
            if n >= 0:
                fi = dynamic_fib_v2(int(n))
                return Response({f"The {str(n)}th fibonacci number": str(fi)})
            else:
                raise ValueError

        except ValueError:
            return Response({"Error": f"{n} is incorrect data."}, status=400)

    return Response({"Error": "No data has been provided."}, status=400)
