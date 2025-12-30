import { useState } from "react";
import MapView from "./MapView";
import "./App.css";

export default function App() {
  const [source, setSource] = useState("Bhandara");
  const [destination, setDestination] = useState("Mumbai");
  const [routeInfo, setRouteInfo] = useState(null);

  return (
    <div className="app-container">
      <h2 className="app-title">AI Travel Planner</h2>

      {/* Input Section */}
      <div className="input-row">
        <input
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Source"
        />
        <input
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="Destination"
        />
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
                  {stop.recommended_stop_time}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
