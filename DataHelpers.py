import math

"""
Some functions to help with repetitive tasks
"""


def distanceBetweenPoints(x, y, x2, y2):
    deltaX = x2 - x
    deltaY = y2 - y

    return math.sqrt(deltaX ** 2 + deltaY ** 2)


def interpolate(value, in_min, in_max, out_min, out_max):
    """
    Interpolates a value from the input range to the output range
    """
    in_span = in_max - in_min
    out_span = out_max - out_min

    scaled = float(value - in_min) / float(in_span)
    return out_min + (scaled * out_span)


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
