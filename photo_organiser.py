import os
import re
import glob
import shutil
import argparse
from tqdm import tqdm
from PIL import Image
from PIL.ExifTags import TAGS


def printTags():
    for (k,v) in Image.open(img_files[0])._getexif().iteritems():
        print("{} = {}".format(TAGS.get(k), v))
        input("...")


def get_field (exif, field) :
    for k, v in exif.items():
        if TAGS.get(k) == field:
            return v


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('src_path', help="origin path where to read pictures from")
    args.add_argument('dst_path', help="destiny path where to copy pictures in folders by date")
    args.add_argument('--move', action="store_true", help="whether to move the files or copy")
    args.add_argument('--recursive', action="store_true", help="whether to explore recursiverlys")
    args.add_argument('--extensions', nargs="*", default=["JPG"],
                      help="list of valid extensions to search for")
    args = args.parse_args()

    img_files = []
    for ext in args.extensions:
        pattrn = "**/*.{}" if args.recursive else "*.{}"
        print("Collectiong *.{} files".format(ext))
        img_files.extend(glob.glob(os.path.join(args.src_path, pattrn.format(ext)),
                                   recursive=args.recursive))

    img_it = tqdm(img_files)
    for img_path in img_it:
        image = Image.open(img_path)
        exif = image._getexif()
        info = get_field(exif,'DateTimeOriginal')
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