from dataclasses import dataclass
from abc import ABC, abstractmethod
import dataclasses
import json


@dataclass
class NameProperty:
    name: str

    @staticmethod
    def dataframe_name():
        return 'Obs Point'


@dataclass
class WaterNameProperty:
    water_name: str

    @staticmethod
    def dataframe_name():
        return 'River'


@dataclass
class WaterLevelProperty:
    water_level: str

    @staticmethod
    def dataframe_name():
        return 'Lvl 0 8_00'


@dataclass
class WaterLevelChangeProperty:
    water_level_change: str

    @staticmethod
    def dataframe_name():
        return 'Lvl Change'


@dataclass
class IceProperty:
    ice: str

    @staticmethod
    def dataframe_name():
        return 'Ice'


@dataclass
class FloodLevelProperty:
    flood_level: str

    @staticmethod
    def dataframe_name():
        return 'Flood Lvl'


@dataclass
class IceThicknessProperty:
    ice_thickness: str

    @staticmethod
    def dataframe_name():
        return 'Ice Thickn'


@dataclass
class FloodplainLevelProperty:
    floodplain_level: str

    @staticmethod
    def dataframe_name():
        return 'Floodplain Lvl'


@dataclass
class ObservationPointDTOBase(
    NameProperty,
    WaterNameProperty,
    ABC
):
    @abstractmethod
    def to_dataframe_dict(self) -> dict[str, str]:
        pass


@dataclass
class ZSObservationPointDTO(
    ObservationPointDTOBase,
    WaterLevelProperty,
    WaterLevelChangeProperty,
    IceProperty,
    FloodLevelProperty,
    IceThicknessProperty
):
    def to_dataframe_dict(self):
        ddict = dict()
        ddict[NameProperty.dataframe_name()] = self.name
        ddict[WaterNameProperty.dataframe_name()] = self.water_name
        ddict[WaterLevelProperty.dataframe_name()] = self.water_level
        ddict[WaterLevelChangeProperty.dataframe_name()] = self.water_level_change
        ddict[IceProperty.dataframe_name()] = self.ice
        ddict[FloodLevelProperty.dataframe_name()] = self.flood_level
        ddict[IceThicknessProperty.dataframe_name()] = self.ice_thickness
        return ddict


@dataclass
class BObservationPointDTO(
    ObservationPointDTOBase,
    WaterLevelProperty,
    WaterLevelChangeProperty,
    IceProperty,
    FloodLevelProperty,
    FloodplainLevelProperty,
    IceThicknessProperty
):
    def to_dataframe_dict(self):
        ddict = dict()
        ddict[NameProperty.dataframe_name()] = self.name
        ddict[WaterNameProperty.dataframe_name()] = self.water_name
        ddict[WaterLevelProperty.dataframe_name()] = self.water_level
        ddict[WaterLevelChangeProperty.dataframe_name()] = self.water_level_change
        ddict[IceProperty.dataframe_name()] = self.ice
        ddict[FloodLevelProperty.dataframe_name()] = self.flood_level
        ddict[IceThicknessProperty.dataframe_name()] = self.ice_thickness
        ddict[FloodplainLevelProperty.dataframe_name()] = self.floodplain_level
        return ddict


@dataclass
class ZBObservationPointDTO(
    ObservationPointDTOBase,
    WaterLevelProperty,
    WaterLevelChangeProperty,
    IceProperty,
    FloodplainLevelProperty,
    IceThicknessProperty
):
    def to_dataframe_dict(self):
        ddict = dict()
        ddict[NameProperty.dataframe_name()] = self.name
        ddict[WaterNameProperty.dataframe_name()] = self.water_name
        ddict[WaterLevelProperty.dataframe_name()] = self.water_level
        ddict[WaterLevelChangeProperty.dataframe_name()] = self.water_level_change
        ddict[IceProperty.dataframe_name()] = self.ice
        ddict[IceThicknessProperty.dataframe_name()] = self.ice_thickness
        ddict[FloodplainLevelProperty.dataframe_name()] = self.floodplain_level
        return ddict


@dataclass
class IObservationPointDTO(
    ObservationPointDTOBase,
    WaterLevelProperty,
    WaterLevelChangeProperty,
    FloodLevelProperty,
    IceProperty,
    IceThicknessProperty
):
    def to_dataframe_dict(self):
        ddict = dict()
        ddict[NameProperty.dataframe_name()] = self.name
        ddict[WaterNameProperty.dataframe_name()] = self.water_name
        ddict[WaterLevelProperty.dataframe_name()] = self.water_level
        ddict[WaterLevelChangeProperty.dataframe_name()] = self.water_level_change
        ddict[FloodLevelProperty.dataframe_name()] = self.flood_level
        ddict[IceProperty.dataframe_name()] = self.ice
        ddict[IceThicknessProperty.dataframe_name()] = self.ice_thickness
        return ddict


@dataclass
class OIObservationPointDTO(
    ObservationPointDTOBase,
    WaterLevelProperty,
    WaterLevelChangeProperty,
    FloodLevelProperty,
    FloodplainLevelProperty,
    IceProperty
):
    def to_dataframe_dict(self):
        ddict = dict()
        ddict[NameProperty.dataframe_name()] = self.name
        ddict[WaterNameProperty.dataframe_name()] = self.water_name
        ddict[WaterLevelProperty.dataframe_name()] = self.water_level
        ddict[WaterLevelChangeProperty.dataframe_name()] = self.water_level_change
        ddict[FloodLevelProperty.dataframe_name()] = self.flood_level
        ddict[IceProperty.dataframe_name()] = self.ice
        ddict[FloodplainLevelProperty.dataframe_name()] = self.floodplain_level
        return ddict


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
