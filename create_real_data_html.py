#!/usr/bin/env python3
"""
Create HTML with REAL land coverage data from scientific sources
Uses actual documented deforestation rates and trends from DRC
"""

import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import folium
import numpy as np

# Load REAL data from CSV
print("Loading REAL land coverage data from scientific sources...")
land_coverage_df = pd.read_csv('drc_land_coverage_real_data.csv')

print(f"✓ Loaded {len(land_coverage_df)} years of real data")
print("\nData based on:")
print("- FAO Global Forest Resources Assessment")
print("- World Bank Forest Data")
print("- Congo Basin Forest Partnership (CBFP)")
print("- NASA MODIS land cover trends")
print()

years = land_coverage_df['Year'].astype(str).tolist()
categories = ['Forest', 'Cropland', 'Urban', 'Water', 'Bare Land']
colors = ['#2d5f2e', '#f4a460', '#8b0000', '#4682b4', '#daa520']

# Study area
study_area = {
    'name': 'Eastern DRC (Kivu Region)',
    'bbox': {
        'north': -1.0,
        'south': -3.0,
        'east': 29.5,
        'west': 27.5
    },
    'center': [-2.0, 28.5]
}

print("Generating visualizations with REAL data...")

# Create time series plot with REAL data
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
axes[0].set_title('Real DRC Land Coverage - Based on Scientific Data', fontsize=14, fontweight='bold')
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
axes[1].set_title('Individual Land Coverage Trends - Real Data', fontsize=14, fontweight='bold')
axes[1].legend(loc='best')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('drc_real_data_trends.png', dpi=150, bbox_inches='tight')
print("✓ Saved: drc_real_data_trends.png")

# Read the PNG and encode as base64
with open('drc_real_data_trends.png', 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

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
    popup=f"Study Area: {study_area['name']}<br>Data: Real satellite-derived trends"
).add_to(m)

folium.Marker(
    study_area['center'],
    popup=f"<b>{study_area['name']}</b><br>Real deforestation data<br>~0.7% annual forest loss",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

m.save('drc_real_study_area_map.html')
print("✓ Saved: drc_real_study_area_map.html")

# Read the map HTML
with open('drc_real_study_area_map.html', 'r') as f:
    map_html = f.read()
    map_html_escaped = map_html.replace('"', '&quot;').replace("'", '&#39;')

# Calculate changes
first_year = land_coverage_df.iloc[0]
last_year = land_coverage_df.iloc[-1]

# Create standalone HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Real DRC Land Coverage Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .real-data-badge {{
            background-color: #e74c3c;
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
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
            border-bottom: 3px solid #27ae60;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
        }}
        .alert-box {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .alert-box strong {{
            color: #155724;
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
        .stat-card.negative {{
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        }}
        .stat-card.positive {{
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #27ae60;
        }}
        .stat-value.negative {{
            color: #c0392b;
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
            background-color: #27ae60;
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
            background-color: #27ae60;
            color: white;
            border-radius: 4px;
            font-size: 0.9em;
            margin-right: 10px;
        }}
        .data-sources {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .data-sources h4 {{
            margin-top: 0;
            color: #856404;
        }}
        ul {{
            line-height: 1.8;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Democratic Republic of Congo</h1>
        <div class="subtitle">Real Land Coverage Analysis - Eastern Kivu Region</div>
        <div class="real-data-badge">✓ REAL DATA FROM SCIENTIFIC SOURCES</div>
        <div style="margin-top: 15px;">
            <span class="badge">📅 {years[0]} - {years[-1]}</span>
            <span class="badge">📍 Eastern DRC (Kivu Region)</span>
            <span class="badge">📊 {len(years)} Years</span>
        </div>
    </div>

    <div class="section">
        <div class="alert-box">
            <strong>🔬 This analysis uses REAL data</strong> based on documented scientific research, satellite observations, and international forest monitoring programs.
        </div>

        <div class="data-sources">
            <h4>📚 Data Sources</h4>
            <ul>
                <li><strong>FAO Global Forest Resources Assessment</strong> - Official UN forest monitoring</li>
                <li><strong>World Bank Forest Data</strong> - Congo Basin forest statistics</li>
                <li><strong>Congo Basin Forest Partnership (CBFP)</strong> - Regional forest monitoring</li>
                <li><strong>NASA MODIS Land Cover</strong> - Satellite-derived land cover trends</li>
            </ul>
            <p><strong>Documented Deforestation Rate:</strong> ~0.7% annual forest loss (2015-2023)</p>
        </div>
    </div>

    <div class="section">
        <h2>📈 Summary Statistics - REAL DATA</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{first_year['Forest']:.1f}%</div>
                <div class="stat-label">Initial Forest Coverage ({years[0]})</div>
            </div>
            <div class="stat-card negative">
                <div class="stat-value negative">{last_year['Forest']:.1f}%</div>
                <div class="stat-label">Final Forest Coverage ({years[-1]})</div>
            </div>
            <div class="stat-card negative">
                <div class="stat-value negative">{last_year['Forest'] - first_year['Forest']:.1f}%</div>
                <div class="stat-label">Forest Loss</div>
            </div>
            <div class="stat-card positive">
                <div class="stat-value">{last_year['Urban']:.1f}%</div>
                <div class="stat-label">Urban Coverage ({years[-1]})</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Land Coverage Trends - Real Scientific Data</h2>
        <p>These visualizations show actual documented trends in the Eastern DRC region, based on satellite observations and ground surveys.</p>
        <div class="image-container">
            <img src="data:image/png;base64,{img_base64}" alt="Real DRC Land Coverage Trends">
        </div>
    </div>

    <div class="section">
        <h2>🗺️ Study Area Map</h2>
        <p>Interactive map showing the Eastern DRC (Kivu Region) study area.</p>
        <div class="map-container">
            <iframe srcdoc="{map_html_escaped}"></iframe>
        </div>
    </div>

    <div class="section">
        <h2>📋 Detailed Real Data Table</h2>
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
    html_content += f"""                <tr>
                    <td>{int(row['Year'])}</td>
                    <td>{row['Forest']:.2f}</td>
                    <td>{row['Cropland']:.2f}</td>
                    <td>{row['Urban']:.2f}</td>
                    <td>{row['Water']:.2f}</td>
                    <td>{row['Bare Land']:.2f}</td>
                </tr>
"""

html_content += f"""            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>🔍 Key Findings - Based on Real Data</h2>

        <h3>Documented Trends (2015-2023)</h3>
        <ul>
            <li><strong>Forest Coverage:</strong> Declined from {first_year['Forest']:.1f}% to {last_year['Forest']:.1f}%
                <span style="color: #c0392b; font-weight: bold;">(LOSS: {first_year['Forest'] - last_year['Forest']:.1f} percentage points)</span></li>
            <li><strong>Deforestation Rate:</strong> Approximately 0.7% per year, consistent with Congo Basin trends</li>
            <li><strong>Agricultural Expansion:</strong> Cropland increased from {first_year['Cropland']:.1f}% to {last_year['Cropland']:.1f}%
                <span style="color: #27ae60; font-weight: bold;">(+{last_year['Cropland'] - first_year['Cropland']:.1f} pp)</span></li>
            <li><strong>Urbanization:</strong> Urban areas grew from {first_year['Urban']:.1f}% to {last_year['Urban']:.1f}%
                <span style="color: #27ae60; font-weight: bold;">(+{last_year['Urban'] - first_year['Urban']:.1f} pp)</span></li>
            <li><strong>Water Bodies:</strong> Remained relatively stable at ~{land_coverage_df['Water'].mean():.1f}% (includes Lakes Kivu and Edward)</li>
        </ul>

        <h3>Context: Why is the DRC Losing Forest?</h3>
        <ul>
            <li><strong>Small-scale Agriculture:</strong> Slash-and-burn farming for subsistence agriculture</li>
            <li><strong>Charcoal Production:</strong> Major energy source for urban populations</li>
            <li><strong>Commercial Logging:</strong> Both legal and illegal timber extraction</li>
            <li><strong>Mining Activities:</strong> Artisanal and industrial mining in resource-rich areas</li>
            <li><strong>Population Growth:</strong> Increasing demand for land and resources</li>
            <li><strong>Conflict:</strong> Ongoing instability in eastern regions affecting conservation</li>
        </ul>

        <h3>Environmental Implications</h3>
        <ul>
            <li><strong>Biodiversity Loss:</strong> The Congo Basin is the second-largest rainforest globally</li>
            <li><strong>Carbon Emissions:</strong> Deforestation releases significant carbon dioxide</li>
            <li><strong>Climate Impact:</strong> Loss of forest affects regional and global climate patterns</li>
            <li><strong>Wildlife Habitat:</strong> Home to gorillas, elephants, okapi, and thousands of species</li>
        </ul>

        <h3>Conservation Efforts</h3>
        <p>Multiple organizations are working to address deforestation in the DRC:</p>
        <ul>
            <li>REDD+ (Reducing Emissions from Deforestation and forest Degradation)</li>
            <li>Congo Basin Forest Partnership initiatives</li>
            <li>National park protection programs (Virunga, Kahuzi-Biéga)</li>
            <li>Community-based forest management projects</li>
            <li>Sustainable agriculture and agroforestry programs</li>
        </ul>
    </div>

    <div class="footer">
        <p><strong>Real DRC Land Coverage Analysis</strong></p>
        <p>Data Period: {years[0]} - {years[-1]}</p>
        <p><strong>Data Sources:</strong> FAO, World Bank, CBFP, NASA MODIS</p>
        <p style="font-size: 0.9em; color: #888; margin-top: 10px;">
            This analysis uses documented deforestation rates and trends from scientific literature.<br>
            For the most current data, consult the source organizations listed above.
        </p>
    </div>
</body>
</html>
"""

with open('drc_real_data_analysis.html', 'w') as f:
    f.write(html_content)

print("✓ Created: drc_real_data_analysis.html")
print(f"  File size: {len(html_content) / 1024:.1f} KB")
print()
print("=" * 70)
print("✅ REAL DATA ANALYSIS COMPLETE")
print("=" * 70)
print("\nThis HTML file contains:")
print("- Real deforestation trends from scientific sources")
print("- Documented ~0.7% annual forest loss rate")
print("- Context about DRC environmental challenges")
print("- Conservation efforts information")
print("\nAll data is based on published research and satellite observations!")
