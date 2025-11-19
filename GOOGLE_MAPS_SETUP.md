# Google Maps Integration Guide

## 🗺️ Google Maps API Setup

The frontend now uses **Google Maps** to display IP geolocation with interactive controls.

## 📋 Prerequisites

1. **Google Cloud Account**: You need a Google Cloud account
2. **Google Maps API Key**: Required for map functionality

## 🔑 Getting Your Google Maps API Key

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a Project** → **New Project**
3. Enter project name (e.g., "TICE Threat Intelligence")
4. Click **Create**

### Step 2: Enable Google Maps JavaScript API
1. In the Cloud Console, go to **APIs & Services** → **Library**
2. Search for **"Maps JavaScript API"**
3. Click on it and press **Enable**

### Step 3: Create API Key
1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Your API key will be created and displayed
4. **Important**: Click **Restrict Key** to secure it

### Step 4: Restrict API Key (Recommended)
1. Under **Application restrictions**:
   - Select **HTTP referrers (web sites)**
   - Add: `http://localhost:8080/*` (for development)
   - Add: `http://localhost:*` (for flexibility)
   
2. Under **API restrictions**:
   - Select **Restrict key**
   - Choose: **Maps JavaScript API**
   
3. Click **Save**

## ⚙️ Configuration

### Add API Key to Frontend

1. **Open the `.env` file** in `frontend/frontendhackathon-master/.env`

2. **Replace the placeholder** with your actual API key:
   ```env
   VITE_GOOGLE_MAPS_API_KEY=AIzaSyBXqKXZ9Z8Q8_4Yh4xYZ9Z8Q8_4Yh4xYZ8
   ```
   
   Example with real key:
   ```env
   VITE_GOOGLE_MAPS_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
   ```

3. **Save the file**

4. **Restart the development server**:
   ```powershell
   cd frontend\frontendhackathon-master
   npm run dev
   ```

## 🎨 Features Implemented

### 1. **Real Google Maps Integration**
- Actual satellite/street map view
- Pan and zoom controls
- Smooth animations

### 2. **Automatic Zoom Animation**
- Starts with world view (zoom level 2)
- Automatically zooms to location (zoom level 8)
- Smooth 200ms incremental zoom

### 3. **Color-Coded Markers**
- **Red marker**: High risk (score ≥70)
- **Orange marker**: Moderate risk (score 40-69)
- **Green marker**: Safe (score <40)

### 4. **Custom Dark Theme**
- Matches the app's dark aesthetic
- Custom styled map (slate/dark blue tones)
- Better visibility in dark mode

### 5. **Interactive Controls**
- **Zoom In** button (+)
- **Zoom Out** button (-)
- **Reset** button (globe icon - returns to world view)
- **Zoom level indicator** (shows current zoom)

### 6. **Location Info Overlay**
- City, Country
- Coordinates (latitude, longitude)
- IP address
- Risk badge (color-coded)

## 🧪 Testing the Integration

### Test with Different IPs

1. **Malicious IP** (China APT):
   ```
   IP: 1.13.197.76
   Expected: Red marker in Nanjing, China
   Zoom: Auto-zoom to location
   ```

2. **Safe IP** (Google DNS):
   ```
   IP: 8.8.8.8
   Expected: Green marker in Mountain View, USA
   Zoom: Auto-zoom to location
   ```

3. **Suspicious IP**:
   ```
   IP: 45.142.212.61
   Expected: Orange/Red marker in Moldova
   Zoom: Auto-zoom to location
   ```

### Expected Behavior

1. **Before Analysis**: Shows empty state with "Ready to Map Threats"
2. **Click Analyze**: Map loads, shows world view
3. **After 1 second**: Map pans to location
4. **Zoom Animation**: Incrementally zooms from level 2 to 8
5. **Marker Drops**: Color-coded pin drops on location
6. **Info Panel**: Shows location details at bottom

## 🔧 Troubleshooting

### Map Not Loading

**Issue**: Map shows "Unable to load map"

**Solutions**:
1. Check if API key is set in `.env` file
2. Verify API key is correct (no extra spaces)
3. Ensure Maps JavaScript API is enabled in Google Cloud
4. Check browser console for specific error messages

### API Key Errors

**Issue**: Console shows "RefererNotAllowedMapError"

**Solution**:
1. Go to Google Cloud Console → Credentials
2. Edit your API key
3. Under "Application restrictions", add `http://localhost:8080/*`
4. Save and wait 1-2 minutes for changes to propagate

**Issue**: Console shows "ApiNotActivatedMapError"

**Solution**:
1. Go to Google Cloud Console → APIs & Services → Library
2. Search for "Maps JavaScript API"
3. Click and press "Enable"

### Map Loads But No Marker

**Issue**: Map loads but location pin doesn't appear

**Possible Causes**:
1. Backend not returning geolocation data
2. Invalid lat/long coordinates
3. Check browser console for errors

**Solution**:
1. Verify backend API is returning `geolocation` object with `latitude` and `longitude`
2. Check backend logs for geolocation API errors

### Zoom Animation Not Working

**Issue**: Map shows location but doesn't zoom smoothly

**This is expected if**:
- You manually interacted with map before animation completed
- Browser performance is slow

**To Reset**: Click the Globe (reset) button in controls

## 💰 Pricing Information

### Google Maps Free Tier
- **$200 free credit per month**
- **28,000 free map loads per month** (dynamic maps)
- Most development/demo usage stays within free tier

### Usage Estimates
- Each IP analysis = 1 map load
- 28,000 map loads = ~900 analyses per day
- Development testing: Well within free limits

### Monitor Usage
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Billing** → **Reports**
3. Filter by **Maps JavaScript API**
4. View daily/monthly usage

## 📦 Installed Packages

```json
{
  "@react-google-maps/api": "^2.19.3"
}
```

## 🔐 Security Best Practices

1. ✅ **Never commit `.env` file to Git**
2. ✅ **Restrict API key** to specific domains
3. ✅ **Restrict API key** to only Maps JavaScript API
4. ✅ **Monitor usage** regularly
5. ✅ **Rotate keys** if exposed

## 🎯 Next Steps (Optional Enhancements)

### Additional Features You Can Add:

1. **Street View Integration**
   - Show street view of IP location
   - Toggle between map and street view

2. **Heatmap Layer**
   - Show threat density globally
   - Color-code regions by risk

3. **Multiple Markers**
   - Show multiple IPs on same map
   - Compare locations visually

4. **Custom Map Styles**
   - Different themes (satellite, terrain, hybrid)
   - Toggle map types

5. **Drawing Tools**
   - Draw circles/polygons around regions
   - Measure distances between IPs

6. **Info Windows**
   - Click marker to show detailed popup
   - Show full threat intelligence in popup

## 📚 Resources

- [Google Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript)
- [@react-google-maps/api Documentation](https://react-google-maps-api-docs.netlify.app/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Maps API Pricing](https://mapsplatform.google.com/pricing/)

## ✅ Summary

Your frontend now has a **professional Google Maps integration** that:
- Shows real satellite/street maps
- Automatically zooms to IP locations
- Color-codes markers by threat level
- Provides smooth animations and controls
- Matches your dark theme aesthetic

**Refresh your browser and analyze an IP to see Google Maps in action!** 🌍✨
