#!/usr/bin/env python3
"""
Create a fully self-contained HTML with embedded images and code blocks
Includes toggle functionality to show/hide code
"""

import base64
import numpy as np
import pandas as pd

# Read the PNG image and encode as base64
with open('land_coverage_trends.png', 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

# Read the map HTML
with open('study_area_map.html', 'r') as f:
    map_html = f.read()
    # Escape for embedding in iframe srcdoc
    map_html_escaped = map_html.replace('"', '&quot;').replace("'", '&#39;')

# Generate the data for code blocks
np.random.seed(42)
time_periods = pd.date_range(start='2015-01-01', end='2024-01-01', freq='Y')
years = [str(date.year) for date in time_periods]

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

# Create standalone HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Geospatial Land Coverage Analysis - DRC</title>
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
        h3 {{
            color: #555;
            margin-top: 20px;
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

        /* Code block styles */
        .code-block-container {{
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .code-toggle {{
            background-color: #f8f9fa;
            padding: 10px 15px;
            cursor: pointer;
            user-select: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #ddd;
        }}
        .code-toggle:hover {{
            background-color: #e9ecef;
        }}
        .code-toggle-text {{
            font-weight: 600;
            color: #495057;
        }}
        .code-toggle-icon {{
            font-family: monospace;
            font-size: 1.2em;
            color: #667eea;
        }}
        .code-content {{
            display: none;
            background-color: #282c34;
            padding: 20px;
            overflow-x: auto;
        }}
        .code-content.show {{
            display: block;
        }}
        .code-content pre {{
            margin: 0;
            color: #abb2bf;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        .code-keyword {{
            color: #c678dd;
        }}
        .code-string {{
            color: #98c379;
        }}
        .code-comment {{
            color: #5c6370;
            font-style: italic;
        }}
        .code-number {{
            color: #d19a66;
        }}
        .code-function {{
            color: #61afef;
        }}
        .global-toggle {{
            text-align: right;
            margin-bottom: 20px;
        }}
        .global-toggle button {{
            background-color: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
        }}
        .global-toggle button:hover {{
            background-color: #5568d3;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Geospatial Land Coverage Analysis</h1>
        <div class="subtitle">Time Series Analysis of Land Use Changes - Democratic Republic of Congo</div>
        <div style="margin-top: 15px;">
            <span class="badge">📅 {years[0]} - {years[-1]}</span>
            <span class="badge">📍 Eastern DRC (Kivu Region)</span>
            <span class="badge">📊 {len(years)} Time Periods</span>
        </div>
    </div>

    <div class="global-toggle">
        <button onclick="toggleAllCode()">Toggle All Code Blocks</button>
    </div>

    <div class="section">
        <h2>📖 Introduction</h2>
        <p>This analysis examines land coverage changes in the Democratic Republic of Congo, specifically focusing on the eastern Kivu region. This area has experienced significant environmental changes due to various factors including agriculture expansion, urbanization, and resource extraction.</p>

        <h3>Study Area Details</h3>
        <ul>
            <li><strong>Region:</strong> Eastern DRC (Kivu Region)</li>
            <li><strong>Coordinates:</strong> Latitude -1.0° to -3.0°, Longitude 27.5° to 29.5°</li>
            <li><strong>Area Coverage:</strong> Approximately 40,000 km²</li>
            <li><strong>Time Period:</strong> {years[0]} - {years[-1]}</li>
        </ul>

        <div class="code-block-container">
            <div class="code-toggle" onclick="toggleCode(this)">
                <span class="code-toggle-text">📄 Study Area Configuration</span>
                <span class="code-toggle-icon">▶</span>
            </div>
            <div class="code-content">
                <pre><span class="code-comment"># Define study area (Eastern DRC - Kivu region)</span>
<span class="code-keyword">study_area</span> = {{
    <span class="code-string">'name'</span>: <span class="code-string">'Eastern DRC (Kivu Region)'</span>,
    <span class="code-string">'bbox'</span>: {{
        <span class="code-string">'north'</span>: <span class="code-number">-1.0</span>,
        <span class="code-string">'south'</span>: <span class="code-number">-3.0</span>,
        <span class="code-string">'east'</span>: <span class="code-number">29.5</span>,
        <span class="code-string">'west'</span>: <span class="code-number">27.5</span>
    }},
    <span class="code-string">'center'</span>: [<span class="code-number">-2.0</span>, <span class="code-number">28.5</span>]
}}</pre>
            </div>
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

        <div class="code-block-container">
            <div class="code-toggle" onclick="toggleCode(this)">
                <span class="code-toggle-text">📄 Data Generation Function</span>
                <span class="code-toggle-icon">▶</span>
            </div>
            <div class="code-content">
                <pre><span class="code-keyword">def</span> <span class="code-function">generate_land_coverage_data</span>(years, simulate_deforestation=<span class="code-keyword">True</span>):
    <span class="code-comment">\"\"\"Generate simulated land coverage data showing realistic trends\"\"\"</span>
    data = []

    <span class="code-comment"># Initial percentages (sum to 100)</span>
    initial_forest = <span class="code-number">65.0</span>
    initial_cropland = <span class="code-number">20.0</span>
    initial_urban = <span class="code-number">5.0</span>
    initial_water = <span class="code-number">7.0</span>
    initial_bare = <span class="code-number">3.0</span>

    <span class="code-keyword">for</span> i, year <span class="code-keyword">in</span> <span class="code-function">enumerate</span>(years):
        <span class="code-keyword">if</span> simulate_deforestation:
            forest = initial_forest - (i * <span class="code-number">1.5</span>) + np.random.normal(<span class="code-number">0</span>, <span class="code-number">0.5</span>)
            urban = initial_urban + (i * <span class="code-number">0.8</span>) + np.random.normal(<span class="code-number">0</span>, <span class="code-number">0.3</span>)
            cropland = initial_cropland + (i * <span class="code-number">0.5</span>) + np.random.normal(<span class="code-number">0</span>, <span class="code-number">0.4</span>)
            <span class="code-comment"># ... normalize and return DataFrame</span>

    <span class="code-keyword">return</span> pd.DataFrame(data)</pre>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Land Coverage Trends</h2>
        <p>The visualizations below show the evolution of land coverage across different categories over the study period.</p>
        <div class="image-container">
            <img src="data:image/png;base64,{img_base64}" alt="Land Coverage Trends">
        </div>

        <div class="code-block-container">
            <div class="code-toggle" onclick="toggleCode(this)">
                <span class="code-toggle-text">📄 Visualization Code</span>
                <span class="code-toggle-icon">▶</span>
            </div>
            <div class="code-content">
                <pre><span class="code-keyword">import</span> matplotlib.pyplot <span class="code-keyword">as</span> plt

categories = [<span class="code-string">'Forest'</span>, <span class="code-string">'Cropland'</span>, <span class="code-string">'Urban'</span>, <span class="code-string">'Water'</span>, <span class="code-string">'Bare Land'</span>]
colors = [<span class="code-string">'#2d5f2e'</span>, <span class="code-string">'#f4a460'</span>, <span class="code-string">'#8b0000'</span>, <span class="code-string">'#4682b4'</span>, <span class="code-string">'#daa520'</span>]

fig, axes = plt.subplots(<span class="code-number">2</span>, <span class="code-number">1</span>, figsize=(<span class="code-number">12</span>, <span class="code-number">10</span>))

<span class="code-comment"># Stacked area chart</span>
axes[<span class="code-number">0</span>].stackplot(land_coverage_df[<span class="code-string">'Year'</span>],
                  land_coverage_df[<span class="code-string">'Forest'</span>],
                  land_coverage_df[<span class="code-string">'Cropland'</span>],
                  land_coverage_df[<span class="code-string">'Urban'</span>],
                  land_coverage_df[<span class="code-string">'Water'</span>],
                  land_coverage_df[<span class="code-string">'Bare Land'</span>],
                  labels=categories, colors=colors, alpha=<span class="code-number">0.8</span>)

<span class="code-comment"># Individual trend lines</span>
<span class="code-keyword">for</span> category, color <span class="code-keyword">in</span> <span class="code-function">zip</span>(categories, colors):
    axes[<span class="code-number">1</span>].plot(land_coverage_df[<span class="code-string">'Year'</span>], land_coverage_df[category],
                 marker=<span class="code-string">'o'</span>, label=category, color=color, linewidth=<span class="code-number">2</span>)</pre>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🗺️ Study Area Map</h2>
        <p>Interactive map showing the location of the study area in the Democratic Republic of Congo.</p>
        <div class="map-container">
            <iframe srcdoc="{map_html_escaped}"></iframe>
        </div>

        <div class="code-block-container">
            <div class="code-toggle" onclick="toggleCode(this)">
                <span class="code-toggle-text">📄 Map Generation Code</span>
                <span class="code-toggle-icon">▶</span>
            </div>
            <div class="code-content">
                <pre><span class="code-keyword">import</span> folium

<span class="code-comment"># Create an interactive map</span>
m = folium.Map(
    location=study_area[<span class="code-string">'center'</span>],
    zoom_start=<span class="code-number">8</span>,
    tiles=<span class="code-string">'OpenStreetMap'</span>
)

<span class="code-comment"># Add study area boundary</span>
folium.Rectangle(
    bounds=[
        [study_area[<span class="code-string">'bbox'</span>][<span class="code-string">'south'</span>], study_area[<span class="code-string">'bbox'</span>][<span class="code-string">'west'</span>]],
        [study_area[<span class="code-string">'bbox'</span>][<span class="code-string">'north'</span>], study_area[<span class="code-string">'bbox'</span>][<span class="code-string">'east'</span>]]
    ],
    color=<span class="code-string">'red'</span>,
    fill=<span class="code-keyword">True</span>,
    fillOpacity=<span class="code-number">0.2</span>,
    popup=<span class="code-string">f"Study Area: {{study_area['name']}}"</span>
).add_to(m)</pre>
            </div>
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
    html_content += f"""                <tr>
                    <td>{row['Year']}</td>
                    <td>{row['Forest']:.2f}</td>
                    <td>{row['Cropland']:.2f}</td>
                    <td>{row['Urban']:.2f}</td>
                    <td>{row['Water']:.2f}</td>
                    <td>{row['Bare Land']:.2f}</td>
                </tr>
"""

html_content += f"""            </tbody>
        </table>

        <div class="code-block-container">
            <div class="code-toggle" onclick="toggleCode(this)">
                <span class="code-toggle-text">📄 Data Processing Code</span>
                <span class="code-toggle-icon">▶</span>
            </div>
            <div class="code-content">
                <pre><span class="code-keyword">import</span> pandas <span class="code-keyword">as</span> pd

<span class="code-comment"># Create DataFrame with land coverage data</span>
land_coverage_df = generate_land_coverage_data(years)

<span class="code-comment"># Display summary statistics</span>
<span class="code-function">print</span>(land_coverage_df.describe().round(<span class="code-number">2</span>))

<span class="code-comment"># Calculate year-over-year changes</span>
<span class="code-keyword">for</span> col <span class="code-keyword">in</span> categories:
    land_coverage_df[<span class="code-string">f'{{col}}_change'</span>] = land_coverage_df[col].diff()</pre>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🔍 Key Findings</h2>
        <ul>
            <li><strong>Forest Coverage:</strong> Declined from {land_coverage_df.iloc[0]['Forest']:.1f}% to {land_coverage_df.iloc[-1]['Forest']:.1f}% (change of {land_coverage_df.iloc[-1]['Forest'] - land_coverage_df.iloc[0]['Forest']:.1f} percentage points)</li>
            <li><strong>Urban Expansion:</strong> Increased from {land_coverage_df.iloc[0]['Urban']:.1f}% to {land_coverage_df.iloc[-1]['Urban']:.1f}% (change of {land_coverage_df.iloc[-1]['Urban'] - land_coverage_df.iloc[0]['Urban']:.1f} percentage points)</li>
            <li><strong>Agricultural Land:</strong> Cropland coverage changed from {land_coverage_df.iloc[0]['Cropland']:.1f}% to {land_coverage_df.iloc[-1]['Cropland']:.1f}%</li>
            <li><strong>Water Bodies:</strong> Remained relatively stable at approximately {land_coverage_df['Water'].mean():.1f}%</li>
        </ul>

        <h3>Implications for the DRC</h3>
        <p>The observed trends in the Eastern DRC region reflect broader environmental challenges:</p>
        <ul>
            <li><strong>Deforestation:</strong> The decline in forest coverage is consistent with documented deforestation in the Congo Basin, driven by agricultural expansion and logging.</li>
            <li><strong>Urbanization:</strong> Growing urban areas reflect population growth and migration patterns in the region.</li>
            <li><strong>Agricultural Pressure:</strong> Increasing cropland suggests rising food production needs and potential conflicts between conservation and development.</li>
            <li><strong>Conservation Needs:</strong> These trends highlight the importance of sustainable land management and conservation efforts in this biodiversity hotspot.</li>
        </ul>
    </div>

    <div class="footer">
        <p><strong>Geospatial Land Coverage Analysis - Democratic Republic of Congo</strong></p>
        <p>Generated on 2026-01-10</p>
        <p>Data: Simulated for demonstration purposes. For production use, integrate real satellite data from Google Earth Engine or ESA WorldCover.</p>
    </div>

    <script>
        function toggleCode(element) {{
            const content = element.nextElementSibling;
            const icon = element.querySelector('.code-toggle-icon');

            if (content.classList.contains('show')) {{
                content.classList.remove('show');
                icon.textContent = '▶';
            }} else {{
                content.classList.add('show');
                icon.textContent = '▼';
            }}
        }}

        function toggleAllCode() {{
            const allCodeBlocks = document.querySelectorAll('.code-content');
            const allIcons = document.querySelectorAll('.code-toggle-icon');
            const firstBlock = allCodeBlocks[0];

            // Check if first block is shown to determine action
            const shouldShow = !firstBlock.classList.contains('show');

            allCodeBlocks.forEach(block => {{
                if (shouldShow) {{
                    block.classList.add('show');
                }} else {{
                    block.classList.remove('show');
                }}
            }});

            allIcons.forEach(icon => {{
                icon.textContent = shouldShow ? '▼' : '▶';
            }});
        }}
    </script>
</body>
</html>
"""

with open('land_coverage_drc_with_code.html', 'w') as f:
    f.write(html_content)

print("✓ Created land_coverage_drc_with_code.html (fully self-contained with code blocks)")
print(f"  File size: {len(html_content) / 1024:.1f} KB")
print("\nFeatures:")
print("  - Study area: Eastern DRC (Kivu Region)")
print("  - Collapsible code blocks throughout")
print("  - Toggle all code button")
print("  - Syntax highlighting")
print("  - Embedded images and maps")
