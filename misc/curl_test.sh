#curl -i -H "Accept: application/json" -X POST -d "path=/AuthenticationSource/EXAMPLE.COM%20AD" http://localhost:8000/api/AuthenticationSources

#curl -i --user admin:1 -H "Accept: application/json" -X GET http://localhost:8000/api/Devices/Servers?format=ext-json
curl -i --user acme_user:1 -H "Accept: application/json" -X GET http://localhost:8000/api/Devices/Servers/SERVER01?format=xml
#curl -i --user acme_user:1 -X GET http://localhost:8000/api/Devices/Servers?format=ext-json
