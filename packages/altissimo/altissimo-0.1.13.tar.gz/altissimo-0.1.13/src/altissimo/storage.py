"""Altissimo Storage Class file."""

from google.cloud import storage


class Storage:
    """Storage class."""

    def __init__(self):
        """Initialize a class instance."""
        self.client = storage.Client()

    def upload_from_string(self, bucket_name, object_name, data, content_type=None, metadata=None):
        """Upload a new object from a string."""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        if metadata:
            blob.metadata = metadata
        blob.upload_from_string(data, content_type=content_type)
        return blob
