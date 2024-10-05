
# Table of Contents

1.  [j2o](#org0f5b20b)
2.  [Command line usage](#org849eb57)
3.  [How this works](#org03a1552)
4.  [Info: Other useful projects](#org70dde9a)
5.  [Info: Format of ipynb](#org5aa75ac)
6.  [features](#orgbd220b4)

    ![badge](https://github.com/Anoncheg1/j2o/actions/workflows/python-test.yml/badge.svg?event=push)
    ![badge](https://github.com/Anoncheg1/j2o/actions/workflows/python-publish.yml/badge.svg?event=release)


<a id="org0f5b20b"></a>

# j2o

Converter from Jupyter to Org file format without any dependencies.

Without this package your only alternative is to use nbconver or pandoc with 164
 dependencies just to be able to convert simple JSON format.

TODO: make reverse convrter.

<https://pypi.org/project/j2o/>


<a id="org849eb57"></a>

# Command line usage

    usage: j2o myfile.ipynb [-w] [-j myfile.ipynb] [-o myfile.org]

    Convert a Jupyter notebook to Org file (Emacs) and vice versa

    positional arguments:
      jupfile_              Jupyter file

    options:
      -h, --help            show this help message and exit
      -j JUPFILE, --jupfile JUPFILE
                            Jupyter file
      -o ORGFILE, --orgfile ORGFILE
                            Target filename of Org file. If not specified, it will
                            use the filename of the Jupyter file and append .ipynb
      -w, --overwrite       Flag whether to overwrite existing target file.


For Linux add this line to ```~/.bashrc```
```sh
  export PATH=$PATH:/home/u/.local/bin
```
<a id="org03a1552"></a>

# How this works

1.  Loops through "cells".
2.  Extract "source"
3.  add Org header and tail around source ("#+begin\_src python &#x2026;", "#+end\_src")


<a id="org70dde9a"></a>

# Info: Other useful projects

-   p2j <https://pypi.org/project/p2j/> <https://github.com/remykarem/python2jupyter>
-   <https://github.com/jkitchin/ox-ipynb>


<a id="org5aa75ac"></a>

# Info: Format of ipynb

JSON

    {
      cells: [
        cell_type: "code/markdown",
        source: ["\n","\n",""],
        outputs: [{
          text: ["\n", "\n"],
          data: {
            image/png: "base64....",
            text/plain: "image description"}
          }
        ]
      ],
      metadata: {
        kernelspec: {
          language: "python"
        }
      }
    }


<a id="orgbd220b4"></a>

# features

-   in markdown cells conversion: source blocks, ‘#’ to ‘\*’.
-   code cells: images
-   Tested for nbformat: 4.2.
