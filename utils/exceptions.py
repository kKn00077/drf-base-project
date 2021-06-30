from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.views import exception_handler


"""
TODO: 모든 에러코드, 디테일 등 자세히 정하고 수정
"""

VALIDATION_ERROR_CODE = 2000
NOT_FOUNT_ERROR_CODE = 2001
AUTHENTICATION_ERROR_CODE = 2002


def exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:

        error_detail = exc.args[0] if isinstance(
            exc, Http404) else exc.default_detail
        data = {'status_code': response.status_code,
                'error_code': getattr(exc, 'error_code', 'N/A'),
                'error_class': exc.__class__.__name__,
                'error_detail': error_detail}

        if isinstance(exc, serializers.ValidationError):
            data['error_code'] = VALIDATION_ERROR_CODE

            if isinstance(response.data, list):
                if isinstance(response.data[-1], dict):
                    targets = []
                    for d in response.data:
                        errors = []
                        for key, val in d.items():
                            errors.append({'string':key, 'code':val[0].code})
                        targets.append(errors)
                else:
                    targets = [{'string': str(error_detail), 'code': error_detail.code} for error_detail in
                               response.data]
            elif isinstance(response.data, dict):
                targets = [{'string': key, 'code': val[0].code}
                           for key, val in response.data.items()]
            data['targets'] = targets
            response.data = data
        else:
            
            if isinstance(exc, Http404):
                data['error_code'] = NOT_FOUNT_ERROR_CODE
            elif isinstance(exc, AuthenticationFailed):
                data['error_code'] = AUTHENTICATION_ERROR_CODE

            error_detail = response.data.pop('detail', None)
            targets = {'string': str(
                error_detail), 'code': error_detail.code} if error_detail is not None else 'N/A'
            data['targets'] = [targets]
            response.data.update(data)

    return response


class AppExceptions:
    class ExampleException(APIException):
        error_code = None
        status_code = 400
        default_detail = ''
        default_code = ''