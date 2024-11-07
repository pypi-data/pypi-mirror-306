from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['illuminance']
def illuminance(spectral_irradiance: benanalysis._benpy_core.Scan) -> float:
    """
      Calculates the illuminance at a given distance from a light source.
    
      This function computes the illuminance (in lux, lm/m²) based on the spectral
      irradiance of a light source (in watts per nanometer, W·nm⁻¹·m⁻²). The 
      calculation uses the CIE 1931 standard observer Y data to integrate the 
      spectral flux over the visible wavelength range (380 nm to 780 nm).
    
      Parameters:
        spectral_irradiance (Scan const&): The spectral irradiance of the light source 
                                           (in W·nm⁻¹·m⁻²).
    
      Returns:
        double: The illuminance at the given distance (in lux, lm/m²).
    """
