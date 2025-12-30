import { useState } from "react";
import MapView from "./MapView";

export default function App() {
  const [source, setSource] = useState("Bhandara");
  const [destination, setDestination] = useState("Mumbai");
  const [routeInfo, setRouteInfo] = useState(null);

  return (
    <div style={{ padding: 20 }}>
      <h2>AI Travel Planner</h2>

      <input value={source} onChange={(e) => setSource(e.target.value)} />
      <input
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
      />

      <MapView
        source={source}
        destination={destination}
        onRouteLoaded={setRouteInfo}
      />

      {routeInfo && (
        <div>
          <h3>Route Info</h3>
          <p>Distance: {routeInfo.distance_text}</p>
          <p>Duration: {routeInfo.duration_text}</p>
        </div>
      )}
    </div>
  );
}
