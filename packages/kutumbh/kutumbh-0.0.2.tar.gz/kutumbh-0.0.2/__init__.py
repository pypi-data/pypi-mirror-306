import pandas as pd

# Define basic mathematical operations
def add_num(num1, num2):
    """Returns the sum of two numbers."""
    return num1 + num2

def sub_num(num1, num2):
    """Returns the difference between two numbers."""
    return num1 - num2

def mul_num(num1, num2):
    """Returns the product of two numbers."""
    return num1 * num2

def div_num(num1, num2):
    """Returns the division of two numbers. Raises an error if the divisor is zero."""
    if num2 == 0:
        raise ValueError("Division by zero is undefined.")
    return num1 / num2

# Define a function to read EPW files
def read_epw(epw_file_path):
    """
    Reads an EPW (EnergyPlus Weather) file and returns a DataFrame.

    Args:
        epw_file_path (str): Path to the EPW file.

    Returns:
        DataFrame: Pandas DataFrame containing the weather data.
    """
    column_names = [
        "Year", "Month", "Day", "Hour", "Minute", "Data Source and Uncertainty Flags",
        "Dry Bulb Temperature [C]", "Dew Point Temperature [C]", "Relative Humidity [%]",
        "Atmospheric Station Pressure [Pa]", "Extraterrestrial Horizontal Radiation [Wh/m2]",
        "Extraterrestrial Direct Normal Radiation [Wh/m2]", "Horizontal Infrared Radiation Intensity [Wh/m2]",
        "Global Horizontal Radiation [Wh/m2]", "Direct Normal Radiation [Wh/m2]",
        "Diffuse Horizontal Radiation [Wh/m2]", "Global Horizontal Illuminance [lux]",
        "Direct Normal Illuminance [lux]", "Diffuse Horizontal Illuminance [lux]",
        "Zenith Luminance [Cd/m2]", "Wind Direction [degrees]", "Wind Speed [m/s]",
        "Total Sky Cover", "Opaque Sky Cover", "Visibility [km]", "Ceiling Height [m]",
        "Present Weather Observation", "Present Weather Codes", "Precipitable Water [mm]",
        "Aerosol Optical Depth", "Snow Depth [cm]", "Days Since Last Snowfall",
        "Albedo", "Liquid Precipitation Depth [mm]", "Liquid Precipitation Quantity [hr]"
    ]

    try:
        # Read the EPW file into a DataFrame
        data = pd.read_csv(epw_file_path, skiprows=8, header=None, names=column_names, skipinitialspace=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {epw_file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
    return data
