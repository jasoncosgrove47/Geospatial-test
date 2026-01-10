# Geospatial Land Coverage Analysis

This project provides a comprehensive time series analysis of land coverage changes using satellite imagery and geospatial data, packaged as an interactive Quarto HTML report.

## Features

- **Time Series Analysis**: Track land coverage changes over multiple years
- **Multiple Land Cover Types**: Forest, Cropland, Urban, Water, and Bare Land
- **Statistical Analysis**: Linear regression, correlation analysis, and trend detection
- **Interactive Visualizations**: Stacked area charts, trend lines, and interactive maps
- **Spatial Analysis**: Simulated land coverage maps showing spatial distribution
- **HTML Report**: Self-contained HTML output with embedded visualizations

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
./setup.sh
source venv/bin/activate
quarto render land_coverage_analysis.qmd
```

### Option 2: Manual Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Quarto (if not already installed):
   - **Ubuntu/Debian**: `wget https://quarto.org/download/latest/quarto-linux-amd64.deb && sudo dpkg -i quarto-linux-amd64.deb`
   - **macOS**: `brew install quarto`
   - **Other**: Visit https://quarto.org/docs/get-started/

3. Render the analysis:
```bash
quarto render land_coverage_analysis.qmd
```

The output HTML file will be generated as `land_coverage_analysis.html`

## Project Structure

```
.
├── land_coverage_analysis.qmd    # Main Quarto analysis document
├── earth_engine_downloader.py    # Optional: Download real satellite data
├── requirements.txt               # Python dependencies
├── setup.sh                       # Automated setup script
├── README.md                      # This file
└── .gitignore                     # Git ignore patterns
```

## Output

The analysis generates a comprehensive HTML report with:

- **Interactive Maps**: Folium-based maps showing the study area
- **Time Series Plots**: Stacked area charts and individual trend lines
- **Rate of Change Analysis**: Year-over-year changes in land coverage
- **Correlation Analysis**: Relationships between land cover types
- **Statistical Summary**: Regression analysis and significance testing
- **Simulated Land Maps**: Visual representation of land coverage distribution

## Customization

### Change Study Area

Edit the study area in `land_coverage_analysis.qmd`:

```python
study_area = {
    'name': 'Your Region Name',
    'bbox': {
        'north': YOUR_NORTH_LAT,
        'south': YOUR_SOUTH_LAT,
        'east': YOUR_EAST_LON,
        'west': YOUR_WEST_LON
    },
    'center': [CENTER_LAT, CENTER_LON]
}
```

### Use Real Satellite Data (Advanced)

The main document uses simulated data for demonstration. To use real satellite imagery:

1. Create a Google Earth Engine account at https://earthengine.google.com/
2. Authenticate: `earthengine authenticate`
3. Use the functions in `earth_engine_downloader.py` to download actual data
4. Replace simulated data in the Quarto document with real data

## Data Sources

This project demonstrates analysis techniques using simulated data. For production use, integrate:

- **Google Earth Engine**: Landsat 8/9, Sentinel-2 imagery
- **ESA WorldCover**: 10m resolution global land cover data
- **USGS Earth Explorer**: Historical Landsat imagery
- **Copernicus**: European satellite data

## Requirements

- Python 3.8+
- Quarto 1.3+
- Dependencies listed in `requirements.txt`

## Dependencies

Key Python libraries used:
- `geopandas`: Geospatial data manipulation
- `rasterio`: Raster data processing
- `folium`: Interactive maps
- `matplotlib`: Static visualizations
- `pandas/numpy`: Data analysis
- `earthengine-api`: Google Earth Engine integration (optional)

## License

This project is provided as-is for educational and research purposes.

## Contributing

Feel free to customize the analysis for your specific use case. Suggestions for improvement:
- Add more sophisticated land cover classification algorithms
- Implement change detection algorithms
- Include climate/weather data correlations
- Add predictive modeling for future land cover scenarios
