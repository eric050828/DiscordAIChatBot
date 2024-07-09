from configparser import ConfigParser, NoOptionError, NoSectionError

from .path import path


def get_config(section, key, key_type:None|int|float|bool=None):
    config = ConfigParser()
    config.read(path("config.ini"))
    type_functions = [config.getint, config.getfloat, config.getboolean, config.get]
    
    for func in type_functions:
        try:
            return func(section, key)

        except ValueError:
            continue
        
        except NoOptionError:
            raise NoOptionError
        
        except NoSectionError:
            raise NoSectionError