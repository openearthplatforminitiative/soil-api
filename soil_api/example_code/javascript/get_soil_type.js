// Get the soil type at the queried location
const response = await fetch(
  "$endpoint_url?" + new URLSearchParams({
        lon: "9.58", 
        lat: "60.1",
  })
);
const json = await response.json();

// Get the soil type
const soilType =
  json.properties.soil_type;

console.log(`Soil type: ${soilType}`);
