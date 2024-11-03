from dataclasses import dataclass
from io import TextIOWrapper
from typing import List, Tuple, Optional
import enum


class MessageStatus(enum.Enum):
    cleared = enum.auto()
    queued = enum.auto()
    comment = enum.auto()
    critical = enum.auto()


@dataclass
class VariableItem:
    value: str
    offset: int


@dataclass
class QueueItem:
    source_filename: str
    source_file: TextIOWrapper
    control_offset: int
    value: str
    status: MessageStatus

    _variables: List[VariableItem]

    ############################################################################
    # mark_as_cleared
    #
    # Mark a specific queue item as cleared and save it to the queue.
    ############################################################################
    def mark_as_cleared(self) -> None:
        position = self.source_file.tell()
        self.source_file.seek(self.control_offset)
        self.source_file.write("=")
        self.source_file.seek(position)
        self.status = MessageStatus.cleared

    ############################################################################
    # mark_as_critical_error
    #
    # Mark a specific queue item as a critical error and save it to the queue.
    ############################################################################
    def mark_as_critical_error(self) -> None:
        position = self.source_file.tell()
        self.source_file.seek(self.control_offset)
        self.source_file.write("!")
        self.source_file.seek(position)
        self.status = MessageStatus.cleared

    def set_variable(self, index: int, value: str) -> None:
        current_variable = self._variables[index].value
        if len(value) < len(current_variable):
            value += " " * (len(current_variable) - len(value))
        elif len(value) > len(current_variable):
            raise ValueError("New variable is too long")

        position = self.source_file.tell()
        self.source_file.seek(self._variables[index].offset + 1)
        self.source_file.write(value)
        self.source_file.seek(position)
        self._variables[index].value = value

    ############################################################################
    # get_variables
    #
    # Get all of the variables that are associated with this queue item.
    ############################################################################
    def get_variables(self) -> Tuple[str, ...]:
        return tuple(x.value for x in self._variables)


class TextQueue:
    input_files: List[Tuple[str, TextIOWrapper]]

    def __init__(self) -> None:
        self.input_files = []

    ############################################################################
    # get_next
    #
    # Gets the next item in the queue
    ############################################################################
    def get_next(self) -> Optional[QueueItem]:
        for i in range(len(self.input_files)):
            val = self.get_next_in_file(i)
            if val is None:
                continue
            return val
        return None

    ############################################################################
    # get_next_in_file
    #
    # A helper function to get the next item in the queue for a given file.
    ############################################################################
    def get_next_in_file(
        self,
        file_index: int,
        include_cleared_items: bool = False,
        include_comment_items: bool = False,
        include_critical_items: bool = False,
    ) -> Optional[QueueItem]:
        while True:
            file = self.input_files[file_index][1]
            filename = self.input_files[file_index][0]
            control_character_index = file.tell()
            line: str = file.readline()

            # End of file
            if line == "":
                return None

            # Blank Line, ignored
            if line == "\n":
                continue

            control_character = line[0]

            message: List[str]
            message_status: MessageStatus

            # Parse out cleared, queued, and comments and handle them accordingly
            if control_character == "=":
                message_status = MessageStatus.cleared
                message = [line[1:]]

            elif control_character == "-":
                message_status = MessageStatus.queued
                message = [line[1:]]

            elif control_character == "#":
                message_status = MessageStatus.comment
                message = [line[1:]]

            elif control_character == "!":
                message_status = MessageStatus.critical
                message = [line[1:]]

            else:
                raise ValueError("Unexpected Control Character '{}' on line '{}'".format(control_character, line))

            # Add all of the extra continued lines if any exist
            while self._peek_at_next_character(file) == " ":
                line = file.readline()
                message.append(line[1:])

            # Gather all of the variables attachede to this message
            variables: List[VariableItem] = []
            while self._peek_at_next_character(file) == "\\":
                offset = file.tell()
                line = file.readline()
                line = remove_trailing_newline(line)
                variables.append(
                    VariableItem(
                        value=line[1:],
                        offset=offset
                    )
                )

            if message_status == MessageStatus.comment and not include_comment_items:
                continue
            if message_status == MessageStatus.cleared and not include_cleared_items:
                continue
            if message_status == MessageStatus.critical and not include_critical_items:
                continue

            return QueueItem(
                source_filename=filename,
                source_file=file,
                control_offset=control_character_index,
                value=remove_trailing_newline("".join(message)),
                status=message_status,
                _variables=variables,
            )

    def close(self) -> None:
        for file in self.input_files:
            file[1].close()

    ############################################################################
    # _peek_at_next_character
    #
    # A helper function to peek at the next character in a file if one exists.
    ############################################################################
    def _peek_at_next_character(self, file: TextIOWrapper) -> str:
        start = file.tell()
        val = file.read(1)
        file.seek(start)
        return val

    ############################################################################
    # add_input
    #
    # Adds a file as a possible input
    ############################################################################
    def add_input(self, filename: str) -> None:
        self.input_files.append((filename, open(filename, 'r+')))


def remove_trailing_newline(string: str) -> str:
    if string.endswith("\n"):
        return string[:-1]
    return string
