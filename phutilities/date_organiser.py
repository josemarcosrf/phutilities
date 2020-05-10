import argparse
import glob
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


def copy_or_move(img_path, new_path, move: bool, move_along: bool, dry_run: bool):
    if move_along:
        # if we need to move along find all files with the same name to move
        files = glob.glob(f"{img_path}*")
    else:
        # otherwise move just the specified image
        files = [img_path]

    for f in files:
        if move:
            if dry_run:
                img_it.write(f"mv {f} {new_path}")
            else:
                shutil.move(f, new_path)
        else:
            if dry_run:
                img_it.write(f"cp {f} {new_path}")
            else:
                shutil.copy(f, new_path)


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("src_path", help="origin path where to read pictures from")
    args.add_argument(
        "dst_path", help="destiny path where to copy pictures in folders by date"
    )
    # File operation options
    op = args.add_argument_group("File operation")
    op.add_argument(
        "--move", action="store_true", help="whether to move the files or copy"
    )
    op.add_argument(
        "--move-along",
        action="store_true",
        help=(
            "Move any file sharing the same name along with the picture. "
            "e.g.: Move/Copy .xmp files created by RawTherappe"
        ),
    )
    # File discovery options
    dis = args.add_argument_group("File disocvery")
    dis.add_argument(
        "--recursive", action="store_true", help="whether to explore recursiverlys"
    )
    dis.add_argument(
        "--extensions",
        nargs="*",
        default=["JPG", "jpg"],
        help="list of valid extensions to search for",
    )
    dis.add_argument(
        "--exclude",
        help="text file with paths to exclude from copying. One path per line",
    )
    # Other options
    args.add_argument(
        "--debug", action="store_true", help="set debugging level to DEBUG"
    )
    args.add_argument(
        "--dry-run",
        action="store_true",
        help="If the flag is present, action will only be printed but not executed",
    )
    return args.parse_args()


if __name__ == "__main__":

    args = get_args()

    configure_colored_logging(logging.DEBUG if args.debug else logging.INFO)

    img_files = gather_images(args.src_path, args.extensions, args.recursive)

    # read a list of files to exclude if present
    exclusion_list = []
    if args.exclude:
        with open(args.exclude, "r") as f:
            exclusion_list = f.readlines()

    img_it = tqdm(img_files)
    for img_path in img_it:
        try:
            if img_path in exclusion_list:
                img_it.set_description(f"Ignoring: {img_path}")
                continue
            else:
                img_it.set_description(f"opening: {img_path}")
                image = Image.open(img_path)
                exif = image._getexif()
                info = get_field(exif, "DateTimeOriginal")

                # get the data attributes as stings
                year, month, day = re.findall(r"(\d+):*", info.split(" ")[0])

                new_path = os.path.join(args.dst_path, year, month, day)
                if not os.path.exists(new_path):
                    img_it.set_description(f"Creating: {new_path}")
                    if not args.dry_run:
                        os.makedirs(new_path)

                copy_or_move(
                    img_path, new_path, args.move, args.move_along, args.dry_run
                )

        except Exception as e:
            logger.error(f"Error organizing img {img_path}")
            logger.exception(e)
