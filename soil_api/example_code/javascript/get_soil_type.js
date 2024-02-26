// Get the most probable soil type at the queried location
const response = await fetch(
  "$endpoint_url?" + new URLSearchParams({
    lon: "9.58",
    lat: "60.1",
  })
);
const json = await response.json();

// Get the most probable soil type
const mostProbableSoilType =
  json.properties.most_probable_soil_type;

console.log(`Most probable soil type: ${mostProbableSoilType}`);

// Get the most probable soil type at the queried location
// and the probability of the top 3 most probable soil types
const response_top_k = await fetch(
  "$endpoint_url?" + new URLSearchParams({
    lon: "9.58",
    lat: "60.1",
    top_k: "3"
  })
);
const json_top_k = await response.json();

// Get the soil type and probability for the second most probable soil type
const soilType2 =
  json.properties.probabilities[1].soil_type;
const probability2 =
  json.properties.probabilities[1].probability;

console.log(`Soil type: ${soilType2}, Probability: ${probability2}`);
