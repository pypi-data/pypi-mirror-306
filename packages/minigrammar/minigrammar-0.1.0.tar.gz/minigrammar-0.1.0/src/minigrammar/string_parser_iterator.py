class StringParserIterator:
    """
    It's used as the one and only parameter for constructors (__init__) of AST-classes where parsing a file is needed.
    This class can be used as a python-iterator (e.g. using next on it) to iterate over characters of a string. It must
    be constructed from a string containing text to parse.
    """

    def __init__(self, source_text: str):
        self._index = 0
        self._current_line = source_text
        self._generator = None

    def __iter__(self):
        return self

    def __next__(self):
        current_value = self.peek()
        if current_value is None:
            raise StopIteration
        self.advance()
        return current_value

    def clone(self) -> 'StringParserIterator':
        """
        :return: an independent clone of this iterator, with its own state
        """
        cloned = StringParserIterator(self._current_line)
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
        if self._index < len(self._current_line):
            return self._current_line[self._index]
        return None

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
        if self._current_line is not None:
            self._generator._current_line = self._current_line
            self._generator._index = self._index