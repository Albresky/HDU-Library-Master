<p align="center">
  <a href="https://github.com/Albresky/HDU-Library-Master"><img src="https://s2.loli.net/2023/05/22/3y6dc51NXmabzgj.png" alt="HDU-Library-Master"></a>
</p>
<p align="center">
Daily Seats Reservation for HDU Library
</p>

<div align="center">

![LICENSE](https://img.shields.io/badge/license-Apache2.0-green)
![Author](https://img.shields.io/badge/Author-Albresky-blue.svg)

</div>

**English** | [中文](https://github.com/Albresky/HDU-Library-Master/blob/main/README.md)

Automatic daily seats reservation via `Github Actions`

## Why choose this repo?

**ONE minute for configuration, FULL year for liberation.**

## How to use

### `Fork` this repo

### Add `Repo Secrets`

 - (Follow the steps in the settings of your forked repo) 
   - `Settings` - `[Security]Secrets and Variables` - `Actions` - `New repository secret`

|| Name | Secrets (Example) | Description |
|--|--|--|--|
|Required| `HLMUSERID`   | `20239999` | Student ID |
|Required| `HLMPASSWORD` | `hDu123321` | Login password of library's system, **differ from the password of HDU-CAS** |
|Required| `HLMPLANCODE` | `1:1000:15:8:2` | Reservation task code, separated by English commas. For example, `code1,code2,code3, ...`  See `Data Field` for details |
|Optional| `HLMMAXTRIALS`| `1` | The maximum number of trials, default value is `1` times |
|Optional| `HLMDELAY`    | `2` | Delay in each query, default value is `2` seconds |
|Optional| `HLMLOGDETAILS` | `false` | whether to output task details in the log of workflows, default value is `false`, you can set it to `true` to display task details |
|Optional| `HLMEXECUTETIME` | `19:20:20` | The time to start executing task, default value is `20:00:00` |
|Optional| `HLMPREEXETIME` | `00:00:00` | The advanced time to execute task, default value is `00:00:00` |


> [!WARNING]\
> `HLMMAXTRIALS` default value is `1`, ≥ `3` times may cause account banning.


### [Note] When to Trigger? (**Do NOT MODIFY**)

 - The current workflow job is triggerred through `schedule` only
 - The `cron` expression in `.github/workflows/workflow.yaml` is used to control the trigger time of the task
 - The timezone of `cron` expression is `UTC-0`


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
   - **[PS]** The duration should be no greater than the opening time of the library, and not exceed `14` hours
     - e.g. If A room opens at `8:00` and closes at `22:00`, then the duration should be no greater than `14` hours (`22 - 8 = 14`), and if your reservation begins at `20:00`, then the duration should be no greater than `2` hours (`22 - 20 = 2`)


## Example

 - `Repo Secrets`
    - `HLMUSERID`
      - `20239999`
    - `HLMPASSWORD`
      - `hDu123123`
    - `HLMPLANCODE`
      - `1:1000:15:8:2,1:1524:34:14:5,3:1412:22:18:2`


 - The example given above is likely to reserve seats like this :

|No.|Place|Location|Seat|Time|Duration|
|---|---|---|---|---|---|
|1|Study Lounge|2F|15|8:00 - 10:00|2 hours|
|2|Study Lounge|2F E-reading Room|34|8:00 - 22:00|5 hours|
|3|Reading Room|Comprehensive 1st Library (11F)|22|18:00 - 20:00|2 hours|


## Acknowledgement

 - [LittleHeroZZZX/hdu-library-killer](https://github.com/LittleHeroZZZX/hdu-library-killer)