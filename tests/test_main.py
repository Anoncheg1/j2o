from filecmp import cmp
import os

#
from j2o.__main__ import jupyter2org, DIR_AUTOIMGS

jupyter_4_2 = "./tests/draw-samples.ipynb"
jupyter_4_2_saved = "./tests/draw-samples.org"
# jupyter_4_2_images = ['10_0.png', '12_0.png', '14_0.png', '8_0.png']
jupyter_4_2_images_sizes = {'8_0.png':71156,
                            '10_0.png':58359,
                            '12_0.png':196616,
                            '14_0.png':272601
                            }

def test_converter():
    target_file_org = '/tmp/a.org'
    s_path = os.path.dirname(target_file_org)
    target_images_dir = os.path.normpath(os.path.join(s_path, DIR_AUTOIMGS))
    # - create directory for images:
    if not os.path.exists(target_images_dir):
        os.makedirs(target_images_dir)
    with open(target_file_org, "w") as f:
        jupyter2org(f,
                    source_file_jupyter=jupyter_4_2,
                    target_images_dir=target_images_dir)
    # - compare output file with our saved one
    assert cmp(target_file_org, jupyter_4_2_saved, shallow=False)
    # - check output files names and sizes in autoimgs directory
    onlyfiles = [f for f in os.listdir(target_images_dir) if os.path.isfile(os.path.join(target_images_dir, f))]
    assert len(onlyfiles) == len(jupyter_4_2_images_sizes.keys())
    assert all([x in onlyfiles for x in jupyter_4_2_images_sizes.keys()])
    for x in onlyfiles:
        assert jupyter_4_2_images_sizes[x] == os.stat(os.path.join(target_images_dir,x)).st_size
    print("success")


if __name__=="__main__":
    test_converter()
