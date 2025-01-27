from configparser import ConfigParser
from dataclasses import dataclass

from utils.path import path

__all__ = ["config"]

# https://gist.github.com/tux-00/6093bfe1b5eef3049a7da493f312c77d
@dataclass
class Sections:
    raw_sections: dict

    def __post_init__(self):
        for section_key, section_value in self.raw_sections.items():
            setattr(self, section_key, SectionContent(section_value.items()))

@dataclass
class SectionContent:
    raw_section_content: dict

    def __post_init__(self):
        for section_content_k, section_content_v in self.raw_section_content:
            if section_content_v.lower() in ("true", "false"):
                section_content_v = section_content_v.lower() == "true"
            elif section_content_v.isdigit():
                section_content_v = int(section_content_v)
            else:
                try:
                    section_content_v = float(section_content_v)
                except ValueError:
                    pass
            setattr(self, section_content_k, section_content_v)

class Config(Sections):
    def __init__(self, raw_config_parser):
        self.parser = raw_config_parser
        Sections.__init__(self, raw_config_parser)
        
    def save(self):
        with open(path("config.ini"), "w", encoding="utf-8") as configfile:
            self.parser.write(configfile)

parser = ConfigParser()
parser.read(path("config.ini"))

config = Config(parser)