import {
  GoogleMap,
  DirectionsRenderer,
  useJsApiLoader,
} from "@react-google-maps/api";
import { useState } from "react";

const containerStyle = {
  width: "100%",
  height: "70vh",
};

export default function MapView({ source, destination, onRouteLoaded }) {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  });

  const [directions, setDirections] = useState(null);

  async function loadRoute() {
    // 1️⃣ Call backend (Datadog metrics fire here)
    const res = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/route?source=${source}&destination=${destination}`
    );
    const routeData = await res.json();

    // 2️⃣ Draw route on map
    const directionsService = new window.google.maps.DirectionsService();

    directionsService.route(
      {
        origin: source,
        destination: destination,
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === "OK") {
          setDirections(result);
          onRouteLoaded(routeData); // pass data up
        }
      }
    );
  }

  if (!isLoaded) return <p>Loading map…</p>;

  return (
    <>
      <button onClick={loadRoute}>Show Route</button>

      <GoogleMap
        mapContainerStyle={containerStyle}
        center={{ lat: 19, lng: 73 }}
        zoom={6}
      >
        {directions && <DirectionsRenderer directions={directions} />}
      </GoogleMap>
    </>
  );
}
