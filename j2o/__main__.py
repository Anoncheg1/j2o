import argparse
import sys
import json
import base64
import os
from io import TextIOWrapper
import logging


# source_filename = './draw-samples.ipynb'
DIR_TARGET = './autoimgs'
org_babel_min_lines_for_block_output = 10 # ob-core.el org-babel-min-lines-for-block-output


def jupyter2org(f:TextIOWrapper, source_file_jupyter: str):

    # PRINT = lambda *x: print("".join(x))
    # f = open("out.org", "w")
    PRINT = lambda *x: f.write("".join(x) + '\n')

    try:
        with open(source_file_jupyter, "r", encoding="utf-8") as infile:
            myfile = json.load(infile)
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)


    for i, cell in enumerate(myfile["cells"]):
        # -- collect source
        source_lines = cell["source"]
        # -- prepare headers
        header = "#+begin_src python :results output :exports both :session s1"
        tail = "#+end_src"

        # -- collect outputs
        outputs = []
        if "outputs" in cell:
            for j, output in enumerate(cell["outputs"]):
                o = {"text": None, "file_path": None, "data_descr": None}
                # -- test
                if "text" in output:
                    outputs_text = output["text"]
                    o["text"] = outputs_text
                # -- data
                if "data" in output and "image/png" in output["data"]:
                    # - 1) save image 2) insert link to output text 3) format source block header with link
                    # - decode image and remember link to file
                    b64img = base64.b64decode(output["data"]["image/png"])
                    fpath = os.path.join(DIR_TARGET, f'{i}_{j}.png')
                    o["file_path"] = fpath
                    # - save to file
                    with open(fpath, 'wb') as b64imgfile:
                        b64imgfile.write(b64img)
                    # - add description for link
                    if "text/plain" in output["data"]:
                        o["data_descr"] = output["data"]["text/plain"]
                    # - change header for image
                    if "graphics" not in header: # add only first image to header
                        header = f"#+begin_src python :results file graphics :file {fpath} :exports both :session s1"
                outputs.append(o)

        # -- print source
        if cell["cell_type"] == "markdown":
            source_lines = [s.replace("<br>", "") for s in source_lines]
            PRINT(source_lines[0].replace("#", "*"))
            if len(source_lines) > 1:
                PRINT("".join(source_lines[1:]))
            # PRINT('# asd')
        else: #== "code":
            PRINT(header)
            PRINT("".join(source_lines))
            PRINT(tail)
            PRINT()

        # -- print outputs - text and data
        for k, o in enumerate(outputs):
            # -- test
            # o = {"text": None, "data_file": None, "data_descr": None}
            if o["text"] is not None:
                if len(o["text"]) <= org_babel_min_lines_for_block_output:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else "")) # add index for several RESULT
                    PRINT("".join([": " + t for t in o["text"]])) # .startswith()
                    PRINT()
                else:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else ""))
                    PRINT("#+begin_example")
                    for t in o["text"]:
                        if t[0] == '*' or t.startswith("#+"):
                            PRINT("," + t)
                        else:
                            PRINT(t)
                    PRINT("#+end_example")
                    PRINT()
            if o["file_path"] is not None:
                # if RESULT is ferst we don't add name to it
                if o["text"] is not None and k == 0:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else ""))
                else:
                    PRINT("#+RESULTS:" + (f"{i}_{k}" if k > 0 else "")) # add index for several RESULT
                # - PRINT link
                # desc = "" if o["data_descr"] is None else "[" + "".join(o["data_descr"]) + "]"
                desc = "" if o["data_descr"] is None else "".join(o["data_descr"])
                PRINT("[[file:" + o["file_path"] +  "]] " + desc)
                PRINT()


def parse():
    parser = argparse.ArgumentParser(
        description="Convert a Jupyter notebook to Org file (Emacs) and vice versa",
        usage="j2o myfile.py")
    parser.add_argument("-j", "--jupfile",
                        help="Jupyter file")
    parser.add_argument("-o", "--orgfile",
                        help="Target filename of Org file. If not specified, " +
                        "it will use the filename of the Jupyter file and append .ipynb")
    parser.add_argument("-w", "--overwrite",
                        action="store_true",
                        help="Flag whether to overwrite existing target file.")
    return parser.parse_args()


def main(source_file_jupyter: str, target_file_org: str = None, overwrite: bool = False):
    """"""
    print(source_file_jupyter, target_file_org, overwrite)
    # - create directory for images:
    if not os.path.exists(DIR_TARGET):
        os.makedirs(DIR_TARGET)
    # - create target_file_org
    if target_file_org is None:
        target_file_org = os.path.splitext(source_file_jupyter)[0] + '.org'

    # - overwrite?
    if not overwrite:
        if os.path.isfile(target_file_org):
            logging.critical("File already exist.")
            return

    # - create target file and start conversion
    with open(target_file_org, "w") as f:
        jupyter2org(f, source_file_jupyter)


if __name__=="__main__":
    args = parse()
    main(args.jupfile, args.orgfile, args.overwrite)
