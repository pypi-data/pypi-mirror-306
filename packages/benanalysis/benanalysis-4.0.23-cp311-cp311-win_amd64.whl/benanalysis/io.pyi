from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['load_ben_scan_binary_data', 'load_ben_scan_data', 'load_csv']
def load_ben_scan_binary_data(buffer: list[int]) -> dict[str, benanalysis._benpy_core.Scan]:
    """
        Loads scan data from a binary buffer.
    
        This function reads binary scan data from the provided buffer and returns
        a map associating spectrum names with their corresponding Scan data.
    
        :param buffer: A vector of bytes containing the binary scan data.
        :return: A map from spectrum names to their corresponding Scan objects.
        :raises RuntimeError: If the buffer is empty.
    """
def load_ben_scan_data(file_path: str) -> dict[str, benanalysis._benpy_core.Scan]:
    """
        Loads scan data from a .ben file.
    
        This function reads a BenWin+ .ben data file from the specified file path
        and returns a map associating spectrum names with their corresponding Scan data.
    
        :param file_path: The path to the .ben file.
        :return: A map from spectrum names to their corresponding Scan objects.
        :raises ReadError: If the file cannot be opened for reading.
    """
def load_csv(file_path: str) -> benanalysis._benpy_core.Scan:
    """
        Loads scan data from a CSV file.
    
        This function reads a CSV file from the specified file path and returns the
        parsed Scan data. The data is expected to be in key-value pairs, separated by
        a specific delimiter.
    
        :param file_path: The path to the CSV file.
        :return: A Scan object containing the data read from the CSV file.
        :raises ReadError: If the file cannot be opened for reading.
    """
