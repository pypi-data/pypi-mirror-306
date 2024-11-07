from __future__ import annotations
import benanalysis._benpy_core
import typing
__all__ = ['StitchResults', 'find_key', 'find_peak', 'find_peaks', 'log', 'log10', 'peak_width', 'stitch_scans', 'transform']
class StitchResults:
    """
    
      Contains the results of a scan stitching operation.
    
      The `StitchResults` class holds the data produced by the `stitch_scans`
      function, including whether the stitching operation was successful, the
      scaling factor, the error metrics, and the final stitched scan.
    
      :param success: Indicates whether the stitching operation was successful.
                      This boolean is set to True if the RMS percentage error is
                      below the specified target error, indicating a successful stitch.
      :type success: bool
    
      :param n: The number of data points used in the stitching region. This value
                represents the count of data points from `scan_1` in the range
                [min_wl, max_wl].
      :type n: int
    
      :param k: The scaling factor applied to `scan_2` to match `scan_1`. This factor
                `k` minimizes the difference between `scan_1` and the scaled `scan_2`
                in the stitching region.
      :type k: float
    
      :param error: The total error between `scan_1` and the scaled `scan_2` in the
                    stitching region. This value represents the sum of squared
                    differences between `scan_1` and `k * scan_2` across the
                    stitching region.
      :type error: float, optional, default: 0.0
    
      :param average: The average signal value in the stitching region. This is the
                      average of `scan_1` and `k * scan_2` over the stitching region.
      :type average: float, optional, default: 0.0
    
      :param percent_error_rms: The root mean square (RMS) percentage error of the
                                fit. This metric represents the RMS error as a
                                percentage of the average signal value in the
                                stitching region.
      :type percent_error_rms: float
    
      :param stitch_point: The wavelength at which the stitch between `scan_1` and
                          `scan_2` occurs. This is the wavelength where the two
                          scans are combined. At this point, `scan_1` and `k * scan_2`
                          meet.
      :type stitch_point: float, optional, default: 0.0
    
      :param stitch_scan: The final stitched scan combining `scan_1` and `k * scan_2`.
                          This `Scan` object contains the merged data from `scan_1`
                          up to the stitch point and `k * scan_2` after the stitch point.
      :type stitch_scan: Scan
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    @property
    def average(self) -> float:
        ...
    @property
    def error(self) -> float:
        ...
    @property
    def k(self) -> float:
        ...
    @property
    def n(self) -> int:
        ...
    @property
    def percent_error_rms(self) -> float:
        ...
    @property
    def stitch_point(self) -> float:
        ...
    @property
    def stitch_scan(self) -> benanalysis._benpy_core.Scan:
        ...
    @property
    def success(self) -> bool:
        ...
def find_key(scan: benanalysis._benpy_core.Scan, lo: float, hi: float, value: float) -> float:
    """
    Find the key between lo and hi that gives a value of the specified value.
    """
def find_peak(scan: benanalysis._benpy_core.Scan) -> float:
    """
      Finds the global peak of a specified Scan scan and returns the found
      (interpolated) key.
    """
def find_peaks(scan: benanalysis._benpy_core.Scan) -> benanalysis._benpy_core.Scan:
    """
      Finds all the peaks in a specified Scan scan and returns a new Scan containing
      the found points.
    """
@typing.overload
def log(scan: benanalysis._benpy_core.Scan) -> benanalysis._benpy_core.Scan:
    """
    Compute natural logarithm of scan [Scan].
    """
@typing.overload
def log(scan: benanalysis._benpy_core.Scan, base: benanalysis._benpy_core.Scan) -> benanalysis._benpy_core.Scan:
    """
    Compute logarithm base [Scan] of scan [Scan].
    """
@typing.overload
def log(scan: benanalysis._benpy_core.Scan, base: float) -> benanalysis._benpy_core.Scan:
    """
    Compute logarithm base [float] of scan [Scan].
    """
@typing.overload
def log(x: float, base: benanalysis._benpy_core.Scan) -> benanalysis._benpy_core.Scan:
    """
    Compute logarithm base [Scan] of x [float].
    """
def log10(scan: benanalysis._benpy_core.Scan) -> benanalysis._benpy_core.Scan:
    """
    Compute logarithm base 10 of scan [Scan].
    """
def peak_width(scan: benanalysis._benpy_core.Scan, height: float) -> float:
    """
      Finds the width of a peak at a specified fractional height from the maximum.
      Assumes the scan contains a single peak.
    """
def stitch_scans(scan_1: benanalysis._benpy_core.Scan, scan_2: benanalysis._benpy_core.Scan, min_wl: float, max_wl: float, target_error: float) -> StitchResults:
    """
      Stitches two scans together over a specified wavelength range.
    
      This function stitches two scans (`scan_1` and `scan_2`) by scaling `scan_2`
      to match `scan_1` over a defined wavelength range [min_wl, max_wl]. It calculates
      a scaling factor `k` to minimize the difference between the two scans within
      the stitching region. It then evaluates the goodness of fit and performs the
      stitch if the error is sufficiently low. A stitching point is then found so
      that at this point `scan_1 = k * scan_2`.
    
      The stitched scan combines `scan_1` up to the stitch point and `scan_2`
      scaled by `k` after the stitch point.
    
      :param scan_1: The first scan, which must contain points at both `min_wl` and `max_wl`.
      :type scan_1: Scan
      :param scan_2: The second scan, which must be defined over the range [min_wl, max_wl].
      :type scan_2: Scan
      :param min_wl: The minimum wavelength in the stitching region.
      :type min_wl: float
      :param max_wl: The maximum wavelength in the stitching region.
      :type max_wl: float
      :param target_error: The target RMS error threshold for a successful stitch.
      :type target_error: float
      :returns: A `StitchResults` object containing the scaling factor, error metrics,
                and the resulting stitched scan if the stitch is successful.
      :rtype: StitchResults
    
      :raises ValueError: If any of the following conditions are met:
          - `max_wl < min_wl`
          - `scan_1` does not contain points at `min_wl` and `max_wl`
          - `scan_2` is not defined over the domain [min_wl, max_wl]
    """
def transform(scan: benanalysis._benpy_core.Scan, binary_operation: typing.Callable[[float, float], float]) -> benanalysis._benpy_core.Scan:
    """
      Returns a new Scan with entries {key, op(key, value)} for each {key, value}
      in the specified Scan.
    """
