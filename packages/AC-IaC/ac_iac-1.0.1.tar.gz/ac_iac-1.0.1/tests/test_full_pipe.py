from pathlib import Path

from AC_IaC.inference.full_pipe import main


def test_rebuilt_filestructure(tmpdir):
    main(
        Path("./tests/test_in_structure"),
        Path(tmpdir),
        "aa",
        "bb",
        False,
        True,
    )
    tmpdir = str(tmpdir)
    assert Path(tmpdir).is_dir()
    assert Path(tmpdir + "/S.txt").is_file()
    assert Path(tmpdir + "/a/").is_dir()
    assert Path(tmpdir + "/a/AA.txt").is_file()
    assert Path(tmpdir + "/b/").is_dir()
    assert Path(tmpdir + "/b/bb/").is_dir()
    assert Path(tmpdir + "/b/bb/BBB.txt").is_file()


def test_single_file_dry(tmpdir):
    main(
        Path("./tests/test_in_file/A.txt"),
        Path(tmpdir),
        "aa",
        "bb",
        False,
        True,
    )
    tmpdir = str(tmpdir)
    assert Path(tmpdir).is_dir()
    assert Path(tmpdir + "/A.txt").is_file()
    assert Path(tmpdir + "/A.ann").is_file()
