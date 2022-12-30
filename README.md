# Watcher
Simple Flask Application to display an influxDB of watched content (personal-influxdb)

Using content from https://github.com/psyciknz/personal-influxdb this displays moves and tv episode watched in a flask application.

First attempt at flask, so learning as I go.

# Setup

## Create a .env file with

```
INFLUX_HOST=[influx host]
INFLUX_PORT=8086
INFLUX_USER=[user]
INFLUX_PWD=[password]
INFLUX_DB=trakt
APP_SERVER_PORT=8080
```

Influx details should be relatively self explanatory.  APP Server port is the post flask listens top display pages.

Navigate to http://[server]:[APP_SERVER_PORT]
