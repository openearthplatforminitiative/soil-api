// Get the mean value of the soil property at the queried location and depth
const response = await fetch(
  "$endpoint_url?" + new URLSearchParams({
    lon: "9.58",
    lat: "60.1",
    depths: "0-5cm",
    properties: "bdod",
    values: "mean"
  })
);
const json = await response.json();

// Get the soil information for the bdod property
const bdod = json.properties.layers[0];

// Get the soil property unit and name
const bdodUnit = bdod.unit_measure.mapped_units
const bdodName = bdod.name

// Get the soil property mean value at depth 0-5cm
const bdodDepth = bdod.depths[0].label
const bdodValue = bdod.depths[0].values.mean

console.log(`Soil property: ${bdodName}, Depth: ${bdodDepth}, Value: ${bdodValue} ${bdodUnit}`);

// Get the mean and the 0.05 quantile of the soil properties at the queried location and depths
const response_multi = await fetch(
  "$endpoint_url?" + new URLSearchParams({
    lon: "9.58",
    lat: "60.1",
    depths: ['0-5cm', '100-200cm'],
    properties: ['bdod', 'phh2o'],
    values: ['mean', 'Q0.05']
  })
);
const json_multi = await response_multi.json();

// Get the soil information for the phh2o property
const phh2o = json_multi.properties.layers[1];

// Get the soil property value, unit and name
const phh2oUnit = phh2o.unit_measure.mapped_units;
const phh2oName = phh2o.name;

// Get the soil property 0.05 quantile value at depth 100-200cm
const phh2oDepth = phh2o.depths[1].label;
const phh2oValue = phh2o.depths[1].values['Q0.05'];

console.log(`Soil property: ${phh2oName}, Depth: ${phh2oDepth}, Value: ${phh2oValue} ${phh2oUnit}`);
