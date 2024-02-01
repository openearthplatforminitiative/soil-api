// Get the value of the soil property at the queried location and depth
const response = await fetch(
  "$endpoint_url?" + new URLSearchParams({
        lon: "9.58", 
        lat: "60.1",
        depth: "0-5",
        property: "bdod"
  })
);
const json = await response.json();

// Get the soil property value, unit and name
const soilValue = json.properties.value
const soilUnit = json.properties.unit
const soilName = json.properties.property

console.log(`${soilName} value: ${soilValue} ${soilUnit}`);
