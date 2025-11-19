import { useEffect, useRef, useState } from 'react';
import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api';
import { Button } from '@/components/ui/button';
import { ZoomIn, ZoomOut, Globe, MapPin } from 'lucide-react';

interface ThreatMapProps {
  latitude: number;
  longitude: number;
  threatScore: number;
  city?: string;
  country?: string;
  ipAddress: string;
}

const ThreatMap = ({ latitude, longitude, threatScore, city, country, ipAddress }: ThreatMapProps) => {
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [zoom, setZoom] = useState(8); // Start zoomed in on location
  const [hasMapError, setHasMapError] = useState(false);
  const hasZoomedRef = useRef(false);

  // Suppress Google Maps error dialogs
  useEffect(() => {
    // Add global CSS to hide error dialogs
    const style = document.createElement('style');
    style.innerHTML = `
      .gm-err-container,
      .gm-err-content,
      .gm-err-title,
      .gm-err-message,
      .dismissButton {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
      }
      div[style*="background-color: white"][style*="padding"] {
        display: none !important;
      }
    `;
    document.head.appendChild(style);

    // Override console.error to suppress Google Maps errors
    const originalError = console.error;
    console.error = (...args) => {
      const errorMessage = args[0]?.toString() || '';
      if (
        errorMessage.includes('Google Maps') ||
        errorMessage.includes('InvalidKeyMapError') ||
        errorMessage.includes('MissingKeyMapError')
      ) {
        setHasMapError(true);
        return; // Suppress the error
      }
      originalError.apply(console, args);
    };

    return () => {
      console.error = originalError;
      document.head.removeChild(style);
    };
  }, []);

  const { isLoaded, loadError } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '',
  });

  const mapContainerStyle = {
    width: '100%',
    height: '100%',
  };

  const locationCenter = {
    lat: latitude,
    lng: longitude,
  };

  // Get pin color based on threat score
  const getPinColor = () => {
    if (threatScore >= 70) return 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
    if (threatScore >= 40) return 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png';
    return 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
  };

  // Ensure map stays centered on location
  useEffect(() => {
    if (map && !hasZoomedRef.current) {
      hasZoomedRef.current = true;
      // Ensure the map is centered on the location
      map.panTo(locationCenter);
      map.setZoom(8);
    }
  }, [map, locationCenter]);

  const handleZoomIn = () => {
    if (map) {
      const newZoom = Math.min((map.getZoom() || zoom) + 1, 20);
      map.setZoom(newZoom);
      setZoom(newZoom);
    }
  };

  const handleZoomOut = () => {
    if (map) {
      const newZoom = Math.max((map.getZoom() || zoom) - 1, 1);
      map.setZoom(newZoom);
      setZoom(newZoom);
    }
  };

  const handleResetView = () => {
    if (map) {
      map.panTo(locationCenter);
      map.setZoom(8);
      setZoom(8);
    }
  };

  const onLoad = (map: google.maps.Map) => {
    setMap(map);
    
    // Listen for map errors
    map.addListener('error', () => {
      setHasMapError(true);
    });
  };

  const onUnmount = () => {
    setMap(null);
  };

  // Show clean error UI if there's a map error or load error
  if (loadError || hasMapError) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-slate-900/40 to-slate-800/40 p-6">
        <div className="text-center space-y-4 max-w-md">
          <MapPin className="h-16 w-16 mx-auto opacity-30 text-amber-400" />
          <div className="space-y-2">
            <p className="text-sm font-semibold text-foreground">Google Maps API Issue</p>
            <p className="text-xs text-muted-foreground leading-relaxed">
              The Google Maps API key is configured but cannot load the map.
              <br /><br />
              <strong>Common fixes:</strong>
              <br />1. Enable "Maps JavaScript API" in{' '}
              <a 
                href="https://console.cloud.google.com/apis/library/maps-backend.googleapis.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                Google Cloud Console
              </a>
              <br />2. Remove API key restrictions (or add localhost)
              <br />3. Wait a few minutes for new keys to activate
              <br />4. Check billing is enabled (required for Google Maps)
            </p>
            <p className="text-xs text-amber-500 mt-3">
              Location: {city || 'Unknown'}, {country || 'Unknown'}<br />
              Coordinates: {latitude.toFixed(4)}°, {longitude.toFixed(4)}°
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center space-y-3">
          <Globe className="h-12 w-12 text-primary mx-auto animate-pulse" />
          <p className="text-sm text-muted-foreground">Loading map...</p>
        </div>
      </div>
    );
  }

  const mapOptions: google.maps.MapOptions = {
    disableDefaultUI: true,
    zoomControl: false,
    mapTypeControl: false,
    scaleControl: false,
    streetViewControl: false,
    rotateControl: false,
    fullscreenControl: false,
    styles: [
      {
        featureType: 'all',
        elementType: 'geometry',
        stylers: [{ color: '#1e293b' }],
      },
      {
        featureType: 'all',
        elementType: 'labels.text.fill',
        stylers: [{ color: '#94a3b8' }],
      },
      {
        featureType: 'all',
        elementType: 'labels.text.stroke',
        stylers: [{ color: '#0f172a' }],
      },
      {
        featureType: 'water',
        elementType: 'geometry',
        stylers: [{ color: '#0f172a' }],
      },
      {
        featureType: 'landscape',
        elementType: 'geometry',
        stylers: [{ color: '#334155' }],
      },
      {
        featureType: 'road',
        elementType: 'geometry',
        stylers: [{ color: '#475569' }],
      },
      {
        featureType: 'poi',
        elementType: 'geometry',
        stylers: [{ color: '#1e293b' }],
      },
    ],
  };

  return (
    <>
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={locationCenter}
        zoom={zoom}
        onLoad={onLoad}
        onUnmount={onUnmount}
        options={mapOptions}
      >
        <Marker
          position={locationCenter}
          icon={{
            url: getPinColor(),
            scaledSize: new google.maps.Size(40, 40),
          }}
          animation={google.maps.Animation.DROP}
          title={`${city || 'Unknown'}, ${country || 'Unknown'}\n${ipAddress}`}
        />
      </GoogleMap>

      {/* Zoom Controls */}
      <div className="absolute top-4 right-4 flex flex-col gap-2 z-10">
        <Button
          size="sm"
          variant="secondary"
          className="h-9 w-9 p-0 bg-background/90 backdrop-blur-sm hover:bg-background border border-border shadow-lg"
          onClick={handleZoomIn}
        >
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="secondary"
          className="h-9 w-9 p-0 bg-background/90 backdrop-blur-sm hover:bg-background border border-border shadow-lg"
          onClick={handleZoomOut}
        >
          <ZoomOut className="h-4 w-4" />
        </Button>
        <div className="h-px bg-border my-1"></div>
        <Button
          size="sm"
          variant="secondary"
          className="h-9 w-9 p-0 bg-background/90 backdrop-blur-sm hover:bg-background border border-border shadow-lg"
          onClick={handleResetView}
          title="Reset to location"
        >
          <Globe className="h-4 w-4" />
        </Button>
      </div>

      {/* Zoom level indicator */}
      <div className="absolute top-4 left-4 bg-background/90 backdrop-blur-sm px-3 py-1.5 rounded-md border border-border text-xs font-medium text-muted-foreground shadow-lg z-10">
        {zoom}x
      </div>

      {/* Location Info Overlay */}
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-background/95 via-background/90 to-transparent backdrop-blur-sm p-4 border-t border-border/50 z-10">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 flex-1">
            <div
              className={`p-2 rounded-lg ${
                threatScore >= 70
                  ? 'bg-red-500/20'
                  : threatScore >= 40
                  ? 'bg-orange-500/20'
                  : 'bg-green-500/20'
              }`}
            >
              <MapPin
                className={`h-5 w-5 ${
                  threatScore >= 70
                    ? 'text-red-500'
                    : threatScore >= 40
                    ? 'text-orange-500'
                    : 'text-green-500'
                }`}
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-0.5">
                <span className="text-sm font-semibold text-foreground truncate">
                  {city && country ? `${city}, ${country}` : country || 'Unknown Location'}
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs text-muted-foreground">
                <span className="font-mono">
                  {latitude.toFixed(4)}°, {longitude.toFixed(4)}°
                </span>
                <span className="flex items-center gap-1">
                  <Globe className="h-3 w-3" />
                  {ipAddress}
                </span>
              </div>
            </div>
          </div>

          {/* Risk Badge */}
          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap border ${
              threatScore >= 70
                ? 'bg-red-500/15 text-red-600 dark:text-red-400 border-red-500/30'
                : threatScore >= 40
                ? 'bg-orange-500/15 text-orange-600 dark:text-orange-400 border-orange-500/30'
                : 'bg-green-500/15 text-green-600 dark:text-green-400 border-green-500/30'
            }`}
          >
            <div
              className={`h-2 w-2 rounded-full ${
                threatScore >= 70
                  ? 'bg-red-500 animate-pulse'
                  : threatScore >= 40
                  ? 'bg-orange-500'
                  : 'bg-green-500'
              }`}
            />
            {threatScore >= 70 ? 'High Risk' : threatScore >= 40 ? 'Moderate' : 'Safe'}
          </div>
        </div>
      </div>
    </>
  );
};

export default ThreatMap;
