import base64
import logging
from OpenSSL import crypto

log = logging.getLogger(__name__)


def to_binary(sign):
    """
    Function that converts the signature to binary.
    """

    try:
        # Str to base64 to binary.
        sign = base64.decodebytes(str.encode(sign))
    except Exception as error:
        # Log.
        log.error(
            '[ERROR][LOGIC - to_binary]: {error} '.format(error=str(error)))
        return False

    return sign


def sanitize_signature(value):
    signature = base64.b64encode(value)
    signature = signature.decode('utf-8')
    return str(signature)


class Certificate(object):
    """
    Class responsible for processing the FNMT certificate.
    """

    def __init__(self, certificate_path, password):
        super(Certificate, self).__init__()
        self.__certificate_path = certificate_path
        self.__password = password

        self.__read_certificate()

        self.pkcs12 = self.__load_pkcs12()
        self.x509 = self.__get_x509()
        self.private_key = self.__get_private_key()

    def __read_certificate(self):
        # Read certificate.
        try:
            file = open(self.__certificate_path, "rb")
            self.__certificate_buffer = file.read()
            file.close()
        except IOError as error:
            # Log.
            log.error('[ERROR][Class Certificate]: {error} '.format(
                error=str(error)))
            raise error

    def __load_pkcs12(self):
        # Load pkcs12.
        return crypto.load_pkcs12(self.__certificate_buffer, self.__password)

    def __get_x509(self):
        # Get x509.
        return self.pkcs12.get_certificate()

    def __get_private_key(self):
        # Get the private key.
        return self.pkcs12.get_privatekey()
