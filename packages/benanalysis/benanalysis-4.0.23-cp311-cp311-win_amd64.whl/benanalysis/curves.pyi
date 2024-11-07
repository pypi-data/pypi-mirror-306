from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['lognormal', 'longpass_filter', 'shortpass_filter']
def lognormal(peak_wl: float, fwhm: float, min_wl: float, max_wl: float, step_wl: float) -> benanalysis._benpy_core.Scan:
    """
      Generates a lognormal scan over a specified wavelength range.
    
      This function computes a lognormal distribution of values over a wavelength
      range specified by the minimum (`min_wl`) and maximum (`max_wl`) wavelengths,
      with a given step size (`step_wl`). The distribution is characterized by a
      peak wavelength (`peak_wl`) and a full width at half maximum (`fwhm`).
    
      :param peak_wl: The peak wavelength of the lognormal distribution. Must be greater than 0.
      :type peak_wl: float
      :param fwhm: The full width at half maximum of the lognormal distribution. Must be greater than 0.
      :type fwhm: float
      :param min_wl: The minimum wavelength for the scan. Must be less than `max_wl`.
      :type min_wl: float
      :param max_wl: The maximum wavelength for the scan. Must be greater than `min_wl`.
      :type max_wl: float
      :param step_wl: The step size for the scan. Must be positive and less than or equal to (`max_wl - min_wl`).
      :type step_wl: float
      :return: A Scan object containing the computed lognormal values mapped to their corresponding wavelengths.
      :rtype: Scan
      :raises ValueError: If any of the following conditions are met:
                          - `peak_wl <= 0`
                          - `fwhm <= 0`
                          - `min_wl >= max_wl`
                          - `step_wl > (max_wl - min_wl)`
                          - `step_wl <= 0`
    """
def longpass_filter(center_wl: float, bandwidth: float, min_wl: float, max_wl: float, step_wl: float) -> benanalysis._benpy_core.Scan:
    """
      Generate a long-pass filter scan based on specified parameters.
    
      The filter's bandwidth is defined as the wavelength range over which transmission
      rises from 5% to 95%. The transmission values in the scan range from 0 to 1.
    
      :param center_wl: The center wavelength of the filter.
      :type center_wl: float
      :param bandwidth: The bandwidth of the filter (5% to 95% transmission range).
      :type bandwidth: float
      :param min_wl: The minimum wavelength for the scan.
      :type min_wl: float
      :param max_wl: The maximum wavelength for the scan.
      :type max_wl: float
      :param step_wl: The step size for the wavelength increments.
      :type step_wl: float
      :return: A Scan object representing the long-pass filter response.
      :rtype: Scan
      :raises ValueError: If the wavelength parameters are invalid (e.g., min_wl >= max_wl,
                          step_wl <= 0, or step_wl > (max_wl - min_wl)).
    """
def shortpass_filter(center_wl: float, bandwidth: float, min_wl: float, max_wl: float, step_wl: float) -> benanalysis._benpy_core.Scan:
    """
      Generate a short-pass filter scan based on specified parameters.
    
      The filter's bandwidth is defined as the wavelength range over which transmission
      falls from 95% to 5%. The transmission values in the scan range from 0 to 1.
    
      :param center_wl: The center wavelength of the filter.
      :type center_wl: float
      :param bandwidth: The bandwidth of the filter (95% to 5% transmission range).
      :type bandwidth: float
      :param min_wl: The minimum wavelength for the scan.
      :type min_wl: float
      :param max_wl: The maximum wavelength for the scan.
      :type max_wl: float
      :param step_wl: The step size for the wavelength increments.
      :type step_wl: float
      :return: A Scan object representing the short-pass filter response.
      :rtype: Scan
      :raises ValueError: If the wavelength parameters are invalid (e.g., min_wl >= max_wl,
                          step_wl <= 0, or step_wl > (max_wl - min_wl)).
    """
