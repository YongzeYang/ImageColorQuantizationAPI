from rest_framework.response import Response
from rest_framework import status

class JsonResponse(Response):

    # General response status
    MISSING_PARAMETERS = (-1, "One or more query parameter(s) are missing.", status.HTTP_400_BAD_REQUEST)
    SUCCESS = (1, "Success", status.HTTP_200_OK)
    UNKNOWN_ERROR = (-1, "Unknown error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    SERVER_ERROR = (-1, "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    UNAUTHORIZED = (-1, "Unauthorized request, please log in first", status.HTTP_401_UNAUTHORIZED)
    NOT_FOUND = (-1, "Not found", status.HTTP_404_NOT_FOUND)
    SERVICE_UNAVAILABLE = (-1, "Service unavailable", status.HTTP_503_SERVICE_UNAVAILABLE)
    INTERNAL_SERVER_ERROR = (-1, "Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    NOT_LOGIN = (-1, "You are not login", status.HTTP_400_BAD_REQUEST)
    EMPTY_ID = (-1, "Please enter the id ", status.HTTP_200_OK)
    NO_QUERY_PARAMETER = (-1, "At least 1 parameter is required!", status.HTTP_400_BAD_REQUEST)

    # User related response
    EMAIL_REQUIRED = (-1, "The Email is required", status.HTTP_200_OK)
    EMAIL_EXISTS = (-1, "The Email is already in use", status.HTTP_200_OK)
    EMAIL_NOT_EXIST = (-1, "The Email does not exist", status.HTTP_200_OK)
    PASSWORD_REQUIRED = (-1, "The Password is required", status.HTTP_200_OK)
    AUTHENTICATION_FAILED = (-1, "The authentication is failed, please check your email or password.", status.HTTP_200_OK)

    # Task related response
    FILE_MISSING = (-1, "The required file is missing. Please upload ALL the files required.", status.HTTP_200_OK)
    FILE_NOT_EXISTS = (-1, "The file does not exist.", status.HTTP_200_OK)
    DATATYPE_UNMATCH = (-1, "The file uploaded does not match the datatype.", status.HTTP_200_OK)
    PIPELINE_FAIL = (-1, "The pipeline is failed. ", status.HTTP_500_INTERNAL_SERVER_ERROR)
    TASK_EXISTS = (-1, "The file already exists. ", status.HTTP_200_OK)
    TASK_NOT_EXISTS = (-1, "The task does not exist. ", status.HTTP_200_OK)
    INVALID_DATASET_TYPE = (-1, "Invalid dataset type. We only support NGS, TGS or mix. ", status.HTTP_200_OK)
    FILE_NOT_FOUND = (-1, "The file(s) do(es) not exist.", status.HTTP_200_OK)
    RESULT_NOT_READY = (-1, "The result file has not been generated.", status.HTTP_200_OK)
    INVALID_FILE_TYPE = (-1, "Invalid file type parameter. Only ngs_fq1, ngs_fq2, tgs_fq or bam is allowed.", status.HTTP_400_BAD_REQUEST)

    # Result related response
    EMPTY_RESULT = (-1, "The database does not contain any generated result. ", status.HTTP_200_OK)
    FILE_UNAVAILABLE = (-1, "The file is not available!", status.HTTP_200_OK)
    NOT_PUBLIC = (-1, "The result is not open to public!", status.HTTP_200_OK)
    RESULT_NOT_EXISTS = (-1, "The result does not exist.", status.HTTP_200_OK)
    RESULT_NOT_EXISTS_BY_TASK_ID = (-1, "The result corresponding to task ID does not exist!", status.HTTP_200_OK)
    ALREADY_EXECUTED = (-1, "The analysis has already been executed!", status.HTTP_200_OK)

    # Image related response
    INVALID_IMAGE_TYPE = (-1, "Please upload a valid image (e.g. jpg, png, ...)!", status.HTTP_200_OK)
    IMAGE_ALREADY_UPLOADED = (-1, "The image has already been uploaded!", status.HTTP_200_OK)
    IMAGE_NOT_UPLOADED = (-1, "The image has not been uploaded!", status.HTTP_200_OK)
    INVALID_IMAGE_ID = (-1, "The image id does not exist!", status.HTTP_200_OK)
    INAVLID_METHOD = (-1, "Invalid method! We only support K-Means, Bisecting K-Means, and Gaussian Mixture.", status.HTTP_200_OK)

    NOT_GENERATED_YET = (-1, "The image has not been generated!", status.HTTP_200_OK)

    def __init__(self, message_tuple=SUCCESS, data=None):
        code, message, status_code = message_tuple
        super().__init__(
            {
                "code": code,
                "message": message,
                "data": data or {}
            },
            status=status_code
        )