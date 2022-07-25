#!/usr/bin/env python3

from pathlib import Path
import os


def create_file(file: Path):
    if file.exists():
        return

    sep = os.path.sep
    str_path = str(file.resolve())

    pp = str_path.split(sep)

    for index, _ in enumerate(pp):
        ppp = pp[0 : (index + 1)]

        str_tmp_p = sep.join(ppp)
        tmp_p = Path(
            str_tmp_p if str_tmp_p.startswith(file.root) else file.root + str_tmp_p
        )

        if tmp_p.exists():
            continue
        else:
            if index < (len(pp) - 1):
                os.makedirs(tmp_p)
            else:
                # is file
                with open(tmp_p, "w") as f:
                    f.write("")
