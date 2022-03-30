Prueba con Flask\
Georreferenciación basada en geojson e inserción de registros en base de datos con autenticación básica.

Endpoint de prueba:
```
    http://localhost:4041/
```

Credenciales:
```
    username: bryan, password: Prueba_Flask_4
```

* Métodos disponibles

| tipo de consulta | endpoint | parámetros | autenticación |
| -- | -- | -- | -- |
| POST | localhost:4040/task | { "name": "bryan" ,"age": 28 } | SI |
| POST | localhost:4040/locateMultipleCoordinates | [{"latitude": -12.046867,"longitude": -76.978432},{"latitude": -12.000545,"longitude": -76.838423},{"latitude":-11.979800,"longitude": -77.059543}] | SI |
| POST | localhost:4040/locate | {"latitude":-11.979800,"longitude": -77.059543} | SI |
| POST | localhost:4040/createMultipleUser | [{"username": "test123", "age": 28, "salary": 5000.2}] | SI |
| POST | localhost:4040/createUser | {"username": "test1234", "age": 29, "salary": 5001.2} | SI |


