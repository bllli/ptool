from typing import Optional

from seeder.oss.smms import SMMSClient


def upload_image(img_path) -> Optional[str]:
    return _upload_using_smms(img_path)


def _upload_using_smms(image_path) -> Optional[str]:
    smms = SMMSClient()
    url = smms.upload(image_path)
    return url
