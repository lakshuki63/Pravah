import { Marker } from "@react-google-maps/api";

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
  // 1️⃣ Call backend route API (for metrics + ETA)
  const routeRes = await fetch(
    `${import.meta.env.VITE_BACKEND_URL}/route?source=${source}&destination=${destination}`
  );
  const routeData = await routeRes.json();

  // 2️⃣ Draw Google route
  const directionsService = new window.google.maps.DirectionsService();

  directionsService.route(
    {
      origin: source,
      destination: destination,
      travelMode: window.google.maps.TravelMode.DRIVING,
    },
    async (result, status) => {
      if (status === "OK") {
        setDirections(result);
        onRouteLoaded(routeData);

        // 3️⃣ Call AI itinerary AFTER route success
        const itineraryRes = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/itinerary` +
            `?source=${source}` +
            `&destination=${destination}` +
            `&distance_text=${routeData.distance_text}` +
            `&duration_text=${routeData.duration_text}`
        );

        const itineraryJson = await itineraryRes.json();
        onRouteLoaded((prev) => ({
          ...prev,
          itinerary: itineraryJson,
        }));
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
