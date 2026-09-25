from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError


def raise_validation_error(exc):
    if hasattr(exc, "error_dict"):
        detail = {
            field: [str(error) for error in errors]
            for field, errors in exc.message_dict.items()
        }
        raise ValidationError(detail) from exc
    raise ValidationError([str(message) for message in exc.messages]) from exc


def save_or_validation_error(serializer):
    try:
        serializer.save()
    except DjangoValidationError as exc:
        raise_validation_error(exc)
