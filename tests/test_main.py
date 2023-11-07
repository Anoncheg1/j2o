from filecmp import cmp
#
from j2o.__main__ import jupyter2org

jupyter_4_2 = "./tests/draw-samples.ipynb"
jupyter_4_2_saved = "./tests/draw-samples.org"

def test_converter():
    target_file_org = '/tmp/a.org'
    with open(target_file_org, "w") as f:
        jupyter2org(f, jupyter_4_2)
    assert cmp(target_file_org, jupyter_4_2_saved, shallow=False)


if __name__=="__main__":
    test_converter()
