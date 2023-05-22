<p align="center">
  <a href="https://github.com/Albresky/HDU-Library-Master"><img src="https://s2.loli.net/2023/05/22/3y6dc51NXmabzgj.png" alt="HDU-Library-Master"></a>
</p>
<p align="center">
Daily Seats Reservation for HDU Library
</p>

**English** | [中文](https://github.com/Albresky/HDU-Library-Master/blob/main/README.md)

Automatic daily seats reservation via `Github Actions`

## How to use

### Fork this repo

### Add `Repo Secrets`

- `Settings` - `[Security]Secrets and Variables` - `Actions` - `New repository secret`

  - `HLMUSERID` Student ID
  - `HLMPASSWORD` HDU Library System Password
    - [PS] `differ from HDU-CAS Password`
  - `HLMPLANCODE` Reservation Task Code, separated by English commas `,`
    - e.g. `code1,code2,code3,...`
    - [PS] You should set at least one task code
  - **[Optional]** `HLMMAXTRIALS` Max trials
    - Default value `2`
  - **[Optional]** `HLMDELAY` Timeout of Single Trial (in seconds)
    - Default value `10`

### **[Optional]** Modify trigger time
 - Modify `cron` expression in `.github/workflows/workflow.yaml` to set the trigger time
 - [PS] The time in `cron` expression is `UTC` time, you should offset it according to your local time zone (`UTC-8` for China)
   - [e.g.] If the trigger time is set to `20:00` (**the earliest time for next day's seats reservation in hdu-library's server**), then the `cron` expression should be set as `0 12 * * *`


## Data Field

 - `code` Reservation Task Code
   - `roomType:floor:seatNum:startTime:duration`
 - `roomType` Room Type
    - `1` Self-study Room
    - `2` Teacher's Rest Room
    - `3` Reading Room
    - `4` Discussion Room
 - `floor` Floor
```json
{
    "Study Lounge":{
        "3F Hall":1525,
        "2F E-reading Room":1524,
        "4F Study Lounge":1221,
        "2F Study Lounge":1000
    },
    "Teacher's Rest Room":{}, # not available for now
    "Reading Room":{
        "Natural Science Library (3F East)":1403,
        "Social Science Library (3F West)":1404,
        "Social Science Library (3F North)":1405,
        "Training Center (6F)":1407,
        "Natural Science 2nd Library (7F)":1408,
        "Social Science 2nd Data (8F)":1409,
        "Literature and Art Library (9F)":1410,
        "Comprehensive 2nd Library (10F)":1411,
        "Comprehensive 1st Library (11F)":141
    },
    "Discussion Room":{} # not available for now
}
```

 - `seatNum` Seat Number
   - You need to refer to the official client
 - `startTime` Start Time of your reservation
   - 24-hour format, `e.g.`:
     - `8` means `08:00`
     - `14` means `14:00`
     - `20` means `20:00`

 - `duration` Duration of your reservation
   - In hours, `e.g.`:
     - `1` means `1` hour
     - `4` means `4` hours
   - **[PS]** The duration should be less than the opening time of the library, and not exceed `14` hours
     - e.g. If that room opens at `8:00` and closes at `22:00`, then the duration should be less than `14` hours (`22 - 8 = 14`), and if your reservation starts at `20:00`, then the duration should be less than `2` hours (`22 - 20 = 2`)


## Example

 - `Repo Secrets`
    - `HLMUSERID`
      - `12345678`
    - `HLMPASSWORD`
      - `hDu123123`
    - `HLMPLANCODE`
      - `1:1000:15:8:2,1:1524:34:14:5,3:1412:22:18:2`


 - The example given above is going to reserve seats like this :

|No.|Place|Location|Seat|Time|Duration|
|---|---|---|---|---|---|
|1|Study Lounge|2F|15|8:00 - 10:00|2 hours|
|2|Study Lounge|2F E-reading Room|34|8:00 - 22:00|5 hours|
|3|Reading Room|Comprehensive 1st Library (11F)|22|18:00 - 20:00|2 hours|


## Acknowledgement

 - [LittleHeroZZZX/hdu-library-killer](https://github.com/LittleHeroZZZX/hdu-library-killer)