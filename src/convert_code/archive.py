import tarfile
import zipfile
from pathlib import Path


class ArchiveError(Exception):
    pass


class UnsupportedArchiveFormat(ArchiveError):
    pass




class BaseArchiver:
    def archive(self, source: Path, destination: Path):
        raise NotImplementedError

    def extract(self, source: Path, destination: Path):
        raise NotImplementedError


class ZipArchiver(BaseArchiver):
    def archive(self, source: Path, destination: Path):
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in source.rglob('*'):
                zipf.write(file, file.relative_to(source))

    def extract(self, source: Path, destination: Path):
        with zipfile.ZipFile(source, 'r') as zipf:
            zipf.extractall(destination)


class TarGzArchiver(BaseArchiver):
    def archive(self, source: Path, destination: Path):
        with tarfile.open(destination, "w:gz") as tar:
            tar.add(source, arcname=".")

    def extract(self, source: Path, destination: Path):
        with tarfile.open(source, "r:gz") as tar:
            tar.extractall(path=destination)

