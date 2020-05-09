import argparse
import logging
import os
import re
import shutil

from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm

from phutilities.helpers import configure_colored_logging
from phutilities.helpers import gather_images
from phutilities.helpers import get_field

logger = logging.getLogger(__name__)


def printTags():
    for (k, v) in Image.open(img_files[0])._getexif().iteritems():
        print("{} = {}".format(TAGS.get(k), v))
        input("...")


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("src_path", help="origin path where to read pictures from")
    args.add_argument(
        "dst_path", help="destiny path where to copy pictures in folders by date"
    )
    args.add_argument(
        "--debug", action="store_true", help="set debugging level to DEBUG"
    )
    args.add_argument(
        "--move", action="store_true", help="whether to move the files or copy"
    )
    args.add_argument(
        "--recursive", action="store_true", help="whether to explore recursiverlys"
    )
    args.add_argument(
        "--extensions",
        nargs="*",
        default=["JPG"],
        help="list of valid extensions to search for",
    )
    return args.parse_args()


if __name__ == "__main__":

    args = get_args()

    configure_colored_logging(logging.DEBUG if args.debug else logging.INFO)

    img_files = gather_images(args.src_path, args.extensions, args.recursive)

    img_it = tqdm(img_files)
    for img_path in img_it:
        try:
            img_it.set_description(f"opening: {img_path}")
            image = Image.open(img_path)
            exif = image._getexif()
            info = get_field(exif, "DateTimeOriginal")

            logger.debug(info)

            year, month, day = re.findall(r"(\d+):*", info.split(" ")[0])

            new_path = os.path.join(args.dst_path, year, month, day)
            if not os.path.exists(new_path):
                img_it.set_description(f"Creating: {new_path}")
                os.makedirs(new_path)

            img_name = os.path.split(img_path)[-1]
            if args.move:
                shutil.move(img_path, os.path.join(new_path, img_name))
            else:
                shutil.copy(img_path, new_path)
        except Exception as e:
            logger.error(f"Error organizing img {img_path}")
            logger.exception(e)
