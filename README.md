
# Table of Contents

1.  [j2o](#org0ada202)
2.  [Command line usage](#orgcd3c96d)
3.  [Other useful projects](#org4772b96)
4.  [Review of format for ipynb](#org9e2dc55)
5.  [How it works](#org4355db8)
6.  [features](#org2ac1c27)


<a id="org0ada202"></a>

# j2o

Converter from Jupyter to Org file format without any dependencies.

I don't want to install Jupyter core and nbconver or pandoc with 164
 dependencies just to be able to convert simple JSON format, that is
 why I just wrote coverter from scratch.

Tested for nbformat: 4.2.

TODO: make reverse convrter.

<https://pypi.org/project/j2o/>


<a id="orgcd3c96d"></a>

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


<a id="org4772b96"></a>

# Other useful projects

-   p2j <https://pypi.org/project/p2j/> <https://github.com/remykarem/python2jupyter>
-   <https://github.com/jkitchin/ox-ipynb>


<a id="org9e2dc55"></a>

# Review of format for ipynb

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


<a id="org4355db8"></a>

# How it works

1.  Loops through "cells".
2.  Extract "source"
3.  add Org header and tail around source ("#+begin\_src python &#x2026;", "#+end\_src")


<a id="org2ac1c27"></a>

# features

-   in markdown cells conversion: source blocks, ‘#’ to ‘\*’.
-   code cells: images

