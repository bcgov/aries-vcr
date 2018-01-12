from rest_framework.exceptions import APIException

class OrganizationNotRegisteredException(APIException):
    """
    Organization Not Registered Exception
    """
    status_code = 400
    default_detail = 'The submitted claim referances an organization that has not been registered.  Please register the organization before submitting the related claims.'
    default_code = 'bad_request'