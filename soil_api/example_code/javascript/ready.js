const response = await fetch(
  "$endpoint_url"
);
const json = await response.json();
const status = json.status;

console.log(`Status: ${status}`);
