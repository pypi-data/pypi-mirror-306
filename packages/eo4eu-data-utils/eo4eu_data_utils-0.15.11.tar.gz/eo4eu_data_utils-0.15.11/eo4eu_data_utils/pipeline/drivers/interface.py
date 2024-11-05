from abc import ABC, abstractmethod
from pathlib import Path


# Some classes may implement this interface only partially
class Driver(ABC):
    @abstractmethod
    def source(self, path: Path) -> list[Path]:
        pass

    @abstractmethod
    def get(self, path: Path) -> bytes:
        pass

    @abstractmethod
    def put(self, path: Path, data: bytes) -> Path:
        pass

    @abstractmethod
    def move(self, src: Path, dst: Path) -> Path:
        pass

    @abstractmethod
    def unpack(self, src: Path, dst: Path) -> list[Path]:
        pass
