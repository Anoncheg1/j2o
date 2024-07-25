from filecmp import cmp
import os

#
from j2o.__main__ import jupyter2org, markdown_to_org

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
    t_path, file_name =  os.path.split(target_file_org)  # "/var/va.org" - > ('/var', 'va.org')
    file_name_short = os.path.splitext(file_name)[0] # # "va.org" -> ('va', '.org')
    image_dir = '/tmp/' + file_name_short[:3] + '-' + file_name_short[-3:] + '-imgs'
    # - create directory for images:
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    with open(target_file_org, "w") as f:
        jupyter2org(f,
                    source_file_jupyter=jupyter_4_2,
                    target_images_dir=image_dir)
    # - compare output file with our saved one
    assert cmp(target_file_org, jupyter_4_2_saved, shallow=False)
    # - check output files names and sizes in autoimgs directory
    onlyfiles = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    assert len(onlyfiles) == len(jupyter_4_2_images_sizes.keys())
    assert all([x in onlyfiles for x in jupyter_4_2_images_sizes.keys()])
    for x in onlyfiles:
        assert jupyter_4_2_images_sizes[x] == os.stat(os.path.join(image_dir,x)).st_size


def test_markdown():
    markdown_lines = [
        '# Header 1',
        'Some text',
        '## Header 2',
        'More text',
        '',
        '``` python ',
        'print("Hello, world!")',
        '```',
        'Even more text'
    ]
    org_lines = [
        '* Header 1',
        'Some text',
        '** Header 2',
        'More text', '',
        '#+begin_src python :results none :exports code :eval no',
        'print("Hello, world!")',
        '#+end_src',
        'Even more text']
    for m, o in zip(markdown_to_org(markdown_lines), org_lines):
        assert (m == o)


if __name__ == "__main__":
    test_converter()
