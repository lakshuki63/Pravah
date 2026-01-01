import { Autocomplete } from "@react-google-maps/api";
import { useRef } from "react";

export default function PlaceAutocomplete({ placeholder, onSelect }) {
  const ref = useRef(null);

  return (
    <Autocomplete
      onLoad={(auto) => (ref.current = auto)}
      onPlaceChanged={() => {
        const place = ref.current.getPlace();
        if (place?.formatted_address) {
          onSelect(place.formatted_address);
        }
      }}
    >
      <input placeholder={placeholder} />
    </Autocomplete>
  );
}
