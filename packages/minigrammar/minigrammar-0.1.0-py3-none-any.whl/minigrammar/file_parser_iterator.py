from typing import TextIO


class FileParserIterator:
    """
    It's used as the one and only parameter for constructors (__init__) of AST-classes where parsing a file is needed.
    This class can be used as a python-iterator (e.g. using next on it) to iterate over characters of a file. It must be
    constructed from a file already opened in read mode, corresponding to the file to parse.
    """

    def __init__(self, source_file: TextIO):
        self._index = 0
        self._source_file = source_file
        self._generator = None

    def __iter__(self):
        return self

    def __next__(self) -> str:
        current_value = self.peek()
        if current_value is None:
            raise StopIteration
        self.advance()
        return current_value

    def clone(self) -> 'FileParserIterator':
        """
        :return: an independent clone of this iterator, with its own state
        """
        cloned = FileParserIterator(self._source_file)
        cloned._index = self._index
        cloned._generator = self
        return cloned

    def advance(self) -> None:
        """
        Advances the iterator by one character. It doesn't return any value,
        to query for the current value of the iterator use the peek() method
        """
        self._index += 1

    def advance_by(self, n: int) -> None:
        """
        Advances the iterator by n character. It doesn't return any value,
        to query for the current value of the iterator use the peek() method

        :param n: how many times to advance the iterator
        """
        self._index += n

    def peek(self) -> str | None:
        """
        Used to see the current value of the iterator without advancing it.
        :return: a string of length 1 corresponding to the current value of the iterator or None if end-of-file is reached.
        """
        self._source_file.seek(self._index)
        current_char = self._source_file.read(1)
        self._source_file.seek(self._index)
        if current_char == "":
            return None
        return current_char

    def get_index(self) -> int:
        """
        Used to check the current index of the iterator
        :return: the current index of the iterator
        """
        return self._index

    def synchronize_with_source(self) -> None:
        """
        When called on an iterator that has been created using the clone method on another iterator,
        it will update the state of the original iterator to match the state of this iterator. If the
        iterator has not been created as a clone, it does nothing.
        """
        if self._source_file is not None:
            self._generator._index = self._index