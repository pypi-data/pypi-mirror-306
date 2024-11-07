from __future__ import annotations
import benanalysis._benpy_core
import typing
from . import data
__all__ = ['ANSI_Z80_3_tau_signal', 'ANSI_Z80_3_tau_spectral_min', 'ANSI_Z80_3_tau_uva', 'ANSI_Z80_3_tau_uvb', 'ANSI_Z80_3_tau_v', 'ASNZS1067_2016_tau_suva', 'CIELAB', 'CIELAB_f', 'CIELAB_tristimulus_values', 'CIEXYZ', 'CIE_tristimulus_values', 'ISO12311_tau_sb', 'ISO8980_3_tau_signal_incandescent', 'ISO8980_3_tau_signal_led', 'ISO8980_3_tau_suva', 'ISO8980_3_tau_suvb', 'ISO8980_3_tau_uva', 'ISO8980_3_tau_v', 'RYG', 'RYGB', 'data', 'f1_prime', 'f2']
class CIELAB:
    """
    
        CIE 1976 (L*, a*, b*) color space (CIELAB) coordinates.
    
        This class represents coordinates in the CIE 1976 color space, which is
        designed to be perceptually uniform. The coordinates include the lightness
        (L*) value and the two color-opponent dimensions (a*, b*).
        
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            Default constructor for CIELAB.
        
            Initializes a CIELAB color point with default values of L* = 0, a* = 0,
            and b* = 0.
        """
    @typing.overload
    def __init__(self, L_star: float, a_star: float, b_star: float) -> None:
        """
            Constructs a CIELAB color point with the given L*, a*, and b* coordinates.
        
            :param L_star: The lightness value (L*) in the CIELAB color space.
            :param a_star: The color-opponent value (a*) in the CIELAB color space.
            :param b_star: The color-opponent value (b*) in the CIELAB color space.
        """
    def __repr__(self) -> str:
        """
            Returns a string representation of the CIELAB color point.
        
            :return: A string in the format "<CIELAB L*: value a*: value b*: value>".
        """
    def __str__(self) -> str:
        """
            Returns a human-readable string representation of the CIELAB color point.
        
            :return: A string in the format "L*: value a*: value b*: value".
        """
    @property
    def L_star(self) -> float:
        """
            The lightness value (L*) in the CIELAB color space.
        """
    @L_star.setter
    def L_star(self, arg0: float) -> None:
        ...
    @property
    def a_star(self) -> float:
        """
            The color-opponent value (a*) in the CIELAB color space.
        """
    @a_star.setter
    def a_star(self, arg0: float) -> None:
        ...
    @property
    def b_star(self) -> float:
        """
            The color-opponent value (b*) in the CIELAB color space.
        """
    @b_star.setter
    def b_star(self, arg0: float) -> None:
        ...
class CIEXYZ:
    """
    
        CIE 1931 (X, Y, Z) color space (CIEXYZ) coordinates.
    
        This class represents the tristimulus values X, Y, and Z in the CIE 1931
        color space. These coordinates define the color characteristics of the
        point in the color space.
        
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            Default constructor for CIEXYZ.
        
            Initializes a CIEXYZ color point with default values of X = 0, Y = 0, and Z = 0.
        """
    @typing.overload
    def __init__(self, X: float, Y: float, Z: float) -> None:
        """
            Constructs a CIEXYZ color point with the given X, Y, and Z coordinates.
        
            :param X: The X tristimulus value in the CIE 1931 color space.
            :param Y: The Y tristimulus value in the CIE 1931 color space.
            :param Z: The Z tristimulus value in the CIE 1931 color space.
        """
    def __repr__(self) -> str:
        """
            Returns a string representation of the CIEXYZ color point.
        
            :return: A string in the format "<CIEXYZ X: value Y: value Z: value>".
        """
    def __str__(self) -> str:
        """
            Returns a human-readable string representation of the CIEXYZ color point.
        
            :return: A string in the format "X: value Y: value Z: value".
        """
    @property
    def X(self) -> float:
        """
            The X tristimulus value in the CIE 1931 color space.
        """
    @X.setter
    def X(self, arg0: float) -> None:
        ...
    @property
    def Y(self) -> float:
        """
            The Y tristimulus value in the CIE 1931 color space.
        """
    @Y.setter
    def Y(self, arg0: float) -> None:
        ...
    @property
    def Z(self) -> float:
        """
            The Z tristimulus value in the CIE 1931 color space.
        """
    @Z.setter
    def Z(self, arg0: float) -> None:
        ...
class RYG:
    """
    
        Red, Yellow, Green coordinates.
    
        This class represents a color in the red-yellow-green (RYG) color space,
        where the intensity of each primary color (red, yellow, and green) is
        stored. This color space is designed around these three primaries.
        
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            Default constructor for RYG.
        
            Initializes an RYG color point with default values of red = 0,
            yellow = 0, and green = 0.
        """
    @typing.overload
    def __init__(self, red: float, yellow: float, green: float) -> None:
        """
            Constructs an RYG color point with the given red, yellow, and green
            intensity values.
        
            :param red: The intensity of the red component.
            :param yellow: The intensity of the yellow component.
            :param green: The intensity of the green component.
        """
    def __repr__(self) -> str:
        """
            Returns a string representation of the RYG color point.
        
            :return: A string in the format "<RYG red: value yellow: value green: value>".
        """
    def __str__(self) -> str:
        """
            Returns a human-readable string representation of the RYG color point.
        
            :return: A string in the format "red: value yellow: value green: value".
        """
    @property
    def green(self) -> float:
        """
            The intensity of the green component.
        """
    @green.setter
    def green(self, arg0: float) -> None:
        ...
    @property
    def red(self) -> float:
        """
            The intensity of the red component.
        """
    @red.setter
    def red(self, arg0: float) -> None:
        ...
    @property
    def yellow(self) -> float:
        """
            The intensity of the yellow component.
        """
    @yellow.setter
    def yellow(self, arg0: float) -> None:
        ...
class RYGB:
    """
    
        Red, Yellow, Green, Blue coordinates.
    
        This class represents a color in the red-yellow-green-blue (RYGB) color
        space, where the intensity of each primary color (red, yellow, green, and
        blue) is stored. This color space is designed around these four primaries.
        
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        """
            Default constructor for RYGB.
        
            Initializes an RYGB color point with default values of red = 0, yellow = 0,
            green = 0, and blue = 0.
        """
    @typing.overload
    def __init__(self, red: float, yellow: float, green: float, blue: float) -> None:
        """
            Constructs an RYGB color point with the given red, yellow, green, and blue
            intensity values.
        
            :param red: The intensity of the red component.
            :param yellow: The intensity of the yellow component.
            :param green: The intensity of the green component.
            :param blue: The intensity of the blue component.
        """
    def __repr__(self) -> str:
        """
            Returns a string representation of the RYGB color point.
        
            :return: A string in the format "<RYGB red: value yellow: value green: value blue: value>".
        """
    def __str__(self) -> str:
        """
            Returns a human-readable string representation of the RYGB color point.
        
            :return: A string in the format "red: value yellow: value green: value blue: value".
        """
    @property
    def blue(self) -> float:
        """
            The intensity of the blue component.
        """
    @blue.setter
    def blue(self, arg0: float) -> None:
        ...
    @property
    def green(self) -> float:
        """
            The intensity of the green component.
        """
    @green.setter
    def green(self, arg0: float) -> None:
        ...
    @property
    def red(self) -> float:
        """
            The intensity of the red component.
        """
    @red.setter
    def red(self, arg0: float) -> None:
        ...
    @property
    def yellow(self) -> float:
        """
            The intensity of the yellow component.
        """
    @yellow.setter
    def yellow(self, arg0: float) -> None:
        ...
def ANSI_Z80_3_tau_signal(trans: benanalysis._benpy_core.Scan) -> RYG:
    """
        Returns the luminous transmittance of the lens for the spectral radiant
        power distribution of the incandescent traffic signal light.
        @see ANSI Z80.3 3.8.2.2
    """
def ANSI_Z80_3_tau_spectral_min(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the minimum of the spectral transmittance tau(lambda) of the lens
        between 475nm and 650nm.
        @see ANSI Z80.3 4.10.2.3
    """
def ANSI_Z80_3_tau_uva(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the mean UV-A transmittance (tau_UVA). The mean transmittance
        between 315 nm and 380 nm.
        @see ANSI Z80.3 2015 3.8.3
    """
def ANSI_Z80_3_tau_uvb(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the mean UV-B transmittance (tau_UVB). The mean transmittance
        between 280 nm and 315 nm.
        @see ANSI Z80.3 2015 3.8.3
    """
def ANSI_Z80_3_tau_v(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the luminous transmittance (tau_V). The ratio of the luminous flux
        transmitted by the lens or filter to the incident luminous flux
        @see ANSI Z80.3-2015 3.8.1
    """
def ASNZS1067_2016_tau_suva(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the solar UV-A transmittance (tau_SUVA). The mean of the spectral
        transmittance between 315 nm and 400 nm weighted by the solar radiation
        distribution Es(λ) at sea level, for air mass 2, and the relative spectral
        effectiveness function for UV radiation S(λ)
        @see ASNZS 1067.2 - 2016
    """
def CIELAB_f(t: float) -> float:
    """
        Non linear function used in the forward transformation from the CIEXYZ
        color space to the CIELAB.
        @see https://en.wikipedia.org/wiki/Lab_color_space
    """
def CIELAB_tristimulus_values(scan: benanalysis._benpy_core.Scan, white_point_reference: benanalysis._benpy_core.Scan, observer: benanalysis._benpy_core.Observer) -> CIELAB:
    """
        Returns the CIE 1976 (L*, a*, b*) color space coordinates for a given
        spectrum given a specific observer and white point reference.
    """
def CIE_tristimulus_values(scan: benanalysis._benpy_core.Scan, observer: benanalysis._benpy_core.Observer) -> CIEXYZ:
    """
        Returns the CIE Tristimulus Values for a given observer and spectrum.
    """
def ISO12311_tau_sb(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the solar blue-light transmittance tau_sb. Solar blue-light
        transmittance is the result of the mean of the spectral transmittance
        between 380 nm and 500 nm and appropriate weighting functions.
        @see ISO12311 Corrected version 2013-11-15 7.4
    """
def ISO8980_3_tau_signal_incandescent(trans: benanalysis._benpy_core.Scan) -> RYGB:
    """
        Returns the luminous transmittance of the lens for the spectral radiant
        power distribution of the incandescent traffic signal light.
        @see ISO8980-3 Third Edition 2013-10-01 3.5
    """
def ISO8980_3_tau_signal_led(trans: benanalysis._benpy_core.Scan) -> RYGB:
    """
        Returns the luminous transmittance of the lens for the spectral radiant
        power distribution of the LED traffic signal light.
        @see ISO8980-3 Third Edition 2013-10-01 3.5
    """
def ISO8980_3_tau_suva(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the solar UV-A transmittance (tau_SUVA). The mean of the spectral
        transmittance between 315 nm and 380 nm weighted by the solar radiation
        distribution Es(λ) at sea level, for air mass 2, and the relative spectral
        effectiveness function for UV radiation S(λ)
        @see ISO8980-3 Third Edition 2013-10-01 3.2
    """
def ISO8980_3_tau_suvb(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the solar UV-B transmittance (tau_SUVB). The mean of the spectral
        transmittance between 280 nm and 315 nm weighted by the solar radiation
        distribution Es(λ) at sea level, for air mass 2, and the relative spectral
        effectiveness function for UV radiation S(λ)
        @see ISO8980-3 Third Edition 2013-10-01 3.3
    """
def ISO8980_3_tau_uva(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the mean UV-A transmittance (tau_UVA). The mean transmittance
        between 315 nm and 380 nm.
        @see ISO8980-3 Third Edition 2013-10-01 3.1
    """
def ISO8980_3_tau_v(trans: benanalysis._benpy_core.Scan) -> float:
    """
        Returns the luminous transmittancev (tau_V). The ratio of the luminous flux
        transmitted by the lens or filter to the incident luminous flux
        @see ISO8980-3 Third Edition 2013-10-01 3.4
    """
def f1_prime(scan: benanalysis._benpy_core.Scan) -> float:
    """
        The integral parameter f1' describes the quality of the spectral match
        between a specified spectrum and the CIE 1931 standard colorimetric
        observer (CIE 1931 2° Standard Observer) Color Matching Function y.
    """
def f2(Y_0: benanalysis._benpy_core.Scan, Y_pi_2: benanalysis._benpy_core.Scan) -> float:
    """
        Calculates the f2 directional deviation for a photometer with a plane
        input window measuring planar illuminances.
    
        This function computes the f2 deviation in directional response to the
        incident radiation for a photometer, based on the output signals as functions
        of the angle of incidence (ɛ) and azimuth angle (φ). The calculation follows
        the ISO/CIE 19476:2014(E) standard.
    
        The f2(ɛ, φ) value is given by:
    
          f2(ɛ, φ) = Y(ɛ, φ) / (Y(0, φ) cos(ɛ)) - 1
    
        The overall f2 value is then computed as:
    
          f2 = average[φ={0, π/2, π, 3π/2}](integral[0 ≤ ɛ ≤ 4π/9](|f2(ɛ, φ)| sin(2ɛ) dɛ))
    
        Where:
          - Y(ɛ, φ) is the output signal as a function of the angle of incidence ɛ
            and azimuth angle φ.
          - ɛ is the angle measured with respect to the normal to the measuring plane
            or optical axis.
          - φ is the azimuth angle.
    
        :param Y_0: The output signal Y(-4π/9 ≤ ɛ ≤ 4π/9, φ = 0) as a function of the
                    angle in radians (-4π/9 ≤ ɛ ≤ 4π/9).
        :type Y_0: float
        :param Y_pi_2: The output signal Y(-4π/9 ≤ ɛ ≤ 4π/9, φ = π/2) as a function
                      of the angle in radians (-4π/9 ≤ ɛ ≤ 4π/9).
        :type Y_pi_2: float
        :return: The f2 directional deviation value.
        :rtype: float
    
        :see: ISO/CIE 19476:2014(E) 5.5.3
    """
