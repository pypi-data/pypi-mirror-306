import base64

from unstructured.documents.elements import Image, ElementMetadata


class ExpandedImage(Image):
    blob: bytes

    def __init__(self, blob: bytes, **kwargs):
        self.blob: bytes = blob
        super().__init__(**kwargs)

    @classmethod
    def load(
            cls,
            desc: str,
            image_bytes: bytes
    ) -> "ExpandedImage":
        image_b64: str = base64.b64encode(image_bytes).decode('utf-8')

        return cls(
            blob=image_bytes,
            text=desc,
            metadata=ElementMetadata(
                image_base64=image_b64
            )
        )