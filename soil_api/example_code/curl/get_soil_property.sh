# Get the mean value of the soil property at the queried location and depth
curl -i -X GET $endpoint_url?lon=9.58&lat=60.1&depths=0-5cm&depths=100-200cm&properties=bdod&values=mean

# Get the mean and the 0.05 quantile of the soil properties at the queried location and depths
curl -i -X GET $endpoint_url?lon=9.58&lat=60.1&depths=0-5cm&depths=100-200cm&properties=bdod&properties=phh2o&values=mean&values=Q0.05
