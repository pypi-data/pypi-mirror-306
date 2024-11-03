class LanguageSettings:
    """
    This class contains language-specific configurations. The user is supposed to define a class that itself inherits
    from this, and overrides the needed configuration-methods. Then use that class as the base-class for all the grammar rules.
    The user-defined configuration-class should be in the same module of all the rules of the grammar.
    """
    context = {}

    def __init__(self):
        self.elems = []

    @classmethod
    def get_id(cls):
        """
        Used by the parsing-logic injected by decorators to know their own fully-qualified rule-name.
        Should be inherited by a language-specific-configuration-class which itself inherits from LanguageSettings.
        :return: the fully-qualified name of this grammar-rule
        """
        return f"{cls.__module__}.{cls.__qualname__}"

    @classmethod
    def get_id_of_rule_assuming_in_same_module(cls, class_name: str) -> str:
        """
        This method is supposed to be aliased, and used to consistently refer to a given grammar-rule using
        just the name of the class. For this to work, such class must be defined within the same module.
        :param class_name: the name of a user-defined class, representing a grammar-rule, in the same module
        :return: the fully-qualified name of the given grammar-rule
        """
        id_of_settings_class_without_last_part = cls.get_id()
        while id_of_settings_class_without_last_part[-1] != '.':
            id_of_settings_class_without_last_part = id_of_settings_class_without_last_part[:-1]
        return id_of_settings_class_without_last_part + class_name

    @classmethod
    def ignore_characters(cls, char: str) -> bool:
        """
        Used by the parsing-logic injected by decorators to know if a character should be ignored.
        Should be overridden by a language-specific configuration class which inherits from LanguageSettings.
        :param char: a single character to inspect
        :return: True if that character should be ignored, False otherwise
        """
        return char == ' ' or char == '\t' or char == '\n' or char == '\r'