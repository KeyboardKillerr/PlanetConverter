from abc import ABC, abstractmethod
from typing import Any
import re
import numpy as np
from pandas import DataFrame
from entities import *
from exceptions import *


class ParserBase(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, file_content):
        pass

    @classmethod
    async def parse_async(cls, file_content):
        return cls.parse(file_content)


class NameChangerParser(ParserBase):

    __BULLETIN_NAMES_COLUMN = 0
    __TARGET_NAMES_COLUMN = 1

    @classmethod
    def parse(cls, file_content: DataFrame) -> dict[str, str]:
        names = dict()
        for i in range(file_content[0].count()):
            names[file_content[cls.__BULLETIN_NAMES_COLUMN][i]] = file_content[cls.__TARGET_NAMES_COLUMN][i]
        return names


class UGMSParserBase(ParserBase, ABC):

    UGMS_CODE = None


class DocParser(UGMSParserBase, ABC):

    @classmethod
    def parse(cls, tables) -> list[ObservationPointDTOBase]:
        table = cls._read_tables(tables)
        table = cls._split_name(table)
        cls._cut_top(table)
        return cls._parse_table(table)

    @staticmethod
    def _read_tables(tables) -> list[list[str]]:
        data = list()
        for table in tables:
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    row_data.append(cell_text)
                if any(row_data):
                    data.append(row_data)
        return data

    @staticmethod
    def _split_name(table: list[list[str]]) -> list[list[str]]:
        new_table = list()
        for row in table:
            if '—' in row[0].replace(' ', ''):
                new_row = row[0].replace(' ', '').split('—')
            elif '–' in row[0].replace(' ', ''):
                new_row = row[0].replace(' ', '').split('–')
            elif '-' in row[0].replace(' ', ''):
                new_row = row[0].replace(' ', '').split('-')
            else:
                raise UnknownFormatException()
            row.pop(0)
            new_row.extend(row)
            new_table.append(new_row)
        return new_table

    @staticmethod
    def _cut_top(table: list[list[str]]) -> None:
        while table[0][0].strip() == 'Река':
            table.pop(0)

    @staticmethod
    def _parse_water_level(value: str) -> str:
        if value.strip() == "-":
            return value
        try:
            int_value = int(value)
            if int_value / 1000 > 0:
                int_value %= 1000
                value = str(int_value)
        except:
            pass
        finally:
            return value

    @classmethod
    def _trim_table(cls, table: list[list[str]]):
        if len(table) == 0:
            return
        for ri, row in enumerate(table):
            for ci, column in enumerate(row):
                table[ri][ci] = cls._trim(column)

    @staticmethod
    def _trim(string: str) -> str:
        if not isinstance(string, str):
            return string
        return string.replace(' ', '').replace('\n', '')

    @classmethod
    @abstractmethod
    def _parse_table(cls, table: list[list[str]]) -> list[ZBObservationPointDTO]:
        pass


class ParserOI(UGMSParserBase):

    UGMS_CODE = 'OI'
    __CONFIDENTIAL_LINE = ('Настоящая информация не подлежит разглашению в общем или частном порядке без '
                           'предварительного согласования')
    __WATER_NAME_COLUMN = 0
    __NAME_COLUMN = 1
    __WATER_LEVEL_COLUMN = 2
    __WATER_LEVEL_CHANGE_COLUMN = 3
    __FLOOD_LEVEL_COLUMN = 4
    __FLOODPLAIN_LEVEL_COLUMN = 5
    __ICE_COLUMN = 6

    @classmethod
    def parse(cls, tables):
        return cls.__parse_table(cls.__read_tables(tables))

    @classmethod
    def __read_tables(cls, file_content):
        table = list()
        check_start = False
        check_end = False
        for row in range(file_content.nrows):
            row_data = file_content.row_values(row)
            if row_data[0] == 'Река':
                check_start = True
            if row_data[0] == cls.__CONFIDENTIAL_LINE:
                check_end = True
            if (check_start
                    and row_data[0] != cls.__CONFIDENTIAL_LINE
                    and row_data[0] != "Река"
                    and row_data[5] != "начальная дата"
                    and row_data[3] != ''):
                if "Чисто" in row_data[13]:
                    row_data[13] = ""
                for i in range(len(row_data) - 1):
                    if row_data[i] == "":
                        row_data[i] = ""
                indices_to_remove = [2, 5, 6, 7, 8, 9, 10]
                for index in sorted(indices_to_remove, reverse=True):
                    del row_data[index]
                table.append(row_data)
            elif check_start and check_end:
                break
        return table

    @classmethod
    def __parse_table(cls, table):
        dto_table = list()
        for row in table:
            observation_point = OIObservationPointDTO(
                water_name=row[cls.__WATER_NAME_COLUMN],
                name=row[cls.__NAME_COLUMN],
                water_level=row[cls.__WATER_LEVEL_COLUMN],
                water_level_change=row[cls.__WATER_LEVEL_CHANGE_COLUMN],
                flood_level=row[cls.__FLOOD_LEVEL_COLUMN],
                floodplain_level=row[cls.__FLOODPLAIN_LEVEL_COLUMN],
                ice=row[cls.__ICE_COLUMN])
            dto_table.append(observation_point)
        return dto_table


class ParserI(DocParser):

    UGMS_CODE = 'I'
    __WATER_STATE_STRING = 'Состояние водного объекта'
    __WATER_NAME_COLUMN = 0
    __NAME_COLUMN = 1
    __WATER_LEVEL_COLUMN = 2
    __WATER_LEVEL_CHANGE_COLUMN = 3
    __ICE_COLUMN = 4
    __FLOOD_LEVEL_COLUMN = 5

    @classmethod
    def parse(cls, tables) -> list[ObservationPointDTOBase]:
        table, has_ice = cls._read_tables(tables)
        table = cls._split_name(table)
        table = cls.__do_some_voodoo_stuff(table)
        cls._cut_top(table)
        if not has_ice:
            cls.__do_some_voodoo_2(table)
        cls.__remove_no_connections(table)
        if has_ice:
            return cls.__parse_table_with_ice(table)
        return cls._parse_table(table)

    @classmethod
    def _read_tables(cls, tables) -> tuple[list[list[str]], bool]:
        table_objects, table_water_objects = cls.__get_tables(tables)
        data1, has_state1 = cls.__default_data_append(table_objects)
        data2, has_state2 = cls.__water_data_append(table_water_objects)
        return data1 + data2, has_state1 or has_state2

    @classmethod
    def __get_tables(cls, tables):
        table_water_objects = None
        table_objects = None
        for i, table in enumerate(tables):
            for row in table.rows:
                for cell in row.cells:
                    if cls.__check_if_water_object_line(cell.text.strip()):
                        table_water_objects = tables[i]
                    elif cls.__check_if_river_line(cell.text.strip()):
                        table_objects = tables[i]
        return table_objects, table_water_objects

    @staticmethod
    def __check_if_water_object_line(cell: str) -> bool:
        cell = cell.replace(' ', '')
        if cell == 'Водныйобъект–пункт':
            return True
        elif cell == 'Водныйобъект-пункт':
            return True
        return False

    @staticmethod
    def __check_if_river_line(cell: str) -> bool:
        cell = cell.replace(' ', '')
        if cell == 'Река–пункт':
            return True
        elif cell == 'Река-пункт':
            return True
        return False

    @classmethod
    def __default_data_append(cls, table):
        data = list()
        has_state = False
        if table is not None:
            for row in table.rows:
                row_data = list()
                for cell in row.cells:
                    if cell.text.strip().replace('\n', ' ') == cls.__WATER_STATE_STRING:
                        has_state = True
                    else:
                        row_data.append(cell.text.replace('\n' '').replace('\t', ''))
                if row_data:
                    data.append(row_data)
        return data, has_state

    @classmethod
    def __water_data_append(cls, table):
        data = list()
        has_state = False
        if table is not None:
            for row in table.rows:
                row_data = list()
                for cell in row.cells:
                    if cell.text.strip().replace('\n', ' ') == cls.__WATER_STATE_STRING:
                        has_state = True
                    else:
                        row_data.append(cell.text.replace('\n', '').replace('\t', ''))
                if row_data:
                    row_data.pop(3)
                    data.append(row_data)
        return data, has_state

    @staticmethod
    def __do_some_voodoo_stuff(table: list[list[str]]) -> list[list[str]]:
        new_table = list()
        for row in table:
            if re.sub(r'[^a-zA-Z\s]', '', row[0]) != re.sub(r'[^a-zA-Z\s]', '', "Водный объект – пункт"):
                new_table.append(row)
        return new_table

    @staticmethod
    def __do_some_voodoo_2(table: list[list[str]]) -> None:
        for row in table:
            if len(row) == 7:
                row.pop(4)
                row.pop(4)

    @staticmethod
    def __remove_no_connections(table) -> None:
        for r in table:
            if r[2].strip() == "нет связи".strip() or r[2].strip() == np.nan:
                table.remove(r)

    @classmethod
    def __parse_table_with_ice(cls, table: list[list[str]]) -> list[IObservationPointDTO]:
        dto_table = list()
        cls._trim_table(table)
        for row in table:
            observation_point = IObservationPointDTO(
                water_name=row[cls.__WATER_NAME_COLUMN],
                name=row[cls.__NAME_COLUMN],
                water_level=row[cls.__WATER_LEVEL_COLUMN],
                water_level_change=row[cls.__WATER_LEVEL_CHANGE_COLUMN],
                flood_level='',
                ice='',
                ice_thickness='')
            if observation_point.name == observation_point.water_name:
                observation_point.name = ''
                observation_point.water_name = ''
            if len(row) == 4:
                pass
            elif len(row) == 5:
                observation_point.ice = row[cls.__ICE_COLUMN]
            elif len(row) == 6:
                observation_point.ice = row[cls.__ICE_COLUMN]
                observation_point.flood_level = row[cls.__FLOOD_LEVEL_COLUMN]
            else:
                raise UnknownFormatException()
            dto_table.append(observation_point)
        return dto_table

    @classmethod
    def _parse_table(cls, table: list[list[str]]) -> list[IObservationPointDTO]:
        dto_table = list()
        cls._trim_table(table)
        for row in table:
            observation_point = IObservationPointDTO(
                water_name=row[cls.__WATER_NAME_COLUMN],
                name=row[cls.__NAME_COLUMN],
                water_level=row[cls.__WATER_LEVEL_COLUMN],
                water_level_change=row[cls.__WATER_LEVEL_CHANGE_COLUMN],
                flood_level='',
                ice='',
                ice_thickness='')
            if observation_point.name == observation_point.water_name:
                observation_point.name = ''
                observation_point.water_name = ''
                observation_point.ice = row[cls.__ICE_COLUMN - 2]
            if len(row) == 4:
                pass
            elif len(row) == 5:
                observation_point.flood_level = row[cls.__FLOOD_LEVEL_COLUMN - 1]
            else:
                raise UnknownFormatException()
            dto_table.append(observation_point)
        return dto_table


class ParserZB(DocParser):

    UGMS_CODE = 'ZB'
    __WATER_NAME_COLUMN = 0
    __NAME_COLUMN = 1
    __WATER_LEVEL_COLUMN = 2
    __WATER_LEVEL_CHANGE_COLUMN = 3
    __ICE_COLUMN = 4
    __FLOODPLAIN_LEVEL_COLUMN = 5

    @classmethod
    def _parse_table(cls, table: list[list[str]]) -> list[ZBObservationPointDTO]:
        dto_table = list()
        cls._trim_table(table)
        for row in table:
            observation_point = ZBObservationPointDTO(
                water_name=row[cls.__WATER_NAME_COLUMN],
                name=row[cls.__NAME_COLUMN],
                water_level=cls._parse_water_level(row[cls.__WATER_LEVEL_COLUMN]),
                water_level_change=row[cls.__WATER_LEVEL_CHANGE_COLUMN],
                ice='',
                floodplain_level='',
                ice_thickness='')
            if len(row) == 8:
                observation_point.ice = row[cls.__ICE_COLUMN]
                observation_point.floodplain_level = row[cls.__FLOODPLAIN_LEVEL_COLUMN]
            elif len(row) == 10:
                observation_point.floodplain_level = row[cls.__FLOODPLAIN_LEVEL_COLUMN + 4]
            else:
                raise UnknownFormatException()
            dto_table.append(observation_point)
        return dto_table


class ParserB(DocParser):

    UGMS_CODE = 'B'
    __WATER_NAME_COLUMN = 0
    __NAME_COLUMN = 1
    __WATER_LEVEL_COLUMN = 2
    __WATER_LEVEL_CHANGE_COLUMN = 3
    __ICE_COLUMN = 4
    __FLOODPLAIN_LEVEL_COLUMN = 5
    __FLOOD_LEVEL_COLUMN = 6

    @classmethod
    def _parse_table(cls, table: list[list[str]]) -> list[BObservationPointDTO]:
        dto_table = list()
        cls._trim_table(table)
        for row in table:
            observation_point = BObservationPointDTO(
                water_name=row[cls.__WATER_NAME_COLUMN],
                name=row[cls.__NAME_COLUMN],
                water_level=cls._parse_water_level(row[cls.__WATER_LEVEL_COLUMN]),
                water_level_change=row[cls.__WATER_LEVEL_CHANGE_COLUMN],
                ice='',
                flood_level='',
                floodplain_level='',
                ice_thickness='')
            if len(row) == 8:
                observation_point.flood_level = row[cls.__FLOOD_LEVEL_COLUMN - 1]
                observation_point.floodplain_level = row[cls.__FLOODPLAIN_LEVEL_COLUMN - 1]
            elif len(row) == 9:
                observation_point.ice = row[cls.__ICE_COLUMN]
                observation_point.flood_level = row[cls.__FLOOD_LEVEL_COLUMN]
                observation_point.floodplain_level = row[cls.__FLOODPLAIN_LEVEL_COLUMN]
            elif len(row) == 10:
                observation_point.flood_level = row[cls.__FLOOD_LEVEL_COLUMN + 1]
                observation_point.floodplain_level = row[cls.__FLOODPLAIN_LEVEL_COLUMN + 1]
            elif len(row) == 11:
                observation_point.flood_level = row[cls.__FLOOD_LEVEL_COLUMN + 2]
                observation_point.floodplain_level = row[cls.__FLOODPLAIN_LEVEL_COLUMN + 1]
            else:
                raise UnknownFormatException()
            dto_table.append(observation_point)
        return dto_table


class ParserZS(UGMSParserBase):

    UGMS_CODE = 'ZS'
    __START_LINE_TEXT = ':-------------+--------------+---------+--------+--------+--------+---------+-------------------:--------:\n'
    __END_LINE_TEXT = '----------------------------------------------------------------------------------------------------------\n'
    __WATER_NAME_COLUMN = 0
    __NAME_COLUMN = 1
    __WATER_LEVEL_COLUMN = 2
    __WATER_LEVEL_CHANGE_COLUMN = 3
    __ICE_COLUMN = 4
    __FLOOD_LEVEL_COLUMN = 5

    @classmethod
    def parse(cls, file_content: list[str]) -> list[ZSObservationPointDTO]:
        cls.__take_useful_content(file_content)
        parsed_lines = cls.__parse_lines(file_content)
        table = cls.__create_table(parsed_lines)
        return table

    @classmethod
    def __take_useful_content(cls, file_content: list[str]) -> list[str]:
        cls.__cut_top(file_content)
        cls.__cut_bottom(file_content)
        return file_content

    @classmethod
    def __cut_top(cls, lines: list[str]) -> None:
        try:
            delete_before = lines.index(cls.__START_LINE_TEXT) + 1
            del lines[:delete_before]
        except ValueError as e:
            raise StartLineNotPresentException() from e

    @classmethod
    def __cut_bottom(cls, lines: list[str]) -> None:
        try:
            delete_after = lines.index(cls.__END_LINE_TEXT)
            del lines[delete_after:]
        except ValueError as e:
            raise EndLineNotPresentException() from e

    @classmethod
    def __parse_lines(cls, lines: list[str]) -> list[list[str]]:
        table = []
        for row in lines:
            columns = cls.__split_by_semicolon(row)
            cls.__remove_unused_columns(columns)
            cls.__parse_columns(columns)
            table.append(columns)
        cls.__process_ice_column(table)
        return table

    @staticmethod
    def __split_by_semicolon(line: str) -> list[str]:
        splitted = line.split(':')
        if len(splitted) != 11:
            raise MissingColumnException()
        return splitted[1:10]

    @staticmethod
    def __remove_unused_columns(columns: list[str]) -> None:
        columns.pop(4)
        columns.pop(4)
        columns.pop(4)

    @classmethod
    def __parse_columns(cls, columns: list[str]) -> None:
        cls.__remove_river_abbreviation(columns)
        cls.__remove_white_spaces(columns)

    @classmethod
    def __remove_river_abbreviation(cls, columns: list[str]) -> None:
        columns[cls.__WATER_NAME_COLUMN] = columns[cls.__WATER_NAME_COLUMN].replace('р.', '')

    @classmethod
    def __remove_white_spaces(cls, columns: list[str]) -> None:
        for index, column in enumerate(columns):
            if index == cls.__ICE_COLUMN: continue
            columns[index] = column.replace(' ', '')

    @classmethod
    def __process_ice_column(cls, lines: list[list[str]]) -> None:
        empty_lines = 0
        for index, line in enumerate(lines):
            line[cls.__ICE_COLUMN] = line[cls.__ICE_COLUMN].strip()
            lines[index] = line
            if cls.__is_line_empty(line):
                empty_lines += 1
                lines[index - empty_lines][cls.__ICE_COLUMN] += ' ' + line[cls.__ICE_COLUMN]
            else:
                empty_lines = 0
        cls.__remove_empty_rows(lines)

    @classmethod
    def __remove_empty_rows(cls, lines: list[list[str]]) -> None:
        for index, line in enumerate(lines):
            if not cls.__is_line_empty(line): continue
            del lines[index]

    @staticmethod
    def __is_line_empty(line: list[str]) -> bool:
        emptiness_check_index = 0
        if line[emptiness_check_index] == '':
            return True
        else:
            return False

    @classmethod
    def __create_table(cls, parsed_lines: list[list[str]]) -> list[ZSObservationPointDTO]:
        table = []
        for line in parsed_lines:
            observation_point = ZSObservationPointDTO(
                water_name=line[cls.__WATER_NAME_COLUMN],
                name=line[cls.__NAME_COLUMN],
                water_level=line[cls.__WATER_LEVEL_COLUMN],
                water_level_change=line[cls.__WATER_LEVEL_CHANGE_COLUMN],
                ice=line[cls.__ICE_COLUMN],
                flood_level=line[cls.__FLOOD_LEVEL_COLUMN],
                ice_thickness='')
            table.append(observation_point)
        return table
