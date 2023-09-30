<p align="center">
  <a href="https://github.com/Albresky/HDU-Library-Master"><img src="https://s2.loli.net/2023/05/22/3y6dc51NXmabzgj.png" alt="HDU-Library-Master"></a>
</p>
<p align="center">
杭电图书馆每日定时[订座/抢座]
</p>

<div align="center">

![LICENSE](https://img.shields.io/badge/license-Apache2.0-green)
![Author](https://img.shields.io/badge/Author-Albresky-blue.svg)

</div>

**中文** | [English](https://github.com/Albresky/HDU-Library-Master/blob/main/readme/README_EN.md)

`Github Actions` 自动触发每日订座任务

---

## 〇、Feature

:heavy_check_mark: 一分钟部署

:x: 配置环境

:x: 私有服务器


### 免责声明

> [!WARNING]\
> 由于杭电图书馆预约系统近期更新（2023.09.11），本仓库所实现的订座/抢座功能有封号的可能，使用本仓库则代表你自愿承担封号后果。
> 本仓库不盈利、不建群，旨在方便爱学习的 `HDUer`，倘若对使用者造成任何方面的损失，本人均不负责。
> 若本仓库所提供的服务对 `HDU服务器` 造成严重负担，请管理员发email，这里会第一时间停止更新并删除仓库。
> 本仓库不提倡 `抢座但不及时赴约` 的恶劣行为，其造成的任何影响，与本仓库无关。
> **欢迎使用，好好学习，天天向上！**


## 一、使用方法

### 1、`Fork` 本仓库

### 2、添加 `Secrets`

 - 在你 Fork 的仓库中，进行以下步骤的配置：
   - `Settings` - `[Security]Secrets and Variables` - `Actions` - `New repository secret`


|| Name | Secrets（示例） | 描述|
|--|--|--|--|
|必填| `HLMUSERID`   | `20239999` | 学号 |
|必填| `HLMPASSWORD` | `hDu123321` | 图书馆系统登录密码，**非数字杭电登录密码** |
|必填| `HLMPLANCODE` | `1:1000:15:8:2` | 订座任务代码，以英文逗号分隔。如 `code1,code2,...` |
|可选| `HLMMAXTRIALS`| `1` | 最大尝试次数，默认为 `1` 次 |
|可选| `HLMDELAY`    | `2` | 请求延迟时间，默认为 `2` 秒 |
|可选| `HLMLOGDETAILS` | `false` | 是否在workflows 的日志中输出任务细节，默认为 `false` |
|可选| `HLMEXECUTETIME` | `19:20:20` | 开始执行任务时间点，默认为 `20:00:00` |
|可选| `HLMPREEXETIME` | `00:00:00` | 提前执行任务时间点，默认为 `00:00:00` |

> [!WARNING]\
> 环境变量 `HLMMAXTRIALS` 最大尝试次数，默认为 `1` 次，大于等于 `3` 次可能导致封号。


### 3、[注] 触发时间说明（**勿修改**）
 - 当前的 workflows 仅通过 `schedule` 触发任务
 - `.github/workflows/workflow.yaml` 中的 `cron` 表达式，用以控制任务触发时间
 - `cron` 表达式时间为 `UTC-0` 时区


## 二、数据字段格式说明


 - `code` 订座任务代码
   - `roomType:floor:seatNum:startTime:duration`
 - `roomType` 房间类型
    - `1` 自习室
    - `2` 教师休息室
    - `3` 阅览室
    - `4` 讨论室
 - `floor` 楼层

```json
{
  "自习室":{
      "二楼自习室": 1000,
      "二楼电子阅览室": 1524,
      "三楼大厅": 1525,
      "四楼自习室": 1221
  },
  "教师休息室": {}, # 暂不可用
  "阅览室": {
      "自然科学书库（三楼东）": 1403,
      "社会科学书库（三楼西）": 1404,
      "社会科学书库（三楼北）": 1405,
      "研修中心（六楼）": 1407,
      "自然科学第二书库（七楼）": 1408,
      "社会科学第二数据（八楼）": 1409,
      "文学艺术书库（九楼）": 1410,
      "综合第二书库（十楼）": 1411,
      "综合第一书库（十一楼）": 1412
  },
  "讨论室": {} # 暂不可用
}
```

 - `seatNum` 座位编号
   - 官方预约系统中该房间的座位编号
 - `startTime` 开始时间
   - 24小时制，如:
     - `8` 代表 `08:00`
     - `14` 代表 `14:00`
     - `20` 代表 `20:00`

 - `duration` 预约时长
   - 以小时为单位，如:
     - `1` 代表 `1` 小时
     - `2` 代表 `2` 小时
     - `3` 代表 `3` 小时
   - **[注意]** 预约时长须根据 `startTime` 确定


## 三、`Secrets` 示例

 - `HLMUSERID`
   - `20239999`
 - `HLMPASSWORD`
   - `hDu123123`
 - `HLMPLANCODE`
   - `1:1000:15:8:2,1:1524:34:14:5,3:1412:22:18:2`


 - 上述示例 `HLMPLANCODE` 对应的预约计划如下:

| 序号 | 类别     | 位置              | 座位号 | 时间          | 时长   |
| ---- | -------- | ----------------- | ------ | ------------- | ------ |
| 1    | 自习室   | 二楼自习室        | 15     | 08:00 - 10:00 | 2小时  |
| 2    | 自习室   | 二楼电子阅览室    | 34     | 14:00 - 19:00 | 5小时  |
| 3    | 阅览室   | 综合第一书库（十一楼）| 22     | 18:00 - 20:00 | 2小时 |


## 四、鸣谢

 - [LittleHeroZZZX/hdu-library-killer](https://github.com/LittleHeroZZZX/hdu-library-killer)
