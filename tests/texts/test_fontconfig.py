from meme_generator import fontconfig as fc


def test_get_font_by_name():
    conf = fc.Config.get_current()
    pattern = fc.Pattern.name_parse("Sans")
    font = conf.font_match(pattern)[0]
    f_name = font.get(fc.FC.FILE, 0)[0]
    assert f_name


def test_get_font_list():
    conf = fc.Config.get_current()
    patterns = conf.font_list(fc.Pattern.create(), None)

    f_list = []
    for p in patterns:
        f_list.append(
            {
                "path": p.get(fc.FC.FILE, 0)[0],
                "family": p.get(fc.FC.FAMILY, 0)[0],
                "color": p.get(fc.FC.COLOR, 0)[0],
                "props": list(p.iter_object_with_values()),
            }
        )
    assert f_list


def test_substitute():
    conf = fc.Config.get_current()
    conf.substitute(fc.Pattern.name_parse("Noto Color Emoji"), fc.FC.MatchPattern)
    patterns = [conf.font_match(fc.Pattern.name_parse("Noto Color Emoji"))[0]]

    f_list = []
    for p in patterns:
        f_list.append(
            {
                "path": p.get(fc.FC.FILE, 0)[0],
                "family": p.get(fc.FC.FAMILY, 0)[0],
                "color": p.get(fc.FC.COLOR, 0)[0],
                "props": list(p.iter_object_with_values()),
            }
        )
    assert f_list
