from __future__ import annotations
import benanalysis._benpy_core
import typing
__all__ = ['ANSI_Z80_3_daylight_chromaticity', 'ANSI_Z80_3_green_chromaticity', 'ANSI_Z80_3_yellow_chromaticity', 'CIE_1931_chromaticity', 'CIExy']
class CIExy:
    """
    
        CIE 1931 (x, y) chromaticity coordinates.
    
        This class represents a point in a two-dimensional chromaticity space
        using the CIE 1931 color model. The x and y coordinates specify the
        chromaticity values of the point, which define its color characteristics.
        
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            Default constructor for CIExy.
        
            Initializes a chromaticity point with default values of x = 0 and y = 0.
        """
    @typing.overload
    def __init__(self, x: float, y: float) -> None:
        """
            Constructs a CIExy chromaticity point with the given x and y coordinates.
        
            :param x: The x-coordinate of the chromaticity point.
            :param y: The y-coordinate of the chromaticity point.
        """
    def __repr__(self) -> str:
        """
            Returns a string representation of the CIExy chromaticity point.
        
            :return: A string representing the CIExy chromaticity point, in the format
                     "<Chromaticity x: value y: value>".
        """
    def __str__(self) -> str:
        """
            Returns a human-readable string representation of the CIExy chromaticity point.
        
            :return: A string representing the CIExy chromaticity point, in the format
                     "x: value y: value".
        """
    @property
    def x(self) -> float:
        """
            The x-coordinate of the chromaticity point.
        
            This attribute represents the x-coordinate in the CIE 1931 chromaticity
            diagram, which defines the color characteristics of the point.
        """
    @x.setter
    def x(self, arg0: float) -> None:
        ...
    @property
    def y(self) -> float:
        """
            The y-coordinate of the chromaticity point.
        
            This attribute represents the y-coordinate in the CIE 1931 chromaticity
            diagram, which defines the color characteristics of the point.
        """
    @y.setter
    def y(self, arg0: float) -> None:
        ...
def ANSI_Z80_3_daylight_chromaticity(scan: benanalysis._benpy_core.Scan) -> CIExy:
    """
        Calculate the ANSI Z80.3 daylight chromaticity (x, y) from scan data.
    
        This function computes the chromaticity coordinates according to the
        ANSI Z80.3 standard for daylight, based on the provided transmission
        scan data.
    
        :param scan: The transmission scan data used to calculate the chromaticity.
        :type scan: Scan
        :return: A ChromaticityPoint representing the ANSI Z80.3 daylight
                 chromaticity coordinates (x, y).
        :rtype: ChromaticityPoint
    """
def ANSI_Z80_3_green_chromaticity(scan: benanalysis._benpy_core.Scan) -> CIExy:
    """
        Calculate the ANSI Z80.3 green chromaticity (x, y) from scan data.
    
        This function computes the chromaticity coordinates according to the
        ANSI Z80.3 standard for green, based on the provided transmission
        scan data.
    
        :param scan: The transmission scan data used to calculate the chromaticity.
        :type scan: Scan
        :return: A ChromaticityPoint representing the ANSI Z80.3 green
                 chromaticity coordinates (x, y).
        :rtype: ChromaticityPoint
    """
def ANSI_Z80_3_yellow_chromaticity(scan: benanalysis._benpy_core.Scan) -> CIExy:
    """
        Calculate the ANSI Z80.3 yellow chromaticity (x, y) from scan data.
    
        This function computes the chromaticity coordinates according to the
        ANSI Z80.3 standard for yellow, based on the provided transmission
        scan data.
    
        :param scan: The transmission scan data used to calculate the chromaticity.
        :type scan: Scan
        :return: A ChromaticityPoint representing the ANSI Z80.3 yellow
                 chromaticity coordinates (x, y).
        :rtype: ChromaticityPoint
    """
def CIE_1931_chromaticity(scan: benanalysis._benpy_core.Scan) -> CIExy:
    """
        Calculate the CIE 1931 chromaticity (x, y) coordinates from scan data.
    
        This function computes the chromaticity coordinates in CIE 1931 color space
        based on the provided transmission scan data. It processes the scan data
        and returns the corresponding (x, y) chromaticity values.
    
        :param scan: The transmission scan data used to calculate the chromaticity.
        :type scan: Scan
        :return: A ChromaticityPoint representing the CIE 1931 chromaticity
                 coordinates (x, y).
        :rtype: ChromaticityPoint
    """
