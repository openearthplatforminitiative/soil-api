const response = await fetch(
  "$endpoint_url"
);
const json = await response.json();
const message = json.message;

console.log(`Message: ${message}`);
