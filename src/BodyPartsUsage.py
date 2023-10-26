"""
Created on Mar 5, 2023

@author: Aaron
Class to hold data pertaining to usage of various body parts during tasks. Used for splitting tasks which overload body
parts.
"""
import abc


class BodyPartsUsage:
    # TODO: bodyparts
    pass


class BodyUserMixin(abc.ABC):
    @abc.abstractmethod
    def bodyUsage(self):
        pass