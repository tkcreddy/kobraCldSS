import socket
import hashlib
import uuid
import hmac
import base64
import time
import re
from utils.singleton import Singleton
from utils.ReadConfig import ReadConfig as rc


class _UtilitiesExtension:
    def __init__(self, key):
        self.key = key

    def generate_time_based_uid(self) -> str:
        # Get current timestamp
        current_time = int(time.time() * 1000000)  # Convert to milliseconds

        # Create a UUID using the timestamp
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, str(current_time))

        # Encode the UID to base64
        base64_encoded = base64.urlsafe_b64encode(uid.bytes).decode('utf-8')

        # Remove padding characters
        base64_encoded = base64_encoded.rstrip("=")
        base64_encoded = re.sub("-", "_", base64_encoded)

        return base64_encoded

    def generate_uuid_with_key(self) -> str:
        # Use SHA-256 hash function
        hash_object = hashlib.sha256(self.key.encode())
        hashed_key = hash_object.digest()

        # Encode the hashed key to base64
        base64_encoded = base64.b64encode(hashed_key).decode('utf-8')

        # Create a UUID-like alphanumeric string
        generated_uuid = base64_encoded[:-2]  # Trim '==' from the end

        return generated_uuid

    def encode_hostname_with_key(self, hash_algorithm='sha256', hostname: str = None) -> str:
        """
        Encodes the hostname using the provided key and a hash algorithm.

        :param hostname:
        :param key: Secret key used for encoding.
        :param hash_algorithm: Hash algorithm to use (default is 'sha256').
        :return: Encoded hash of the hostname.
        """
        # Get the hostname of the machine
        if hostname is None:
            self.hostname = socket.gethostname()
        else:
            self.hostname = hostname

        # Create a HMAC object using the key and hash algorithm
        hmac_object = hmac.new(self.key.encode(), self.hostname.encode(), getattr(hashlib, hash_algorithm))

        # Return the hexadecimal digest of the HMAC
        return hmac_object.hexdigest()


class UtilitiesExtension(_UtilitiesExtension, metaclass=Singleton):
    pass


def main():
    read_config = rc("/Users/krishnareddy/PycharmProjects/kobraCldSS")
    # key = "your_key_here"
    key_read = read_config.encryption_config
    key = key_read['key']
    ue = UtilitiesExtension(key)
    print(ue.encode_hostname_with_key())


if __name__ == "__main__":
    main()