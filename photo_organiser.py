import os
import re
import glob
import shutil
import logging
import argparse
import coloredlogs
from tqdm import tqdm
from PIL import Image
from PIL.ExifTags import TAGS


logger = logging.getLogger(__name__)


def printTags():
    for (k, v) in Image.open(img_files[0])._getexif().iteritems():
        print("{} = {}".format(TAGS.get(k), v))
        input("...")


def get_field(exif, field):
    for k, v in exif.items():
        if TAGS.get(k) == field:
            return v


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('src_path', help="origin path where to read pictures from")
    args.add_argument('dst_path', help="destiny path where to copy pictures in folders by date")
    args.add_argument('--debug', action="store_true", help="set debugging level to DEBUG")
    args.add_argument('--move', action="store_true", help="whether to move the files or copy")
    args.add_argument('--recursive', action="store_true", help="whether to explore recursiverlys")
    args.add_argument('--extensions', nargs="*", default=["JPG"],
                      help="list of valid extensions to search for")
    return args.parse_args()


if __name__ == "__main__":

    args = get_args()

    coloredlogs.install(logger=logger,
                        level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(filename)s:%(lineno)s - %(message)s")

    img_files = []
    for ext in args.extensions:
        logger.info("Collectiong *.{} files".format(ext))
        if args.recursive:
            extensions = "**/*.{}".format(ext)
        else:
            extensions = "*.{}".format(ext)

        img_files.extend(glob.glob(os.path.join(args.src_path, extensions),
                                   recursive=args.recursive))
        logger.info("Found {} total image files.".format(len(img_files)))

    img_it = tqdm(img_files)
    for img_path in img_it:
        try:
            img_it.set_description("opening: {}".format(img_path))
            image = Image.open(img_path)
            exif = image._getexif()
            info = get_field(exif, 'DateTimeOriginal')

            logger.debug(info)

            year, month, day = re.findall("(\d+):*", info.split(" ")[0])

            new_path = os.path.join(args.dst_path, year, month, day)
            if not os.path.exists(new_path):
                img_it.set_description("Creating: {}".format(new_path))
                os.makedirs(new_path)

            img_name = os.path.split(img_path)[-1]
            if args.move:
                shutil.move(img_path, os.path.join(new_path, img_name))
            else:
                shutil.copy(img_path, new_path)
        except Exception as e:
            logger.error("Error organizing img {}".format(img_path))
            logger.exception(e)
