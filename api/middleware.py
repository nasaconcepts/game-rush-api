# from django.utils.deprecation import MiddlewareMixin
# from api.util.utils import api_response
#
# class ExceptionMiddleware(MiddlewareMixin):
#     def process_exception(self, request, exception):
#         """
#         Capture all uncaught exceptions and return a standard API response.
#         """
#         return api_response(
#             success=False,
#             message="An unexpected error occurred",
#             errors=str(exception),
#             status=500
#         )
