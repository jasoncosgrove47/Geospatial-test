#!/usr/bin/env python3
"""
Generate a preview HTML of the land coverage analysis
This script extracts the Python code from the Quarto document and generates visualizations
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import folium
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

print("Generating land coverage analysis preview...")

# Define study area
study_area = {
    'name': 'Sample Amazon Region',
    'bbox': {
        'north': -3.0,
        'south': -4.0,
        'east': -62.0,
        'west': -63.0
    },
    'center': [-3.5, -62.5]
}

# Time periods for analysis
time_periods = pd.date_range(start='2015-01-01', end='2024-01-01', freq='Y')
years = [str(date.year) for date in time_periods]

print(f"Analyzing {len(years)} time periods: {years[0]} to {years[-1]}")

# Generate land coverage data
def generate_land_coverage_data(years, simulate_deforestation=True):
    data = []
    initial_forest = 65.0
    initial_cropland = 20.0
    initial_urban = 5.0
    initial_water = 7.0
    initial_bare = 3.0

    for i, year in enumerate(years):
        if simulate_deforestation:
            forest = initial_forest - (i * 1.5) + np.random.normal(0, 0.5)
            urban = initial_urban + (i * 0.8) + np.random.normal(0, 0.3)
            cropland = initial_cropland + (i * 0.5) + np.random.normal(0, 0.4)
            water = initial_water + np.random.normal(0, 0.2)
            bare = initial_bare + (i * 0.2) + np.random.normal(0, 0.2)
        else:
            forest = initial_forest + np.random.normal(0, 1.0)
            cropland = initial_cropland + np.random.normal(0, 0.8)
            urban = initial_urban + np.random.normal(0, 0.5)
            water = initial_water + np.random.normal(0, 0.3)
            bare = initial_bare + np.random.normal(0, 0.3)

        total = forest + cropland + urban + water + bare

        data.append({
            'Year': year,
            'Forest': (forest / total) * 100,
            'Cropland': (cropland / total) * 100,
            'Urban': (urban / total) * 100,
            'Water': (water / total) * 100,
            'Bare Land': (bare / total) * 100
        })

    return pd.DataFrame(data)

land_coverage_df = generate_land_coverage_data(years)
categories = ['Forest', 'Cropland', 'Urban', 'Water', 'Bare Land']
colors = ['#2d5f2e', '#f4a460', '#8b0000', '#4682b4', '#daa520']

print("\nGenerating visualizations...")

# Create time series plot
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

axes[0].stackplot(land_coverage_df['Year'],
                  land_coverage_df['Forest'],
                  land_coverage_df['Cropland'],
                  land_coverage_df['Urban'],
                  land_coverage_df['Water'],
                  land_coverage_df['Bare Land'],
                  labels=categories,
                  colors=colors,
                  alpha=0.8)

axes[0].set_xlabel('Year', fontsize=12)
axes[0].set_ylabel('Coverage (%)', fontsize=12)
axes[0].set_title('Land Coverage Composition Over Time (Stacked)', fontsize=14, fontweight='bold')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(0, 100)

for category, color in zip(categories, colors):
    axes[1].plot(land_coverage_df['Year'],
                 land_coverage_df[category],
                 marker='o',
                 label=category,
                 color=color,
                 linewidth=2,
                 markersize=6)

axes[1].set_xlabel('Year', fontsize=12)
axes[1].set_ylabel('Coverage (%)', fontsize=12)
axes[1].set_title('Individual Land Coverage Trends', fontsize=14, fontweight='bold')
axes[1].legend(loc='best')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('land_coverage_trends.png', dpi=150, bbox_inches='tight')
print("✓ Saved: land_coverage_trends.png")

# Create interactive map
m = folium.Map(
    location=study_area['center'],
    zoom_start=8,
    tiles='OpenStreetMap'
)

folium.Rectangle(
    bounds=[
        [study_area['bbox']['south'], study_area['bbox']['west']],
        [study_area['bbox']['north'], study_area['bbox']['east']]
    ],
    color='red',
    fill=True,
    fillOpacity=0.2,
    popup=f"Study Area: {study_area['name']}"
).add_to(m)

folium.Marker(
    study_area['center'],
    popup=f"<b>{study_area['name']}</b><br>Center Point",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

m.save('study_area_map.html')
print("✓ Saved: study_area_map.html")

# Generate HTML report
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Geospatial Land Coverage Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .subtitle {{
            margin-top: 10px;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .image-container {{
            margin: 20px 0;
            text-align: center;
        }}
        img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .map-container {{
            margin: 20px 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        iframe {{
            width: 100%;
            height: 600px;
            border: none;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding: 20px;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            background-color: #667eea;
            color: white;
            border-radius: 4px;
            font-size: 0.9em;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Geospatial Land Coverage Analysis</h1>
        <div class="subtitle">Time Series Analysis of Land Use Changes</div>
        <div style="margin-top: 15px;">
            <span class="badge">📅 {years[0]} - {years[-1]}</span>
            <span class="badge">📍 {study_area['name']}</span>
            <span class="badge">📊 {len(years)} Time Periods</span>
        </div>
    </div>

    <div class="section">
        <h2>📈 Summary Statistics</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{land_coverage_df.iloc[0]['Forest']:.1f}%</div>
                <div class="stat-label">Initial Forest Coverage ({years[0]})</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{land_coverage_df.iloc[-1]['Forest']:.1f}%</div>
                <div class="stat-label">Final Forest Coverage ({years[-1]})</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{land_coverage_df.iloc[-1]['Forest'] - land_coverage_df.iloc[0]['Forest']:.1f}%</div>
                <div class="stat-label">Forest Change</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{land_coverage_df.iloc[-1]['Urban']:.1f}%</div>
                <div class="stat-label">Urban Coverage ({years[-1]})</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Land Coverage Trends</h2>
        <div class="image-container">
            <img src="land_coverage_trends.png" alt="Land Coverage Trends">
        </div>
    </div>

    <div class="section">
        <h2>🗺️ Study Area Map</h2>
        <div class="map-container">
            <iframe src="study_area_map.html"></iframe>
        </div>
    </div>

    <div class="section">
        <h2>📋 Detailed Data</h2>
        <table>
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Forest (%)</th>
                    <th>Cropland (%)</th>
                    <th>Urban (%)</th>
                    <th>Water (%)</th>
                    <th>Bare Land (%)</th>
                </tr>
            </thead>
            <tbody>
"""

for _, row in land_coverage_df.iterrows():
    html_content += f"""
                <tr>
                    <td>{row['Year']}</td>
                    <td>{row['Forest']:.2f}</td>
                    <td>{row['Cropland']:.2f}</td>
                    <td>{row['Urban']:.2f}</td>
                    <td>{row['Water']:.2f}</td>
                    <td>{row['Bare Land']:.2f}</td>
                </tr>
"""

html_content += f"""
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>🔍 Key Findings</h2>
        <ul>
            <li><strong>Forest Coverage:</strong> Declined from {land_coverage_df.iloc[0]['Forest']:.1f}% to {land_coverage_df.iloc[-1]['Forest']:.1f}% (change of {land_coverage_df.iloc[-1]['Forest'] - land_coverage_df.iloc[0]['Forest']:.1f} percentage points)</li>
            <li><strong>Urban Expansion:</strong> Increased from {land_coverage_df.iloc[0]['Urban']:.1f}% to {land_coverage_df.iloc[-1]['Urban']:.1f}% (change of {land_coverage_df.iloc[-1]['Urban'] - land_coverage_df.iloc[0]['Urban']:.1f} percentage points)</li>
            <li><strong>Agricultural Land:</strong> Cropland coverage changed from {land_coverage_df.iloc[0]['Cropland']:.1f}% to {land_coverage_df.iloc[-1]['Cropland']:.1f}%</li>
            <li><strong>Water Bodies:</strong> Remained relatively stable at approximately {land_coverage_df['Water'].mean():.1f}%</li>
        </ul>
    </div>

    <div class="footer">
        <p><strong>Geospatial Land Coverage Analysis</strong></p>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Data: Simulated for demonstration purposes</p>
    </div>
</body>
</html>
"""

with open('land_coverage_analysis_preview.html', 'w') as f:
    f.write(html_content)

print("✓ Saved: land_coverage_analysis_preview.html")
print("\n" + "="*60)
print("✓ Preview generation complete!")
print("="*60)
print("\nGenerated files:")
print("  1. land_coverage_analysis_preview.html (Main report)")
print("  2. land_coverage_trends.png (Charts)")
print("  3. study_area_map.html (Interactive map)")
print("\nOpen land_coverage_analysis_preview.html in your browser to view the analysis.")
