// Get a summary of the soil types in the queried bounding box, represented
// by a mapping of each soil type to the number of occurrences in the bounding box
const response = await fetch(
    "$endpoint_url?" + new URLSearchParams({
          min_lon: "9.5",
          max_lon: "9.6",
          min_lat: "60.1",
          max_lat: "60.12",
    })
  );
  const json = await response.json();
  
  // Get the summary of the soil types in the bounding box
  const summaryList =
    json.properties.summaries;

  // Get the soil type and the number of occurrences
  const soilType1 = summaryList[0].soil_type
  const count1 = summaryList[0].count
  const soilType2 = summaryList[1].soil_type
  const count2 = summaryList[1].count
  console.log(`Soil type: ${soilType1}, Count: ${count1}`);
  console.log(`Soil type: ${soilType2}, Count: ${count2}`);
  