import { useState } from "react";
import { useJsApiLoader } from "@react-google-maps/api";
import MapView from "./MapView";
import PlaceAutocomplete from "./PlaceAutocomplete";
import "./App.css";

const MAP_LIBRARIES = ["places"];

export default function App() {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries: MAP_LIBRARIES,
  });

  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [routeInfo, setRouteInfo] = useState(null);

  if (!isLoaded) return <p>Loading Google Maps…</p>;

  return (
    <div className="app-container">
      <h2>PRAVAH</h2>

      <div className="input-row">
        <PlaceAutocomplete placeholder="Start location" onSelect={setSource} />
        <PlaceAutocomplete placeholder="Destination" onSelect={setDestination} />
      </div>

      <MapView
        source={source}
        destination={destination}
        onRouteLoaded={setRouteInfo}
      />

      {routeInfo?.distance_text && (
        <div className="route-card">
          <p><strong>Distance:</strong> {routeInfo.distance_text}</p>
          <p><strong>Duration:</strong> {routeInfo.duration_text}</p>
        </div>
      )}

      {Array.isArray(routeInfo?.itinerary) && (
        <div className="itinerary-section">
          <h3>Recommended Stops</h3>
          {routeInfo.itinerary.map((stop, idx) => (
            <div key={idx} className="itinerary-card">
              <h4>{stop.name}</h4>
              <p><strong>Category:</strong> {stop.category}</p>
              <p>{stop.reason}</p>
              <p><strong>Stop Time:</strong> {stop.recommended_stop_time}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
