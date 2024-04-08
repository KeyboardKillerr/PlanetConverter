class ParseException(BaseException):

    _MESSAGE = 'Parsing exception'

    def __init__(self):
        super().__init__(self._MESSAGE)


class ParseZSException(ParseException):

    _MESSAGE = 'Parsing exception in ZS parser'

    def __init__(self):
        super().__init__()


class StartLineNotPresentException(ParseZSException):

    _MESSAGE = 'Start line is not present in parsed text'

    def __init__(self):
        super().__init__()


class EndLineNotPresentException(ParseZSException):

    _MESSAGE = 'End line is not present in parsed text'

    def __init__(self):
        super().__init__()


class MissingColumnException(ParseZSException):

    _MESSAGE = 'Some columns were missing'

    def __init__(self):
        super().__init__()


class UnknownFormatException(ParseZSException):

    _MESSAGE = 'None of the provided parsers can parse'

    def __init__(self):
        super().__init__()


class ConverterAppException(BaseException):

    _MESSAGE = 'Error in main conversion module'

    def __init__(self):
        super().__init__(self._MESSAGE)


class FileSysException(BaseException):

    _MESSAGE = 'File system exception'

    def __init__(self):
        super().__init__(self._MESSAGE)


class MissingDefaultPrjException(FileSysException):

    _MESSAGE = ('Prj was not provided,'
                'tried to load default prj,'
                'default prj file was missing at <project_dir>\\resources\\prj.txt')

    def __init__(self):
        super().__init__()


class MissingNameChangerException(FileSysException):

    _MESSAGE = 'Name changer is missing at provided path'

    def __init__(self):
        super().__init__()


class MissingInputDirException(FileSysException):

    _MESSAGE = 'Input dir not found or missing'

    def __init__(self):
        super().__init__()


class MissingTemplateException(FileSysException):

    _MESSAGE = 'Template file not found or missing'

    def __init__(self):
        super().__init__()
