import { useState } from "react";
import { useJsApiLoader, Autocomplete } from "@react-google-maps/api";
import MapView from "./MapView";
import "./App.css";

// 🔒 MUST be static (important for hooks)
const MAP_LIBRARIES = ["places"];

export default function App() {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries: MAP_LIBRARIES,
  });

  // Autocomplete instances
  const [sourceAuto, setSourceAuto] = useState(null);
  const [destAuto, setDestAuto] = useState(null);

  // Input values
  const [source, setSource] = useState(null);
  const [destination, setDestination] = useState(null);

  // Route + itinerary info
  const [routeInfo, setRouteInfo] = useState(null);

  // ⛔ Do NOT render anything until Maps is loaded
  if (!isLoaded) {
    return <p>Loading Google Maps…</p>;
  }

  return (
    <div className="app-container">
      <h2 className="app-title">AI Travel Planner</h2>

      {/* Input Section with Autocomplete */}
      <div className="input-row">
        <Autocomplete
          onLoad={(auto) => setSourceAuto(auto)}
          onPlaceChanged={() => {
            if (!sourceAuto) return;
            const place = sourceAuto.getPlace();
            if (place?.formatted_address) {
              setSource(place.formatted_address);
            }
          }}
        >
          <input
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Start location"
          />
        </Autocomplete>

        <Autocomplete
          onLoad={(auto) => setDestAuto(auto)}
          onPlaceChanged={() => {
            if (!destAuto) return;
            const place = destAuto.getPlace();
            if (place?.formatted_address) {
              setDestination(place.formatted_address);
            }
          }}
        >
          <input
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Destination"
          />
        </Autocomplete>
      </div>

      {/* Map Section */}
      <div className="map-card">
        <MapView
          source={source}
          destination={destination}
          onRouteLoaded={setRouteInfo}
        />
      </div>

      {/* Route Summary */}
      {routeInfo?.distance_text && (
        <div className="route-card">
          <h3>Route Info</h3>
          <p>
            <strong>Distance:</strong> {routeInfo.distance_text}
          </p>
          <p>
            <strong>Duration:</strong> {routeInfo.duration_text}
          </p>
        </div>
      )}

      {/* AI Itinerary Section */}
      {routeInfo?.itinerary && Array.isArray(routeInfo.itinerary) && (
        <div className="itinerary-section">
          <h3 className="section-title">AI-Recommended Stops</h3>

          <div className="itinerary-grid">
            {routeInfo.itinerary.map((stop, idx) => (
              <div key={idx} className="itinerary-card">
                <h4 className="stop-name">{stop.name}</h4>

                <p className="stop-category">
                  <strong>Category:</strong> {stop.category}
                </p>

                <p className="stop-reason">{stop.reason}</p>

                <p className="stop-time">
                  <strong>Recommended Stop:</strong>{" "}
                  {stop.recommended_stop_duration}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
