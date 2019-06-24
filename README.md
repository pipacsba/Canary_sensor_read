# Canary_sensor_read
python script to read Canary Home security device sensors (https://canary.is/)

idea based on: https://www.joshdurbin.net/posts/2015-10-reading-sensor-data-from-canary/

fill the conf, rename the conf, and use it

```
Home assistant example config:
  - platform: command_line
    name: canary_temperature
    command: 'python3 /home/homeassistant/.homeassistant/scripts/Canary_sensor_read/read_sensor_data.py'
    scan_interval: 903
    value_template: '{{ value_json.temperature | round(1)}}'
    unit_of_measurement: '°C'
    json_attributes:
      - humidity
      - air_quality
      - read_ok
    command_timeout: 30

  - platform: template
    sensors:
      canary_air_quality:
      friendly_name: "Canary Air Quality"
      value_template: "{{ (state_attr('sensor.canary_temperature', 'air_quality')|float * 1000 )| round(0) }}"
      unit_of_measurement: "ppm"

      canary_humidity:
        friendly_name: "Canary Humidity"
        value_template: "{{ (state_attr('sensor.canary_temperature', 'humidity')) | round(0) }}"
        unit_of_measurement: "%"
```
