"""
Earth Engine Data Downloader (Optional)

This module provides functions to download real satellite imagery using Google Earth Engine.
To use this, you'll need to:
1. Create a Google Earth Engine account at https://earthengine.google.com/
2. Authenticate using: earthengine authenticate
3. Run the functions below to download actual satellite data

This is optional - the Quarto document works with simulated data by default.
"""

import ee
import geemap
import os
from datetime import datetime


def initialize_earth_engine():
    """Initialize Google Earth Engine"""
    try:
        ee.Initialize()
        print("Earth Engine initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing Earth Engine: {e}")
        print("Please run: earthengine authenticate")
        return False


def download_landsat_time_series(bbox, start_date, end_date, output_dir='data'):
    """
    Download Landsat imagery time series for a given area

    Parameters:
    -----------
    bbox : dict
        Bounding box with keys: north, south, east, west
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    output_dir : str
        Directory to save downloaded images
    """

    if not initialize_earth_engine():
        return None

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Define area of interest
    aoi = ee.Geometry.Rectangle([
        bbox['west'], bbox['south'],
        bbox['east'], bbox['north']
    ])

    # Load Landsat 8 collection
    collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                  .filterBounds(aoi)
                  .filterDate(start_date, end_date)
                  .filter(ee.Filter.lt('CLOUD_COVER', 20)))

    print(f"Found {collection.size().getInfo()} images")

    # Get image list
    image_list = collection.toList(collection.size())

    return collection, aoi


def calculate_ndvi(image):
    """
    Calculate NDVI (Normalized Difference Vegetation Index)

    NDVI is used to identify vegetated areas:
    - High values (0.6-0.9) indicate dense vegetation
    - Medium values (0.2-0.6) indicate sparse vegetation
    - Low values (-1-0.2) indicate water, urban, bare soil
    """
    nir = image.select('SR_B5')
    red = image.select('SR_B4')
    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
    return image.addBands(ndvi)


def classify_land_cover(image, aoi):
    """
    Simple land cover classification based on NDVI and spectral indices

    Returns:
    --------
    Classified image with categories:
    1 - Water
    2 - Bare soil/Urban
    3 - Grassland/Sparse vegetation
    4 - Forest/Dense vegetation
    """

    # Calculate indices
    image = calculate_ndvi(image)

    # Simple classification rules
    water = image.select('NDVI').lt(0)
    bare = image.select('NDVI').gte(0).And(image.select('NDVI').lt(0.2))
    grass = image.select('NDVI').gte(0.2).And(image.select('NDVI').lt(0.5))
    forest = image.select('NDVI').gte(0.5)

    # Create classified image
    classified = (water.multiply(1)
                  .add(bare.multiply(2))
                  .add(grass.multiply(3))
                  .add(forest.multiply(4)))

    return classified.rename('land_cover')


def export_land_cover_statistics(collection, aoi, year_start, year_end):
    """
    Export land cover statistics for multiple years

    Returns:
    --------
    Dictionary with land cover percentages for each year
    """

    results = {}

    for year in range(year_start, year_end + 1):
        # Filter images for this year
        year_collection = collection.filterDate(f'{year}-01-01', f'{year}-12-31')

        if year_collection.size().getInfo() == 0:
            continue

        # Get median composite for the year
        composite = year_collection.median()

        # Classify land cover
        classified = classify_land_cover(composite, aoi)

        # Calculate area statistics
        area_image = ee.Image.pixelArea().addBands(classified)

        stats = area_image.reduceRegion(
            reducer=ee.Reducer.sum().group(
                groupField=1,
                groupName='land_cover'
            ),
            geometry=aoi,
            scale=30,
            maxPixels=1e9
        )

        results[year] = stats.getInfo()
        print(f"Processed year {year}")

    return results


def create_interactive_map(bbox, collection):
    """
    Create an interactive map with the satellite imagery
    """

    Map = geemap.Map()
    Map.centerObject(ee.Geometry.Rectangle([
        bbox['west'], bbox['south'],
        bbox['east'], bbox['north']
    ]), zoom=10)

    # Add latest image
    latest_image = collection.sort('system:time_start', False).first()

    vis_params = {
        'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
        'min': 7000,
        'max': 12000,
        'gamma': 1.4
    }

    Map.addLayer(latest_image, vis_params, 'Latest RGB Image')

    # Add NDVI
    ndvi_image = calculate_ndvi(latest_image)
    ndvi_params = {
        'bands': ['NDVI'],
        'min': -1,
        'max': 1,
        'palette': ['blue', 'white', 'green']
    }

    Map.addLayer(ndvi_image, ndvi_params, 'NDVI')

    return Map


if __name__ == '__main__':
    """
    Example usage
    """

    # Define study area (Amazon example)
    study_area = {
        'north': -3.0,
        'south': -4.0,
        'east': -62.0,
        'west': -63.0
    }

    # Download data
    print("Initializing Earth Engine...")
    collection, aoi = download_landsat_time_series(
        bbox=study_area,
        start_date='2015-01-01',
        end_date='2024-12-31'
    )

    # Export statistics
    print("\nCalculating land cover statistics...")
    stats = export_land_cover_statistics(collection, aoi, 2015, 2024)

    print("\nLand cover statistics:")
    print(stats)

    # Create map
    print("\nCreating interactive map...")
    Map = create_interactive_map(study_area, collection)
    Map.save('satellite_map.html')
    print("Map saved to satellite_map.html")
