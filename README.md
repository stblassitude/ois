# DiVOC Hybrid Example

See [\*OIS\*](https://zkm.de/de/werk/ois) at ZKM.

## Tasmota Configuration

### Configure button to send MQTT message and not toggle the power

```
SetOption73 1
Backlog ButtonTopic 0
SwitchMode 15
```
