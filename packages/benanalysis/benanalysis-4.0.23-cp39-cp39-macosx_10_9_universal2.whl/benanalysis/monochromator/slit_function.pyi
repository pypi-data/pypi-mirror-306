from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['uniform_fibres', 'uniform_fibres_value']
def uniform_fibres(central_wavelength: float, bandwidth: float, points: int) -> benanalysis._benpy_core.Scan:
    """
        Returns the normalized slit function formed by the perfect image of a
        uniform circular input fibre passing across a circular exit fibre.
    
        This function computes the slit function, normalized to 1, for the perfect
        image of a uniform circular input fibre as it moves across a circular exit
        fibre. Both the input and exit fibres are assumed to have equal diameters.
        The slit function is generated over a specified number of points.
    
        :param central_wavelength: The central wavelength of the fibre system.
        :param bandwidth: The bandwidth of the fibre system.
        :param points: The number of points over which to compute the slit function.
        :return: A `Scan` object representing the slit function over the specified
                 number of points, normalized to 1.
    """
def uniform_fibres_value(central_wavelength: float, bandwidth: float, wavelength: float) -> float:
    """
        Returns the normalized slit function value for a uniform circular input fibre passing across a circular exit fibre.
    
        This function calculates the slit function value, normalized to 1, for the
        perfect image of a uniform circular input fibre as it moves across a circular
        exit fibre. Both the input and exit fibres are assumed to have equal diameters.
    
        :param central_wavelength: The central wavelength of the fibre system.
        :param bandwidth: The bandwidth of the fibre system.
        :param wavelength: The specific wavelength at which to calculate the slit
                           function value.
        :return: The normalized slit function value at the given wavelength.
    """
