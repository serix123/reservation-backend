from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        view = renderer_context.get('view')
        status_code = response.status_code if response else 200

        # Default message based on status code
        default_messages = {
            200: 'Success',
            201: 'Created successfully',
            204: 'Deleted successfully',
            400: 'Validation error',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
            500: 'Server error'
        }

        # Initialize response structure
        formatted_response = {
            'status': 'success' if status_code < 400 else 'error',
            'message': None,
            'data': None,
            'errors': None
        }

        # Handle success responses
        if status_code < 400:
            if isinstance(data, dict):
                formatted_response['message'] = data.pop(
                    'message', default_messages.get(status_code, 'Success'))
                formatted_response['data'] = data
            else:
                formatted_response['message'] = default_messages.get(
                    status_code, 'Success')
                formatted_response['data'] = data

        # Handle error responses
        else:
            formatted_response['message'] = data.get(
                'detail', default_messages.get(status_code, 'Error occurred'))
            formatted_response['errors'] = data

        return super().render(formatted_response, accepted_media_type, renderer_context)

    def custom_exception_handler(exc, context):
        response = exception_handler(exc, context)

        if response is not None:
            error_data = response.data
            response.data = {
                'status': 'error',
                'message': error_data.get('detail', 'An error occurred'),
                'errors': error_data
            }

        return response
