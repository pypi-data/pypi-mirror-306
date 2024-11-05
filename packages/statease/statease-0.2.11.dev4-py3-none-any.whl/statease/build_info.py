from .factor import Factor
from .response import Response
import json

class BuildInfo:
    def __init__(self, study_type, design_type):
        self.__factors = []
        self.__responses = []
        self.__block_levels = []
        self.__design_properties = {}
        self.__study_type = study_type
        self.__design_type = design_type

    def __str__(self):
        return json.dumps(self.to_dict())

    @property
    def study_type(self):
        return self.__study_type

    @study_type.setter
    def study_type(self, study_type):
        self.__study_type = study_type

    @property
    def design_type(self):
        return self.__design_type

    @design_type.setter
    def design_type(self, design_type):
        self.__design_type = design_type

    @property
    def blocks(self):
        return self.__block_levels

    @blocks.setter
    def blocks(self, block_levels):
        self.__block_levels = block_levels

    @property
    def design_properties(self):
        return self.__design_properties

    def add_design_property(self, property_names, property_value):
        self.__design_properties[property_names] = property_value

    def add_factor(self, name, units, low, high):
        facInfo = Factor()
        facInfo.set_name(name)
        facInfo.set_units(units)
        facInfo.set_low(low)
        facInfo.set_high(high)
        self.__factors.append(facInfo)

    @property
    def factors(self):
        return self.__factors

    def add_response(self, name, units):
        rsp = Response()
        rsp.set_name(name)
        rsp.set_units(units)
        self.__responses.append(rsp)

    @property
    def responses(self):
        return self.__factors

    def to_dict(self):
        data = {}
        data['study_type'] = self.__study_type
        data['design_type'] = self.__design_type
        data['factors'] = [ factor.to_dict() for factor in self.__factors ]
        data['responses'] = [ response.to_dict() for response in self.__responses ]
        data['block_levels'] = self.__block_levels
        data['design_properties'] = self.__design_properties
        return data
