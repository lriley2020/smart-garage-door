
Parameters can be changed in the cfg.json file.

http://x.x.x.x/edit  
![](https://i.ibb.co/6wDWWY0/1.png)

### Übersicht der Parameter
|Typ|Name|Beschreibung|
|---|----|-----------|  
|char     |cfgApSsid[32]                |SSID of the initial Access Point|
|char     |cfgApPass[63]                |Password of the initial Access Point|
|char     |cfgNtpServer[30]             |NTP server e.g. "fritz.box" for local access, if empty: "europe.pool.ntp.or
|uint8_t  |cfgTxEnable;                 | 0: disable TX, 1: enable TX|
|uint8_t  |cfgTimeOn;                   | Hour to  enable button|
|uint8_t  |cfgTimeOff;                  | Hour to disable button|
|uint16_t |cfgBtnDebounce;              | Debounce time for button [ms]|
|uint8_t  |cfgAcTime;                   | Hour to start the auto-close [h]|
|uint8_t  |cfgAcDur1;                   | Duration of the auto-close PREWARN phase [s]|
|uint8_t  |cfgAcDur2;                   | Duration of the auto-close WAIT    phase [s]|
|uint8_t  |cfgPdTimeOn;                 | Hour to  enable package drop function|
|uint8_t  |cfgPdTimeOff;                | Hour to disable package drop function|
|uint8_t  |cfgPdWaitTime;               | Duration of the package drop  WAIT phase [s]|
|uint8_t  |cfgPdTimeout;                | Timeout of the package drop function, when venting position is missed [s]|
|uint16_t |cfgPdWaitError;              | Wait time for error correction before start [ms]|
|uint8_t  |cfgLogMonths;                | Months to be logged|
|uint8_t  |cfgTrace;                    | 0: disable Trace Feature, 1: enable|
|uint8_t  |cfgAutoErrorCorr;            | 0: disable AutoErrorCorrection, 1: enable|
|uint8_t  |cfgMasterAddr;               | Master address: 128 (0x80) per default, 144 (0x90) for HAP1-HCP-Adapter|

Changes only take effect **after a reset**
