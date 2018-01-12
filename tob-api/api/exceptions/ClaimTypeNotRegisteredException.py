from rest_framework.exceptions import APIException

class ClaimTypeNotRegisteredException(APIException):
    """
    Claim Type Not Registered Exception
    """
    status_code = 400
    default_detail = 'The submitted claim type has not been registered.  Please register the claim type before submitting claims of that type.'
    default_code = 'bad_request'