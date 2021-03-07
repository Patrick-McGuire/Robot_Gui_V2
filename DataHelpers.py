#!/usr/bin/python

"""
Some functions to help getting values from data structures
"""


def getXMLAttribute(XLM, attribute: str, default: str):
    """
    Returns the value from a chunk of xml data, with the option for a default value
    :param XLM: the chunk of xml data
    :param attribute: the name of the attribute to get
    :param default: default value
    """
    if XLM.hasAttribute(attribute):
        return XLM.getAttribute(attribute)
    else:
        return default


def getValueFromDictionary(dictionary: {}, key: str, default):
    """
    Returns the dictionary entry for a given key, or the default
    """

    if key in dictionary:
        return dictionary[key]
    else:
        return default
