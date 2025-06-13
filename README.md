# SolarMan App ☀️ - Solar API Edition

This version of the SolarMan app integrates with the Google Solar API to provide real-time data on roof shading, azimuth, and optimal panel placement.

## Features:
- Geocode home address to lat/lon
- Query Solar API for solar potential
- Estimate system size, panel count, and bill offset
- Dynamic kWh-to-panel recommendation

## Setup:
Add the following keys to your Streamlit Secrets:

```toml
GOOGLE_MAPS_API_KEY = "your-maps-api-key"
GOOGLE_SOLAR_API_KEY = "your-solar-api-key"
```
