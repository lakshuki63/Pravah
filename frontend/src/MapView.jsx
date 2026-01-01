import {
  GoogleMap,
  DirectionsRenderer,
  Marker,
} from "@react-google-maps/api";
import { useState } from "react";

const containerStyle = {
  width: "100%",
  height: "70vh",
};

export default function MapView({ source, destination, onRouteLoaded }) {
  const [directions, setDirections] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [loading, setLoading] = useState(false);

  async function geocodeStop(name) {
    const geocoder = new window.google.maps.Geocoder();

    return new Promise((resolve) => {
      geocoder.geocode({ address: name }, (results, status) => {
        if (status === "OK" && results[0]) {
          resolve(results[0].geometry.location);
        } else {
          resolve(null);
        }
      });
    });
  }

  async function loadRoute() {
    if (!source || !destination) return;

    setLoading(true);
    setMarkers([]);

    // 1️⃣ Fetch route info
    const routeRes = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/route?source=${encodeURIComponent(
        source
      )}&destination=${encodeURIComponent(destination)}`
    );

    const routeData = await routeRes.json();

    // 2️⃣ Draw route
    const directionsService = new window.google.maps.DirectionsService();
    directionsService.route(
      {
        origin: source,
        destination,
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      async (result, status) => {
        if (status === "OK") {
          setDirections(result);
          onRouteLoaded(routeData);

          // 3️⃣ Fetch itinerary
          const itineraryRes = await fetch(
            `${import.meta.env.VITE_BACKEND_URL}/itinerary` +
              `?source=${source}` +
              `&destination=${destination}` +
              `&distance_text=${routeData.distance_text}` +
              `&duration_text=${routeData.duration_text}`
          );

          const itinerary = await itineraryRes.json();

          if (Array.isArray(itinerary)) {
            onRouteLoaded((prev) => ({ ...prev, itinerary }));

            // 4️⃣ Geocode & place markers
            const stopMarkers = [];
            for (let i = 0; i < itinerary.length; i++) {
              const loc = await geocodeStop(itinerary[i].name);
              if (loc) {
                stopMarkers.push({
                  position: loc,
                  label: String(i + 1),
                });
              }
            }

            setMarkers(stopMarkers);
          }
        }
        setLoading(false);
      }
    );
  }

  return (
    <>
      <button onClick={loadRoute} disabled={loading}>
        {loading ? "Loading…" : "Show Route"}
      </button>

      <GoogleMap
        mapContainerStyle={containerStyle}
        center={{ lat: 19, lng: 73 }}
        zoom={6}
      >
        {directions && <DirectionsRenderer directions={directions} />}
        {markers.map((m, i) => (
          <Marker key={i} position={m.position} label={m.label} />
        ))}
      </GoogleMap>
    </>
  );
}
