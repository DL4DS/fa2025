#!/usr/bin/env python3

import pathlib
import re
import sys

with open("lecture_dates.tsv") as lecture_dates_fp:
    lecture_dates = lecture_dates_fp.readlines()

lecture_dates = [l.rstrip().split("\t") for l in lecture_dates]

path = pathlib.Path(".")
for (lecture_number, lecture_date) in lecture_dates:
    lecture_mds = path.glob(f"{lecture_number:s}_*.md")
    lecture_mds = list(lecture_mds)
    if len(lecture_mds) == 0:
        sys.stderr.write(f"Lecture {lecture_number:s} not found.\n")
        continue

    if len(lecture_mds) > 1:
        sys.stderr.write(f"Multiple lecture {lecture_number:s}s found.\n")
        for f in lecture_mds:
            sys.stderr.write(str(f) + "\n")
        sys.exit(1)

    (lecture_md,) = lecture_mds
    lecture_slug = str(lecture_md).split(".")[0]
    with open(lecture_md) as read_fp:
        lecture_data = read_fp.readlines()

    for (i, l) in enumerate(lecture_data):
        if l.startswith("date:"):
            lecture_data[i] = f"date: {lecture_date}\n"

        if l.startswith("hide_from_announcments:"):
            lecture_data[i] = "hide_from_announcments: true\n"

        slide_prefix = "    - url: /static_files/lectures/"
        if l.startswith(slide_prefix) and "_annotated.pdf" in l:
            lecture_data[i] = f"{slide_prefix}{lecture_slug}_annotated.pdf\n"
        elif l.startswith(slide_prefix):
            lecture_data[i] = f"{slide_prefix}{lecture_slug}.pdf\n"
            pass

        if l.startswith("title:"):
            l = l.split()
            if re.fullmatch("([0-9]+)", l[1]):
                l[1] = lecture_number
            elif re.match('"([0-9]+)', l[1]):
                l[1] = '"' + lecture_number
            lecture_data[i] = " ".join(l) + "\n"

    with open(lecture_md, "w") as write_fp:
        for l in lecture_data:
            write_fp.write(l)
