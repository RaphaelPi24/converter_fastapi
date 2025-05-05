import tarfile
import zipfile
from pathlib import Path


class ArchiveError(Exception):
    pass


class UnsupportedArchiveFormat(ArchiveError):
    pass




class BaseArchiver:
    def __init__(self, source: Path, destination: Path):
        self.source = source
        self.destination = destination

    def archive(self):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError



class ZipArchiver(BaseArchiver):
    def archive(self):
        with zipfile.ZipFile(self.destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in self.source.rglob('*'):
                zipf.write(file, file.relative_to(self.source))

    def extract(self):
        with zipfile.ZipFile(self.source, 'r') as zipf:
            zipf.extractall(self.destination)


class TarGzArchiver(BaseArchiver):
    def archive(self):
        with tarfile.open(self.destination, "w:gz") as tar:
            tar.add(self.source, arcname=".")

    def extract(self):
        with tarfile.open(self.source, "r:gz") as tar:
            tar.extractall(path=self.destination)
