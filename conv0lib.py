from enum import Enum
import ffmpeg
import os


class ConvV0Exception(BaseException):
    """Base exception class for this lib"""
    pass


class ConversionFailure(ConvV0Exception):
    """Raised when the flac file cannot be converted for any reason"""
    pass


class UnknownFailure(ConvV0Exception):
    """Raised when something goes wrong and we don't know why"""
    pass


class Result(Enum):
    """What happened when we attempted to handle a path"""
    ConversionSuccessful = 1
    ConversionFailed = 2
    Directory = 3
    NotFlac = 4
    DoesNotExist = 5


def output_path(path):
    return os.path.splitext(path)[0] + '.mp3'


def convert_to_v0(path):
    """Handle converting .flac to mp3 v0"""
    mp3_path = output_path(path)
    if os.path.exists(mp3_path):
        print("Removing .mp3 with same path as {}".format(path))
        os.remove(mp3_path)

    encode = ffmpeg.input(path).output(mp3_path, acodec='libmp3lame')
    try:
        result = encode.run()
    except:
        raise ConversionFailure


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
