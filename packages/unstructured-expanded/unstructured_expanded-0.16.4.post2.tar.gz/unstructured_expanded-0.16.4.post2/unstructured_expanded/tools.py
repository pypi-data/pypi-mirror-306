import base64
from typing import Any

from unstructured.documents.elements import Image, ElementMetadata


def extract_desc(
        blip: Any,
        base_tag: str,
        namespaces: dict[str, str]
) -> str:
    blip_pic = blip.getparent().getparent()
    desc: str = "No Description Available"

    nv_pic_pr = blip_pic.find(f'{base_tag}:nvPicPr', namespaces=namespaces)
    if nv_pic_pr is not None:
        c_nv_pr = nv_pic_pr.find(f'{base_tag}:cNvPr', namespaces=namespaces)
        if c_nv_pr is not None:
            desc = c_nv_pr.attrib.get("descr")
            desc = desc.replace('\n\nDescription automatically generated', '')

    return desc


def create_image(
        image_bytes: bytes,
        desc: str,
) -> Image:
    image_b64: str = base64.b64encode(image_bytes).decode('utf-8')

    return Image(
        text=desc,
        metadata=ElementMetadata(
            image_base64=image_b64
        )
    )
