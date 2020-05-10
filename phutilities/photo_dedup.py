import argparse
import logging
from pprint import pformat

from PIL import Image
from tqdm import tqdm

from phutilities.helpers import configure_colored_logging
from phutilities.helpers import gather_images
from phutilities.helpers import get_field

logger = logging.getLogger(__name__)


def map_date_to_file(img_file_list):
    img_it = tqdm(img_file_list)
    times = {}
    errors = []
    for img_path in img_it:
        img_it.set_description(f"Scanning dir: {args.src_path_1}")

        try:
            image = Image.open(img_path)
            exif = image._getexif()
            date = get_field(exif, "DateTimeOriginal")
            times[date] = img_path
        except OSError:
            errors.append(img_path)

    return times, errors


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
        "-o", "--output", help="Output file to write duplicate files from 'src_path_2'"
    )
    args.add_argument(
        "--debug", action="store_true", help="set debugging level to DEBUG"
    )
    return args.parse_args()


if __name__ == "__main__":

    args = get_args()

    configure_colored_logging(logging.DEBUG if args.debug else logging.INFO)

    img_files_1 = gather_images(args.src_path_1, args.extensions, args.recursive)
    d1, e1 = map_date_to_file(img_files_1)

    img_files_2 = gather_images(args.src_path_2, args.extensions, args.recursive)
    d2, e2 = map_date_to_file(img_files_2)

    # find same keys
    logger.info(f"Computing list of possible duplicates (based on time of shot)")
    d_common = {k: (d1[k], d2[k]) for k in set(d1.keys()) & set(d2.keys())}

    if args.output:
        logger.info(f"Writing output file to: {args.output}")
        with open(args.output, "w") as f:
            f.write("\n".join(p[1] for p in d_common.values()))
    else:
        print(pformat(d_common))

    logger.warning(f"List of errored image files:")
    logger.debug(pformat(e1 + e2))
