import sys
from typing import Iterator


class Configuration:
    _documentation_identifier: tuple
    _signature_identifier: str

    def set_language(self, language: str):
        if language == 'C#':
            self._documentation_identifier = ('/**', '///')
            self._signature_identifier = 'public'

    def get_documentation_identifier(self) -> tuple:
        return self._documentation_identifier

    # For now just one possible, might look into making this a tuple.
    def get_signature_identifier(self) -> str:
        return self._signature_identifier


class Concept:
    _configuration: Configuration

    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    def generate(self) -> str:
        ...

    def link(self) -> str:
        ...


class Item:
    lines: list[str] = []
    _configuration: Configuration

    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    def include(self, line: str):
        self.lines.append(line)

    def parse(self) -> Concept:
        concept = Concept(self._configuration)

        return concept


def document(buffer: Iterator[str], configuration: Configuration):
    items: list[Item] = []
    in_comment: bool = False
    # Assignment below is required in case that the first public member has no documentation.
    item = Item(configuration)
    for line in buffer:
        if line.strip().startswith(configuration.get_documentation_identifier()):
            in_comment = True
            item = Item(configuration)
        elif line.strip().startswith(('public',)):
            in_comment = False
            item.include(line)
            items.append(item)
        if in_comment:
            item.include(line)
    sections = [item.parse() for item in items]
    documentation = [section.generate() for section in sections]
    toc = [section.link() for section in sections]
    manual = toc.copy()
    manual.extend(documentation)
    return '\n'.join(manual)


if __name__ == '__main__':
    # TODO add a branch to handle either this as default or files or folders via arguments.
    configurator = Configuration()
    configurator.set_language('C#')
    print(document(sys.stdin, configurator))
