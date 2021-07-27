import os
import tempfile
from pathlib import Path
from typing import List, Union, Optional

from . import fontconfig as fc

FONTS_ROOT = os.path.join(os.path.dirname(__file__), "../fonts")


class FontManager:
    def __init__(self):
        self._conf_files = []
        self._fonts = [FONTS_ROOT]
        self.conf: Optional[fc.Config] = None
        self._default_emoji = "Apple Color Emoji"
        system_config = fc.Config.get_current()
        # Копируем системные настройки и шрифты
        self.system_config_files = list(
            [c for c in system_config.config_files if not c.startswith("/tmp")]
        )
        self.system_fonts = list(system_config.font_dirs)
        del system_config

    def __del__(self):
        del self.conf
        for f in self._conf_files:
            os.unlink(f)

    def init(
        self,
        fonts: Optional[List[Union[str, Path]]] = None,
        default_emoji: Optional[str] = None,
    ):
        fonts = fonts or self._fonts
        default_emoji = default_emoji or self._default_emoji
        self._fonts = fonts
        self._default_emoji = default_emoji
        if self.conf:
            del self.conf
        self.conf = fc.Config.create()
        self.conf.app_font_clear()
        self.configure_system_fc()
        self.conf.set_current()

        self.load_fonts(fonts)
        self.set_default_emoji_font(default_emoji)
        self.conf.build_fonts()

    def configure_system_fc(self):
        for cf in self.system_config_files:
            self.conf.parse_and_load(cf, True)
        self.load_fonts(self.system_fonts)

    def load_fonts(self, fonts: List[str]):
        for font in fonts:
            self.load_font(font)

    def load_font(self, font: Union[str, Path]):
        font = str(font)
        if not os.path.exists(font):
            return
        if os.path.isdir(font):
            self.conf.app_font_add_dir(font)
        else:
            self.conf.app_font_add_file(font)

    def reset_config(self):
        for cf in self._conf_files:
            xml = """
            <!DOCTYPE fontconfig SYSTEM "fonts.dtd">
            <fontconfig>
            </fontconfig>
            """
            with open(cf, "w") as f:
                f.write(xml)
            self.conf.parse_and_load(cf, True)

    def set_default_emoji_font(self, font_name: str):
        # self.reset_config()
        xml = f"""
        <!DOCTYPE fontconfig SYSTEM "fonts.dtd">
        <fontconfig>
                <match target="pattern">
                    <test name="family" qual="first" compare="contains">
                        <string>emoji</string>
                    </test>
                    <edit name="family" mode="prepend" binding="strong">
                            <string>{font_name}</string>
                    </edit>
                </match>
        </fontconfig>
        """
        fd, conf_filename = tempfile.mkstemp()
        os.write(fd, xml.encode("utf-8"))
        os.close(fd)
        self.conf.parse_and_load(conf_filename, True)
        self._conf_files.append(conf_filename)


font_manager = FontManager()
