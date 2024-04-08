import os
import sys
from pathlib import Path
from typing import Any
from abc import ABC
from abc import abstractmethod
from entities import *


class TestSource(ABC):

    def __init__(self, root_dir: str = None):
        if root_dir is None or root_dir == '':
            self._root_dir = self.__get_default_path()
        self._root_dir = Path(root_dir)

    @abstractmethod
    def get_given(self, file_name: str) -> Any:
        pass

    @abstractmethod
    def get_expected(self, file_name: str) -> Any:
        pass

    def _read_file(self, file_name: str) -> list[str]:
        with open(self._root_dir.joinpath(file_name), 'r') as file:
            lines = file.readlines()
        return lines

    @staticmethod
    def __get_default_path() -> Path:
        executable_path = sys.argv[0]
        absolute_path = os.path.abspath(executable_path)
        return Path(os.path.dirname(absolute_path))


class ParserZSTestSource(TestSource):

    def __init__(self, root_dir: str = None):
        super().__init__(root_dir)

    def get_given(self, file_name: str) -> list[str]:
        return self._read_file(file_name)

    def get_expected(self, file_name: str) -> list[ZSObservationPointDTO]:
        plain_text_lines = self._read_file(file_name)
        plain_text = ''.join(map(str, plain_text_lines))
        json_data = json.loads(plain_text)
        python_objects = [ZSObservationPointDTO(**json_object) for json_object in json_data]
        return python_objects
