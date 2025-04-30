from enum import Enum
class BookUploadStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"