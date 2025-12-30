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

  function placeMarkersUsingSteps(directionsResult, stops) {
    const steps = directionsResult.routes[0].legs[0].steps;
    const path = directionsResult.routes[0].overview_path;

    const generatedMarkers = [];
    const pathChunk = Math.floor(path.length / (stops.length + 1));

    stops.forEach((stop, idx) => {
      const stopName = stop.name.toLowerCase();

      const matchedStep = steps.find((step) =>
        step.instructions
          .replace(/<[^>]+>/g, "")
          .toLowerCase()
          .includes(stopName.split(" ")[0])
      );

      if (matchedStep) {
        generatedMarkers.push({
          position: {
            lat: matchedStep.end_location.lat(),
            lng: matchedStep.end_location.lng(),
          },
          label: String(idx + 1),
        });
      } else {
        const fallbackPoint = path[pathChunk * (idx + 1)];
        if (fallbackPoint) {
          generatedMarkers.push({
            position: {
              lat: fallbackPoint.lat(),
              lng: fallbackPoint.lng(),
            },
            label: String(idx + 1),
          });
        }
      }
    });

    setMarkers(generatedMarkers);
  }

  async function loadRoute() {
    // 1️⃣ Fetch backend route (distance + duration)
    const routeRes = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/route?source=${source}&destination=${destination}`
    );
    const routeData = await routeRes.json();

    // 2️⃣ Draw route on map
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

          // 3️⃣ Fetch AI itinerary
          const itineraryRes = await fetch(
            `${import.meta.env.VITE_BACKEND_URL}/itinerary` +
              `?source=${source}` +
              `&destination=${destination}` +
              `&distance_text=${routeData.distance_text}` +
              `&duration_text=${routeData.duration_text}`
          );

          const itineraryResponse = await itineraryRes.json();
          const itinerary = itineraryResponse.itinerary ?? itineraryResponse;

          if (Array.isArray(itinerary)) {
            onRouteLoaded((prev) => ({
              ...prev,
              itinerary,
            }));
            placeMarkersUsingSteps(result, itinerary);
          }
        }
      }
    );
  }

  return (
    <>
      <button onClick={loadRoute}>Show Route</button>

      <GoogleMap
        mapContainerStyle={containerStyle}
        center={{ lat: 19, lng: 73 }}
        zoom={6}
      >
        {directions && <DirectionsRenderer directions={directions} />}
        {markers.map((m, idx) => (
          <Marker key={idx} position={m.position} label={m.label} />
        ))}
      </GoogleMap>
    </>
  );
}
