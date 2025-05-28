import subprocess
from pathlib import Path

from convert_code.funcs.archive import ArchiveFunction
from convert_code.funcs.image import ImageFunction
from convert_code.funcs.text import TextFunction
from convert_code.funcs.video import VideoFunction


# авторгенерация словаря исходя из названий функций??? а?
# class_registry = {}
#
# def register_conversion(source, target):
#     def decorator(func):
#         class_registry.setdefault(source, {})[target] = func
#         return func
#     return decorator


class BaseInterface:
    conversion_formats = None
    class_func = None

    def __init__(self):
        if self.conversion_formats is None or self.class_func is None:
            raise NotImplementedError("Subclasses must define `conversion_formats` and `class_func`")

    def convert(self, source_format, target_format, input_path, output_path):
        if source_format not in self.conversion_formats or target_format not in self.conversion_formats[source_format]:
            raise ValueError(f'Unknown format: {source_format} -> {target_format}')
        method_name = f'{source_format}_to_{target_format}'
        method = getattr(self.class_func, method_name, None)
        if not method:
            raise AttributeError(
                f'В словаре форматы для конвертирования есть, а >{method_name}< такого нет в {self.class_func.__name__}')
        return method(input_path, output_path)


class ImageInterface(BaseInterface):
    conversion_formats = {
        'jpg': ['webp', 'svg'],
        'png': ['webp', 'svg'],
        'webp': ['png', 'jpg'],
        'svg': ['png']
    }
    class_func = ImageFunction


class TextInterface(BaseInterface):
    conversion_formats = {
        'txt': ['csv', 'json', 'pdf', 'docx'],
        'csv': ['txt'],
        'json': ['txt'],
        'pdf': ['txt'],
        'docx': ['txt']
    }
    class_func = TextFunction


class VideoInterface(BaseInterface):
    class_func = VideoFunction  # здесь нет класса с функциями, но можно указать self как заглушку
    conversion_formats = {
        'mp4': ['avi', 'webm', 'mov'],
        'avi': ['mp4'],
        'webm': ['mp4'],
        'mov': ['mp4']
    }

    def convert(self, source_format, target_format, input_path, output_path):
        if source_format not in self.conversion_formats or target_format not in self.conversion_formats[source_format]:
            raise ValueError(f'Unknown format: {source_format} -> {target_format}')
        method_name = f'{source_format}_to_{target_format}'
        method = getattr(self.class_func, method_name, None)
        if not method:
            raise AttributeError(
                f'В словаре форматы для конвертирования есть, а >{method_name}< такого нет в {self.class_func.__name__}')
        params = method()
        command = ["ffmpeg", "-i", str(self.input_path)] + params + [str(self.output_path)]
        subprocess.run(command, check=True)


class DecompressingError(Exception):
    pass


# TODO: можно ли привести к тому же виду, что и остальные интерфейсы? можно
class ArchiveInterface(BaseInterface):
    conversion_formats = {
        'folder': ['.zip', '.tar.gz'],
        'zip': ['folder'],
        'tar_gz': ['folder']
    }
    class_func = ArchiveFunction

    def check_tar_gz(self, source_format, target_format):
        if 'tar.gz' in source_format:
            source_format = 'tar_gz'
        if 'tar.gz' in target_format:
            target_format = 'tar_gz'
        return source_format, target_format


    def convert(self, source_format: str, target_format: str, input_path: Path, output_path: Path):
        source_format, target_format = self.check_tar_gz(source_format, target_format)
        if source_format not in self.conversion_formats or target_format not in self.conversion_formats[source_format]:
            raise ValueError(f'Unknown format: {source_format} -> {target_format}')
        method_name = f'{source_format}_to_{target_format}'
        method = getattr(self.class_func, method_name, None)
        if not method:
            raise AttributeError(
                f'В словаре форматы для конвертирования есть, а >{method_name}< такого нет в {self.class_func.__name__}')
        return method(input_path, output_path)


class UniversalInterface:
    INTERFACES = [TextInterface, VideoInterface, ImageInterface, ArchiveInterface]

    def __init__(self, source_format: str, target_format: str, input_path: Path, output_path: Path):
        self.source_format = source_format
        self.target_format = target_format
        self.input_path = input_path
        self.output_path = output_path
        self.interface = self.resolve_interface()

    def resolve_interface(self):
        for iface_cls in self.INTERFACES:
            if (
                    self.source_format in iface_cls.conversion_formats
                    or self.target_format in iface_cls.conversion_formats
            ):
                return iface_cls(self.source_format, self.target_format, self.input_path, self.output_path)
        raise ValueError(
            f"Формат '{self.source_format}' → '{self.target_format}' не поддерживается ни одним интерфейсом.")

    def run(self) -> bool:
        return self.interface.convert(self.source_format, self.target_format, self.input_path, self.output_path)

    @classmethod
    def get_all_supported_pairs(cls):  # я общаюсь с фронтом и на этот класс мне плевать
        pairs = []
        for iface in cls.INTERFACES:
            pairs.extend(iface.conversion_formats)
        return pairs
