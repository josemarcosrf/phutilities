import argparse
import logging
import re

from PIL import Image
from tqdm import tqdm

from phutilities.helpers import configure_colored_logging
from phutilities.helpers import gather_images
from phutilities.helpers import get_field

logger = logging.getLogger(__name__)


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("src_path_1", help="first path where to scan for pictures")
    args.add_argument("src_path_2", help="second path where to scan for pictures")

    args.add_argument(
        "--recursive", action="store_true", help="whether to explore recursiverlys"
    )
    args.add_argument(
        "--extensions",
        nargs="*",
        default=["JPG", "jpg"],
        help="list of valid extensions to search for",
    )
    args.add_argument(
        "--debug", action="store_true", help="set debugging level to DEBUG"
    )
    return args.parse_args()


if __name__ == "__main__":

    args = get_args()

    configure_colored_logging(logging.DEBUG if args.debug else logging.INFO)

    img_files_1 = gather_images(args.src_path_1, args.extensions, args.recursive)
    img_files_2 = gather_images(args.src_path_2, args.extensions, args.recursive)

    img_it = tqdm(img_files_1)
    for img_path in img_it:

        image = Image.open(img_path)
        exif = image._getexif()
        info = get_field(exif, "DateTimeOriginal")

        logger.debug(info)

        year, month, day = re.findall(r"(\d+):*", info.split(" ")[0])
        hour, minute, seconds = re.findall(r"(\d+):*", info.split(" ")[1])

        logger.debug(f"EXif date info: {info}")

        exit()
