import logging
import sys

def error_message_detail(error, error_details: sys):
    _, _, exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    err = "Error occurred in python script [{0}] on line [{1}] with message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    return err

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  # Corrected use of super()
        self.error_message = error_message_detail(error_message, error_details=error_detail)

    def __str__(self):
        return self.error_message


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     try:
#         a = 1 / 0
#     except Exception as e:
#         logging.error("An error occurred: %s", str(e))
#         raise CustomException(e, sys)
