from enum import Enum

class AuthProvider(Enum):
    LOCAL = "local"
    GOOGLE = "google"
    FACEBOOK = "facebook"