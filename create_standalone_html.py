#!/usr/bin/env python3
"""
Create a fully self-contained HTML with embedded images
"""

import base64

# Read the PNG image and encode as base64
with open('land_coverage_trends.png', 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

# Read the map HTML
with open('study_area_map.html', 'r') as f:
    map_html = f.read()
    # Escape for embedding in iframe srcdoc
    map_html_escaped = map_html.replace('"', '&quot;').replace("'", '&#39;')

# Create standalone HTML
html_content = f"""<!DOCTYPE html>
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
            <span class="badge">📅 2015 - 2023</span>
            <span class="badge">📍 Sample Amazon Region</span>
            <span class="badge">📊 9 Time Periods</span>
        </div>
    </div>

    <div class="section">
        <h2>📈 Summary Statistics</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">64.8%</div>
                <div class="stat-label">Initial Forest Coverage (2015)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">53.4%</div>
                <div class="stat-label">Final Forest Coverage (2023)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">-11.4%</div>
                <div class="stat-label">Forest Change</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">11.4%</div>
                <div class="stat-label">Urban Coverage (2023)</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Land Coverage Trends</h2>
        <div class="image-container">
            <img src="data:image/png;base64,{img_base64}" alt="Land Coverage Trends">
        </div>
    </div>

    <div class="section">
        <h2>🗺️ Study Area Map</h2>
        <div class="map-container">
            <iframe srcdoc="{map_html_escaped}"></iframe>
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
                <tr>
                    <td>2015</td>
                    <td>64.78</td>
                    <td>20.11</td>
                    <td>4.92</td>
                    <td>7.25</td>
                    <td>2.93</td>
                </tr>
                <tr>
                    <td>2016</td>
                    <td>62.96</td>
                    <td>20.67</td>
                    <td>6.23</td>
                    <td>6.86</td>
                    <td>3.29</td>
                </tr>
                <tr>
                    <td>2017</td>
                    <td>62.39</td>
                    <td>21.31</td>
                    <td>6.53</td>
                    <td>6.68</td>
                    <td>3.09</td>
                </tr>
                <tr>
                    <td>2018</td>
                    <td>60.78</td>
                    <td>21.83</td>
                    <td>7.16</td>
                    <td>6.88</td>
                    <td>3.35</td>
                </tr>
                <tr>
                    <td>2019</td>
                    <td>59.56</td>
                    <td>21.96</td>
                    <td>8.11</td>
                    <td>6.70</td>
                    <td>3.68</td>
                </tr>
                <tr>
                    <td>2020</td>
                    <td>57.74</td>
                    <td>22.72</td>
                    <td>8.68</td>
                    <td>6.90</td>
                    <td>3.95</td>
                </tr>
                <tr>
                    <td>2021</td>
                    <td>55.59</td>
                    <td>22.95</td>
                    <td>10.33</td>
                    <td>6.77</td>
                    <td>4.36</td>
                </tr>
                <tr>
                    <td>2022</td>
                    <td>54.74</td>
                    <td>23.08</td>
                    <td>10.83</td>
                    <td>6.84</td>
                    <td>4.51</td>
                </tr>
                <tr>
                    <td>2023</td>
                    <td>53.36</td>
                    <td>23.95</td>
                    <td>11.45</td>
                    <td>6.94</td>
                    <td>4.30</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>🔍 Key Findings</h2>
        <ul>
            <li><strong>Forest Coverage:</strong> Declined from 64.8% to 53.4% (change of -11.4 percentage points)</li>
            <li><strong>Urban Expansion:</strong> Increased from 4.9% to 11.4% (change of 6.5 percentage points)</li>
            <li><strong>Agricultural Land:</strong> Cropland coverage changed from 20.1% to 23.9%</li>
            <li><strong>Water Bodies:</strong> Remained relatively stable at approximately 6.9%</li>
        </ul>
    </div>

    <div class="footer">
        <p><strong>Geospatial Land Coverage Analysis</strong></p>
        <p>Generated on 2026-01-10</p>
        <p>Data: Simulated for demonstration purposes</p>
    </div>
</body>
</html>
"""

with open('land_coverage_standalone.html', 'w') as f:
    f.write(html_content)

print("✓ Created land_coverage_standalone.html (fully self-contained)")
print(f"  File size: {len(html_content) / 1024:.1f} KB")
