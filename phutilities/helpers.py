import glob
import logging
import os
from datetime import datetime
from typing import List

from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)


def get_field(exif, field: str):
    for k, v in exif.items():
        if TAGS.get(k) == field:
            return v


def get_time_taken(exif, fmt: str = "%Y:%m:%d %H:%M:%S") -> datetime:
    d = get_field(exif, "DateTimeOriginal")

    logger.debug(f"Image time: {d}")
    return datetime.strptime(d, fmt)


def gather_images(from_dir: str, extensions: List[str], recursive: bool = True):
    img_files = []
    for ext in extensions:

        logger.info(f"Collectiong *.{ext} files")
        pattrn = "**/*.{}" if recursive else "*.{}"

        img_files.extend(
            glob.glob(os.path.join(from_dir, pattrn.format(ext)), recursive=recursive,)
        )
        logger.info("Found {} total image files.".format(len(img_files)))

    return img_files


def configure_colored_logging(loglevel):
    # more info on coloredlogs formatting:
    # https://coloredlogs.readthedocs.io/en/latest/api.html#changing-the-colors-styles
    import coloredlogs

    field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
    field_styles["asctime"] = {}
    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
    # level_styles["debug"] = {}
    level_styles["debug"] = {"color": "white", "faint": True}
    coloredlogs.install(
        level=loglevel,
        use_chroot=False,
        fmt="%(levelname)-8s %(name)s:%(lineno)s  - %(message)s",
        level_styles=level_styles,
        field_styles=field_styles,
    )
