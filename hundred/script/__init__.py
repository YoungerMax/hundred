from abc import abstractmethod
from typing import List

from hundred.classes import Configuration


class ScriptSection:
    def __init__(self, config: Configuration):
        self.config = config

    @abstractmethod
    def get_content(self) -> str:
        raise NotImplementedError('get_content is not implemented')


class ScriptGenerator:
    def __init__(self, config: Configuration, section_order: List[List[ScriptSection]]):
        self.config = config
        self.section_order = section_order

    def generate_script(self) -> str:
        script_segments = ''

        for section_element in self.section_order:
            for section in section_element:
                try:
                    script_segments += section.get_content() + ' '
                    break
                except RuntimeError:
                    print(f'Section "{section}" is not applicable')
                    pass

        return script_segments

