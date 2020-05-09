Ph(oto)-Utilities
=======

Small collection of utilities to handle image files.

- Organize pictures by date: Explore, maybe recursiverly, a folder and 
  copy or move to a date based folder structure: `year > month > day`
- Find duplicates: Scan two directories, maybe recursively, to find possible duplicate images based in the time of `DateTimeOriginal` in the exif metadata. 

<!--ts-->
   * [Ph(oto)-Utilities](#photo-utilities)
      * [Run](#run)
      * [Requierements](#requierements)

<!-- Added by: jose, at: Sat  9 May 19:21:18 CEST 2020 -->

<!--te-->

Run
--

```sh
	python photo_organiser.py <src_fodler> <dst_folder> \
        [--recursively] [--move] \
        [--extensions <ext1> <ext2>]
```

Requierements
-------

* python>=3.5
* tqdm==4.14.0
