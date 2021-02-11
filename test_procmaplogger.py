import procmaplogger

EXAMPLE_LINE_1 = """
00400000-00424000 r--p 00000000 fd:00 6819394                            /home/user/something/executable
"""

EXAMPLE_LINE_2 = """
c003400000-c003600000 rw-p 00000000 00:00 0 
"""

EXAMPLE_LINE_3 = """
032d5000-03bdd000 rw-p 00000000 00:00 0                                  [heap]
"""


def test_MapLine_from_line():
    mapline = procmaplogger.MapLine.from_line(EXAMPLE_LINE_1)
    assert 0x00400000 == mapline.start
    assert 0x00424000 == mapline.end
    assert 0x24000 == mapline.size
    assert 'r--p' == mapline.permissions
    assert 6819394 == mapline.inode
    assert '/home/user/something/executable' == mapline.path

    mapline = procmaplogger.MapLine.from_line(EXAMPLE_LINE_2)
    assert 0xc003400000 == mapline.start
    assert 0xc003600000 == mapline.end
    assert 0x200000 == mapline.size
    assert 'rw-p' == mapline.permissions
    assert 0 == mapline.inode

    mapline = procmaplogger.MapLine.from_line(EXAMPLE_LINE_3)
    assert 0x032d5000 == mapline.start
    assert 0x03bdd000 == mapline.end
    assert 0x908000 == mapline.size
    assert 'rw-p' == mapline.permissions
    assert 0 == mapline.inode
    assert '[heap]' == mapline.path
