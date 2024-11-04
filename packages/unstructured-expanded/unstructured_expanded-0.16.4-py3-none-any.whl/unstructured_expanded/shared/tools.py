from typing import Any


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
