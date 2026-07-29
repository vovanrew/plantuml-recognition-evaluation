# Failure-case index — zero-shot image→PlantUML benchmark

**Models included: 7/7** (panel label: main) — 233 sampled cases.

Stratified sample of failures: up to **2 case(s) per (model × diagram type × tier × outcome class)** over the failure classes `provider_drop`, `compile_fail`, `compiled_low_structural`. `compiled_low_structural` = rendered but Element or Relationship F1 < 0.5. Selection is a seeded shuffle (seed=20260614) over key-sorted rows — deterministic and per-cell independent. A missing prediction/render file is itself signal (a provider drop or a non-rendering prediction).

## Coverage (available → sampled)

| Model | provider_drop | compile_fail | compiled_low_structural |
|---|---|---|---|
| GPT-5.2 | 1→1 | 64→16 | 94→16 |
| Claude Opus 4.6 | — | 59→14 | 120→16 |
| Gemini 3.1 Pro | — | 28→13 | 53→16 |
| Qwen3.5-2B | 25→12 | 774→16 | 100→16 |
| Qwen3.5-9B | — | 569→16 | 201→16 |
| Qwen3.5-27B | 1→1 | 398→16 | 104→16 |
| Qwen3.5-397B-A17B | — | 213→16 | 122→16 |

_108 cell(s) capped at 2 (full list in the JSON `capped_cells`) — the sample is a subset of those cells, not the complete failure set._

## Cases

### GPT-5.2

#### outcome: provider_drop

#### `b3d43297c56f7d7d725d9d50288912cf40e8ed50` — provider_drop (class, tier 1)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 0.00
- Files: GT `data/puml_files/b3d43297c56f7d7d725d9d50288912cf40e8ed50.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/b3d43297c56f7d7d725d9d50288912cf40e8ed50.puml` (MISSING) · input `data/puml_images_1568/b3d43297c56f7d7d725d9d50288912cf40e8ed50.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/b3d43297c56f7d7d725d9d50288912cf40e8ed50.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: b3d43297c56f7d7d725d9d50288912cf40e8ed50
' Original Path: /Отчеты/ОтчетАнализПричинПроигрышаСделок.wsd
' Source: World of Code

﻿@startuml
'!include templates.wsd
'..\include templates.wsd
class Отчет.АнализПричинПроигрышаСделок as "Анализ причин проигрыша сделок" <<Отчеты>>
{
..Макеты..
ОсновнаяСхемаКомпоновкиДанных : СхемаКомпоновкиДанных
}
@enduml
```

_Prediction: no file on disk (provider/harness drop)._

#### outcome: compile_fail

#### `05af3d5892f56a4b70714d0b17d90ff90d8a945c` — compile_fail (sequence, tier 2)

- CSR: `Error line 8 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/05af3d5892f56a4b70714d0b17d90ff90d8a945c.puml`
- Element: tp=0 fp=0 fn=11 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=14 F1=0.000; missed: message
- chrF++: 81.21
- Files: GT `data/puml_files/05af3d5892f56a4b70714d0b17d90ff90d8a945c.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/05af3d5892f56a4b70714d0b17d90ff90d8a945c.puml` (yes) · input `data/puml_images_1568/05af3d5892f56a4b70714d0b17d90ff90d8a945c.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/05af3d5892f56a4b70714d0b17d90ff90d8a945c.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 05af3d5892f56a4b70714d0b17d90ff90d8a945c
' Original Path: /029/quick_start_share_application_more_installed_dlg_seq.uml
' Source: World of Code

@startuml
[-> CShareMoreDlg : OnBtnShareOtherApp
note over CShareMoreDlg : User Click "Other Application"

CShareMoreDlg -> CSharingMoreWrapper : ShareOtherApp
CSharingMoreWrapper -> CPfwMainFrame : SendMessage
note over CSharingMoreWrapper, CPfwMainFrame : PFW_QS_MENU_SHARE_OTHER_APP_ID
CPfwMainFrame -> CPfwChainMessageMapT : PfwChainProcessWindowMessage
CPfwChainMessageMapT -> CPfwMainFrame : ProcessWindowMessage
CPfwMainFrame -> CMCUIMgr : OnWindowMsg
CMCUIMgr -> CSmDefUIMgr : OnWindowMsg
CSmDefUIMgr -> CSmDefUIMgr : ChainToMsgCenter
CSmDefUIMgr -> CPfwMessageCenterAgent : SendMessage
CPfwMessageCenterAgent -> CSmFITUIMgr::ProcessWindowMessage
CSmFITUIMgr -> CMCFITUIMgr :OnCommand
CMCFITUIMgr -> CSmFITUIMgr : OnCommand
CSmFITUIMgr -> CSmAppShareSessionMgr : SelectANewApplication
CSmAppShareSessionMgr -> CPcmAppShareMgr : ShowInstalledAppDialog

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true
skinparam ParticipantPadding 20
skinparam BoxPadding 10

participant "CShareMoreDlg" as CShareMoreDlg
participant "CSharingMoreWrapper" as CSharingMoreWrapper
participant "CPfwMainFrame" as CPfwMainFrame
participant "CPfwChainMessageMapT" as CPfwChainMessageMapT
participant "CMCUIMgr" as CMCUIMgr
participant "CSmDefUIMgr" as CSmDefUIMgr
participant "CPfwMessageCenterAgent" as CPfwMessageCenterAgent
participant "CSmFITUIMgr" as CSmFITUIMgr
participant "CMCFITUIMgr" as CMCFITUIMgr
participant "CSmAppShareSessionMgr" as CSmAppShareSessionMgr
participant "CPcmAppShareMgr" as CPcmAppShareMgr

CShareMoreDlg -> CShareMoreDlg : OnBtnShareOtherApp
note right of CShareMoreDlg
User Click "Other Application"
end note

CShareMoreDlg -> CSharingMoreWrapper : ShareOtherApp
CSharingMoreWrapper -> CPfwMainFrame : SendMessage
note over CSharingMoreWrapper,CPfwMainFrame
PFW_QS_MENU_SHARE_OTHER_APP_ID
end note

CPfwMainFrame -> CPfwChainMessageMapT : PfwChainProcessWindowMessage
CPfwChainMessageMapT --> CPfwMainFrame : ProcessWindowMessage
CPfwMainFrame -> CMCUIMgr : OnWindowMsg
CMCUIMgr -> CSmDefUIMgr : OnWindowMsg
CSmDefUIMgr -> CSmDefUIMgr : ChainToMsgCenter
CSmDefUIMgr -> CPfwMessageCenterAgent : SendMessage
CPfwMessageCenterAgent -> CSmFITUIMgr : ProcessWindowMessage
CSmFITUIMgr -> CMCFITUIMgr : OnCommand
CMCFITUIMgr --> CSmFITUIMgr : OnCommand
CSmFITUIMgr -> CSmAppShareSessionMgr : SelectANewApplication
CSmAppShareSessionMgr -> CPcmAppShareMgr : ShowInstalledAppDialog

@enduml
```

#### `2fc02b638db7d0314c7594c6f6a03f1a6f247100` — compile_fail (class, tier 3)

- CSR: `Error line 9 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/2fc02b638db7d0314c7594c6f6a03f1a6f247100.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: inheritance, aggregation, association
- chrF++: 71.49
- Files: GT `data/puml_files/2fc02b638db7d0314c7594c6f6a03f1a6f247100.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/2fc02b638db7d0314c7594c6f6a03f1a6f247100.puml` (yes) · input `data/puml_images_1568/2fc02b638db7d0314c7594c6f6a03f1a6f247100.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/2fc02b638db7d0314c7594c6f6a03f1a6f247100.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 2fc02b638db7d0314c7594c6f6a03f1a6f247100
' Original Path: /09_bridge/bridge.pu
' Source: World of Code

@startuml

title ブリッジパターン

package main {
    object main {
    }
}

package Bridge {
    'abstract Display {
    class Display {
        impl
        open(arg): void
        print(arg): void
        close(arg): void
        display(arg): void
    }

    class CountDisplay {
        multi_display(arg): void
    }

    abstract DisplayImpl {
        {abstract} raw_open(arg): void
        {abstract} raw_print(arg): void
        {abstract} raw_close(arg): void
    }
    'displayのメソッド使わない？

    class StringDisplayImpl {
        raw_open(arg): void
        raw_print(arg): void
        raw_close(arg): void
    } 
}
    main --> Display : Uses
    main -right-> CountDisplay : Uses
    main --> StringDisplayImpl : Create
    CountDisplay -up-|> Display
    Display o-right-> DisplayImpl
    StringDisplayImpl -up-|> DisplayImpl
    

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title ブリッジパターン

skinparam shadowing false
skinparam packageStyle folder
skinparam classAttributeIconSize 0

package "main" as PKG_MAIN {
  class main as MAIN
}

package "Bridge" as PKG_BRIDGE {

  abstract class Display << (C,#B7E1B0) >> {
    impl
    --
    open(arg): void
    print(arg): void
    close(arg): void
    display(arg): void
  }

  abstract class DisplayImpl << (A,#BFE9EA) >> {
    --
    {abstract} raw_open(arg): void
    {abstract} raw_print(arg): void
    {abstract} raw_close(arg): void
  }

  class CountDisplay << (C,#B7E1B0) >> {
    --
    multi_display(arg): void
  }

  class StringDisplayImpl << (C,#B7E1B0) >> {
    --
    raw_open(arg): void
    raw_print(arg): void
    raw_close(arg): void
  }

  Display o--> DisplayImpl
  CountDisplay --|> Display
  StringDisplayImpl --|> DisplayImpl
}

MAIN ..> Display : Uses
MAIN ..> StringDisplayImpl : Uses
MAIN ..> StringDisplayImpl : Create

@enduml
```
```

#### `30969b941c87171a79af4ee7c2f2ca6f1178a0fe` — compile_fail (class, tier 2)

- CSR: `Error line 46 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/30969b941c87171a79af4ee7c2f2ca6f1178a0fe.puml`
- Element: tp=0 fp=0 fn=6 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: aggregation, association
- chrF++: 42.52
- Files: GT `data/puml_files/30969b941c87171a79af4ee7c2f2ca6f1178a0fe.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/30969b941c87171a79af4ee7c2f2ca6f1178a0fe.puml` (yes) · input `data/puml_images_1568/30969b941c87171a79af4ee7c2f2ca6f1178a0fe.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/30969b941c87171a79af4ee7c2f2ca6f1178a0fe.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 30969b941c87171a79af4ee7c2f2ca6f1178a0fe
' Original Path: /src/uml/aggregate.puml
' Source: World of Code

@startuml
'https://plantuml.com/class-diagram

package Aggregate-Buch <<Rectangle>> {
  class Buch <root entity>
  class AutorID <value>
  class BuchID <value>
  class Kapitel <entity>
  class KapitelID <value>
  enum Status <value>


  Buch o-- Kapitel
  Buch o-- AutorID
  Buch --> BuchID
  Kapitel --> Status
  Kapitel -->KapitelID
  Buch --> Status

}

hide members
@enduml


'Aggregation:ist eine (besteht aus)-Beziehung zwischen zwei voneinander unabhängige Klassen (nicht gefülltes Pfile)
'--Pc hat eine Tastatur, und eine Tastatur gehört zu genau einem Pc. 1-1-Beziehung
'
'Composition:Ist ein SonderFall der Aggregation. Hier zwischen zwei voneinander abhängige Klassen (gefülltes Pfile)
'--Pc hat einen LieferSchein. existiert Pc nicht => existiert LieferSchein nicht
```

Prediction PlantUML (truncated):
```plantuml
@startuml
title Aggregate-Buch

skinparam shadowing false
skinparam backgroundColor white
skinparam roundcorner 12
skinparam class {
  BackgroundColor #f7f7f7
  BorderColor #333333
  ArrowColor #333333
  FontSize 22
}
skinparam note {
  BackgroundColor white
  BorderColor #333333
  FontSize 22
}

' Helper stereotypes for colored circle letters
class Buch <<C>> 
class AutorID <<C>>
class BuchID <<C>>
class Kapitel <<C>>
class KapitelID <<C>>
class Status <<E>>

' Color the stereotype circles
skinparam class<<C>> {
  BackgroundColor #f7f7f7
  BorderColor #333333
  StereotypeFontColor #000000
  StereotypeBackgroundColor #b9d7bf
}
skinparam class<<E>> {
  BackgroundColor #f7f7f7
  BorderColor #333333
  StereotypeFontColor #000000
  StereotypeBackgroundColor #f2a08f
}

' Show only the stereotype letter in a circle-like badge
hide members
hide circle

' Notes (dashed boxes)
note top right of Buch
  <i>root entity</i>
end note

note top right of AutorID
  <i>value</i>
end note

note top right of BuchID
  <i>value</i>
end note

note top right of Kapitel
  <i>entity</i>
end note

note top right of KapitelID
  <i>value</i>
end note

note top right of Status
  <i>value</i>
end note

' Layout hints
Buch -[hidden]down-> BuchID
AutorID -[hidden]right-> BuchID
BuchID -[hidden]right-> Kapitel
Kapitel -[hidden]down-> KapitelID
KapitelID -[hidden]right-> Status

' Relationships
Buch o-- AutorID
Buch --> BuchID
Buch o-- Kapitel
```

#### `32e297812885b315c9ec8f772b7a81897cfbaed0` — compile_fail (sequence, tier 3)

- CSR: `Error line 24 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/32e297812885b315c9ec8f772b7a81897cfbaed0.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: message
- chrF++: 74.22
- Files: GT `data/puml_files/32e297812885b315c9ec8f772b7a81897cfbaed0.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/32e297812885b315c9ec8f772b7a81897cfbaed0.puml` (yes) · input `data/puml_images_1568/32e297812885b315c9ec8f772b7a81897cfbaed0.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/32e297812885b315c9ec8f772b7a81897cfbaed0.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 32e297812885b315c9ec8f772b7a81897cfbaed0
' Original Path: /web/doc/sequence-diagram/15.ネットワーク情報変更通知.puml
' Source: World of Code

@startuml

actor Webブラウザ as client
participant "CCM GUI\n(Web)" as web
participant "CCM GUI\n(WebSocket)" as ws
participant "CCM SDK\n(IPC)" as ccm

' 各サーバーはすべて起動状態から開始
activate client
activate web
activate ws
activate ccm

ccm -> ccm : ネットワーク情報変更通知 受信\n(RegistRecieveNetworkInfoHandler)

ws <<-- ccm : ネットワーク情報変更通知 [notify]
note left
    {
        "command": "NetworkInfo",
        "type": "notify",
        "data": {
            "ID": "xxx",
            "CellularInfo": [{
                "SignalStrength": "...",
                "SignalStrengthUnit": "...",
                "Operator": "...",
                "PLMN": "...",
                "Band": "...",
                "CellID": "...",
                "AirInterface": "...",
                "Manufacture": "...",
                "ModelName": "...",
                "IMEI": "..."
            }],
            "QosInterfaceType": {
                "key1": "val1",
                ...
            }
        }
    }
end note
client <<-- ws

client -> client : 1秒間隔で保持データを画面に表示

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
hide footbox
skinparam shadowing false
skinparam sequence {
  ParticipantPadding 40
  BoxPadding 10
  MessageAlign left
  LifeLineBorderColor #000000
  LifeLineBackgroundColor #FFFFFF
  ParticipantBorderColor #666666
  ParticipantBackgroundColor #D9D9E8
  NoteBackgroundColor #FFFED6
  NoteBorderColor #666666
}

actor "Webブラウザ" as WB

participant "CCM GUI\n(Web)" as WEB
participant "CCM GUI\n(WebSocket)" as WS
participant "CCM SDK\n(IPC)" as SDK

SDK -> SDK : ネットワーク情報変更通知 受信\n(RegistRecieveNetworkInfoHandler)

SDK ..> WS : ネットワーク情報変更通知 [notify]

note over WEB,WS
{
  "command": "NetworkInfo",
  "type": "notify",
  "data": {
    "ID": "xxx",
    "CellularInfo": [{
      "SignalStrength": "...",
      "SignalStrengthUnit": "...",
      "Operator": "...",
      "PLMN": "...",
      "Band": "...",
      "CellID": "...",
      "AirInterface": "...",
      "Manufacture": "...",
      "ModelName": "...",
      "IMEI": "..."
    }],
    "QosInterfaceType": {
      "key1": "val1",
      ...
    }
  }
}
end note

WS ..> WB : 1秒間隔で保持データを画面に表示
WB -> WB

@enduml
```

#### `3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e_15` — compile_fail (class, tier 1)

- CSR: `Error line 11 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e_15.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: association
- chrF++: 66.53
- Files: GT `data/puml_files/3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e_15.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e_15.puml` (yes) · input `data/puml_images_1568/3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e_15.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e_15.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 3e8ecc26a5a423e016c2d7c2fe96a7e63fe2de0e
' Original Path: /JavaUML/ClassDiagram.puml
' Source: World of Code

@startuml
class Dummy
Dummy --> Foo:A link
note on link #red:note that is red
Dummy--> Foo2: Another link
note right on link #blue
this is my note on right link
and in blue
end note
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0

class Dummy
class Foo
class Foo2

Dummy -down-> Foo : A link
Dummy -down-> Foo2 : Another link

note left of Dummy -[#red,fill=red] 
note that is red
end note

note right of Dummy -[#blue,fill=blue]
this is my note on right link
and in blue
end note
@enduml
```

#### `4aad380673ff1225b973f740bf80ec99dfb70724` — compile_fail (sequence, tier 1)

- CSR: `Error line 22 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/4aad380673ff1225b973f740bf80ec99dfb70724.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 71.42
- Files: GT `data/puml_files/4aad380673ff1225b973f740bf80ec99dfb70724.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/4aad380673ff1225b973f740bf80ec99dfb70724.puml` (yes) · input `data/puml_images_1568/4aad380673ff1225b973f740bf80ec99dfb70724.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/4aad380673ff1225b973f740bf80ec99dfb70724.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 4aad380673ff1225b973f740bf80ec99dfb70724
' Original Path: /MyBackup/MyBackup/UML/SequenceDiagram.puml
' Source: World of Code

@startuml

actor User

User -> MyBackupService : SimpleBackup()
Create TaskDispatcher
MyBackupService -->> TaskDispatcher : New
MyBackupService <<-- TaskDispatcher : TaskDispatcher
MyBackupService -> TaskDispatcher : SimpleTask()

TaskDispatcher -> TaskFactory : Create()
Create SimpleTask
TaskFactory -->> SimpleTask : new 
TaskDispatcher <<-- SimpleTask : Task
TaskDispatcher -> SimpleTask : Execute()

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
hide footbox
skinparam shadowing false
skinparam sequence {
  ParticipantPadding 40
  BoxPadding 10
  LifeLineBorderColor #666666
  LifeLineBackgroundColor #FFFFFF
  ParticipantBorderColor #333333
  ParticipantBackgroundColor #E6E6F2
  ActorBorderColor #333333
  ActorBackgroundColor #E6E6F2
}

actor User
participant MyBackupService
participant TaskDispatcher
participant TaskFactory
participant SimpleTask

User -> MyBackupService : SimpleBackup()
MyBackupService ..> TaskDispatcher : New
TaskDispatcher ..> MyBackupService : TaskDispatcher
MyBackupService -> TaskDispatcher : SimpleTask()
TaskDispatcher -> TaskFactory : Create()
TaskFactory ..> SimpleTask : new
SimpleTask ..> TaskDispatcher : Task
TaskDispatcher -> SimpleTask : Execute()

@enduml
```

#### `532d5a1ff757de7127780cff4493ccdd7a51c49a` — compile_fail (sequence, tier 4)

- CSR: `Error line 68 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml`
- Element: tp=0 fp=0 fn=13 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=34 F1=0.000; missed: message
- chrF++: 57.86
- Files: GT `data/puml_files/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml` (yes) · input `data/puml_images_1568/532d5a1ff757de7127780cff4493ccdd7a51c49a.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/532d5a1ff757de7127780cff4493ccdd7a51c49a.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 532d5a1ff757de7127780cff4493ccdd7a51c49a
' Original Path: /docs/SprintD/US1006/SD.puml
' Source: World of Code

@startuml
actor "Sales Clerk" as SC
participant "Presentation<U+226B>\n: OrderDeliveredUI" as presentation
participant "<U+226A>Application<U+226B>\n: OrderDeliveredController" as controller
participant "<U+226A>Service<U+226B>\n: OrderDeliveredService" as service
participant "<U+226A>Persistence<U+226B>\n: PersistenceContext" as context
participant "<U+226A>Factory<U+226B>\nfactory : RepositoryFactory" as factory
database "<U+226A>Repository<U+226B>\norderRepository : Repository" as repository
participant "<U+226A>Domain<U+226B>\norderList : List<Order>" as list
participant "<U+226A>DTO<U+226B>\norderDTOList : List<OrderDTO>" as listDTO
participant "<U+226A>DTO<U+226B>\n : OrderMapper" as mapper
participant "<U+226A>DTO<U+226B>\norderDTO : OrderDTO" as dto
participant "<U+226A>DTO<U+226B>\nselectedOrderDTOList : List<OrderDTO>" as listOrdDTOer
participant "<U+226A>Domain<U+226B>\norder : Order" as orders



SC -> presentation: The Sales Clerk initializes\nthe process of updating the status of the order
activate presentation

presentation -> controller: create
activate controller

controller -> service: create
activate service
service -> context: repositories()
activate context

context -> factory: create
context --> service: factory
deactivate context

service -> factory: orderRepository()
activate factory

factory -> repository: create

factory--> service: orderRepository
deactivate factory
deactivate service
deactivate controller

presentation -> controller: listAllDispatchedOrders()
activate controller

controller -> service: listAllDispatchedOrders()
activate service

service -> repository: getAllDispatchedOrders()
activate repository

repository -> list: create

repository --> service: orderList
deactivate repository

service -> listDTO: create

loop foreach
    service -> list: getNext()
    activate list

    list --> service: order
    deactivate list

    service -> mapper: toDTO(order)
    activate mapper

    mapper -> dto: create

    mapper --> service: orderDTO
    deactivate mapper

    service -> listDTO: add(orderDTO)
    activate listDTO
    deactivate listDTO
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam backgroundColor white
skinparam shadowing false
skinparam sequenceMessageAlign center
skinparam responseMessageBelowArrow true
skinparam ParticipantPadding 18
skinparam BoxPadding 10
skinparam ArrowColor #333333
skinparam LifeLineBorderColor #999999
skinparam LifeLineBackgroundColor #FFFFFF
skinparam ParticipantBorderColor #999999
skinparam ParticipantBackgroundColor #E9E9F2
skinparam NoteBackgroundColor #FFFFFF
skinparam NoteBorderColor #999999

actor "Sales Clerk" as SalesClerk

participant "Presentation>>\n: OrderDeliveredUI" as UI
participant "«Application»\n: OrderDeliveredController" as Controller
participant "«Service»\n: OrderDeliveredService" as Service
participant "«Persistence»\n: PersistenceContext" as PC
participant "«Factory»\nfactory : RepositoryFactory" as RF
database "«Repository»\norderRepository : Repository" as Repo
participant "«Domain»\norderList : List<Order>" as OrderList
participant "«DTO»\norderDTOList : List<OrderDTO>" as OrderDTOList
participant "«DTO»\n: OrderMapper" as Mapper
participant "«DTO»\norderDTO : OrderDTO" as OrderDTO
participant "«DTO»\nselectedOrderDTOList : List<OrderDTO>" as SelectedOrderDTOList
participant "«Domain»\norder : Order" as Order

note left of SalesClerk
The Sales Clerk initializes
the process of updating the status of the order
end note

create UI
SalesClerk -> UI : create
activate UI

create Controller
UI -> Controller : create
activate Controller

create Service
Controller -> Service : create
activate Service

Service -> PC : repositories()
activate PC
PC --> Service : factory
deactivate PC

create RF
Service -> RF : create
activate RF

Service -> RF : orderRepository()
RF --> Service : orderRepository

create Repo
Service -> Repo : create
activate Repo

UI -> Controller : listAllDispatchedOrders()
Controller -> Service : listAllDispatchedOrders()
Service -> Repo : getAllDispatchedOrders()
create OrderList
Repo --> Service : orderList

create OrderDTOList
Service -> OrderDTOList : create

loop foreach
  Service -> OrderList : getNext()
  OrderList --> Service : order
  Service -> Mapper : toDTO(order)
  create OrderDTO
  Mapper --> Service : orderDTO
  Service -> OrderDTOList : add(orderDTO)
end
```

#### `5922ccf81ce292fdd445209df90f8035c5b34c23` — compile_fail (class, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 8.29
- Files: GT `data/puml_files/5922ccf81ce292fdd445209df90f8035c5b34c23.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/5922ccf81ce292fdd445209df90f8035c5b34c23.puml` (yes) · input `data/puml_images_1568/5922ccf81ce292fdd445209df90f8035c5b34c23.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/5922ccf81ce292fdd445209df90f8035c5b34c23.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 5922ccf81ce292fdd445209df90f8035c5b34c23
' Original Path: /РегистрыСведений/РегистрСведенийВзаимозависимыеЛица.wsd
' Source: World of Code

﻿@startuml
'!include templates.wsd
'..\include templates.wsd
class РегистрСведений.ВзаимозависимыеЛица as "Взаимозависимые лица" <<РегистрыСведений>>
{
..Измерения..
Организация : Справочник.Организация
Контрагент : Справочник.Организация\rСправочник.Контрагент
..Ресурсы..
ТипВзаимозависимости : Типы взаимозависимости
}
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam shadowing false
skinparam backgroundColor white
skinparam packageStyle rectangle
skinparam packageBorderThickness 3
skinparam packageFontSize 28
skinparam classBorderThickness 1
skinparam classFontSize 26
skinparam classAttributeFontSize 26
skinparam classHeaderFontSize 26
skinparam classBackgroundColor #F2F2F2

package "РегистрСведений" {
  class "«РегистрыСведений»\nВзаимозависимые лица" as Reg {
    ..
    ..Измерения..
    Организация : Справочник.Организация
    Контрагент : Справочник.Организация
    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \
```

#### `704b783235640f12565d250b751599d621aff349` — compile_fail (sequence, tier 1)

- CSR: `Error line 16 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/704b783235640f12565d250b751599d621aff349.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 34.18
- Files: GT `data/puml_files/704b783235640f12565d250b751599d621aff349.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/704b783235640f12565d250b751599d621aff349.puml` (yes) · input `data/puml_images_1568/704b783235640f12565d250b751599d621aff349.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/704b783235640f12565d250b751599d621aff349.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 704b783235640f12565d250b751599d621aff349
' Original Path: /docs/activity_diagram.puml
' Source: World of Code

@startuml

title Activity Diagram

participant "Bot Service" as svc
participant "Listener" as lsn
participant "Worker" as wrk
participant "Publisher" as pub


@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Activity Diagram

skinparam shadowing false
skinparam backgroundColor white
skinparam defaultTextAlignment center
skinparam roundcorner 10
skinparam activity {
  BackgroundColor #E6E6FA
  BorderColor #333333
  FontSize 28
  FontColor #000000
}

' Top row
activity "Bot Service" as BS1
activity "Listener" as L1
activity "Worker" as W1
activity "Publisher" as P1

' Bottom row
activity "Bot Service" as BS2
activity "Listener" as L2
activity "Worker" as W2
activity "Publisher" as P2

' Layout helpers
BS1 -[hidden]-> L1
L1  -[hidden]-> W1
W1  -[hidden]-> P1

BS2 -[hidden]-> L2
L2  -[hidden]-> W2
W2  -[hidden]-> P2

BS1 -[hidden]down-> BS2
L1  -[hidden]down-> L2
W1  -[hidden]down-> W2
P1  -[hidden]down-> P2

' Dashed vertical connectors
BS1 ..down.. BS2
L1  ..down.. L2
W1  ..down.. W2
P1  ..down.. P2
@enduml
```

#### `784e17a8866ba13c13db1d894170cfb21ee51dbb` — compile_fail (class, tier 4)

- CSR: `Error line 14 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/784e17a8866ba13c13db1d894170cfb21ee51dbb.puml`
- Element: tp=0 fp=0 fn=12 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=10 F1=0.000; missed: inheritance, association
- chrF++: 73.45
- Files: GT `data/puml_files/784e17a8866ba13c13db1d894170cfb21ee51dbb.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/784e17a8866ba13c13db1d894170cfb21ee51dbb.puml` (yes) · input `data/puml_images_1568/784e17a8866ba13c13db1d894170cfb21ee51dbb.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/784e17a8866ba13c13db1d894170cfb21ee51dbb.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 784e17a8866ba13c13db1d894170cfb21ee51dbb
' Original Path: /docs/diagramas/class_diagram_acompanhamentos.puml
' Source: World of Code

@startuml

title "Diagrama de Classe - Acompanhamentos"

enum Tamanho {
    PEQUENO
    MEDIO
    GRANDE
}

abstract class Acai << abstract >>{
    #String descricao
    #Tamanho tamanho
    +{abstract} double getPreco()
    + String getDescricao()
    + Tamanho getTamanho()
}

note left of Acai::"getPreco()"
Método abstrato que deve ser
implmentado por toda Classe
que herda de <b>Acai</b>
end note

class AcaiNaBarca
class AcaiNaTigela
class AcaiNoCopo

class Morango{
    -double preco
    +double getPreo()
}

class AcaiNaBarcaComMorango{
    -AcaiNaBarca acaiNaBarca
    -Morango morango
}

class AcaiNaTigelaComMorango{
    -AcaiNaTigela AcaiNaTigela
    -Morango morango
}

class AcaiNoCopoComMorango{
    -AcaiNoCopo AcaiNoCopo
    -Morango morango
}

class AcaiNaBarcaComMorangoELeiteEmPo{
    -AcaiNaBarca acaiNaBarca
    -Morango morango
    -LeiteEmPo leiteEmPo
}

class Morango{
    -double preco
    +double getPreco()
}

class LeiteEmPo{
    -double preco
    +double getPreco()
}

Acai <|-- AcaiNaBarca
Acai <|-- AcaiNaTigela
Acai <|-- AcaiNoCopo
Acai <|-- AcaiNaBarcaComMorango
Acai <|-- AcaiNaTigelaComMorango
Acai <|-- AcaiNoCopoComMorango
Acai <|-- AcaiNaBarcaComMorangoELeiteEmPo

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
title Diagrama de Classe - Acompanhamentos

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam linetype ortho

note left of Acai
Método abstrato que deve ser
implementado por toda Classe
que herda de Acai
end note

abstract class Acai <<abstract>> {
  String descricao
  Tamanho tamanho
  {abstract} double getPreco()
  String getDescricao()
  Tamanho getTamanho()
}

enum Tamanho {
  PEQUENO
  MEDIO
  GRANDE
}

class AcaiNaBarca
class AcaiNaTigela
class AcaiNoCopo

class Morango {
  double preco
  double preco
  double getPre()
  double getPreco()
}

class LeiteEmPo {
  double preco
  double getPreco()
}

class AcaiNaBarcaComMorango {
  AcaiNaBarca acaiNaBarca
  Morango morango
}

class AcaiNaTigelaComMorango {
  AcaiNaTigela AcaiNaTigela
  Morango morango
}

class AcaiNoCopoComMorango {
  AcaiNoCopo AcaiNoCopo
  Morango morango
}

class AcaiNaBarcaComMorangoELeiteEmPo {
  AcaiNaBarca acaiNaBarca
  Morango morango
  LeiteEmPo leiteEmPo
}

AcaiNaBarca --|> Acai
AcaiNaTigela --|> Acai
AcaiNoCopo --|> Acai

AcaiNaBarcaComMorango --|> Acai
AcaiNaTigelaComMorango --|> Acai
AcaiNoCopoComMorango --|> Acai
AcaiNaBarcaComMorangoELeiteEmPo --|> Acai

AcaiNaBarcaComMorango --> AcaiNaBarca
AcaiNaBarcaComMorango --> Morango

AcaiNaTigelaComMorango --> AcaiNaTigela
AcaiNaTigelaComMorango --> Morango

AcaiNoCopoComMorango --> AcaiNoCopo
```

#### `880c4bc548f9e57bcce86d0e90a558cd9dad31d5` — compile_fail (sequence, tier 2)

- CSR: `Error line 23 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/880c4bc548f9e57bcce86d0e90a558cd9dad31d5.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: message
- chrF++: 67.45
- Files: GT `data/puml_files/880c4bc548f9e57bcce86d0e90a558cd9dad31d5.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/880c4bc548f9e57bcce86d0e90a558cd9dad31d5.puml` (yes) · input `data/puml_images_1568/880c4bc548f9e57bcce86d0e90a558cd9dad31d5.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/880c4bc548f9e57bcce86d0e90a558cd9dad31d5.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 880c4bc548f9e57bcce86d0e90a558cd9dad31d5
' Original Path: /docs/US/US14/US014_SD_getListFromExternalModule(fileName).puml
' Source: World of Code

@startuml
autonumber

skinparam titleFontSize 25


participant "store: SnsUserStore " as store
participant "<<interface>>\n:LoadSnsUsersFromExternalSource" as externalSource
participant ":List<SnsUserDTO>" as listDTO

title : SD_getListFromExternalModule(fileName)
'1'
[o-> store : getListFromExternalModule(fileName)
activate store
'2'
store -> store : className = getClassName(fileName)
activate store
deactivate store

'5'
store -> externalSource : dtoList = readFileFromExternalSource(fileName)

activate externalSource

'6'
externalSource --> listDTO **: create()
note over externalSource
 <w:#FFAAAA>multiple interactions in the externalSource to extract a list of SnsUserDTO</w>
end note
deactivate externalSource

'7'
[<-- store : return dtoList

deactivate store















@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title SD_getListFromExternalModule(fileName)

hide footbox
skinparam sequenceMessageAlign left
skinparam ParticipantPadding 40
skinparam BoxPadding 10

actor " " as caller

participant "store: SnsUserStore" as store
participant "<<interface>>\n:LoadSnsUsersFromExternalSource" as loader
participant ":List<SnsUserDTO>" as list

caller -> store : 1 getListFromExternalModule(fileName)
activate store

store -> store : 2 className = getClassName(fileName)

store -> loader : 3 dtoList = readFileFromExternalSource(fileName)
activate loader

loader ..> list : 4 create()

note over loader, list
multiple interactions in the externalSource to extract a list of SnsUserDTO
end note

deactivate loader

store --> caller : 5 return dtoList
deactivate store

@enduml
```

#### `a3716c3d98cce05fe2a292cf86bf6bc243cd15bf` — compile_fail (sequence, tier 4)

- CSR: `Error line 56 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/a3716c3d98cce05fe2a292cf86bf6bc243cd15bf.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=19 F1=0.000; missed: message
- chrF++: 36.37
- Files: GT `data/puml_files/a3716c3d98cce05fe2a292cf86bf6bc243cd15bf.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/a3716c3d98cce05fe2a292cf86bf6bc243cd15bf.puml` (yes) · input `data/puml_images_1568/a3716c3d98cce05fe2a292cf86bf6bc243cd15bf.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/a3716c3d98cce05fe2a292cf86bf6bc243cd15bf.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: a3716c3d98cce05fe2a292cf86bf6bc243cd15bf
' Original Path: /docs/sequence_close_server.uml
' Source: World of Code

@startuml
box "Client"
	participant client
	participant tcpclient
end box
box "Server"
	participant tcpserver
	participant server
end box

server -> tcpserver : listen
activate tcpserver  #0066FF
hnote over tcpserver #0066FF : LISTEN
	

client -> tcpclient : connect
activate client

activate tcpclient #009999
deactivate tcpserver
tcpclient -> tcpserver : SYN
hnote over tcpclient #009999 : SYN-SENT
hnote over tcpserver #0099FF : SYN-RECEIVED
activate tcpserver  #0099FF

tcpserver -> tcpclient : SYN, ACK
deactivate tcpclient
deactivate tcpserver

tcpclient -> tcpserver : ACK
hnote over tcpclient #ADD1B2 : ESTABLISHED
hnote over tcpserver #ADD1B2 : ESTABLISHED
activate tcpclient #ADD1B2
activate tcpserver #ADD1B2
deactivate client


tcpserver -> server : EPOLLIN
activate server
server -> tcpserver : write
tcpserver -> tcpclient : PSH, ACK
tcpclient -> tcpserver : ACK
tcpclient -> client : EPOLLIN
activate client
client -> tcpclient : read
deactivate client

deactivate tcpserver
server -> tcpserver : close
activate tcpserver 	#B4A7E5
hnote over tcpserver #B4A7E5 : FIN_WAIT1
deactivate tcpclient
tcpserver -> tcpclient : FIN, ACK
activate tcpclient #FF99FF
deactivate tcpserver
hnote over tcpclient #FF99FF : CLOSE_WAIT
tcpclient -> tcpserver : ACK
deactivate server
activate tcpserver #FF9966
hnote over tcpserver #FF9966 : FIN_WAIT2
tcpclient -> client : EPOLLRDHUP
deactivate tcpclient #FF00FF
activate client
client -> tcpclient : close
hnote over tcpclient #FF00FF : LAST_ACK

activate tcpclient #FF00FF
tcpclient ->tcpserver : FIN




deactivate tcpserver
tcpserver -> tcpclient : ACK

deactivate tcpclient
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam shadowing false
skinparam sequence {
  ParticipantPadding 40
  BoxPadding 20
  LifeLineBorderColor #888888
  LifeLineBorderThickness 1
  LifeLineBackgroundColor transparent
  MessageAlign center
  ArrowColor #000000
  ArrowThickness 1
  ActorBorderColor #666666
  ParticipantBorderColor #666666
  ParticipantBackgroundColor #E9E9F2
}

hide footbox

box "Client" #DDDDDD
participant client as C
participant tcpclient as TC
end box

box "Server" #DDDDDD
participant tcpserver as TS
participant server as S
end box

activate C #FFFFFF
C -> TC : connect
deactivate C

activate TC #0B8F86
note over TC #0B8F86
SYN-SENT
end note

TC -> TS : SYN

activate TS #1E88E5
note over TS #1E88E5
LISTEN
end note

S -> TS : listen

note over TS #4FC3F7
SYN-RECEIVED
end note

TS -> TC : SYN, ACK
TC -> TS : ACK

deactivate TC
activate TC #BFE6C6
note over TC #CFE8CF
ESTABLISHED
end note

deactivate TS
activate TS #BFE6C6
note over TS #CFE8CF
ESTABLISHED
end note

TS -> S : EPOLLIN
S -> TS : write

TS -> TC : PSH, ACK
TC -> TS : ACK

C <- TC : EPOLLIN
C -> TC : read

S -> TS : close

deactivate TS
activate TS #B9A7E6
note over TS #B9A7E6
```

#### `a4ace769617f9198bb8eb533e526af564df13977` — compile_fail (sequence, tier 3)

- CSR: `Error line 28 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/a4ace769617f9198bb8eb533e526af564df13977.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 43.08
- Files: GT `data/puml_files/a4ace769617f9198bb8eb533e526af564df13977.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/a4ace769617f9198bb8eb533e526af564df13977.puml` (yes) · input `data/puml_images_1568/a4ace769617f9198bb8eb533e526af564df13977.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/a4ace769617f9198bb8eb533e526af564df13977.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a4ace769617f9198bb8eb533e526af564df13977
' Original Path: /starter-auth/docs/puml/user_authorization_code.puml
' Source: World of Code

@startuml

participant "接入平台的前端页"
participant "权限中心登录页"
participant "starter-auth(权限中心)"
database "auth数据库"
database "redis"

"接入平台的前端页" -> "权限中心登录页" : \
未登录的请求自动重定向

"权限中心登录页" -> "starter-auth(权限中心)" : \
获取用户登录授权码接口

"starter-auth(权限中心)" -> "auth数据库" : \
查询用户信息

"starter-auth(权限中心)" <- "auth数据库" : \
返回用户信息

"starter-auth(权限中心)" -> "starter-auth(权限中心)" : \
验证用户密码\n\
不匹配则响应：登陆失败\n\
创建授权码

"starter-auth(权限中心)" --> "redis" : \
异步：缓存授权码关联的用户信息60s

"权限中心登录页" <- "starter-auth(权限中心)" : \
响应授权码和重定向页面

"接入平台的前端页" <- "权限中心登录页"   : \
重定向到接入服务指定的前端页\n\
在请求路径中带上用户登录授权码\n\
路径如：https://www.xxx.com/?aucoCode=xxxxxxxxxxxx

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
hide footbox
skinparam shadowing false
skinparam sequence {
  ParticipantPadding 40
  BoxPadding 10
  MessageAlign left
}

participant "接入平台的前端页" as FE
participant "权限中心登录页" as LOGIN
participant "starter-auth(权限中心)" as AUTH
database "auth数据库" as DB
database "redis" as REDIS

FE -> LOGIN : 未登录的请求自动重定向
LOGIN -> AUTH : 获取用户登录授权码接口
AUTH -> DB : 查询用户信息
DB --> AUTH : 返回用户信息

note right of AUTH
验证用户密码
不匹配则响应：登陆失败
创建授权码
end note

AUTH -> AUTH : 
AUTH ..> REDIS : 异步：缓存授权码关联的用户信息60s
AUTH --> LOGIN : 响应授权码和重定向页面

LOGIN --> FE : 重定向到接入服务指定的前端页\n在请求路径中带上用户登录授权码\n路径如： https://www.xxx.com/?aucoCode=xxxxxxxxxxxx

@enduml
```
```

#### `a87c8d584bf40e45101b8425d63c9ac5fb06c7d6` — compile_fail (class, tier 3)

- CSR: `Error line 20 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/a87c8d584bf40e45101b8425d63c9ac5fb06c7d6.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: inheritance, dependency
- chrF++: 57.38
- Files: GT `data/puml_files/a87c8d584bf40e45101b8425d63c9ac5fb06c7d6.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/a87c8d584bf40e45101b8425d63c9ac5fb06c7d6.puml` (yes) · input `data/puml_images_1568/a87c8d584bf40e45101b8425d63c9ac5fb06c7d6.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/a87c8d584bf40e45101b8425d63c9ac5fb06c7d6.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a87c8d584bf40e45101b8425d63c9ac5fb06c7d6
' Original Path: /uml/booknote-class.plantuml
' Source: World of Code

@startuml
scale 2
page 1x1
title
    在键盘上添加输入框的实现方式
    创建时间: <2019-09-11 21:17>
    endtitle
    left header
        设计到两个知识点
        1. 半遮罩层
        2. 键盘监听事件
        3. 自动布局实现动态控制TextView的高度
    endheader
    class "SuperAlertBgView" as baseView {
        --属性组 --
        NSString *placeholder;
        void(^ComfirmHandler)(NSString *);
        UIView *bgView;

        __ 函数组__
        -(void)show;
        -(void)hide;
    }
    note left of baseView 
        封装半透明遮罩层,和展示隐藏逻辑实现
    end note
    class "KeyBoardFieldView" as keyBoardField {
        --属性组 --
        __ 函数组__
    }
    baseView <|-- keyBoardField:继承<
    @enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam shadowing false
skinparam classAttributeIconSize 0
skinparam class {
  BackgroundColor #f7f7f7
  BorderColor #333333
  ArrowColor #333333
  HeaderBackgroundColor #f7f7f7
}

title 在键盘上添加输入框的实现方式\n创建时间：<2019-09-11 21:17>

note top
设计到两个知识点
1. 半遮罩层
2. 键盘监听事件
3. 自动布局实现动态控制TextView的高度
end note

class SuperAlertBgView <<C>> {
== 属性组 ==
NSString *placeholder;
void(^ComfirmHandler)(NSString *);
UIView *bgView;

== 函数组 ==
■ (void)show;
■ (void)hide;
}

class KeyBoardFieldView <<C>> {
== 属性组 ==

== 函数组 ==
}

KeyBoardFieldView -up-|> SuperAlertBgView : 继承<

note left of SuperAlertBgView
封装半透明遮罩层,和展示隐藏逻辑实现
end note
@enduml
```

#### `aa416d26b5e8ab9e0af098522a5e026c5a67fe35` — compile_fail (class, tier 4)

- CSR: `Error line 72 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/aa416d26b5e8ab9e0af098522a5e026c5a67fe35.puml`
- Element: tp=0 fp=0 fn=10 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=12 F1=0.000; missed: association
- chrF++: 44.02
- Files: GT `data/puml_files/aa416d26b5e8ab9e0af098522a5e026c5a67fe35.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/aa416d26b5e8ab9e0af098522a5e026c5a67fe35.puml` (yes) · input `data/puml_images_1568/aa416d26b5e8ab9e0af098522a5e026c5a67fe35.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/aa416d26b5e8ab9e0af098522a5e026c5a67fe35.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: aa416d26b5e8ab9e0af098522a5e026c5a67fe35
' Original Path: /docs/SPRINT_005/DDD_Aggregates_v4_MacroVision.puml
' Source: World of Code

@startuml
'https://plantuml.com/class-diagram

'SWitCH G4 THEME
'
'COLORS
'Blue #application
'Pink #pink
'Red #salmon
'Yellow #khaki
'Green #technology
'
'DEFAULTS

hide members
hide circle
skinparam linetype ortho

skinparam minClassWidth 200
skinparam nodesep 20
skinparam ranksep 20
skinparam padding 0
skinparam roundCorner 8




skinparam package {
    backgroundColor white
    borderColor grey
    shadowing false
    fontStyle normal
    fontSize 16
    borderThickness 0.5
    fontColor #aaa
    stereotypeFontSize 10
    stereotypeFontColor lightGrey
}

skinparam class {
    stereotypeFontSize 10
    fontSize 16
    fontName Helvetica
    arrowColor black
    arrowThickness 1
    attributeIconSize 0
    borderThickness 0.5
}

skinparam class<<AGGREGATE ROOT>> {
    borderColor black
    backgroundColor #eee
}

skinparam class<<ENTITY>> {
    borderColor yellow
    backgroundColor #khaki
}

skinparam class<<VALUE OBJECT>> {
    borderColor green
    backgroundColor #technology
}



skinparam note {
    fontSize 14
    fontName Helvetica
    borderColor black
    borderThickness 0.5
    backgroundColor AliceBlue
}


'TITLE ON TOP
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam shadowing false
skinparam packageStyle rectangle
skinparam defaultTextAlignment center
skinparam wrapWidth 200
skinparam PackageBorderColor #999999
skinparam PackageFontColor #999999
skinparam PackageFontSize 22
skinparam PackageBackgroundColor white
skinparam ClassBackgroundColor #F2F2F2
skinparam ClassBorderColor #333333
skinparam ClassFontColor #000000
skinparam ClassFontSize 22
skinparam ArrowColor #000000
skinparam ArrowThickness 2

hide empty members

package "Task" <<AGGREGATE>> as P_Task {
  class "Task" as Task <<AGGREGATE ROOT>> <<ENTITY>>
}

package "Sprint" <<AGGREGATE>> as P_Sprint {
  class "Sprint" as Sprint <<AGGREGATE ROOT>> <<ENTITY>>
}

package "UserStory" <<AGGREGATE>> as P_UserStory {
  class "UserStory" as UserStory <<AGGREGATE ROOT>> <<ENTITY>>
}

package "Project" <<AGGREGATE>> as P_Project {
  class "Project" as Project <<AGGREGATE ROOT>> <<ENTITY>>
  class "Resource" as ProjectResource <<AGGREGATE ROOT>> <<ENTITY>>
}

package "Typology" <<AGGREGATE>> as P_Typology {
  class "Typology" as Typology <<AGGREGATE ROOT>> <<ENTITY>>
}

package "ProfileRequest" <<AGGREGATE>> as P_ProfileRequest {
  class "ProfileRequest" as ProfileRequest <<AGGREGATE ROOT>> <<ENTITY>>
}

package "Profile" <<AGGREGATE>> as P_Profile {
  class "Profile" as Profile <<AGGREGATE ROOT>> <<ENTITY>>
}

package "Resource" <<AGGREGATE>> as P_Resource {
  class "Resource" as Resource <<AGGREGATE ROOT>> <<ENTITY>>
}

package "User" <<AGGREGATE>> as P_User {
  class "User" as User <<AGGREGATE ROOT>> <<ENTITY>>
}

' Layout hints (approximate)
P_Task -down- P_Sprint
P_UserStory -right- P_Sprint
P_Typology -right- P_Project
P_ProfileRequest -right- P_Profile
P_Profile -right- P_Resource
P_Profile -down- P_User

' Relationships (as shown by arrows)
Sprint --> UserStory
Profile --> Typology
Profile --> User
ProjectResource --> Resource
Resource --> User

' Right-side vertical bus with multiple incoming arrows (approximated with a hidden node)
rectangle " " as Bus #white
Bus -[hidden]right- P_Project
Bus -[hidden]right- P_Sprint
Bus -[hidden]right- P_Task
Bus -[hidden]right- P_Resource
Bus -[hidden]right- P_User

Task --> Bus
Sprint --> Bus
```

#### `b21a6faaf6a180c501e0aba4b0056672ede1ea2d` — compile_fail (class, tier 2)

- CSR: `Error line 25 in file: data/csr/gpt-5.2-2025-12-11_20260613T154248Z/extracted/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: inheritance, aggregation, association
- chrF++: 74.49
- Files: GT `data/puml_files/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.puml` (yes) · input `data/puml_images_1568/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: b21a6faaf6a180c501e0aba4b0056672ede1ea2d
' Original Path: /Documentation/plantuml/Grid/BuildingTile.puml
' Source: World of Code

@startuml
class BuildingTile {
    + IsLocationValid : bool <<get>>
    + BuildingTile(type:StructureType, facing:Facing)
    + <<override>> ToString() : string
}
class "Dictionary`2"<T1,T2> {
}
enum StructureType {
    House= 0,
    Office= 1,
    TestStruct= 2,
}
Tile <|-- BuildingTile
BuildingTile o-> "ModelLookup<StructureType,string>" "Dictionary`2"
BuildingTile --> "structure" StructureType
BuildingTile +-- StructureType
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0

class Tile

class BuildingTile {
  + IsLocationValid : bool <<get>>
  --
  + BuildingTile(type:StructureType, facing:Facing)
  + <<override>> ToString() : string
}

enum StructureType {
  House=0,
  Office=1,
  TestStruct=2,
}

class "Dictionary`2" as Dictionary2

note right of Dictionary2
ModelLookup<StructureType,string>
end note

note top right of Dictionary2
T1,T2
end note

Tile <|-- BuildingTile

BuildingTile o--> Dictionary2

BuildingTile --> StructureType : structure
@enduml
```

#### outcome: compiled_low_structural

#### `0b04c29eb903fbeb733c3ec5c0f834ffb7a1dadf` — compiled_low_structural (class, tier 4)

- Element: tp=5 fp=22 fn=6 F1=0.263; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=4 fp=24 fn=9 F1=0.195; missed: composition, dependency; extra: inheritance, aggregation, dependency
- chrF++: 56.63
- Files: GT `data/puml_files/0b04c29eb903fbeb733c3ec5c0f834ffb7a1dadf.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/0b04c29eb903fbeb733c3ec5c0f834ffb7a1dadf.puml` (yes) · input `data/puml_images_1568/0b04c29eb903fbeb733c3ec5c0f834ffb7a1dadf.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/0b04c29eb903fbeb733c3ec5c0f834ffb7a1dadf.png` (yes)

#### `0bffda3c561066aa0dda7f556b2ce91406230f86` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=1 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 54.51
- Files: GT `data/puml_files/0bffda3c561066aa0dda7f556b2ce91406230f86.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/0bffda3c561066aa0dda7f556b2ce91406230f86.puml` (yes) · input `data/puml_images_1568/0bffda3c561066aa0dda7f556b2ce91406230f86.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/0bffda3c561066aa0dda7f556b2ce91406230f86.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 0bffda3c561066aa0dda7f556b2ce91406230f86
' Original Path: /docs/javadocs/soen6441riskgame/enums/ConquestMapPart.puml
' Source: World of Code

@startuml

skinparam svgLinkTarget _parent
skinparam linetype ortho
set namespaceSeparator none
enum "<b><size:14>ConquestMapPart</b>\n<size:10>soen6441riskgame.enums" as soen6441riskgame.enums.ConquestMapPart  [[../../soen6441riskgame/enums/ConquestMapPart.html{soen6441riskgame.enums.ConquestMapPart}]] {
-String part
-ConquestMapPart(String part)
{static} +ConquestMapPart values()
{static} +ConquestMapPart valueOf(String name)
+String getPart()
{static} +ConquestMapPart fromString(String part)
}



@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0

class "ConquestMapPart\nsoen6441riskgame.enums" << (E,#f4a08a) E >> {
  - String part
  --
  - ConquestMapPart(String part)
  {static} ConquestMapPart[] values()
  {static} ConquestMapPart valueOf(String name)
  + String getPart()
  {static} ConquestMapPart fromString(String part)
}
@enduml
```

#### `13535b2cbd8a085a55557cd59dee9ac4e2096202_20` — compiled_low_structural (sequence, tier 1)

- Element: tp=5 fp=5 fn=0 F1=0.667; type-acc matched=5 correct=0 excluded=0
- Relationship: tp=0 fp=9 fn=0 F1=0.000; extra: association
- chrF++: 27.28
- Files: GT `data/puml_files/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.puml` (yes) · input `data/puml_images_1568/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 13535b2cbd8a085a55557cd59dee9ac4e2096202
' Original Path: /apex-Walle钱包系统.wsd
' Source: World of Code

@startuml
scale 3
title uc2_6活动执行时序图
actor 管理员 as adm
participant web 
participant sever as se 
database 活动快照表 as kz
database 活动结果表 as jg
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title uc2_6活动执行时序图

skinparam backgroundColor white
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 28

skinparam actor {
  BackgroundColor #E6E6F2
  BorderColor #000000
}

skinparam rectangle {
  BackgroundColor #E6E6F2
  BorderColor #000000
  RoundCorner 12
}

skinparam database {
  BackgroundColor #E6E6F2
  BorderColor #000000
}

left to right direction

actor "管理员" as A1
rectangle "web" as W1
rectangle "sever" as S1
database "活动快照表" as D1
database "活动结果表" as D2

actor "管理员" as A2
rectangle "web" as W2
rectangle "sever" as S2
database "活动快照表" as D3
database "活动结果表" as D4

@enduml
```

#### `2830a2eabd8ada9ad42a0d10eeeacad0dc53a202` — compiled_low_structural (sequence, tier 4)

- Element: tp=0 fp=14 fn=14 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=38 fn=40 F1=0.000; missed: message; extra: message
- chrF++: 44.31
- Files: GT `data/puml_files/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.puml` (yes) · input `data/puml_images_1568/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.png` (yes)

#### `42fc85c2e1d580aedd56311d963ecb8df37a5cb1` — compiled_low_structural (class, tier 2)

- Element: tp=2 fp=0 fn=0 F1=1.000; type-acc matched=2 correct=1 excluded=1
- Relationship: tp=0 fp=1 fn=0 F1=0.000; extra: dependency
- chrF++: 87.71
- Files: GT `data/puml_files/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.puml` (yes) · input `data/puml_images_1568/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 42fc85c2e1d580aedd56311d963ecb8df37a5cb1
' Original Path: /shacl-diagram/src/specs/07-maxCount/expected.iuml
' Source: World of Code

@startuml
class "ex:MyShapemaxCount" 
"ex:MyShapemaxCount" : age : integer : maxCount[0..1]


note as N1
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/ns#> .

ex:MyShapemaxCount a sh:NodeShape ;
sh:targetClass ex:Person ;
sh:property[
  sh:path ex:age ;
  sh:maxCount 1 ;
  sh:datatype xsd:integer ;
] .
end note


hide circle
hide empty members
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam shadowing false
skinparam classAttributeIconSize 0

class "ex:MyShapemaxCount" as MyShapemaxCount {
  age : integer : maxCount[0..1]
}

note right
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/ns#> .

ex:MyShapemaxCount a sh:NodeShape ;
sh:targetClass ex:Person ;
sh:property[
  sh:path ex:age ;
  sh:maxCount 1 ;
  sh:datatype xsd:integer ;
] .
end note
@enduml
```

#### `6c7324c7eaeb23cd5644654ea022ca212ecd24ea` — compiled_low_structural (sequence, tier 1)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=4 fn=4 F1=0.000; missed: message; extra: message
- chrF++: 47.69
- Files: GT `data/puml_files/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · input `data/puml_images_1568/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 6c7324c7eaeb23cd5644654ea022ca212ecd24ea
' Original Path: /Documentação/1201384/US1005/US1005_SSD.puml
' Source: World of Code

@startuml
actor SalesClerk as adm
participant "//<<presentation>>//\nDefineNewCategoryUI" as ui

autonumber

adm-->ui: Define new category

activate ui

ui-->adm: asks user information

adm-->ui: Code, Description

ui-->adm: displayCategoryInfo

deactivate ui
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
hide footbox
skinparam shadowing false
skinparam sequence {
  LifeLineBorderColor #666666
  LifeLineBackgroundColor #FFFFFF
  ParticipantBorderColor #666666
  ParticipantBackgroundColor #E6E6F2
  ActorBorderColor #666666
  ActorBackgroundColor #E6E6F2
  ArrowColor #333333
  ArrowThickness 2
  MessageAlign left
}

actor SalesClerk as SC
participant "«presentation»\nDefineNewCategoryUI" as UI

SC ->> UI : 1 Define new category
UI ->> SC : 2 asks user information
SC ->> UI : 3 Code, Description
UI ->> SC : 4 displayCategoryInfo

@enduml
```

#### `75d17323e3f57e506be51b5455aa97ae89d8c5cc` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=3 fn=3 F1=0.250; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=6 fn=6 F1=0.000; missed: message; extra: message
- chrF++: 61.07
- Files: GT `data/puml_files/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · input `data/puml_images_1568/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 75d17323e3f57e506be51b5455aa97ae89d8c5cc
' Original Path: /input/images-source/Implementing-PDQm-as-a-gateway.plantuml
' Source: World of Code

@startuml
hide footbox

Participant "Patient\nDemographics\nConsumer" as Client1
box "PDQm Implementation\ngrouped as a façade "
    Participant "Patient\n Demographics\nSupplier" as Server1
    Participant "Patient\n Demographics\nConsumer" as Client2
endbox
Participant "Patient\n Demographics\nSupplier" as Server2

Client1 -> Server1: Mobile Patient\nDemographics\nQuery [ITI-78]
activate Client1
activate Server1
Server1 --> Client2: Internal processing
activate Client2
activate Server2
Client2 -> Server2: Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]
Client2 <- Server2: [ITI-21] or [ITI-47] Response
Server1 <-- Client2: Internal processing
deactivate Client2
deactivate Server2
Client1 <- Server1: [ITI-78] Response
deactivate Client2
deactivate Server1

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
hide footbox
skinparam backgroundColor white
skinparam sequence {
  ParticipantPadding 40
  BoxPadding 20
  LifeLineBorderColor #666666
  LifeLineBorderThickness 1
  LifeLineBackgroundColor white
  ActorBorderColor #666666
  ActorBackgroundColor #E9E9F6
  ParticipantBorderColor #666666
  ParticipantBackgroundColor #E9E9F6
  BoxBorderColor #666666
  BoxBackgroundColor #DDDDDD
  ArrowColor #333333
  ArrowThickness 1
}

participant "Patient\nDemographics\nConsumer" as PDC_left
box "PDQm Implementation\ngrouped as a façade" #DDDDDD
  participant "Patient\nDemographics\nSupplier" as PDS_facade
  participant "Patient\nDemographics\nConsumer" as PDC_facade
end box
participant "Patient\nDemographics\nSupplier" as PDS_right

PDC_left -> PDS_facade : Mobile Patient\nDemographics\nQuery [ITI-78]
activate PDC_left
activate PDS_facade

PDS_facade ->> PDC_facade : Internal processing
activate PDC_facade

PDC_facade -> PDS_right : Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]
activate PDS_right
PDS_right --> PDC_facade : [ITI-21] or [ITI-47] Response
deactivate PDS_right

PDC_facade ->> PDS_facade : Internal processing
deactivate PDC_facade

PDS_facade --> PDC_left : [ITI-78] Response
deactivate PDS_facade
deactivate PDC_left

@enduml
```

#### `7c320c768ad2b452a09b81e3f91305beec4280f0` — compiled_low_structural (sequence, tier 3)

- Element: tp=4 fp=1 fn=1 F1=0.800; type-acc matched=4 correct=4 excluded=0
- Relationship: tp=2 fp=8 fn=8 F1=0.200; missed: message; extra: message
- chrF++: 45.36
- Files: GT `data/puml_files/7c320c768ad2b452a09b81e3f91305beec4280f0.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/7c320c768ad2b452a09b81e3f91305beec4280f0.puml` (yes) · input `data/puml_images_1568/7c320c768ad2b452a09b81e3f91305beec4280f0.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/7c320c768ad2b452a09b81e3f91305beec4280f0.png` (yes)

#### `8bce1d211b840b53b1ecdec7fd054e684c345b2d` — compiled_low_structural (sequence, tier 3)

- Element: tp=2 fp=2 fn=2 F1=0.500; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=11 fn=11 F1=0.000; missed: message; extra: message
- chrF++: 68.13
- Files: GT `data/puml_files/8bce1d211b840b53b1ecdec7fd054e684c345b2d.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/8bce1d211b840b53b1ecdec7fd054e684c345b2d.puml` (yes) · input `data/puml_images_1568/8bce1d211b840b53b1ecdec7fd054e684c345b2d.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/8bce1d211b840b53b1ecdec7fd054e684c345b2d.png` (yes)

#### `938e9cc0e6b8dda26422f35f30282f7d202efb9d_02` — compiled_low_structural (sequence, tier 4)

- Element: tp=1 fp=4 fn=4 F1=0.200; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=20 fn=20 F1=0.000; missed: message; extra: message
- chrF++: 62.52
- Files: GT `data/puml_files/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · input `data/puml_images_1568/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes)

#### `a33039e4fbdeb76d8d991f13075eb6aabf979e31` — compiled_low_structural (class, tier 2)

- Element: tp=0 fp=2 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=1 fn=0 F1=0.000; extra: dependency
- chrF++: 58.01
- Files: GT `data/puml_files/a33039e4fbdeb76d8d991f13075eb6aabf979e31.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/a33039e4fbdeb76d8d991f13075eb6aabf979e31.puml` (yes) · input `data/puml_images_1568/a33039e4fbdeb76d8d991f13075eb6aabf979e31.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/a33039e4fbdeb76d8d991f13075eb6aabf979e31.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: a33039e4fbdeb76d8d991f13075eb6aabf979e31
' Original Path: /northernwind/1.2-ALPHA-10/apidocs/it/tidalwave/northernwind/frontend/ui/component/gallery/spi/GalleryAdapter.puml
' Source: World of Code

@startuml
    set namespaceSeparator none
    hide empty fields
    hide empty methods

    interface "<size:14>GalleryAdapter\n<size:10>it.tidalwave.northernwind.frontend.ui.component.gallery.spi" as it.tidalwave.northernwind.frontend.ui.component.gallery.spi.GalleryAdapter [[GalleryAdapter.html]] {
        {abstract} +getExtraViewProperties(Id): ResourceProperties
        {abstract} +getInlinedScript(): String
        {abstract} +prepareCatalog(List<? extends GalleryItem>): void
        {abstract} +prepareGallery(GalleryItem, List<? extends GalleryItem>): void
        {abstract} +prepareFallbackGallery(GalleryItem, List<? extends GalleryItem>): void
        {abstract} +prepareFallbackLightbox(List<? extends GalleryItem>): void
        {abstract} +render(RenderContext): void
    }

    center footer UMLDoclet 2.0.12, PlantUML 1.2020.16
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
interface "GalleryAdapter" as GalleryAdapter << (I,#b7b0ff) >>
note top of GalleryAdapter
it.tidalwave.northernwind.frontend.ui.component.gallery.spi
end note

GalleryAdapter : + getExtraViewProperties(Id): ResourceProperties
GalleryAdapter : + getInlinedScript(): String
GalleryAdapter : + prepareCatalog(List<? extends GalleryItem>): void
GalleryAdapter : + prepareGallery(GalleryItem, List<? extends GalleryItem>): void
GalleryAdapter : + prepareFallbackGallery(GalleryItem, List<? extends GalleryItem>): void
GalleryAdapter : + prepareFallbackLightbox(List<? extends GalleryItem>): void
GalleryAdapter : + render(RenderContext): void
@enduml
```

#### `c5bb3816232672cc44f741e2b5d82d69ebdf932c` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=3 fn=1 F1=0.333; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: message; extra: message
- chrF++: 50.53
- Files: GT `data/puml_files/c5bb3816232672cc44f741e2b5d82d69ebdf932c.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/c5bb3816232672cc44f741e2b5d82d69ebdf932c.puml` (yes) · input `data/puml_images_1568/c5bb3816232672cc44f741e2b5d82d69ebdf932c.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/c5bb3816232672cc44f741e2b5d82d69ebdf932c.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: c5bb3816232672cc44f741e2b5d82d69ebdf932c
' Original Path: /doc/profiles/representation/minimal.puml
' Source: World of Code

@startuml
title Omit Representation
actor Client
participant "<&transfer> Representation" as Representation

Client -> Representation: PUT / POST / PATCH
rnote right #lightblue
  <#lightblue,lightblue>|= Header |= Value |
  | ""Prefer"" | ""return=minimal"" |
end note
Representation --> Client: 204 No Content / 201 Created
rnote left #lightgreen
  <#lightgreen,lightgreen>|= Header |= Value |
  | ""Preference-Applied"" | ""return=minimal"" |
end note
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Omit Representation

hide footbox

actor Client as C

participant "⇄ Representation" as R

note right of R #ADD8E6
<b>Header  Value</b>
Prefer  return=minimal
end note

C -> R : PUT / POST / PATCH

C <-- R : 204 No Content / 201 Created

note left of C #90EE90
<b>Header  Value</b>
Preference-Applied  return=minimal
end note

actor Client as C2
participant "⇄ Representation" as R2

@enduml
```

#### `da5358c8083486d43e592f36f3e194ccc1f9f6e0_03` — compiled_low_structural (class, tier 4)

- Element: tp=17 fp=0 fn=0 F1=1.000; type-acc matched=17 correct=14 excluded=3
- Relationship: tp=10 fp=11 fn=10 F1=0.488; missed: inheritance, composition, association; extra: inheritance, composition, dependency, association
- chrF++: 69.18
- Files: GT `data/puml_files/da5358c8083486d43e592f36f3e194ccc1f9f6e0_03.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/da5358c8083486d43e592f36f3e194ccc1f9f6e0_03.puml` (yes) · input `data/puml_images_1568/da5358c8083486d43e592f36f3e194ccc1f9f6e0_03.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/da5358c8083486d43e592f36f3e194ccc1f9f6e0_03.png` (yes)

#### `f39d1a63230c7db352af29e57065e9218c1f0a3d` — compiled_low_structural (class, tier 3)

- Element: tp=10 fp=0 fn=0 F1=1.000; type-acc matched=10 correct=10 excluded=0
- Relationship: tp=4 fp=6 fn=6 F1=0.400; missed: composition, aggregation; extra: composition, aggregation
- chrF++: 87.10
- Files: GT `data/puml_files/f39d1a63230c7db352af29e57065e9218c1f0a3d.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/f39d1a63230c7db352af29e57065e9218c1f0a3d.puml` (yes) · input `data/puml_images_1568/f39d1a63230c7db352af29e57065e9218c1f0a3d.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/f39d1a63230c7db352af29e57065e9218c1f0a3d.png` (yes)

#### `fcd65f7d8920511a96fcffe53538f6014bb6f64f` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=2 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=1 fn=1 F1=0.000; missed: inheritance; extra: inheritance
- chrF++: 37.27
- Files: GT `data/puml_files/fcd65f7d8920511a96fcffe53538f6014bb6f64f.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/fcd65f7d8920511a96fcffe53538f6014bb6f64f.puml` (yes) · input `data/puml_images_1568/fcd65f7d8920511a96fcffe53538f6014bb6f64f.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/fcd65f7d8920511a96fcffe53538f6014bb6f64f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: fcd65f7d8920511a96fcffe53538f6014bb6f64f
' Original Path: /northernwind/1.2-ALPHA-10/it-tidalwave-northernwind-modules/it-tidalwave-northernwind-core-default/testapidocs/it/tidalwave/northernwind/frontend/ui/spi/mock/MockRequestProcessor3.puml
' Source: World of Code

@startuml
    set namespaceSeparator none
    hide empty fields
    hide empty methods

    class "<size:14>MockRequestProcessor3\n<size:10>it.tidalwave.northernwind.frontend.ui.spi.mock" as it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessor3 [[MockRequestProcessor3.html]]

    class "<size:14>MockRequestProcessorSupport\n<size:10>it.tidalwave.northernwind.frontend.ui.spi.mock" as it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessorSupport [[MockRequestProcessorSupport.html]]

    it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessorSupport <|-- it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessor3

    center footer UMLDoclet 2.0.12, PlantUML 1.2020.16
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0

class "MockRequestProcessorSupport\nit.tidalwave.northernwind.frontend.ui.spi.mock" as MockRequestProcessorSupport <<C>>
class "MockRequestProcessor3\nit.tidalwave.northernwind.frontend.ui.spi.mock" as MockRequestProcessor3 <<C>>

MockRequestProcessor3 -|> MockRequestProcessorSupport
@enduml
```

#### `fff389a2f264c9d5a71da3c2e50c05082884a074` — compiled_low_structural (class, tier 3)

- Element: tp=6 fp=0 fn=0 F1=1.000; type-acc matched=6 correct=6 excluded=0
- Relationship: tp=0 fp=5 fn=5 F1=0.000; missed: inheritance; extra: inheritance
- chrF++: 81.29
- Files: GT `data/puml_files/fff389a2f264c9d5a71da3c2e50c05082884a074.puml` (yes) · pred `data/runs/gpt-5.2-2025-12-11_20260613T154248Z/fff389a2f264c9d5a71da3c2e50c05082884a074.puml` (yes) · input `data/puml_images_1568/fff389a2f264c9d5a71da3c2e50c05082884a074.png` (yes) · render `data/csr/gpt-5.2-2025-12-11_20260613T154248Z/png/fff389a2f264c9d5a71da3c2e50c05082884a074.png` (yes)

### Claude Opus 4.6

#### outcome: compile_fail

#### `2ba4e7f17f9f45f359569c1285dafccb3b4f54ab` — compile_fail (sequence, tier 2)

- CSR: `Error line 15 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: message
- chrF++: 70.56
- Files: GT `data/puml_files/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml` (yes) · input `data/puml_images_1568/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 2ba4e7f17f9f45f359569c1285dafccb3b4f54ab
' Original Path: /docs/edgemere/sa/spm/usecases/managesecurityprofiles/MonitorSecurityProfile.puml
' Source: World of Code

@startuml

actor "SecurityEngineer"


entity EventBus

box Security Profile Manager #cc8888
    boundary spm #white
end box


box Software Defined Infrastructure #cccc88
            participant storageresource
    end box

box Security Profile Manager #cc8888
    end box


"SecurityEngineer" -> spm: Monitor Security Profile

    spm -> "storageresource": create (name: secProfileMSP,file: ./templates/secprofile.yml)

    "storageresource" --/ EventBus: securityprofile.create

    spm -> "securityprofile": status (name: secProfileMSP)

    "securityprofile" --/ EventBus: securityprofile.status



@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

actor SecurityEngineer
participant EventBus
box "Security Profile Manager" #CC8888
participant spm
end box
box "Software Defined Infrastructure" #BBBB77
participant storageresource
participant securityprofile
end box

SecurityEngineer -> spm : Monitor Security Profile
spm -> securityprofile : create (name: secProfileMSP,file: ./templates/secprofile.yml)
spm <.. EventBus : securityprofile.create
spm -> securityprofile : status (name: secProfileMSP)
spm <.. EventBus : securityprofile.status

@enduml
```
```

#### `50efbc2a904f22fbb497d5a040e14bc419bebf26` — compile_fail (class, tier 3)

- CSR: `Error line 30 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/50efbc2a904f22fbb497d5a040e14bc419bebf26.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: inheritance, dependency
- chrF++: 61.86
- Files: GT `data/puml_files/50efbc2a904f22fbb497d5a040e14bc419bebf26.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/50efbc2a904f22fbb497d5a040e14bc419bebf26.puml` (yes) · input `data/puml_images_1568/50efbc2a904f22fbb497d5a040e14bc419bebf26.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/50efbc2a904f22fbb497d5a040e14bc419bebf26.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 50efbc2a904f22fbb497d5a040e14bc419bebf26
' Original Path: /uml/controller-class.puml
' Source: World of Code

@startuml
hide empty members
namespace controller {
    interface Controller {
        + execute(args : json) : json
    }
    class Factory {
        + create(name : string) : Controller
    }
    class Amount
    class Transfer
    class TransferSend

    Controller <|.. Amount
    Controller <|.. Transfer
    Controller <|.. TransferSend
    Amount <.. Factory : create
    Transfer <.. Factory : create
    TransferSend <.. Factory : create
    model.User <.. Amount
    Amount ..> view.Amount
}
namespace view {
    class Amount
}
namespace model {
    class User
}
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

package "controller" {
    package "model" as controller_model {
        class User
    }

    interface Controller {
        + execute(args : json) : json
    }

    class Amount

    class TransferSend

    class Transfer

    package "view" as controller_view {
        class "Amount" as ViewAmount
    }

    class Factory {
        + create(name : string) : Controller
    }

    TransferSend ..|> Controller
    Transfer ..|> Controller
    Amount ..|> Controller

    Amount ..> User : 

    TransferSend ..> User : 

    Factory ..> Amount : create
    Factory ..> TransferSend : create
    Factory ..> Transfer : create

    Amount ..> ViewAmount
}

package "view" as ext_view {
    class "Amount" as ExtViewAmount
}

package "model" as ext_model {
    class "User" as ExtModelUser
}

@enduml
```
```

#### `5ff302fdb03929946120216bea43c4393359b490` — compile_fail (sequence, tier 4)

- CSR: `Error line 66 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/5ff302fdb03929946120216bea43c4393359b490.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=24 F1=0.000; missed: message
- chrF++: 80.13
- Files: GT `data/puml_files/5ff302fdb03929946120216bea43c4393359b490.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/5ff302fdb03929946120216bea43c4393359b490.puml` (yes) · input `data/puml_images_1568/5ff302fdb03929946120216bea43c4393359b490.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/5ff302fdb03929946120216bea43c4393359b490.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 5ff302fdb03929946120216bea43c4393359b490
' Original Path: /design/ReservationSequence.puml
' Source: World of Code

@startuml
actor User
participant Frontend
box "Clerk" #LightBlue
participant ReservationService
participant TicketRepository
end box
queue EventBus
box "TicketMaster" #LightBlue
participant TicketMasterService
participant TicketMasterRepository
end box
participant OrderManager
database DB

User --> Frontend: reserve button
Frontend -> ReservationService: POST /reservations

note left
    POST /reservations
    {
        tickets: [
            {
                programId: 1,
                sectorId: 1,
                seatId: 5
            },
            {
                programId: 1,
                sectorId: 1,
                seatId: 6
            }
        ]
    }
end note

activate ReservationService
    ReservationService --> TicketRepository: validate tickets
    ReservationService <-- TicketRepository
    alt invalid
        ReservationService --> Frontend: ReservationRejected: code, reason
    else valid
        ReservationService --> ReservationService: createReservationCommand
        note left
            CreateReservation {
                reservation: {
                    reservationId: "abc123"
                    tickets: [
                        {
                            programId: 1,
                            sectorId: 1,
                            seatId: 5
                        },
                        {
                            programId: 1,
                            sectorId: 1,
                            seatId: 6
                        }
                    ]
                }
            }
        end note
        ReservationService --> EventBus: publish CreateReservation
        ReservationService --> Frontend: ReservationAccepted: reservationId
    end
deactivate ReservationService

    EventBus --> TicketMasterService: handle CreateReservation
activate TicketMasterService

    TicketMasterService --> TicketMasterRepository: check if all tickets are FREE
    TicketMasterService <-- TicketMasterRepository

    alt ticket status = FREE
        TicketMasterService --> TicketMasterRepository: set status of tickets to RESERVED
        TicketMasterService <-- TicketMasterRepository:
```

Prediction PlantUML (truncated):
```plantuml
@startuml

actor User
participant Frontend
box "Clerk" #LightCyan
participant ReservationService
participant TicketRepository
end box
participant EventBus
box "TicketMaster" #LightCyan
participant TicketMasterService
participant TicketMasterRepository
end box
participant OrderManager
database DB

User -> Frontend : reserve button

note left of Frontend
POST /reservations
{
  tickets: [
    {
      programId: 1,
      sectorId: 1,
      seatId: 5
    },
    {
      programId: 1,
      sectorId: 1,
      seatId: 6
    }
  ]
}
end note

Frontend -> ReservationService : POST /reservations

ReservationService -> TicketRepository : validate tickets

alt [invalid]
ReservationService <-- TicketRepository
Frontend <-- ReservationService : ReservationRejected: code, reason
else [valid]

note left of ReservationService #LightYellow
CreateReservation {
  reservation: {
    reservationId: "abc123"
    tickets: [
      {
        programId: 1,
        sectorId: 1,
        seatId: 5
      },
      {
        programId: 1,
        sectorId: 1,
        seatId: 6
      }
    ]
  }
}
end note

ReservationService <.. TicketRepository : createReservationCommand

ReservationService -> EventBus : publish CreateReservation

Frontend <-- ReservationService : ReservationAccepted: reservationId

end

EventBus -> TicketMasterService : handle CreateReservation

TicketMasterService -> TicketMasterRepository : check if all tickets are FREE

alt [ticket status = FREE]
TicketMasterService <-- TicketMasterRepository : set status of tickets to RESERVED
TicketMasterService -> EventBus : publish ReservationAccepted
```

#### `6084305e9660aa52a87f03713a2c2186550b7b67` — compile_fail (sequence, tier 3)

- CSR: `Error line 9 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/6084305e9660aa52a87f03713a2c2186550b7b67.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=7 F1=0.000; missed: message
- chrF++: 37.63
- Files: GT `data/puml_files/6084305e9660aa52a87f03713a2c2186550b7b67.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/6084305e9660aa52a87f03713a2c2186550b7b67.puml` (yes) · input `data/puml_images_1568/6084305e9660aa52a87f03713a2c2186550b7b67.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/6084305e9660aa52a87f03713a2c2186550b7b67.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 6084305e9660aa52a87f03713a2c2186550b7b67
' Original Path: /doc/bufr_uml/BigPictureSeq.puml
' Source: World of Code

@startuml
hide footbox
skinparam dpi 300
skinparam SequenceActorBorderThickness 2
skinparam SequenceActorBorderColor #firebrick
skinparam ActorBackgroundColor #lightyellow
skinparam ParticipantBackgroundColor #lightyellow
skinparam ParticipantBorderThickness 2
skinparam ParticipantBorderColor #firebrick

actor Main
participant YAMLConfiguration
participant BufrParser
participant DataContainer
participant IodaEncoder

activate Main

create YAMLConfiguration
Main -> YAMLConfiguration : YAMLConfiguration(confPath)

create BufrParser
Main -> BufrParser : BufrParser(conf)


Main -> BufrParser : parse
activate BufrParser

note right
  See Query Collecting Data sequence.
end note

create DataContainer
BufrParser -> DataContainer : DataContainer()
return dataContainer
deactivate BufrParser

create IodaEncoder
Main -> IodaEncoder : IodaEncoder(conf)
Main -> IodaEncoder : encode(dataContainer)
activate IodaEncoder
note right
  See Query Getting Data sequence.
end note
deactivate IodaEncoder


deactivate Main


@enduml
```

Prediction PlantUML:
```plantuml
@startuml
actor Main

Main -> "YAMLConfiguration" ** : YAMLConfiguration(confPath)
Main -> "BufrParser" ** : BufrParser(conf)
Main -> "BufrParser" : parse
note right : See Query Collecting Data sequence.
"BufrParser" -> "DataContainer" ** : DataContainer()
"BufrParser" ..> Main : dataContainer
Main -> "IodaEncoder" ** : IodaEncoder(conf)
Main -> "IodaEncoder" : encode(dataContainer)
note right : See Query Getting Data sequence.
@enduml
```

#### `685ed63861f107bdd4c1567f840f159d819d7604` — compile_fail (sequence, tier 1)

- CSR: `Error line 9 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/685ed63861f107bdd4c1567f840f159d819d7604.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 80.85
- Files: GT `data/puml_files/685ed63861f107bdd4c1567f840f159d819d7604.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/685ed63861f107bdd4c1567f840f159d819d7604.puml` (yes) · input `data/puml_images_1568/685ed63861f107bdd4c1567f840f159d819d7604.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/685ed63861f107bdd4c1567f840f159d819d7604.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 685ed63861f107bdd4c1567f840f159d819d7604
' Original Path: /src/test/GetOrders.puml
' Source: World of Code

@startuml
AppUser -> Webserver: Get https://xxx/orders?uuid=123
Webserver --> OrderController: uuid
OrderController --> OrderService: uuid
OrderService --> OrderDao: uuid
OrderDao --> OrderService: List<OrderPO>
OrderService --> OrderController: List<OrderVO>
OrderController --> Webserver: List<OrderVO>
AppUser <-- Webserver
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
participant AppUser
participant Webserver
participant OrderController
participant OrderService
participant OrderDao

AppUser -> Webserver : Get https://xxx/orders?uuid=123
Webserver -..> OrderController : uuid
OrderController -..> OrderService : uuid
OrderService -..> OrderDao : uuid
OrderDao -..> OrderService : List<OrderPO>
OrderService -..> OrderController : List<OrderVO>
Webserver <..- OrderController : List<OrderVO>
AppUser <..- Webserver
@enduml
```
```

#### `75d17323e3f57e506be51b5455aa97ae89d8c5cc` — compile_fail (sequence, tier 2)

- CSR: `Error line 13 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: message
- chrF++: 58.51
- Files: GT `data/puml_files/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · input `data/puml_images_1568/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 75d17323e3f57e506be51b5455aa97ae89d8c5cc
' Original Path: /input/images-source/Implementing-PDQm-as-a-gateway.plantuml
' Source: World of Code

@startuml
hide footbox

Participant "Patient\nDemographics\nConsumer" as Client1
box "PDQm Implementation\ngrouped as a façade "
    Participant "Patient\n Demographics\nSupplier" as Server1
    Participant "Patient\n Demographics\nConsumer" as Client2
endbox
Participant "Patient\n Demographics\nSupplier" as Server2

Client1 -> Server1: Mobile Patient\nDemographics\nQuery [ITI-78]
activate Client1
activate Server1
Server1 --> Client2: Internal processing
activate Client2
activate Server2
Client2 -> Server2: Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]
Client2 <- Server2: [ITI-21] or [ITI-47] Response
Server1 <-- Client2: Internal processing
deactivate Client2
deactivate Server2
Client1 <- Server1: [ITI-78] Response
deactivate Client2
deactivate Server1

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

box "PDQm Implementation\ngrouped as a façade" #LightGray
participant "Patient\nDemographics\nSupplier" as PDSm
participant "Patient\nDemographics\nConsumer" as PDCi
end box

participant "Patient\nDemographics\nConsumer" as PDC order 1
participant "Patient\nDemographics\nSupplier" as PDS order 99

PDC -> PDSm : Mobile Patient\nDemographics\nQuery [ITI-78]

PDSm ..> PDCi : Internal processing

PDCi -> PDS : Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]

PDS --> PDCi : [ITI-21] or [ITI-47] Response

PDCi ..> PDSm : Internal processing

PDSm --> PDC : [ITI-78] Response

@enduml
```
```

#### `836fc1be71c455412e94cfec349f181ac525ab0f` — compile_fail (class, tier 2)

- CSR: `Error line 26 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/836fc1be71c455412e94cfec349f181ac525ab0f.puml`
- Element: tp=0 fp=0 fn=8 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: dependency, association
- chrF++: 63.93
- Files: GT `data/puml_files/836fc1be71c455412e94cfec349f181ac525ab0f.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/836fc1be71c455412e94cfec349f181ac525ab0f.puml` (yes) · input `data/puml_images_1568/836fc1be71c455412e94cfec349f181ac525ab0f.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/836fc1be71c455412e94cfec349f181ac525ab0f.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 836fc1be71c455412e94cfec349f181ac525ab0f
' Original Path: /figure/chap1/frontend_pascal.uml
' Source: World of Code

@startuml



package "frontend" #DDDDDD {
  Parser .[hidden]r Scanner
}

class "Parser" as Parser {
+ paser ()
+ getDErrorCount () : int
}

class "Scanner" as Scanner {
# ExactToken ()
}

package "frontend.pascal" #DDDDDD {
  PascalParserTd .[hidden]r PascalScanner
}

class "PascalParserTd" as PascalParserTd {
+ paser ()
+ getDErrorCount () : int
}

class "PascalScanner" as PascalScanner {
# ExactToken ()
}

PascalParserTd -u-> Parser
PascalScanner -u-> Scanner

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

class Scanner {
    ◇ ExactToken ()
}

class Parser {
    + paser ()
    + getDErrorCount () : int
}

class PascalScanner {
    ◇ ExactToken ()
}

class PascalParserTd {
    + paser ()
    + getDErrorCount () : int
}

PascalScanner --|> Scanner
PascalParserTd --|> Parser

package "frontend" {
    package "pascal" {
        class PascalParserTd as FPT
        class PascalScanner as FPS
    }
    class Parser as FP
    class Scanner as FS
}

@enduml
```
```

#### `86104112046f63abd2abd544f9b5c3a608848d6e` — compile_fail (class, tier 3)

- CSR: `Error line 5 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/86104112046f63abd2abd544f9b5c3a608848d6e.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: dependency, association
- chrF++: 17.69
- Files: GT `data/puml_files/86104112046f63abd2abd544f9b5c3a608848d6e.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/86104112046f63abd2abd544f9b5c3a608848d6e.puml` (yes) · input `data/puml_images_1568/86104112046f63abd2abd544f9b5c3a608848d6e.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/86104112046f63abd2abd544f9b5c3a608848d6e.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 86104112046f63abd2abd544f9b5c3a608848d6e
' Original Path: /DDI-CDI/DDI-CDI_2022-07-20b/doc/_rst/DDICDILibrary/Classes/Conceptual/VariableRelationship.pu
' Source: World of Code

/'
PLEASE DO NOT EDIT THIS CODE!
 This code was generated by the Eclipse Acceleo module UCMIS M2T.
 Target language is 'Plantuml' generated on the basis of the model 'DDICDIModels'.
'/


@startuml
!pragma ratio 0.5625
' HD display aspect ratio 16:9
' hyperlinkColor and pathHoverColor do not seem to work with class diagrams
' working approach: colors per item
' default font size for class names is 14

hide circle
hide empty members
scale 0.9

skinparam {
  ArrowThickness 1.5
  MinClassWidth 150
}

skinparam legend {
  BackgroundColor white
  FontSize 10
}

skinparam note {
  BackgroundColor white
}

skinparam class {
  ArrowColor #404040
  BorderColor #404040
}

skinparam package {
  FontColor lightgrey
  BorderColor lightgrey
}

title <size:20>UML Diagram: Class VariableRelationship in Context\n
footer \n\nDDI Cross Domain Integration (DDI-CDI) \
  1.0 - Conceptual::VariableRelationship

legend top left
**Hints**
<color:grey>- Move the mouse cursor over a name to see more information.
<color:grey>- Click on a name to go to the corresponding page.
endlegend

' Core class of diagram
class DDICDIModels::DDICDILibrary::Classes::Conceptual::VariableRelationship as "<size:10>Conceptual::\n<color:black>VariableRelationship" #FFD700 {
  identifier : <color:blue>Identifier \
  	  [[[../DDICDILibrary/DataTypes/StructuredDataTypes/Identifier.html#diagram{ <U+2015> Identifier:\nIdentifier for objects requiring short- or long-lasting referencing and management.}]]]
  semantics : <color:blue>ControlledVocabularyEntry \
  	  [[[../DDICDILibrary/DataTypes/StructuredDataTypes/ControlledVocabularyEntry.html#diagram{ <U+2015> ControlledVocabularyEntry:\nAllows for unstructured content which may be an entry from an externally maintained controlled vocabulary.If the content is from a controlled vocabulary provide the code value of the entry, as well as a reference to the controlled vocabulary from which the value is taken. Provide as many of the iden ...}]]]
}

' Class definitions for associated classes without superclass (might have also an association)
' This would be too many constraints for Graphviz. 
together {
  class DDICDIModels::DDICDILibrary::Classes::Conceptual::ConceptualVariable as "<size:10>Conceptual::\n<color:blue>ConceptualVariable" [[../DDICDILibrary/Classes/Conceptual/ConceptualVariable.html#super-class-hierarchy-generalization{ <U+2015> ConceptualVariable:\nConceptual variable with a substantive value domain specified.}]]
  class DDICDIModels::DDICDILibrary::Classes::Conceptual::VariableStructure as "<size:10>Conceptual::\n<color:blue>VariableStructure" [[../DDICDILibrary/Classes/Conceptual/VariableStructure.html#super-class-hierarchy-generalization{ <U+2015> VariableStructure:\nRelation structure for use with any set of variables in the variable cascade (conceptual, represented, instance).}]]
}

' Class definitions for suppliers of abstractions
together {
  abstract class DDICDIModels::DesignPatterns::CollectionsPattern::MemberRelationship as "<size:10>CollectionsPattern::\n<color:blue>MemberRelationship" [[../DesignPatterns/CollectionsPattern/MemberRelationship.html#super-class-hierarchy-generalization{ <U+2015> MemberRelationship:\nRelationship between members in a collection with directionality given by source and target.}]]
}

' Rest of class definitions, without associated classes of core class and abstraction supplier classes



```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

title UML Diagram: Class VariableRelationship in Context

note top left
  **Hints**
  - Move the mouse cursor over a name to see more information.
  - Click on a name to go to the corresponding page.
end note

class "Conceptual::\nVariableRelationship" as VR #Yellow {
  identifier : <color:blue>Identifier</color>
  semantics : <color:blue>ControlledVocabularyEntry</color>
}

class "Conceptual::\n<color:blue>ConceptualVariable</color>" as CV #LightGray {
}

class "Conceptual::\n<color:blue>VariableStructure</color>" as VS #LightGray {
}

class "CollectionsPattern::\n<color:blue><i>MemberRelationship</i></color>" as MR #LightGray {
}

VR --> CV : hasSource
VR --> CV : hasTarget
VS --> VR : has

VR ..|> MR : <<Refine>>

caption DDI Cross Domain Integration (DDI-CDI)  1.0 – Conceptual::VariableRelationship

@enduml
```
```

#### `8db937ff1aa2482e25096ce400100023484400be` — compile_fail (sequence, tier 4)

- CSR: `Error line 16 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/8db937ff1aa2482e25096ce400100023484400be.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: message
- chrF++: 82.50
- Files: GT `data/puml_files/8db937ff1aa2482e25096ce400100023484400be.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/8db937ff1aa2482e25096ce400100023484400be.puml` (yes) · input `data/puml_images_1568/8db937ff1aa2482e25096ce400100023484400be.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/8db937ff1aa2482e25096ce400100023484400be.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 8db937ff1aa2482e25096ce400100023484400be
' Original Path: /PB-428 - Goals 2.0/Sequence/PB-428 UC12 - View fund details.puml
' Source: World of Code

@startuml
'diagram parameters'
autonumber
'skinparam dpi 300
skinparam LegendBackgroundColor #white

'diagram title'
title PB-428 UC12 View fund details

'a list of the actors and participants'
actor "Next Customer" as UI
box "Next Platform"
participant "Core Next" as Next
database "Next Database" as DB
end box
participant "Core Bradesco" as BR

'a brief description of the diagram'
legend top
-- \t**Abstract:**\t --
This use case will return fund details for a single fund. This is an existing endpoint and we
will add additional response fields to this endpoint. They include:
1. FundCategory (new)
2. RequireFundTC (new)
3. RiskScore (existing field in table, but needs to be added in response)
4. IncomeValue (new)
5. IncomeDescription (new)
6. isNextSimples (new)
end legend

UI -> Next: **HTTP**\nGET /investments/funds/completeDetails
note right of UI
  The App will make a call
  to Core Next to get all the
  details for a fund. It will
  pass required input:
  - Fund ID
end note
note right of UI #orange
  **Note to Dev**
  Please check if the input
  parameter Fund ID is the
  Product ID or the External_
  Core_Product_ID. From what
  I can see, there are two
  product records with the
  same External_Core_Product_ID
  (Next Simples) and this may
  create issues.
end note


activate Next

ref over Next
  Use existing methodology to get
  complete details for a fund.
end ref


Next -> DB: GET additional fields from Product table
activate DB
  DB --> Next: Response
  note right of Next
    Core Next will retrieve additional
    data from the PRODUCT table and return
    them to the App:
    1. FundCategory (new)
    2. RequireFundTC (new)
    3. RiskScore (existing field in table,
        but needs to be added in response)
    4. IncomeValue (new)
    5. IncomeDescription (new)
    6. isNextSimples (new)
  end note
deactivate DB
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
title PB-428 UC12 View fund details

note top of "Core Next"
<b>Abstract:</b>
This use case will return fund details for a single fund. This is an existing endpoint and we
will add additional response fields to this endpoint. They include:
1. FundCategory (new)
2. RequireFundTC (new)
3. RiskScore (existing field in table, but needs to be added in response)
4. IncomeValue (new)
5. IncomeDescription (new)
6. isNextSimples (new)
end note

actor "Next Customer" as customer
box "Next Platform"
participant "Core Next" as corenext
database "Next Database" as nextdb
end box
participant "Core Bradesco" as bradesco

customer -> corenext : 1 **HTTP**\nGET /investments/funds/completeDetails

note left
The App will make a call
to Core Next to get all the
details for a fund. It will
pass required input:
– Fund ID
end note

note left #orange
<b>Note to Dev</b>
Please check if the input
parameter Fund ID is the
Product ID or the External_
Core_Product_ID. From what
I can see, there are two
product records with the
same External_Core_Product_ID
(Next Simples) and this may
create issues.
end note

ref over corenext, nextdb
Use existing methodology to get
complete details for a fund.
end ref

corenext -> nextdb : 2 GET additional fields from Product table

corenext <-- nextdb : 3 Response

note right
Core Next will retrieve additional
data from the PRODUCT table and return
them to the App:
1. FundCategory (new)
2. RequireFundTC (new)
3. RiskScore (existing field in table,
   but needs to be added in response)
4. IncomeValue (new)
5. IncomeDescription (new)
6. isNextSimples (new)
end note

customer <-- corenext : 4 Response

note left
Core Next will return all
existing fields in the response
+ the following new response
fields:
1. FundCategory (new)
2. RequireFundTC (new)
3. RiskScore (existing field in table,
   but needs to be added in response)
4. IncomeValue (new)
```

#### `8ff4bbffcff8d5961efc7a028967f4572a8afabd` — compile_fail (sequence, tier 3)

- CSR: `Error line 17 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/8ff4bbffcff8d5961efc7a028967f4572a8afabd.puml`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=11 F1=0.000; missed: message
- chrF++: 83.48
- Files: GT `data/puml_files/8ff4bbffcff8d5961efc7a028967f4572a8afabd.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/8ff4bbffcff8d5961efc7a028967f4572a8afabd.puml` (yes) · input `data/puml_images_1568/8ff4bbffcff8d5961efc7a028967f4572a8afabd.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/8ff4bbffcff8d5961efc7a028967f4572a8afabd.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 8ff4bbffcff8d5961efc7a028967f4572a8afabd
' Original Path: /Individual Workspaces/brec9824/a/diagrams/sequence-syntax.uml
' Source: World of Code

@startuml
hide circle
activate File
File -> LexicalAnalysisDriver : invokes
activate LexicalAnalysisDriver
LexicalAnalysisDriver -> LexicalAnalysisJava : Calls
deactivate LexicalAnalysisDriver


activate LexicalAnalysisJava
LexicalAnalysisJava -> JavaSyntaxLib : Calls


activate JavaSyntaxLib
JavaSyntaxLib --> LexicalAnalysisJava
deactivate JavaSyntaxLib


LexicalAnalysisJava  -> TypeCheck : SyntaxTypeCheck()


activate TypeCheck
TypeCheck --> File : Return(TypeCheck)
deactivate TypeCheck


LexicalAnalysisJava -> ColorCode  : SyntaxColorCheck()
activate ColorCode
ColorCode --> File : Return(ColorCode)
deactivate ColorCode


LexicalAnalysisJava -> ErrorCheck  : SyntaxErrorCheck()
activate ErrorCheck

alt successful case
ErrorCheck --> File: Error Free
else Error Case
ErrorCheck --> File: Return Error Message 
deactivate ErrorCheck
end
deactivate LexicalAnalysisJava


deactivate File
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

participant File
participant LexicalAnalysisDriver
participant LexicalAnalysisJava
participant JavaSyntaxLib
participant TypeCheck
participant ColorCode
participant ErrorCheck

File -> LexicalAnalysisDriver : invokes
activate LexicalAnalysisDriver
LexicalAnalysisDriver -> LexicalAnalysisJava : Calls
activate LexicalAnalysisJava
LexicalAnalysisJava -> JavaSyntaxLib : Calls
activate JavaSyntaxLib
JavaSyntaxLib ..> LexicalAnalysisJava
deactivate JavaSyntaxLib

LexicalAnalysisJava -> TypeCheck : SyntaxTypeCheck()
activate TypeCheck
File <.. TypeCheck : Return(TypeCheck)
deactivate TypeCheck

LexicalAnalysisJava -> ColorCode : SyntaxColorCheck()
activate ColorCode
File <.. ColorCode : Return(ColorCode)
deactivate ColorCode

LexicalAnalysisJava -> ErrorCheck : SyntaxErrorCheck()
activate ErrorCheck

alt [successful case]
    File <.. ErrorCheck : Error Free
else [Error Case]
    File <.. ErrorCheck : Return Error Message
end

deactivate ErrorCheck
deactivate LexicalAnalysisJava
deactivate LexicalAnalysisDriver

@enduml
```
```

#### `9117c4347190b93368d0254f3612ae5840b89d7b` — compile_fail (sequence, tier 1)

- CSR: `Error line 12 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/9117c4347190b93368d0254f3612ae5840b89d7b.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: message
- chrF++: 46.34
- Files: GT `data/puml_files/9117c4347190b93368d0254f3612ae5840b89d7b.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/9117c4347190b93368d0254f3612ae5840b89d7b.puml` (yes) · input `data/puml_images_1568/9117c4347190b93368d0254f3612ae5840b89d7b.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/9117c4347190b93368d0254f3612ae5840b89d7b.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 9117c4347190b93368d0254f3612ae5840b89d7b
' Original Path: /uml_detail/seq_detail.pu
' Source: World of Code

@startuml
title ユーザの詳細

autonumber "#."

actor 管理者
participant ユーザ一覧画面
participant 詳細画面
database ユーザDB

管理者 -[#green]> ユーザ一覧画面:ユーザネームをクリック
ユーザ一覧画面 -[#blue]> 詳細画面:遷移
詳細画面 -> ユーザDB:データ検索
ユーザDB --> 詳細画面:ユーザ情報

詳細画面 --[#green]> 管理者:ユーザ詳細


@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title ユーザの詳細

actor 管理者
participant "ユーザー覧画面" as list
participant "詳細画面" as detail
database "ユーザDB" as db

管理者 -[#green]> list : 1. ユーザネームをクリック
list -[#blue]> detail : 2. 遷移
detail -> db : 3. データ検索
detail <.. db : 4. ユーザ情報
管理者 <.[#green]. detail : 5. ユーザ詳細

@enduml
```
```

#### `98d73a86be25154e58fe9707f994f4d0dc788d10` — compile_fail (class, tier 4)

- CSR: `Error line 126 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/98d73a86be25154e58fe9707f994f4d0dc788d10.puml`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: inheritance, composition, association
- chrF++: 80.53
- Files: GT `data/puml_files/98d73a86be25154e58fe9707f994f4d0dc788d10.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/98d73a86be25154e58fe9707f994f4d0dc788d10.puml` (yes) · input `data/puml_images_1568/98d73a86be25154e58fe9707f994f4d0dc788d10.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/98d73a86be25154e58fe9707f994f4d0dc788d10.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 98d73a86be25154e58fe9707f994f4d0dc788d10
' Original Path: /TrainSystem/UML/Class Diagrams/TrainModelClassDiagram.puml
' Source: World of Code

@startuml

title Train Model Class Diagram
'skinparam backgroundColor transparent'
skinparam classBackgroundColor #e6ffcc
skinparam classBorderColor 	#049595
skinparam packageBorderCOlor  #049595
skinparam arrowColor #006666

package Shared{
  interface Module{
    +timeUpdate(SimTime) : Boolean
  }
  class SimTime{
    +hr : int
    +min : int
    +sec : int
    +toString() : String
  }
}
package Module.TrainModel {
    class TrainModel {
        -trainID : String
        -trainModel : TrainModel
        __
        +time : SimTime
        +trncntrl : TrainController
        +trkmdl : TrackModel
        __
        -calcDeltaTime(SimTime, SimTime) : integer
        -updateList()
        +timeUpdate(SimTime)
        +getTrainAtBlock(Block)
        +setBeacon(trainID,int)
		+dispatchTrainToBlock(String, String, int, String[])
		+transmitCtcAuthority(String, double)
		+suggestSetpointSpeed(String, double)
		+setEmergencyBrake(String, boolean)
		+setSchedule(String, String[])
		+setBeacon(String, int_32)
		+getPosition(String) : String[2]
		+setPower(String, double)
		+setLeft(String, boolean)
		+setRight(String, boolean)
		+setService(String, boolean)
		+setEmergency(String, boolean)
		+setLights(String, boolean)
		+setTemperature(String, int)
		+setTrainPosition(String) : String[2]
		+setTrainActualSpeed(String) : double
    }

    class Train {
        -id : String
        -weight : double
        -height : double
        -length : double
        -width : double
        -numCars : int
        -capacity : int
        -lineColor : String
        -grade : double
        -gpsStatus : boolean
        -mboStatus : boolean
        -engineFailureStatus : boolean
        -signalFailureStatus : boolean
        -brakeFailureStatus : boolean
        -nextStationID : String
        -timeOfArrival : double
        -arrivalStatus : boolean
        -numPassengers : int
        -currentSpeed : double
        -CTCSpeed : double
        -CTCAuthority : double
        -powerOut : double
        -leftDoorStatus : boolean
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
title Train Model Class Diagram

package "Module" {
    package "TrainModel" {
        class Train {
            - id : String
            - weight : double
            - height : double
            - length : double
            - width : double
            - numCars : int
            - capacity : int
            - lineColor : String
            - grade : double
            - gpsStatus : boolean
            - mboStatus : boolean
            - engineFailureStatus : boolean
            - signalFailureStatus : boolean
            - brakeFailureStatus : boolean
            - nextStationID : String
            - timeOfArrival : double
            - arrivalStatus : boolean
            - numPassengers : int
            - currentSpeed : double
            - CTCSpeed : double
            - CTCAuthority : double
            - powerOut : double
            - leftDoorStatus : boolean
            - rightDoorStatus : boolean
            - lightsStatus : boolean
            - temperature : int
            - serviceBrake : boolean
            - emerBrake : boolean
            - trainActive : boolean
            - force : double
            - normalForce : double
            - downwardForce : double
            - totalForce : double
            - friction : double
            - slope : double
            - finalSpeed : double
            - trainAcceleration : double
            - gpsSignal : Gps
            ~ trainModelGUI : TrainModelNewGUI
            ~ trainList : TrainModel[]
            # showTrainGUI()
            # updateTrainValues()
            # CreateNewGUI(TrainModel)
            # activateFailureModeTest()
            # endFailureModeTest()
            # getTrainController()
            # updateTrainList()
            # updateArrivalStatus()
            # setPos(double)
            # getPos()
            # getGrade(Block)
            # getSetpointSpeed()
            # setSetpointSpeed()
            # getAuthority()
            # setAuthority(double)
            # setLightStatus(boolean)
            # setLeftDoorStatus(boolean)
            # setRightDoorStatus(boolean)
            # setTemperature(int)
            # truncateTo(double,int)
        }

        class Gps {
            - line : String
            - currPos : double[2]
            # setGpsPos(double[2])
            # getGpsPos()
        }

        class TrainModel {
            - trainID : String
            - trainModel : TrainModel
            ~ time : SimTime
```

#### `bd045dcdf9f93711b701665ba6c426c083ce0277` — compile_fail (class, tier 4)

- CSR: `Error line 133 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/bd045dcdf9f93711b701665ba6c426c083ce0277.puml`
- Element: tp=0 fp=0 fn=27 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=32 F1=0.000; missed: inheritance, composition, aggregation, association
- chrF++: 79.16
- Files: GT `data/puml_files/bd045dcdf9f93711b701665ba6c426c083ce0277.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/bd045dcdf9f93711b701665ba6c426c083ce0277.puml` (yes) · input `data/puml_images_1568/bd045dcdf9f93711b701665ba6c426c083ce0277.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/bd045dcdf9f93711b701665ba6c426c083ce0277.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: bd045dcdf9f93711b701665ba6c426c083ce0277
' Original Path: /DesignFiles/ClassDiagram.plantuml
' Source: World of Code

@startuml
title Facebook Smart View -  Class Diagram

interface IXmlSerializable {
    +ReadXml(XmlReader reader): void
    +WriteXml(XmlWriter writer): void
}

interface IEnumerable {
    +GetEnumerator(): IEnumerator
}

class FormMain extends Form {
    +event MainFormLoadEventArgs
}

class FormLogin extends Form {
}

class FormLoader extends Form {
}

class AppUser {
    +constructor(User)
    +GetNewsFeed(PostFilter): FacebookObjectCollection<Post>
    +GetUserAlbums(): FacebookObjectCollection<Album>
    +GetUserProfilePicture(): string
    +PostToUserWall(string): string
    +LikePhoto(string): bool
    +CommentPhoto(string, string): bool
    +Name: string {getter}
    +Birthday: string {getter}
    +Gender: string {getter}
    +Age: int {getter}
    +UserLivesIn: string {getter}
    +LastEducationStudyPlace: string {getter}

}

class LoginLogic{
    +constructor()
    +GetSavedAccessToken(): string
    +SaveAccessToken(string)
    +LoginToFacebook(): LoginResult
    +LoginToFacebookAndSaveToken(): LiginResult
    +ConnectToFacebook(string): LoginResult
    +SaveRememberBox(bool)
    +GetRememberBoxCheckedValue(): bool
}

FormMain *-down-AppUser

AppUser "1" o-down- "1" User: Holds the facebook user
AppUser "1" o-down- "*" Post
AppUser "1" o-down- "*" Album


FormLogin *-down-LoginLogic
FormLogin "1" -> "1" FormLoader
FormLogin "1" -down-> "1" FormMain

package "Post Filtering Feature" <<Frame>> {

    class PostFilter{
        +constructor()
        +AddGroup(FilterGroup)
        +RemoveGroup(FilterGroup)
        +Save()
        +FilterGroups: IList<FilterGroup> {getter, setter}
    }

    class FilterGroup implements IXmlSerializable, IEnumerable{
         -IList<FilterItem>
        +constructor()
        +AddItem(FilterItem)
        +RemoveItem(FilterItem)
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
title Facebook Smart View - Class Diagram

class Form

class FormLogin
class FormLoader

FormLogin --|> Form
FormLoader --|> Form

FormLogin "1" -- "1" FormLoader

class LoginLogic {
  + constructor()
  + GetSavedAccessToken(): string
  + SaveAccessToken(string)
  + LoginToFacebook(): LoginResult
  + LoginToFacebookAndSaveToken(): LoginResult
  + ConnectToFacebook(string): LoginResult
  + SaveRememberBox(bool)
  + GetRememberBoxCheckedValue(): bool
}

class FormMain {
  + event MainFormLoadEventArgs
}

class EventArgs

FormMain --|> Form
FormMain -- EventArgs

class MainFormLoadEventArgs {
  + FinishedLoading: bool {getter, setter}
  + Message: string {getter, setter}
  + constructor()
}

MainFormLoadEventArgs --|> EventArgs

class AppUser {
  + Name: string {getter}
  + Birthday: string {getter}
  + Gender: string {getter}
  + Age: int {getter}
  + UserLivesin: string {getter}
  + LastEducationStudyPlace: string {getter}
  + constructor(User)
  + GetNewsFeed(PostFilter): FacebookObjectCollection<Post>
  + GetUserAlbums(): FacebookObjectCollection<Album>
  + GetUserProfilePicture(): string
  + PostToUserWall(string): string
  + LikePhoto(string): bool
  + CommentPhoto(string, string): bool
}

class Album
class User
class Post

AppUser "1" -- "*" Album
AppUser "1" -- "1" User : Holds the facebook user
AppUser "1" -- "*" Post

package "Top Photos Feature" {
  class PictureObjectBasic {
    + NumberOfLikes: int {getter, setter}
    + NumberOfComment: int {getter, setter}
    + PictureUrl: string {getter, setter}
    + Score: int {getter, setter}
    + ObjectId: string {getter, setter}
    - constructor(string, int, int, int, string, string)
  }

  class PictureObject {
    - constructor(string, int, int, int, string, string, PictureBox, Label)
    + LoadInformation()
  }
```

#### `eff76e684b657103a5b9a074acbaf89a607557e1` — compile_fail (class, tier 2)

- CSR: `Error line 13 in file: data/csr/claude-opus-4-6_20260614T081502Z/extracted/eff76e684b657103a5b9a074acbaf89a607557e1.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 89.77
- Files: GT `data/puml_files/eff76e684b657103a5b9a074acbaf89a607557e1.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/eff76e684b657103a5b9a074acbaf89a607557e1.puml` (yes) · input `data/puml_images_1568/eff76e684b657103a5b9a074acbaf89a607557e1.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/eff76e684b657103a5b9a074acbaf89a607557e1.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: eff76e684b657103a5b9a074acbaf89a607557e1
' Original Path: /Singleton/singleton.pu
' Source: World of Code

@startuml

note as N1
  Singleton (シングルトン)
  <概要>
  システム内に存在するオブジェクトが1つであることを保証する。
  このパターンでは外部からのオブジェクトを生成を禁止する。
  システムの起動中はオブジェクト1つだけ制限したいときに使う
  <メリット>
  ・オブジェクトが1つしかないことが保証されている
end note

class FileFormatter {
  - singleton : Singleton
  - Singleton()
  + GetInstance() : Singleton
}

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

note left
Singleton (シングルトン)
<概要＞
システム内に存在するオブジェクトが1つであることを保証する。
このパターンでは外部からのオブジェクトを生成を禁止する。
システムの起動中はオブジェクト1つだけ制限したいときに使う
<メリット＞
・オブジェクトが1つしかないことが保証されている
end note

class FileFormatter {
    - singleton : Singleton
    --
    - Singleton()
    + GetInstance() : Singleton
}

@enduml
```
```

#### outcome: compiled_low_structural

#### `0bffda3c561066aa0dda7f556b2ce91406230f86` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=2 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 49.99
- Files: GT `data/puml_files/0bffda3c561066aa0dda7f556b2ce91406230f86.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/0bffda3c561066aa0dda7f556b2ce91406230f86.puml` (yes) · input `data/puml_images_1568/0bffda3c561066aa0dda7f556b2ce91406230f86.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/0bffda3c561066aa0dda7f556b2ce91406230f86.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 0bffda3c561066aa0dda7f556b2ce91406230f86
' Original Path: /docs/javadocs/soen6441riskgame/enums/ConquestMapPart.puml
' Source: World of Code

@startuml

skinparam svgLinkTarget _parent
skinparam linetype ortho
set namespaceSeparator none
enum "<b><size:14>ConquestMapPart</b>\n<size:10>soen6441riskgame.enums" as soen6441riskgame.enums.ConquestMapPart  [[../../soen6441riskgame/enums/ConquestMapPart.html{soen6441riskgame.enums.ConquestMapPart}]] {
-String part
-ConquestMapPart(String part)
{static} +ConquestMapPart values()
{static} +ConquestMapPart valueOf(String name)
+String getPart()
{static} +ConquestMapPart fromString(String part)
}



@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

enum ConquestMapPart <<E>> {
    - part : String
    --
    - ConquestMapPart(String part)
    + {static} ConquestMapPart values()
    + {static} ConquestMapPart valueOf(String name)
    + String getPart()
    + {static} ConquestMapPart fromString(String part)
}

note as N1
    soen6441riskgame.enums
end note

@enduml
```
```

#### `1010a06e412b3aa575a498e6287b9ddb5f519153_03` — compiled_low_structural (sequence, tier 2)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=1 fp=4 fn=4 F1=0.200; missed: message; extra: message
- chrF++: 87.10
- Files: GT `data/puml_files/1010a06e412b3aa575a498e6287b9ddb5f519153_03.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/1010a06e412b3aa575a498e6287b9ddb5f519153_03.puml` (yes) · input `data/puml_images_1568/1010a06e412b3aa575a498e6287b9ddb5f519153_03.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/1010a06e412b3aa575a498e6287b9ddb5f519153_03.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 1010a06e412b3aa575a498e6287b9ddb5f519153
' Original Path: /docs/diagrams/src/modeloDominio.plantuml
' Source: World of Code

@startuml

actor Player
participant Board as ":Board"
participant  pawn as "pawn :Pawn"
participant  draught as "draught :Draught"
participant OponentPiece as "oponentPiece :Piece"

Player -> Board : Select origin square
alt origin == pawn
loop pawn.row + 1 == oponentPiece.row && \n (pawn.column + 1 == oponentPiece.column ||  pawn.column - 1 == oponentPiece.column) && \n there is only one piece between origin and target
Player -> Board : Move pawn to target square
Player -> Board : Delete oponentPiece
end
end
alt origin == draught
loop target is in diagonal with draught && \n there is only one piece between origin and target
Player -> Board : Move draught to target square
Player -> Board : Delete oponentPiece
end
end
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

actor Player

participant ":Board" as Board
participant "pawn :Pawn" as Pawn
participant "draught :Draught" as Draught
participant "oponentPiece :Piece" as OponentPiece

Player -> Board : Select origin square

alt origin == pawn
    loop pawn.row + 1 == oponentPiece.row &&\n(pawn.column + 1 == oponentPiece.column || pawn.column - 1 == oponentPiece.column) &&\nthere is only one piece between origin and target
        Player -> Pawn : Move pawn to target square
        Player -> Pawn : Delete oponentPiece
    end
end

alt origin == draught
    loop target is in diagonal with draught &&\nthere is only one piece between origin and target
        Player -> Draught : Move draught to target square
        Player -> Draught : Delete oponentPiece
    end
end

@enduml
```
```

#### `145fbd18e198eee56d4b12fedb058ad3ecf5a1c7` — compiled_low_structural (class, tier 4)

- Element: tp=18 fp=2 fn=2 F1=0.900; type-acc matched=18 correct=5 excluded=0
- Relationship: tp=2 fp=14 fn=9 F1=0.148; missed: inheritance, composition, dependency; extra: dependency, association
- chrF++: 75.03
- Files: GT `data/puml_files/145fbd18e198eee56d4b12fedb058ad3ecf5a1c7.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/145fbd18e198eee56d4b12fedb058ad3ecf5a1c7.puml` (yes) · input `data/puml_images_1568/145fbd18e198eee56d4b12fedb058ad3ecf5a1c7.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/145fbd18e198eee56d4b12fedb058ad3ecf5a1c7.png` (yes)

#### `254624d1e8c3cdf5489c09bbdb8e2c4ac88ce780` — compiled_low_structural (sequence, tier 3)

- Element: tp=8 fp=0 fn=0 F1=1.000; type-acc matched=8 correct=8 excluded=0
- Relationship: tp=3 fp=7 fn=7 F1=0.300; missed: message; extra: message
- chrF++: 70.08
- Files: GT `data/puml_files/254624d1e8c3cdf5489c09bbdb8e2c4ac88ce780.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/254624d1e8c3cdf5489c09bbdb8e2c4ac88ce780.puml` (yes) · input `data/puml_images_1568/254624d1e8c3cdf5489c09bbdb8e2c4ac88ce780.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/254624d1e8c3cdf5489c09bbdb8e2c4ac88ce780.png` (yes)

#### `277002f45b6496b4fe9f41f3fae3b1dd35e31816` — compiled_low_structural (class, tier 4)

- Element: tp=7 fp=1 fn=1 F1=0.875; type-acc matched=7 correct=7 excluded=0
- Relationship: tp=5 fp=5 fn=9 F1=0.417; missed: inheritance, association; extra: association
- chrF++: 70.88
- Files: GT `data/puml_files/277002f45b6496b4fe9f41f3fae3b1dd35e31816.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/277002f45b6496b4fe9f41f3fae3b1dd35e31816.puml` (yes) · input `data/puml_images_1568/277002f45b6496b4fe9f41f3fae3b1dd35e31816.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/277002f45b6496b4fe9f41f3fae3b1dd35e31816.png` (yes)

#### `532d5a1ff757de7127780cff4493ccdd7a51c49a` — compiled_low_structural (sequence, tier 4)

- Element: tp=1 fp=12 fn=12 F1=0.077; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=30 fn=34 F1=0.000; missed: message; extra: message
- chrF++: 63.31
- Files: GT `data/puml_files/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml` (yes) · input `data/puml_images_1568/532d5a1ff757de7127780cff4493ccdd7a51c49a.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/532d5a1ff757de7127780cff4493ccdd7a51c49a.png` (yes)

#### `549be1e00dbfe4db4474e99a2b4bdd46280e6c14` — compiled_low_structural (class, tier 2)

- Element: tp=6 fp=2 fn=0 F1=0.857; type-acc matched=6 correct=6 excluded=0
- Relationship: tp=0 fp=7 fn=7 F1=0.000; missed: association; extra: dependency, association
- chrF++: 67.39
- Files: GT `data/puml_files/549be1e00dbfe4db4474e99a2b4bdd46280e6c14.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/549be1e00dbfe4db4474e99a2b4bdd46280e6c14.puml` (yes) · input `data/puml_images_1568/549be1e00dbfe4db4474e99a2b4bdd46280e6c14.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/549be1e00dbfe4db4474e99a2b4bdd46280e6c14.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 549be1e00dbfe4db4474e99a2b4bdd46280e6c14
' Original Path: /Versagen/Events/versagen/Versagen/Events/IEvent.puml
' Source: World of Code

@startuml
interface IEvent {
    IgnoreThis : bool <<get>> <<set>>
    IsSystemMessage : bool <<get>> <<set>>
}
class EventHelpers <<static>> {
    + {static} GetPlayer(evnt:IEvent, GetPlayerFunc:Func<VersaCommsID, TPlayer>) : TPlayer
    + {static} GetPlayerID(evnt:IEvent) : VersaCommsID
    + {static} GetEntity(evnt:IEvent, getEntityFunc:Func<VersaCommsID, TEntity>) : TEntity
    + {static} GetEntityID(evnt:IEvent) : VersaCommsID
    + {static} GetScenario(evnt:IEvent, getScenarioFunction:Func<VersaCommsID, TScenario>) : TScenario
    + {static} GetScenarioID(evnt:IEvent) : VersaCommsID
}
class "UnionType`2"<T1,T2> {
}
class "IList`1"<T> {
}
IEvent --> "SourcePipe" IEventPipe
IEvent --> "Services" IServiceProvider
IEvent --> "Scenario<VersaCommsID,IScenario>" "UnionType`2"
IEvent --> "Terminal<VersaCommsID,IVersaWriter>" "UnionType`2"
IEvent --> "Player<VersaCommsID,IPlayer>" "UnionType`2"
IEvent --> "Entity<VersaCommsID,IEntity>" "UnionType`2"
IEvent --> "EventSpecificCommands<ICommandGroup>" "IList`1"
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml

interface IEvent {
  IgnoreThis : bool «get» «set»
  IsSystemMessage : bool «get» «set»
}

class EventHelpers <<static>> {
  + GetPlayer(evnt:IEvent, GetPlayerFunc:Func<VersaCommsID, TPlayer>) : TPlayer
  + GetPlayerID(evnt:IEvent) : VersaCommsID
  + GetEntity(evnt:IEvent, getEntityFunc:Func<VersaCommsID, TEntity>) : TEntity
  + GetEntityID(evnt:IEvent) : VersaCommsID
  + GetScenario(evnt:IEvent, getScenarioFunction:Func<VersaCommsID, TScenario>) : TScenario
  + GetScenarioID(evnt:IEvent) : VersaCommsID
}

class "UnionType`2" as UnionType2 << (C,#90EE90) >> {
}

class "IList`1" as IList1 << (C,#90EE90) >> {
}

class IEventPipe << (C,#90EE90) >> {
}

class IServiceProvider << (C,#90EE90) >> {
}

note right of UnionType2 : T1,T2
note right of IList1 : T

EventHelpers --> IEvent
EventHelpers --> UnionType2 : Scenario<VersaCommsID,Entity>\nPlayer<VersaCommsID,IPlayer>
EventHelpers --> IList1 : Terminal<VersaCommsID,\nCommands<ICommandGroup>
EventHelpers --> IEventPipe : IEventPipe
EventHelpers --> IServiceProvider : Service>

@enduml
```
```

#### `6c7324c7eaeb23cd5644654ea022ca212ecd24ea` — compiled_low_structural (sequence, tier 1)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=4 fn=4 F1=0.000; missed: message; extra: message
- chrF++: 54.47
- Files: GT `data/puml_files/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · input `data/puml_images_1568/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 6c7324c7eaeb23cd5644654ea022ca212ecd24ea
' Original Path: /Documentação/1201384/US1005/US1005_SSD.puml
' Source: World of Code

@startuml
actor SalesClerk as adm
participant "//<<presentation>>//\nDefineNewCategoryUI" as ui

autonumber

adm-->ui: Define new category

activate ui

ui-->adm: asks user information

adm-->ui: Code, Description

ui-->adm: displayCategoryInfo

deactivate ui
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
actor SalesClerk

participant "<<presentation>>\nDefineNewCategoryUI" as UI

SalesClerk -[dashed]-> UI : **1** Define new category
SalesClerk <-[dashed]- UI : **2** asks user information
SalesClerk -[dashed]-> UI : **3** Code, Description
SalesClerk <-[dashed]- UI : **4** displayCategoryInfo
@enduml
```

#### `72202da46f364f84aa0b0362094fe311bd4240e1` — compiled_low_structural (class, tier 2)

- Element: tp=6 fp=0 fn=0 F1=1.000; type-acc matched=6 correct=6 excluded=0
- Relationship: tp=2 fp=5 fn=6 F1=0.267; missed: inheritance, composition, aggregation, dependency; extra: inheritance, composition, dependency
- chrF++: 65.27
- Files: GT `data/puml_files/72202da46f364f84aa0b0362094fe311bd4240e1.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/72202da46f364f84aa0b0362094fe311bd4240e1.puml` (yes) · input `data/puml_images_1568/72202da46f364f84aa0b0362094fe311bd4240e1.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/72202da46f364f84aa0b0362094fe311bd4240e1.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 72202da46f364f84aa0b0362094fe311bd4240e1
' Original Path: /src/builderPattern/builder.puml
' Source: World of Code

@startuml

interface computerBuilder
class computer
class advancedComputer
class middleComputer
class lowComputer
class director


computerBuilder <|-- advancedComputer
computerBuilder <|-- middleComputer
computerBuilder <|-- lowComputer

computerBuilder o-- director
computer *-- advancedComputer
computer *-- middleComputer
computer *-- lowComputer
computer <.. computerBuilder





@enduml
```

Prediction PlantUML:
```plantuml
@startuml

class computer {
}

interface computerBuilder {
}

class advancedComputer {
}

class middleComputer {
}

class director {
}

class lowComputer {
}

advancedComputer *-- computer
middleComputer *-- computer
lowComputer *-- computer

middleComputer --|> computerBuilder
director --|> computerBuilder

director ..> computer

advancedComputer --|> computerBuilder

@enduml
```

#### `938e9cc0e6b8dda26422f35f30282f7d202efb9d_02` — compiled_low_structural (sequence, tier 4)

- Element: tp=1 fp=4 fn=4 F1=0.200; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=20 fn=20 F1=0.000; missed: message; extra: message
- chrF++: 54.07
- Files: GT `data/puml_files/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · input `data/puml_images_1568/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes)

#### `acc3c1fb18dc04ab90e90b2c3a280a78b4b3f9e6` — compiled_low_structural (class, tier 3)

- Element: tp=6 fp=0 fn=0 F1=1.000; type-acc matched=6 correct=6 excluded=0
- Relationship: tp=2 fp=3 fn=3 F1=0.400; missed: dependency; extra: inheritance
- chrF++: 86.03
- Files: GT `data/puml_files/acc3c1fb18dc04ab90e90b2c3a280a78b4b3f9e6.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/acc3c1fb18dc04ab90e90b2c3a280a78b4b3f9e6.puml` (yes) · input `data/puml_images_1568/acc3c1fb18dc04ab90e90b2c3a280a78b4b3f9e6.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/acc3c1fb18dc04ab90e90b2c3a280a78b4b3f9e6.png` (yes)

#### `cf7676f21794d171bc25382fc353f2a4be806a88` — compiled_low_structural (sequence, tier 3)

- Element: tp=6 fp=0 fn=0 F1=1.000; type-acc matched=6 correct=6 excluded=0
- Relationship: tp=1 fp=13 fn=7 F1=0.091; missed: message; extra: message
- chrF++: 47.20
- Files: GT `data/puml_files/cf7676f21794d171bc25382fc353f2a4be806a88.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/cf7676f21794d171bc25382fc353f2a4be806a88.puml` (yes) · input `data/puml_images_1568/cf7676f21794d171bc25382fc353f2a4be806a88.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/cf7676f21794d171bc25382fc353f2a4be806a88.png` (yes)

#### `e99fda9abbdee4e0acb98ec78ece52cfec4db184` — compiled_low_structural (sequence, tier 2)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=4 fp=6 fn=4 F1=0.444; missed: message; extra: message
- chrF++: 61.84
- Files: GT `data/puml_files/e99fda9abbdee4e0acb98ec78ece52cfec4db184.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/e99fda9abbdee4e0acb98ec78ece52cfec4db184.puml` (yes) · input `data/puml_images_1568/e99fda9abbdee4e0acb98ec78ece52cfec4db184.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/e99fda9abbdee4e0acb98ec78ece52cfec4db184.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: e99fda9abbdee4e0acb98ec78ece52cfec4db184
' Original Path: /src/main/java/com/puml/qingqing/live_5.1.5/备课上传图片/资料图片编辑.puml
' Source: World of Code

@startuml
title 资料图片编辑
participant 授课端
participant "cos/oss" AS oss
participant imgsvc
participant livesvc
授课端 -> livesvc: （wiki:206898375 课程备课详情）\n/{h5|}pt/v1/live_order_course/preparing_info
授课端 -> liveteachingsvc: （预览/编辑 资料图片 wiki:288817172 PT 根据不同类型获取课程绑定资料的信息）\n<color #green>/{h5|}pt/v1/live_order_course/material_info
note right 授课端: 旋转/裁剪/删除 前端行为，等点击<b>确认</b>时再汇报后端
授课端 -> livesvc: （PT V3 wiki:185074611 多地址文件上传前获取签名）\n/{h5|}pt/v3/image/object_upload_auth<color #red>（PT）</color>
create oss
授课端 -> oss: 上传图片
授课端 -> imgsvc: /pb/v1/media/add/image（wiki:11574780）
'额外调一次替换接口，可能存在替换成功，覆盖失败情况
'授课端 -> liveteachingsvc: <color #green>（wiki: 288325995 PT 学习资料图片批量替换）\n<color #green>/{h5|}pt/v1/study_material/batch_replace_images</color>（入参：旋转/裁剪的图片列表）
'liveteachingsvc -[#blue]> liveteachingsvc: delete t_general_file（原general_file）\ninsert t_general_file（替换的general_file）
授课端 -> liveteachingsvc: <color #green>（wiki:288327306 PT 覆盖已绑定课程学习资料图片）\n（入参：需要解绑的general_file_id列表、需要替换的image列表（包含被替换的general_file_id））\n<color #green>/{h5|}pt/v1/study_material/course_images_cover</color>
liveteachingsvc -[#blue]> liveteachingsvc: delete t_general_file（原general_file）\ninsert t_general_file（替换的general_file）
liveteachingsvc -[#blue]> liveteachingsvc: delete t_live_order_course_general_file（解绑+被替换的general_file）\ninsert t_live_order_course_general_file（替换的general_file）
'liveteachingsvc --> 授课端: mqtt sendSignal subCmdType:20（老师上传图片完成）
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title 资料图片编辑

participant "授课端" as client
participant "cos/oss" as cos
participant "imgsvc" as imgsvc
participant "livesvc" as livesvc
participant "liveteachingsvc" as liveteachingsvc

client -> livesvc : （wiki:206898375 课程备课详情）\n/{h5|}pt/v1/live_order_course/preparing_info

client -> livesvc : （预览/编辑 资料图片 wiki:288817172 PT 根据不同类型获取课程绑定资料的信息）\n/{h5|}pt/v1/live_order_course/material_info

note over client : 旋转/裁剪/删除 前端行为，等点击**确认**时再汇报后端

client -> livesvc : （PT V3 wiki:185074611 多地址文件上传前获取签名）\n/{h5|}pt/v3/image/object_upload_auth（<color:red>PT</color>）

client -> cos : 上传图片

client -> imgsvc : /pb/v1/media/add/image（wiki:11574780）

client -> livesvc : （<color:red>wiki:288327306 PT 覆盖已绑定课程学习资料图片</color>）\n（入参：需要解绑的general_file_id列表、需要替换的image列表（包含被替换的general_file_id））\n/{h5|}pt/v1/study_material/course_images_cover

livesvc -> liveteachingsvc : delete t_general_file（原general_file）\ninsert t_general_file（替换的general_file）
liveteachingsvc --> livesvc

livesvc -> liveteachingsvc : delete t_live_order_course_general_file（解绑+被替换的general_file）\ninsert t_live_order_course_general_file（替换的general_file）
liveteachingsvc --> livesvc

@enduml
```
```

#### `f3df73144b3aaffd6fb73fceaf960900c01317df` — compiled_low_structural (sequence, tier 1)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=3 fp=4 fn=4 F1=0.429; missed: message; extra: message
- chrF++: 73.39
- Files: GT `data/puml_files/f3df73144b3aaffd6fb73fceaf960900c01317df.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/f3df73144b3aaffd6fb73fceaf960900c01317df.puml` (yes) · input `data/puml_images_1568/f3df73144b3aaffd6fb73fceaf960900c01317df.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/f3df73144b3aaffd6fb73fceaf960900c01317df.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: f3df73144b3aaffd6fb73fceaf960900c01317df
' Original Path: /UML/UserSuccess.puml
' Source: World of Code

@startuml
'Brukeren klarte å kjøpe bilett uten noen feil

User -> GUI: Kjøper bilett
GUI -> Database: Ønske om å kjøpe bilett
Database -> TicketControl: Sjekker om det er ledig
TicketControl -> Authentication: Bekrefter kortinformasjon
Authentication -> Database: Kjøp ble godkjent
Database -> GUI: Registrer kjøp og \n sender informasjon at \n kjøp gikk igjennom
GUI -> User: Kjøp ble godkjent



@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
participant "User" as User
participant "GUI" as GUI
participant "Database" as Database
participant "TicketControl" as TicketControl
participant "Authentication" as Authentication

User -> GUI : Kjøper bilett
GUI -> TicketControl : Ønske om å kjøpe bilett
TicketControl -> Database : Sjekker om det er ledig
TicketControl -> Authentication : Bekrefter kortinformasjon
Authentication --> TicketControl : Kjøp ble godkjent
TicketControl --> GUI : Registrer kjøp og\nsender informasjon at\nkjøp gikk igjennom
GUI --> User : Kjøp ble godkjent
@enduml
```
```

#### `fa3bc8bd559550992fd2c4e024d7a9872ea1ee76` — compiled_low_structural (class, tier 3)

- Element: tp=0 fp=1 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 8.22
- Files: GT `data/puml_files/fa3bc8bd559550992fd2c4e024d7a9872ea1ee76.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/fa3bc8bd559550992fd2c4e024d7a9872ea1ee76.puml` (yes) · input `data/puml_images_1568/fa3bc8bd559550992fd2c4e024d7a9872ea1ee76.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/fa3bc8bd559550992fd2c4e024d7a9872ea1ee76.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: fa3bc8bd559550992fd2c4e024d7a9872ea1ee76
' Original Path: /E-R/_diagrams/type/Type.1.0.0.ref.puml
' Source: World of Code

@startuml
hide methods
skinparam groupInheritance 2
skinparam class {
    ArrowColor Black
    BorderColor Black
    BackgroundColor<<master-data>> LightSalmon
    BackgroundColor<<work-product-component>> Gold
    BackgroundColor<<abstract>> LightSteelBlue
    BackgroundColor<<dataset>> Ivory
    BackgroundColor<<reference-data>> Turquoise
    BackgroundColor<<Abstraction>> LightSkyBlue
    BackgroundColor<<error>> Red
    BackgroundColor<<Activity>> LightSkyBlue
    BackgroundColor<<ReferenceType>> LightSkyBlue
    BackgroundColor<<WorkProductComponent>> LightSkyBlue
    BackgroundColor<<Project>> LightSkyBlue
    BackgroundColor<<File>> LightSkyBlue
    BackgroundColor<<FileCollection>> LightSkyBlue
    BackgroundColor<<MasterData>> LightSkyBlue
    BackgroundColor<<nested array>> WhiteSmoke
    BackgroundColor<<nested>> WhiteSmoke
    packageStyle rectangle
}
package "Type Referenced-by View" <<rectangle>>
{
class "<size:16>Type</size>" as Type <<type>>
left to right direction
class "Type" <<type>>
}
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title Type Referenced-by View

class Type <<type>> {
}

@enduml
```
```

#### `fcd65f7d8920511a96fcffe53538f6014bb6f64f` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=4 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=2 fn=1 F1=0.000; missed: inheritance; extra: inheritance, association
- chrF++: 33.97
- Files: GT `data/puml_files/fcd65f7d8920511a96fcffe53538f6014bb6f64f.puml` (yes) · pred `data/runs/claude-opus-4-6_20260614T081502Z/fcd65f7d8920511a96fcffe53538f6014bb6f64f.puml` (yes) · input `data/puml_images_1568/fcd65f7d8920511a96fcffe53538f6014bb6f64f.png` (yes) · render `data/csr/claude-opus-4-6_20260614T081502Z/png/fcd65f7d8920511a96fcffe53538f6014bb6f64f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: fcd65f7d8920511a96fcffe53538f6014bb6f64f
' Original Path: /northernwind/1.2-ALPHA-10/it-tidalwave-northernwind-modules/it-tidalwave-northernwind-core-default/testapidocs/it/tidalwave/northernwind/frontend/ui/spi/mock/MockRequestProcessor3.puml
' Source: World of Code

@startuml
    set namespaceSeparator none
    hide empty fields
    hide empty methods

    class "<size:14>MockRequestProcessor3\n<size:10>it.tidalwave.northernwind.frontend.ui.spi.mock" as it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessor3 [[MockRequestProcessor3.html]]

    class "<size:14>MockRequestProcessorSupport\n<size:10>it.tidalwave.northernwind.frontend.ui.spi.mock" as it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessorSupport [[MockRequestProcessorSupport.html]]

    it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessorSupport <|-- it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessor3

    center footer UMLDoclet 2.0.12, PlantUML 1.2020.16
@enduml
```

Prediction PlantUML:
```plantuml
@startuml

class "MockRequestProcessorSupport" as MockRequestProcessorSupport {
}

class "MockRequestProcessor3" as MockRequestProcessor3 {
}

MockRequestProcessor3 --|> MockRequestProcessorSupport

package "it.tidalwave.northwind.frontend.ui.spi.mock" {
}

note as N1
end note

hide N1

MockRequestProcessorSupport -[hidden]- N1

@enduml
```

### Gemini 3.1 Pro

#### outcome: compile_fail

#### `09ba2de07109b08b037d680246f10d2d5832b75f` — compile_fail (class, tier 1)

- CSR: `Error line 3 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/09ba2de07109b08b037d680246f10d2d5832b75f.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: inheritance, association
- chrF++: 34.37
- Files: GT `data/puml_files/09ba2de07109b08b037d680246f10d2d5832b75f.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/09ba2de07109b08b037d680246f10d2d5832b75f.puml` (yes) · input `data/puml_images_1568/09ba2de07109b08b037d680246f10d2d5832b75f.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/09ba2de07109b08b037d680246f10d2d5832b75f.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 09ba2de07109b08b037d680246f10d2d5832b75f
' Original Path: /examples/namespaces2.example.puml
' Source: World of Code

@startuml
class pkg_1.ClassDefinition
class pkg_2.ClassDefinition
pkg_1.ClassDefinition --> pkg_2.ClassDefinition 
pkg_1.ClassDefinition <|-- pkg_2.ClassDefinition 
@enduml 
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
package pkg_1 {
  class ClassDefinition as c1
}

package pkg_2 {
  class ClassDefinition as c2
}

c1 --> c2
c2 -up-|> c1
@enduml
```
```

#### `1067b9cef0f7617223a7f9ea212a6c7aa62e70cc` — compile_fail (class, tier 3)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 0.00
- Files: GT `data/puml_files/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.puml` (yes) · input `data/puml_images_1568/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 1067b9cef0f7617223a7f9ea212a6c7aa62e70cc
' Original Path: /UML/Character.puml
' Source: World of Code

@startuml
skinparam class{
    BorderColor black
    BackgroundColor #a3a3a3
}

class Character{
-GameDataRef _data;
-sf::Sprite sprite;
-sf::Vector2f position;
-sf::Texture texture;
-sf::Texture texture_flip;
-sf::Texture run_right1;
-sf::Texture run_right2;
-sf::Texture run_left1;
-sf::Texture run_left2;
-bool flip = false;
-sf::Clock animationClock;
-int animationRun = 0;
-bool air_texture = false;

+sf::Vector2f velocity = {0,0};
+float speed = 400.0f;
+float jump_speed = 600.0f;
+float slow_down = 0.0f, slow_down_ground = 40.0f, slow_down_air = 5.0f;
+float speed_up = 0.0f, speed_up_ground = 40.0f, speed_up_air = 30.0f;
+int max_jump =1, jump = 0;
+bool jump_done = false, on_ground = false;


-void flipTexture();

+Character(GameDataRef data);
+void update();
+void setTexture(6 Textures);
+void setPosition(const sf::Vector2f& position_);
+void setPosition(const float& x, const float& y);
+sf::Vector2f getPosition();
+void draw(sf::RenderWindow& renderWindow);
+void move(sf::Vector2f movement);
+void move(const float& x, const float& y);
+sf::Vector2f nextPosition(sf::Vector2f movement);
+sf::Sprite nextSprite(sf::Vector2f movement);
+sf::Sprite& getSprite();
+bool objectCollisionAndFalling(const sf::Sprite &object, const float& dt);
+void updateVelocity(const float& dt);
+void respawn(sf::Vector2f spawn);
+void characterKeyboardInput();
}

@enduml
```

Prediction PlantUML:
```plantuml

```

#### `2ad68bfb96f503d07911975c60844bae213469b5` — compile_fail (class, tier 1)

- CSR: `Error line 6 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/2ad68bfb96f503d07911975c60844bae213469b5.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=1 F1=0.000; missed: inheritance
- chrF++: 72.37
- Files: GT `data/puml_files/2ad68bfb96f503d07911975c60844bae213469b5.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/2ad68bfb96f503d07911975c60844bae213469b5.puml` (yes) · input `data/puml_images_1568/2ad68bfb96f503d07911975c60844bae213469b5.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/2ad68bfb96f503d07911975c60844bae213469b5.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 2ad68bfb96f503d07911975c60844bae213469b5
' Original Path: /Plantuml/DAL/Repositories/ITourRepository.puml
' Source: World of Code

@startuml
interface ITourRepository {
}
class "IRepository`1"<T> {
}
"IRepository`1" "<Tour>" <|-- ITourRepository
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
class IRepository`1<T> {
}
interface ITourRepository {
}
IRepository`1 <|-- ITourRepository : <Tour>
@enduml
```
```

#### `3478cb721e35eb60255dbb35c383ddac53a2789c` — compile_fail (sequence, tier 3)

- CSR: `Error line 23 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/3478cb721e35eb60255dbb35c383ddac53a2789c.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=10 F1=0.000; missed: message
- chrF++: 65.68
- Files: GT `data/puml_files/3478cb721e35eb60255dbb35c383ddac53a2789c.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/3478cb721e35eb60255dbb35c383ddac53a2789c.puml` (yes) · input `data/puml_images_1568/3478cb721e35eb60255dbb35c383ddac53a2789c.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/3478cb721e35eb60255dbb35c383ddac53a2789c.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 3478cb721e35eb60255dbb35c383ddac53a2789c
' Original Path: /GameEnginePlugin/Docs/SourceDiagrams/GameEnginePlugin-Lifecycle-Sequence.plantuml
' Source: World of Code

@startuml

title "GameEnginePluginLifecycle"

participant "Host Application" as HA

HA -> HA: Initialization
activate HA

create participant "Host Application Interop" as HAI
HA -> HAI: new

deactivate HA

HAI -> HAI: Load GE Plugin(s)
activate HAI

create participant "Game Engine Plugin" as GEP
HAI -> GEP: load into memory
HAI -> GEP: GEP_Initialize
activate GEP
GEP --> HAI: initialization_ok = 0
deactivate GEP
...

loop Repeat Every Frame Period
HAI -> GEP: GEP_HandleSimulationReponseMessages
activate GEP
GEP --> HAI: handled_ok = 0
deactivate GEP
... delays ...
HAI -> GEP: GEP_HandleSimulationControlMessages
activate GEP
GEP --> HAI: handled_ok = 0
deactivate GEP
end



@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title GameEnginePluginLifecycle

participant "Host Application" as HostApp
participant "Host Application Interop" as HostAppInterop
participant "Game Engine Plugin" as GameEnginePlugin

HostApp -> HostApp : Initialization
activate HostApp
HostApp -> HostAppInterop : new
deactivate HostApp

activate HostAppInterop
HostAppInterop -> HostAppInterop : Load GE Plugin(s)
HostAppInterop -> GameEnginePlugin : load into memory
HostAppInterop -> GameEnginePlugin : GEP_Initialize
activate GameEnginePlugin
GameEnginePlugin --> HostAppInterop : initialization_ok = 0
deactivate GameEnginePlugin
deactivate HostAppInterop

loop Repeat Every Frame Period
    activate HostAppInterop
    HostAppInterop -> GameEnginePlugin : GEP_HandleSimulationReponseMessages
    activate GameEnginePlugin
    GameEnginePlugin --> HostAppInterop : handled_ok = 0
    deactivate GameEnginePlugin
    deactivate HostAppInterop
    
    ... delays ...
    
    activate HostAppInterop
    HostAppInterop -> GameEnginePlugin : GEP_HandleSimulationControlMessages
    activate GameEnginePlugin
    GameEnginePlugin --> HostAppInterop : handled_ok = 0
    deactivate GameEnginePlugin
    deactivate HostAppInterop
end

@enduml
```
```

#### `50efbc2a904f22fbb497d5a040e14bc419bebf26` — compile_fail (class, tier 3)

- CSR: `Error line 4 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/50efbc2a904f22fbb497d5a040e14bc419bebf26.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: inheritance, dependency
- chrF++: 69.80
- Files: GT `data/puml_files/50efbc2a904f22fbb497d5a040e14bc419bebf26.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/50efbc2a904f22fbb497d5a040e14bc419bebf26.puml` (yes) · input `data/puml_images_1568/50efbc2a904f22fbb497d5a040e14bc419bebf26.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/50efbc2a904f22fbb497d5a040e14bc419bebf26.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 50efbc2a904f22fbb497d5a040e14bc419bebf26
' Original Path: /uml/controller-class.puml
' Source: World of Code

@startuml
hide empty members
namespace controller {
    interface Controller {
        + execute(args : json) : json
    }
    class Factory {
        + create(name : string) : Controller
    }
    class Amount
    class Transfer
    class TransferSend

    Controller <|.. Amount
    Controller <|.. Transfer
    Controller <|.. TransferSend
    Amount <.. Factory : create
    Transfer <.. Factory : create
    TransferSend <.. Factory : create
    model.User <.. Amount
    Amount ..> view.Amount
}
namespace view {
    class Amount
}
namespace model {
    class User
}
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
package controller {
  package model as c_model {
    class User as c_User
  }
  
  interface Controller {
    + execute(args : json) : json
  }
  
  class Amount as c_Amount
  class TransferSend
  class Transfer
  
  class Factory {
    + create(name : string) : Controller
  }
  
  package view as c_view {
    class Amount as cv_Amount
  }
  
  Controller <|.. c_Amount
  Controller <|.. TransferSend
  Controller <|.. Transfer
  
  c_Amount .up.> c_User
  c_Amount .down.> cv_Amount
  
  Factory .up.> c_Amount : create
  Factory .up.> TransferSend : create
  Factory .up.> Transfer : create
}

package view {
  class Amount as v_Amount
}

package model {
  class User as m_User
}
@enduml
```
```

#### `73ece5e02bc2f9114ad86167383908b5178e2e6a` — compile_fail (sequence, tier 4)

- CSR: `Error line 12 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/73ece5e02bc2f9114ad86167383908b5178e2e6a.puml`
- Element: tp=0 fp=0 fn=8 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=20 F1=0.000; missed: message
- chrF++: 41.42
- Files: GT `data/puml_files/73ece5e02bc2f9114ad86167383908b5178e2e6a.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/73ece5e02bc2f9114ad86167383908b5178e2e6a.puml` (yes) · input `data/puml_images_1568/73ece5e02bc2f9114ad86167383908b5178e2e6a.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/73ece5e02bc2f9114ad86167383908b5178e2e6a.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 73ece5e02bc2f9114ad86167383908b5178e2e6a
' Original Path: /docs/gradivo/plantuml/diagramZaporedja350.puml
' Source: World of Code

@startuml
hide footbox

skinparam backgroundcolor transparent
skinparam defaultTextAlignment center
skinparam actorBorderColor black
skinparam actorBackgroundColor white
skinparam arrowColor black  
skinparam sequenceLifeLineBorderColor #5FB8EC
skinparam sequenceParticipantBorderColor #5FB8EC
skinparam sequenceParticipantBackgroundColor white


actor "Upravljalec dogodkov" as Prijavljen <<actor>>
participant "ZMDomačaStran" as DomacaStran <<boundary>>  #lightBlue
participant "KrmilnikNovica" as NKrmilnik <<control>> #lightGray
participant "KrmilnikPredloga" as PKrmilnik <<control>> #lightGray
participant "KrmilnikDogodek" as DKrmilnik <<control>> #lightGray
participant "PredlogProjekta" as Predloga <<entity>> #lightYellow
participant Novica <<entity>> #lightYellow
participant "SVGoogleCalendar\n API" as Dogodek <<boundary>>  #lightBlue

Prijavljen -> DomacaStran: 1. prikazDomacaStran()

DomacaStran -> DKrmilnik: 2. vrniSeznamDogodkov(req, res)
activate DKrmilnik
DKrmilnik -> Dogodek: 3. vrniSeznamDogodkovIzKoledarja()\n // GET klic na\nhttps://www.googleapis.com/calendar/v3/users/me/calendarList
activate Dogodek
DKrmilnik <-- Dogodek: // sporočilo OK in seznam dogodkov
deactivate Dogodek
DomacaStran <-- DKrmilnik: // vrni seznam dogodkov
deactivate DKrmilnik
DomacaStran -> NKrmilnik: 4. vrniZadnjeNovice(req, res)
activate NKrmilnik
NKrmilnik -> Novica: 5. vrniVsiFilter(req, res)
activate Novica
NKrmilnik <-- Novica: // sporočilo OK in seznam zadnjih 4 novic
deactivate Novica
DomacaStran <-- NKrmilnik: // vrni zadnje 4 novice
deactivate NKrmilnik
DomacaStran -> PKrmilnik: 6. vrniNajPriljubljeni(req, res)
activate PKrmilnik
PKrmilnik -> Predloga: 7. vrniVsiFilter(req, res)
activate Predloga
PKrmilnik <-- Predloga: // sporočilo OK in seznam\nnajbolj priljubljenih predlogov
deactivate Predloga
DomacaStran <-- PKrmilnik: // vrni najbolj priljubljenih predlogov\nin prikaži domačo stran
deactivate PKrmilnik
activate DomacaStran
DomacaStran -> DKrmilnik: 8. prikaziDogodek(req, res)
activate DKrmilnik
DKrmilnik -> Dogodek: 9. prikaziDogodekIzKoledarja()\n // GET klic na\nhttps://www.googleapis.com/calendar/v3/calendars/[calendarId]/events
activate Dogodek
DKrmilnik <-- Dogodek: // sporočilo OK in izbran dogodek
deactivate Dogodek
DomacaStran <-- DKrmilnik: // prikaži podatke o izbranega dogodka\n(odpri modalno okno)
deactivate DKrmilnik
activate DomacaStran
DomacaStran -> DKrmilnik: 10. dodajDogodek(req, res)
activate DKrmilnik
DKrmilnik -> DKrmilnik: 11. validacijaAtriburov(body)
activate DKrmilnik
deactivate DKrmilnik
DomacaStran <-- DKrmilnik: // sporočilo o napačni vnosni vrednosti
deactivate DKrmilnik
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam backgroundColor black
skinparam defaultFontColor white
skinparam sequence {
    ArrowColor white
    LifeLineBorderColor white
    LifeLineBackgroundColor white
    ParticipantBorderColor white
    ParticipantBackgroundColor lightblue
}

actor "" as User

participant "<<boundary>>\nZMDomačaStran" as ZMDomačaStran
participant "<<control>>\nKrmilnikNovica" as KrmilnikNovica
participant "<<control>>\nKrmilnikPredloga" as KrmilnikPredloga
participant "<<control>>\nKrmilnikDogodek" as KrmilnikDogodek
participant "<<entity>>\nPredlogProjekta" as PredlogProjekta <<entity>> #lightyellow
participant "<<entity>>\nNovica" as Novica <<entity>> #lightyellow
participant "<<boundary>>\nSVGoogleCalendar\nAPI" as SVGoogleCalendarAPI

activate KrmilnikDogodek
KrmilnikDogodek -> SVGoogleCalendarAPI : pridobiDogodke()
activate SVGoogleCalendarAPI
SVGoogleCalendarAPI --> KrmilnikDogodek : dogodki
deactivate SVGoogleCalendarAPI
deactivate KrmilnikDogodek

activate KrmilnikNovica
KrmilnikNovica -> Novica : pridobiNovice()
activate Novica
Novica --> KrmilnikNovica : novice
deactivate Novica
deactivate KrmilnikNovica

activate KrmilnikPredloga
KrmilnikPredloga -> PredlogProjekta : pridobiPredloge()
activate PredlogProjekta
PredlogProjekta --> KrmilnikPredloga : predlogi
deactivate PredlogProjekta
deactivate KrmilnikPredloga

User -> ZMDomačaStran : prikažiDomačoStran()
activate ZMDomačaStran

ZMDomačaStran -> KrmilnikDogodek : pridobiDogodke()
activate KrmilnikDogodek
KrmilnikDogodek -> SVGoogleCalendarAPI : pridobiDogodke()
activate SVGoogleCalendarAPI
SVGoogleCalendarAPI --> KrmilnikDogodek : dogodki
deactivate SVGoogleCalendarAPI
KrmilnikDogodek --> ZMDomačaStran : dogodki
deactivate KrmilnikDogodek

ZMDomačaStran -> KrmilnikDogodek : prikažiDogodke()
activate ZMDomačaStran
activate KrmilnikDogodek
KrmilnikDogodek --> ZMDomačaStran : prikazani dogodki
deactivate KrmilnikDogodek
deactivate ZMDomačaStran

deactivate ZMDomačaStran

@enduml
```
```

#### `7b304edd43574ce0671a402e1bb4c248595eafe1` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=18 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=13 F1=0.000; missed: inheritance, association
- chrF++: 0.00
- Files: GT `data/puml_files/7b304edd43574ce0671a402e1bb4c248595eafe1.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/7b304edd43574ce0671a402e1bb4c248595eafe1.puml` (yes) · input `data/puml_images_1568/7b304edd43574ce0671a402e1bb4c248595eafe1.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/7b304edd43574ce0671a402e1bb4c248595eafe1.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 7b304edd43574ce0671a402e1bb4c248595eafe1
' Original Path: /documents/diagram/FAQ/FAQClass.puml
' Source: World of Code

@startuml

package dao {


    abstract QuestionDao{
        # OfferDao()
        + {static} getInstance() : QuestionDao
        - {static} LazyHolder()
        getQuestionsByOfferId(offerId : int) : ArrayList<Question>
        questionExists(id : int) : boolean
        hasAnAnswer(id : int) : boolean
    }

    abstract AnswerDao{
        # OfferDao()
        + {static} getInstance() : QuestionDao
        - {static} LazyHolder()
        getAnswersByOfferId(offerId : int) : ArrayList<Answer>
        answerExists(id : int) : boolean
    }

    class QuestionDaoMySQL
    QuestionDaoMySQL -up-|> QuestionDao

    class AnswerDaoMySQL
    FactoryDaoMySQL -up-|> AbstractFactoryDao
    AnswerDaoMySQL -up-|> AnswerDao

    interface DAO<T>{
        find(id : int) : T
        create(T obj) : T
        update(T obj) : T
        delete(T obj) : boolean
    }

    abstract AbstractFactoryDao{
        - {static} final connectionDB : ConnectionDB
        + {static} getFactory(type : TypeDB) : AbstractFactoryDao
        + getAnswerDao() : AnswerDao
        + getQuestionDao() : QuestionDao
    }

    class FactoryDaoMySQL{
    }

    DAO <|.. AnswerDao
    DAO <|.. QuestionDao
    QuestionDao-->AbstractFactoryDao
    AnswerDao-->AbstractFactoryDao
}
package db{
    class ConnectionDBMySQL{
        - connection : Connection
        - ConnectionDBMySQL()
        + {static} getInstance() : ConnectionDBMySQL
        + getDb() : Connection
    }

    class LazyHolderDB{
        + {static} final INSTANCE : ConnectionDBMySQL
    }
    interface ConnectionDB
    ConnectionDBMySQL -Left-> LazyHolderDB
    ConnectionDBMySQL .up.|> ConnectionDB

}
package business{
    class SessionFacade{
        + SessionFacade()
        + getUser() : User
    }

    class Question{
        -questionId : int
        -content : String
```

Prediction PlantUML:
```plantuml

```

#### `aa009f3e775e94758c8ab4de152c1c180ba307cf` — compile_fail (sequence, tier 2)

- CSR: `Error line 7 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/aa009f3e775e94758c8ab4de152c1c180ba307cf.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: message
- chrF++: 77.62
- Files: GT `data/puml_files/aa009f3e775e94758c8ab4de152c1c180ba307cf.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/aa009f3e775e94758c8ab4de152c1c180ba307cf.puml` (yes) · input `data/puml_images_1568/aa009f3e775e94758c8ab4de152c1c180ba307cf.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/aa009f3e775e94758c8ab4de152c1c180ba307cf.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: aa009f3e775e94758c8ab4de152c1c180ba307cf
' Original Path: /RASD/uml/sequence/request_help.puml
' Source: World of Code

@startuml

mainframe Request help
autonumber

actor Farmer
participant DREAM

Farmer -> DREAM++: Request help
DREAM --> Farmer--: Show help request creation form

Farmer -> DREAM++: Provide topic and contents of the message
DREAM -> DREAM++: Create help request
deactivate DREAM

alt operation successful
    DREAM --> Farmer : Display the request created
else operation failed
    DREAM --> Farmer--: Show error message
end

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
hide footbox
skinparam sequenceMessageAlign left

frame "Request help" {
    actor Farmer
    participant DREAM

    Farmer -> DREAM : 1 Request help
    activate DREAM
    DREAM --> Farmer : 2 Show help request creation form
    deactivate DREAM

    Farmer -> DREAM : 3 Provide topic and contents of the message
    activate DREAM
    DREAM -> DREAM : 4 Create help request
    activate DREAM
    deactivate DREAM

    alt operation successful
        DREAM --> Farmer : 5 Display the request created
    else operation failed
        DREAM --> Farmer : 6 Show error message
    end
    deactivate DREAM
}
@enduml
```
```

#### `c6ac7f451f42cac92507604a1b841848a2618f30` — compile_fail (sequence, tier 2)

- CSR: `Error line 17 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/c6ac7f451f42cac92507604a1b841848a2618f30.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: message
- chrF++: 77.69
- Files: GT `data/puml_files/c6ac7f451f42cac92507604a1b841848a2618f30.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/c6ac7f451f42cac92507604a1b841848a2618f30.puml` (yes) · input `data/puml_images_1568/c6ac7f451f42cac92507604a1b841848a2618f30.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/c6ac7f451f42cac92507604a1b841848a2618f30.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: c6ac7f451f42cac92507604a1b841848a2618f30
' Original Path: /sequence_code/professor/professor.viewallstudents.wsd
' Source: World of Code

@startuml
actor Professor
boundary "tela principal" as home
'boundary "tela de documentos" as documentos
control StudentController
'control DocumentController
entity StudentEntity
'entity DocumentEntity
activate Professor
Professor -> home: visualizar a lista de alunos
activate home
home ->> StudentController: requisitar lista de alunos
'deactivate home
activate StudentController
StudentController -> StudentEntity: buscar por alunos
deactivate StudentController
activate StudentEntity
StudentEntity --> StudentController: lista de alunos
deactivate StudentEntity
activate StudentController
StudentController -->> home: responder com a lista de alunos
deactivate StudentController
'activate home
home --> Professor: exibir lista de alunos
deactivate home
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
actor Professor
boundary "tela principal" as tela
control StudentController
entity StudentEntity

activate Professor
Professor -> tela : visualizar a lista de alunos
activate tela
tela -> StudentController : requisitar lista de alunos
activate StudentController
StudentController -> StudentEntity : buscar por alunos
activate StudentEntity
StudentEntity --> StudentController : lista de alunos
deactivate StudentEntity
deactivate StudentController
activate StudentController
StudentController --> tela : responder com a lista de alunos
deactivate StudentController
tela --> Professor : exibir lista de alunos
deactivate tela
deactivate Professor
@enduml
```
```

#### `d88ff3fb6aa3f88e69a804beac0eb19ed5b0d639` — compile_fail (sequence, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=17 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=62 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/d88ff3fb6aa3f88e69a804beac0eb19ed5b0d639.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/d88ff3fb6aa3f88e69a804beac0eb19ed5b0d639.puml` (yes) · input `data/puml_images_1568/d88ff3fb6aa3f88e69a804beac0eb19ed5b0d639.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/d88ff3fb6aa3f88e69a804beac0eb19ed5b0d639.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: d88ff3fb6aa3f88e69a804beac0eb19ed5b0d639
' Original Path: /Final/Sequence/Class/BookingClass.wsd
' Source: World of Code

@startuml

skinparam Monochrome true
skinparam Shadowing false
hide footbox

actor Admin
participant ":AddEventPage" as AddEventPage
participant ":AddEventFormContainer" as AddEventFormContainer
participant ":AddClassPopupContainer" as AddClassPopupContainer
participant ":ClassForm" as ClassForm
participant ":ClassService (Frontend)" as FEClassService
participant ":ShiftService (Frontend)" as FEShiftService
participant ":Router" as Router
participant ":ClassHTTPTransport" as ClassHTTPTransport
participant ":ClassEndpoint" as ClassEndpoint
participant ":ClassService" as ClassService
participant ":ClassCommand" as ClassCommand
participant ":ClassQuery" as ClassQuery
participant ":TransactionGRPCTransport" as TransactionGRPCTransport
participant ":StorageGRPC Transport" as StorageGRPCTransport
participant ":MaterialService" as MaterialService
participant ":NatsStreaming" as NatsStreaming

Admin->AddEventPage: Click "Attach New Class" Button
AddEventPage->AddEventFormContainer: attachClass()
AddEventFormContainer-->AddEventPage: attach
AddEventPage-->Admin: attach

Admin->AddClassPopupContainer: Render "Add Class Popup" Container
AddClassPopupContainer->ClassForm: render
ClassForm-->AddClassPopupContainer: rendered
AddClassPopupContainer-->Admin: Rendered

Admin->AddClassPopupContainer: choose date
AddClassPopupContainer->ClassForm: handleDateChange(value)
ClassForm->FEShiftService: fetchAvailableShifts(date)
FEShiftService-->ClassForm: shifts
ClassForm-->AddClassPopupContainer: form data
AddClassPopupContainer-->Admin: form data

Admin->AddClassPopupContainer: choose shift
AddClassPopupContainer->ClassForm: handleShiftChange()
ClassForm->FEShiftService: fetchAvailableShifts(date, []shift)
FEShiftService-->ClassForm: rooms
ClassForm-->AddClassPopupContainer: form data
AddClassPopupContainer-->Admin: form data

Admin->AddClassPopupContainer: Fill Form
AddClassPopupContainer-->Admin: form data

Admin->AddClassPopupContainer: Click "Create Class" Button
AddClassPopupContainer->AddClassPopupContainer: handleClassFormSubmitted()
AddClassPopupContainer->FEClassService: bookingClass(payload)

FEClassService->Router: route("GET", "v2/booking")
Router->ClassHTTPTransport: BookingClass(ClassService, []ServerOption)
ClassHTTPTransport->ClassEndpoint: Booking(ClassService, withPaginated)
ClassEndpoint->ClassService: Create(context, params)
ClassService->ClassService: Validate()

alt "Data Valid"
    ClassService->TransactionGRPCTransport: IsValidTransaction(ProtoBuffer)
    TransactionGRPCTransport-->ClassService: ProtoResponse

    alt "Is Valid Transaction"
        ClassService->ClassService: class := ClassModel()
        ClassService->ClassCommand: Create(context, class)
        ClassCommand-->ClassService: uuid

        opt "has materials"
            ClassService->StorageGRPCTransport: CommitFile(context, ProtoBuffer)
            StorageGRPCTransport-->ClassService: link

            ClassService->MaterialService: Create(context, payload)
            MaterialService-->ClassService: isCreated
```

Prediction PlantUML:
```plantuml

```

#### `dd18a88b118626df1c03faa29d229393627c778c` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=8 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=11 F1=0.000; missed: aggregation
- chrF++: 0.00
- Files: GT `data/puml_files/dd18a88b118626df1c03faa29d229393627c778c.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/dd18a88b118626df1c03faa29d229393627c778c.puml` (yes) · input `data/puml_images_1568/dd18a88b118626df1c03faa29d229393627c778c.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/dd18a88b118626df1c03faa29d229393627c778c.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: dd18a88b118626df1c03faa29d229393627c778c
' Original Path: /7OPR2_KU1/src/cz/osu/student/R19584/Library.puml
' Source: World of Code

@startuml

title 'R19584 KU1 - Knihovna'

class Library {
    - books : ArrayList<Book>
    - persons : ArrayList<Person>
    - borrowings : ArrayList<Borrowing>
    - standardBorrowingPeriod : int

    + Library()

    + addBook(book : Book) : void
    + addPerson(person : Person) : void
    + addBorrowing(borrowing : Borrowing) : void

    + addBooks(books : ArrayList<Book>) : void
    + addPersons(persons : ArrayList<Person>) : void
    + addBorrowings(borrowings : ArrayList<Borrowing>) : void

    + getBooks() : ArrayList<Book>
    + getBookBorrowings(book: Book) : ArrayList<Borrowing>

    + getPersons() : ArrayList<Person>
    + getPersonBorrowings(person: Person) : ArrayList<Borrowing>
    + getPersonPenalties(person: Person) : ArrayList<Penalty>

    + penalisePerson(person : Person, penalty : Penalty) : void

    + getBorrowings() : ArrayList<Borrowing>
    + getAllBorrowingsThatAreOverdue() : ArrayList<Borrowing>

    + isBorrowingOverdue(borrowing : Borrowing) : boolean

    + extendBorrowing(borrowing : Borrowing) : void
    + returnBookAndEndBorrowing(borrowing : Borrowing) : void
    + borrowBookToPerson(person : Person, book : Book) : void

    + toString() : String
}

Library -o IDSingleton
Library -o Book
Library -o Borrowing
Library -o Person
Library -o DateTime

class IDSingleton {
    - instance : IDSingleton <<static>>
    - idCounter : int <<static>>

    - IDSingleton()

    + getInstance() : IDSingleton <<static>>

    + getId() : int
}

class Book {
    - author : Person
    - title : String
    - publisher : String
    - isbn : String

    + Book(author : Person, title : String, publisher : String, isbn : String)

    + getAuthor() : Person
    + getTitle() : String
    + getPublisher() : String
    + getISBN() : String

    + toString() : String
}

Book -o Person

```

Prediction PlantUML:
```plantuml

```

#### `de434622c1f498168c9bccf95ceb52a9dc1ef385` — compile_fail (sequence, tier 3)

- CSR: `Error line 6 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/de434622c1f498168c9bccf95ceb52a9dc1ef385.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=7 F1=0.000; missed: message
- chrF++: 50.86
- Files: GT `data/puml_files/de434622c1f498168c9bccf95ceb52a9dc1ef385.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/de434622c1f498168c9bccf95ceb52a9dc1ef385.puml` (yes) · input `data/puml_images_1568/de434622c1f498168c9bccf95ceb52a9dc1ef385.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/de434622c1f498168c9bccf95ceb52a9dc1ef385.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: de434622c1f498168c9bccf95ceb52a9dc1ef385
' Original Path: /docs/gradivo/plantuml/diagramZaporedja1.puml
' Source: World of Code

@startuml
hide footbox

skinparam backgroundcolor transparent
skinparam defaultTextAlignment center
skinparam actorBorderColor black
skinparam actorBackgroundColor white
skinparam arrowColor black  
skinparam sequenceLifeLineBorderColor #5FB8EC
skinparam sequenceParticipantBorderColor #5FB8EC
skinparam sequenceParticipantBackgroundColor white

actor "Neregistrirani uporabnik" as Neregistriran <<actor>>
participant "ZMRegistracijskiObrazec" as Obrazec <<boundary>> #lightBlue
participant "ZMDomačaStran" as DomacaStran <<boundary>> #lightBlue
participant "KrmilnikRegistracija" as Krmilnik <<control>> #lightGray
participant Uporabnik <<entity>> #lightYellow

Neregistriran -> Obrazec: 1. zacniRegistracijo()
activate Obrazec
Obrazec -> Krmilnik: 2. registracija(req, res)
activate Krmilnik
Krmilnik -> Krmilnik: 3. validacijaAtributov(body)
activate Krmilnik
deactivate Krmilnik
Krmilnik -> Uporabnik: 4. dodajUporabnik(req, res)
activate Uporabnik
Uporabnik -> Uporabnik: 5. preveriAtribute(akcija)
activate Uporabnik
deactivate Uporabnik
Krmilnik <-- Uporabnik: // sporočilo OK
deactivate Uporabnik
Krmilnik -> DomacaStran: 6. preusmeriNaDomacoStran()
deactivate Krmilnik
deactivate Obrazec
activate DomacaStran
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam maxMessageSize 150
skinparam ParticipantPadding 20
skinparam BoxPadding 10

actor "" as User
participant "<<boundary>>\nZMRegistracijskiObrazec" as ZMRegistracijskiObrazec <<boundary>> #LightBlue
participant "<<boundary>>\nZMDomačaStran" as ZMDomačaStran <<boundary>> #LightBlue
participant "<<control>>\nKrmilnikRegistracija" as KrmilnikRegistracija <<control>> #LightGray
participant "<<entity>>\nUporabnik" as Uporabnik <<entity>> #LightYellow

User -> ZMRegistracijskiObrazec : vnesiPodatke(ime, priimek, email, geslo)
activate ZMRegistracijskiObrazec

ZMRegistracijskiObrazec -> KrmilnikRegistracija : registriraj(ime, priimek, email, geslo)
activate KrmilnikRegistracija

KrmilnikRegistracija -> KrmilnikRegistracija : preveriPodatke()
activate KrmilnikRegistracija
deactivate KrmilnikRegistracija

KrmilnikRegistracija -> Uporabnik : ustvari(ime, priimek, email, geslo)
activate Uporabnik

Uporabnik -> Uporabnik : shrani()
activate Uporabnik
deactivate Uporabnik

Uporabnik --> KrmilnikRegistracija : uspeh
deactivate Uporabnik

KrmilnikRegistracija --> ZMRegistracijskiObrazec : uspeh
deactivate KrmilnikRegistracija

ZMRegistracijskiObrazec -> ZMDomačaStran : prikaži()
activate ZMDomačaStran
deactivate ZMDomačaStran

deactivate ZMRegistracijskiObrazec

@enduml
```
```

#### `e9a06725c4d85ec28ca9d343c1f23ab41d0e398f` — compile_fail (sequence, tier 1)

- CSR: `Error line 2 in file: data/csr/gemini-3.1-pro-preview_20260613T154356Z/extracted/e9a06725c4d85ec28ca9d343c1f23ab41d0e398f.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=3 F1=0.000; missed: message
- chrF++: 64.84
- Files: GT `data/puml_files/e9a06725c4d85ec28ca9d343c1f23ab41d0e398f.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/e9a06725c4d85ec28ca9d343c1f23ab41d0e398f.puml` (yes) · input `data/puml_images_1568/e9a06725c4d85ec28ca9d343c1f23ab41d0e398f.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/e9a06725c4d85ec28ca9d343c1f23ab41d0e398f.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: e9a06725c4d85ec28ca9d343c1f23ab41d0e398f
' Original Path: /60030041/sequence diagram1.puml
' Source: World of Code

@startuml
actor "พนักงาน"
participant "ตรวจสอบสินค้า"
participant "จัดการข้อมูลสินค้า"
"พนักงาน" -> "ตรวจสอบสินค้า":สินค้ามาใหม่
"ตรวจสอบสินค้า" --> "จัดการข้อมูลสินค้า":เพิ่มสินค้า
 "จัดการข้อมูลสินค้า" --> "ตรวจสอบสินค้า":เพิ่มสินค้าเรียบร้อย
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
actor พนักงาน
participant ตรวจสอบสินค้า
participant จัดการข้อมูลสินค้า

พนักงาน -> ตรวจสอบสินค้า : สินค้ามาใหม่
ตรวจสอบสินค้า --> จัดการข้อมูลสินค้า : เพิ่มสินค้า
จัดการข้อมูลสินค้า --> ตรวจสอบสินค้า : เพิ่มสินค้าเรียบร้อย
@enduml
```
```

#### outcome: compiled_low_structural

#### `0bffda3c561066aa0dda7f556b2ce91406230f86` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=1 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 52.49
- Files: GT `data/puml_files/0bffda3c561066aa0dda7f556b2ce91406230f86.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/0bffda3c561066aa0dda7f556b2ce91406230f86.puml` (yes) · input `data/puml_images_1568/0bffda3c561066aa0dda7f556b2ce91406230f86.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/0bffda3c561066aa0dda7f556b2ce91406230f86.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 0bffda3c561066aa0dda7f556b2ce91406230f86
' Original Path: /docs/javadocs/soen6441riskgame/enums/ConquestMapPart.puml
' Source: World of Code

@startuml

skinparam svgLinkTarget _parent
skinparam linetype ortho
set namespaceSeparator none
enum "<b><size:14>ConquestMapPart</b>\n<size:10>soen6441riskgame.enums" as soen6441riskgame.enums.ConquestMapPart  [[../../soen6441riskgame/enums/ConquestMapPart.html{soen6441riskgame.enums.ConquestMapPart}]] {
-String part
-ConquestMapPart(String part)
{static} +ConquestMapPart values()
{static} +ConquestMapPart valueOf(String name)
+String getPart()
{static} +ConquestMapPart fromString(String part)
}



@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
enum ConquestMapPart <<soen6441riskgame.enums>> {
  - String part
  - ConquestMapPart(String part)
  + {static} ConquestMapPart values()
  + {static} ConquestMapPart valueOf(String name)
  + String getPart()
  + {static} ConquestMapPart fromString(String part)
}
@enduml
```
```

#### `1348037e5ef89ad46e650939b2d95a74c9b563b9` — compiled_low_structural (class, tier 4)

- Element: tp=16 fp=7 fn=7 F1=0.696; type-acc matched=16 correct=16 excluded=0
- Relationship: tp=10 fp=10 fn=15 F1=0.444; missed: inheritance, association; extra: inheritance, association
- chrF++: 74.05
- Files: GT `data/puml_files/1348037e5ef89ad46e650939b2d95a74c9b563b9.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/1348037e5ef89ad46e650939b2d95a74c9b563b9.puml` (yes) · input `data/puml_images_1568/1348037e5ef89ad46e650939b2d95a74c9b563b9.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/1348037e5ef89ad46e650939b2d95a74c9b563b9.png` (yes)

#### `1bca4778a2b1752ff82d4954b38bd9f6f92cdcda_02` — compiled_low_structural (class, tier 4)

- Element: tp=7 fp=2 fn=2 F1=0.778; type-acc matched=7 correct=7 excluded=0
- Relationship: tp=4 fp=7 fn=7 F1=0.364; missed: composition, association; extra: composition, dependency, association
- chrF++: 77.77
- Files: GT `data/puml_files/1bca4778a2b1752ff82d4954b38bd9f6f92cdcda_02.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/1bca4778a2b1752ff82d4954b38bd9f6f92cdcda_02.puml` (yes) · input `data/puml_images_1568/1bca4778a2b1752ff82d4954b38bd9f6f92cdcda_02.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/1bca4778a2b1752ff82d4954b38bd9f6f92cdcda_02.png` (yes)

#### `32b85a4b1e1cbb51aa4826fda391a023e6375ba1` — compiled_low_structural (sequence, tier 3)

- Element: tp=2 fp=4 fn=4 F1=0.333; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=10 fn=10 F1=0.000; missed: message; extra: message
- chrF++: 83.99
- Files: GT `data/puml_files/32b85a4b1e1cbb51aa4826fda391a023e6375ba1.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/32b85a4b1e1cbb51aa4826fda391a023e6375ba1.puml` (yes) · input `data/puml_images_1568/32b85a4b1e1cbb51aa4826fda391a023e6375ba1.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/32b85a4b1e1cbb51aa4826fda391a023e6375ba1.png` (yes)

#### `4a72ca2b5b92d37dcb648df24cbbd7d0bf7bec7b` — compiled_low_structural (sequence, tier 3)

- Element: tp=1 fp=5 fn=5 F1=0.167; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=16 fn=16 F1=0.000; missed: message; extra: message
- chrF++: 59.98
- Files: GT `data/puml_files/4a72ca2b5b92d37dcb648df24cbbd7d0bf7bec7b.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/4a72ca2b5b92d37dcb648df24cbbd7d0bf7bec7b.puml` (yes) · input `data/puml_images_1568/4a72ca2b5b92d37dcb648df24cbbd7d0bf7bec7b.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/4a72ca2b5b92d37dcb648df24cbbd7d0bf7bec7b.png` (yes)

#### `4dc97fd76002a99da5ddf57b1d44a80dcba69757` — compiled_low_structural (sequence, tier 1)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: message; extra: message
- chrF++: 63.99
- Files: GT `data/puml_files/4dc97fd76002a99da5ddf57b1d44a80dcba69757.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/4dc97fd76002a99da5ddf57b1d44a80dcba69757.puml` (yes) · input `data/puml_images_1568/4dc97fd76002a99da5ddf57b1d44a80dcba69757.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/4dc97fd76002a99da5ddf57b1d44a80dcba69757.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 4dc97fd76002a99da5ddf57b1d44a80dcba69757
' Original Path: /doc/profiles/alias/discovery.puml
' Source: World of Code

@startuml
title Discovery
actor Client
participant "<&share> Alias" as Alias

Client -> Alias: HEAD
Alias --> Client: 307 Temporary Redirect / 308 Permanent Redirect
rnote left #lightgreen
  <#lightgreen,lightgreen>|= Header |= Value |
  | ""Profile"" | ""<http://level3.rest/profiles/alias>"", |
  | | ""<target-profile>"" |
  | ""Allow"" | //target's ""Allow"" values// |
  | ""Location"" | //target URL// |
end note
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title Discovery

actor Client
participant "Alias" as Alias << (R,#E6E6FA) >>

Client -> Alias : HEAD
Alias --> Client : 307 Temporary Redirect / 308 Permanent Redirect

note left of Client
  **Header**    **Value**
  Profile   <http://level3.rest/profiles/alias>,
            <target-profile>
  Allow     //target's Allow values//
  Location  //target URL//
end note

@enduml
```
```

#### `532d5a1ff757de7127780cff4493ccdd7a51c49a` — compiled_low_structural (sequence, tier 4)

- Element: tp=1 fp=12 fn=12 F1=0.077; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=41 fn=34 F1=0.000; missed: message; extra: message
- chrF++: 64.03
- Files: GT `data/puml_files/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/532d5a1ff757de7127780cff4493ccdd7a51c49a.puml` (yes) · input `data/puml_images_1568/532d5a1ff757de7127780cff4493ccdd7a51c49a.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/532d5a1ff757de7127780cff4493ccdd7a51c49a.png` (yes)

#### `5e99debce2d543725f50deb8c3a3dfaa1e065e91` — compiled_low_structural (class, tier 3)

- Element: tp=2 fp=1 fn=1 F1=0.667; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: inheritance, association; extra: inheritance, association
- chrF++: 39.91
- Files: GT `data/puml_files/5e99debce2d543725f50deb8c3a3dfaa1e065e91.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/5e99debce2d543725f50deb8c3a3dfaa1e065e91.puml` (yes) · input `data/puml_images_1568/5e99debce2d543725f50deb8c3a3dfaa1e065e91.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/5e99debce2d543725f50deb8c3a3dfaa1e065e91.png` (yes)

#### `6c7324c7eaeb23cd5644654ea022ca212ecd24ea` — compiled_low_structural (sequence, tier 1)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=4 fn=4 F1=0.000; missed: message; extra: message
- chrF++: 62.51
- Files: GT `data/puml_files/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · input `data/puml_images_1568/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 6c7324c7eaeb23cd5644654ea022ca212ecd24ea
' Original Path: /Documentação/1201384/US1005/US1005_SSD.puml
' Source: World of Code

@startuml
actor SalesClerk as adm
participant "//<<presentation>>//\nDefineNewCategoryUI" as ui

autonumber

adm-->ui: Define new category

activate ui

ui-->adm: asks user information

adm-->ui: Code, Description

ui-->adm: displayCategoryInfo

deactivate ui
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
actor SalesClerk
participant "<<presentation>>\nDefineNewCategoryUI" as UI

SalesClerk --> UI : 1 Define new category
activate UI
UI --> SalesClerk : 2 asks user information
SalesClerk --> UI : 3 Code, Description
UI --> SalesClerk : 4 displayCategoryInfo
deactivate UI
@enduml
```
```

#### `75d17323e3f57e506be51b5455aa97ae89d8c5cc` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=3 fn=3 F1=0.250; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=6 fn=6 F1=0.000; missed: message; extra: message
- chrF++: 67.64
- Files: GT `data/puml_files/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · input `data/puml_images_1568/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 75d17323e3f57e506be51b5455aa97ae89d8c5cc
' Original Path: /input/images-source/Implementing-PDQm-as-a-gateway.plantuml
' Source: World of Code

@startuml
hide footbox

Participant "Patient\nDemographics\nConsumer" as Client1
box "PDQm Implementation\ngrouped as a façade "
    Participant "Patient\n Demographics\nSupplier" as Server1
    Participant "Patient\n Demographics\nConsumer" as Client2
endbox
Participant "Patient\n Demographics\nSupplier" as Server2

Client1 -> Server1: Mobile Patient\nDemographics\nQuery [ITI-78]
activate Client1
activate Server1
Server1 --> Client2: Internal processing
activate Client2
activate Server2
Client2 -> Server2: Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]
Client2 <- Server2: [ITI-21] or [ITI-47] Response
Server1 <-- Client2: Internal processing
deactivate Client2
deactivate Server2
Client1 <- Server1: [ITI-78] Response
deactivate Client2
deactivate Server1

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
hide footbox

participant "Patient\nDemographics\nConsumer" as PDC1

box "PDQm Implementation\ngrouped as a façade" #E0E0E0
participant "Patient\nDemographics\nSupplier" as PDS1
participant "Patient\nDemographics\nConsumer" as PDC2
end box

participant "Patient\nDemographics\nSupplier" as PDS2

activate PDC1
PDC1 -> PDS1 : Mobile Patient\nDemographics\nQuery [ITI-78]
activate PDS1

PDS1 --> PDC2 : Internal processing
activate PDC2

PDC2 -> PDS2 : Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]
activate PDS2

PDS2 -> PDC2 : [ITI-21] or [ITI-47] Response
deactivate PDS2

PDC2 --> PDS1 : Internal processing
deactivate PDC2

PDS1 -> PDC1 : [ITI-78] Response
deactivate PDS1
deactivate PDC1

@enduml
```
```

#### `836fc1be71c455412e94cfec349f181ac525ab0f` — compiled_low_structural (class, tier 2)

- Element: tp=8 fp=0 fn=0 F1=1.000; type-acc matched=8 correct=8 excluded=0
- Relationship: tp=0 fp=2 fn=4 F1=0.000; missed: dependency, association; extra: inheritance
- chrF++: 70.33
- Files: GT `data/puml_files/836fc1be71c455412e94cfec349f181ac525ab0f.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/836fc1be71c455412e94cfec349f181ac525ab0f.puml` (yes) · input `data/puml_images_1568/836fc1be71c455412e94cfec349f181ac525ab0f.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/836fc1be71c455412e94cfec349f181ac525ab0f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 836fc1be71c455412e94cfec349f181ac525ab0f
' Original Path: /figure/chap1/frontend_pascal.uml
' Source: World of Code

@startuml



package "frontend" #DDDDDD {
  Parser .[hidden]r Scanner
}

class "Parser" as Parser {
+ paser ()
+ getDErrorCount () : int
}

class "Scanner" as Scanner {
# ExactToken ()
}

package "frontend.pascal" #DDDDDD {
  PascalParserTd .[hidden]r PascalScanner
}

class "PascalParserTd" as PascalParserTd {
+ paser ()
+ getDErrorCount () : int
}

class "PascalScanner" as PascalScanner {
# ExactToken ()
}

PascalParserTd -u-> Parser
PascalScanner -u-> Scanner

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
class Scanner {
  # ExactToken ()
}

class PascalScanner {
  # ExactToken ()
}

Scanner <|-- PascalScanner

class Parser {
  + paser ()
  + getDErrorCount () : int
}

class PascalParserTd {
  + paser ()
  + getDErrorCount () : int
}

Parser <|-- PascalParserTd

package frontend {
  package pascal {
    class PascalParserTd as "PascalParserTd"
    class PascalScanner as "PascalScanner"
  }
  class Parser as "Parser"
  class Scanner as "Scanner"
}
@enduml
```
```

#### `8acb8a80d5098ca1426fef7adcb6069671ba5465` — compiled_low_structural (class, tier 2)

- Element: tp=3 fp=0 fn=0 F1=1.000; type-acc matched=3 correct=3 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: association; extra: inheritance
- chrF++: 88.65
- Files: GT `data/puml_files/8acb8a80d5098ca1426fef7adcb6069671ba5465.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/8acb8a80d5098ca1426fef7adcb6069671ba5465.puml` (yes) · input `data/puml_images_1568/8acb8a80d5098ca1426fef7adcb6069671ba5465.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/8acb8a80d5098ca1426fef7adcb6069671ba5465.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 8acb8a80d5098ca1426fef7adcb6069671ba5465
' Original Path: /src/main/Diagram.puml
' Source: World of Code

@startuml
class Main{
DateTime()
getMonthOfYear()
getDayOfWeek()
int month
int day

}
class Month{
String name
+ ToText()

}
class Day{
String name
+ ToText()

}

Main <-- Month
Main <-- Day

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
class Main {
  int month
  int day
  DateTime()
  getMonthOfYear()
  getDayOfWeek()
}

class Month {
  String name
  +ToText()
}

class Day {
  String name
  +ToText()
}

Main <|-- Month
Main <|-- Day
@enduml
```
```

#### `938e9cc0e6b8dda26422f35f30282f7d202efb9d_02` — compiled_low_structural (sequence, tier 4)

- Element: tp=1 fp=4 fn=4 F1=0.200; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=20 fn=20 F1=0.000; missed: message; extra: message
- chrF++: 64.80
- Files: GT `data/puml_files/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · input `data/puml_images_1568/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes)

#### `bb081e2cfe075702e0a7c3b354ad0d566c4fee11` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=2 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=1 fn=1 F1=0.000; missed: inheritance; extra: inheritance
- chrF++: 35.57
- Files: GT `data/puml_files/bb081e2cfe075702e0a7c3b354ad0d566c4fee11.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/bb081e2cfe075702e0a7c3b354ad0d566c4fee11.puml` (yes) · input `data/puml_images_1568/bb081e2cfe075702e0a7c3b354ad0d566c4fee11.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/bb081e2cfe075702e0a7c3b354ad0d566c4fee11.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: bb081e2cfe075702e0a7c3b354ad0d566c4fee11
' Original Path: /northernwind/1.2-ALPHA-10/it-tidalwave-northernwind-modules/it-tidalwave-northernwind-frontend-media/apidocs/it/tidalwave/northernwind/frontend/media/impl/interpolator/XmpDcTitleInterpolator.puml
' Source: World of Code

@startuml
    set namespaceSeparator none
    hide empty fields
    hide empty methods

    class "<size:14>XmpDcTitleInterpolator\n<size:10>it.tidalwave.northernwind.frontend.media.impl.interpolator" as it.tidalwave.northernwind.frontend.media.impl.interpolator.XmpDcTitleInterpolator [[XmpDcTitleInterpolator.html]] {
        +interpolate(String, Context): String
    }

    abstract class "<size:14>MetadataInterpolatorSupport\n<size:10>it.tidalwave.northernwind.frontend.media.impl.interpolator" as it.tidalwave.northernwind.frontend.media.impl.interpolator.MetadataInterpolatorSupport [[MetadataInterpolatorSupport.html]]

    it.tidalwave.northernwind.frontend.media.impl.interpolator.MetadataInterpolatorSupport <|-- it.tidalwave.northernwind.frontend.media.impl.interpolator.XmpDcTitleInterpolator

    center footer UMLDoclet 2.0.12, PlantUML 1.2020.16
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
abstract class MetadataInterpolatorSupport <<it.tidalwave.northernwind.frontend.media.impl.interpolator>> {
}
class XmpDcTitleInterpolator <<it.tidalwave.northernwind.frontend.media.impl.interpolator>> {
  + interpolate(String, Context): String
}
MetadataInterpolatorSupport <|-- XmpDcTitleInterpolator
@enduml
```
```

#### `c5bb3816232672cc44f741e2b5d82d69ebdf932c` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: message; extra: message
- chrF++: 63.89
- Files: GT `data/puml_files/c5bb3816232672cc44f741e2b5d82d69ebdf932c.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/c5bb3816232672cc44f741e2b5d82d69ebdf932c.puml` (yes) · input `data/puml_images_1568/c5bb3816232672cc44f741e2b5d82d69ebdf932c.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/c5bb3816232672cc44f741e2b5d82d69ebdf932c.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: c5bb3816232672cc44f741e2b5d82d69ebdf932c
' Original Path: /doc/profiles/representation/minimal.puml
' Source: World of Code

@startuml
title Omit Representation
actor Client
participant "<&transfer> Representation" as Representation

Client -> Representation: PUT / POST / PATCH
rnote right #lightblue
  <#lightblue,lightblue>|= Header |= Value |
  | ""Prefer"" | ""return=minimal"" |
end note
Representation --> Client: 204 No Content / 201 Created
rnote left #lightgreen
  <#lightgreen,lightgreen>|= Header |= Value |
  | ""Preference-Applied"" | ""return=minimal"" |
end note
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title Omit Representation

actor Client
participant "⇄ Representation" as Representation

Client -> Representation : PUT / POST / PATCH
note right
  **Header**        **Value**
  Prefer            return=minimal
end note

Representation --> Client : 204 No Content / 201 Created
note left #LightGreen
  **Header**              **Value**
  Preference-Applied      return=minimal
end note

@enduml
```
```

#### `fd42228e66f2cdac362a90aeba71752f6729472c` — compiled_low_structural (class, tier 3)

- Element: tp=2 fp=1 fn=1 F1=0.667; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: inheritance, association; extra: inheritance, association
- chrF++: 30.61
- Files: GT `data/puml_files/fd42228e66f2cdac362a90aeba71752f6729472c.puml` (yes) · pred `data/runs/gemini-3.1-pro-preview_20260613T154356Z/fd42228e66f2cdac362a90aeba71752f6729472c.puml` (yes) · input `data/puml_images_1568/fd42228e66f2cdac362a90aeba71752f6729472c.png` (yes) · render `data/csr/gemini-3.1-pro-preview_20260613T154356Z/png/fd42228e66f2cdac362a90aeba71752f6729472c.png` (yes)

### Qwen3.5-2B

#### outcome: provider_drop

#### `09bde3e2f993e72fe98411f8d968d9e2b33b4b73` — provider_drop (sequence, tier 4)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=11 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/09bde3e2f993e72fe98411f8d968d9e2b33b4b73.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/09bde3e2f993e72fe98411f8d968d9e2b33b4b73.puml` (MISSING) · input `data/puml_images_1568/09bde3e2f993e72fe98411f8d968d9e2b33b4b73.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/09bde3e2f993e72fe98411f8d968d9e2b33b4b73.png` (MISSING)

#### `10cd98eb5787832faa18a5eb64a43b451dfda7e4` — provider_drop (sequence, tier 4)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=30 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=42 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/10cd98eb5787832faa18a5eb64a43b451dfda7e4.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/10cd98eb5787832faa18a5eb64a43b451dfda7e4.puml` (MISSING) · input `data/puml_images_1568/10cd98eb5787832faa18a5eb64a43b451dfda7e4.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/10cd98eb5787832faa18a5eb64a43b451dfda7e4.png` (MISSING)

#### `2ba4e7f17f9f45f359569c1285dafccb3b4f54ab` — provider_drop (sequence, tier 2)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml` (MISSING) · input `data/puml_images_1568/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 2ba4e7f17f9f45f359569c1285dafccb3b4f54ab
' Original Path: /docs/edgemere/sa/spm/usecases/managesecurityprofiles/MonitorSecurityProfile.puml
' Source: World of Code

@startuml

actor "SecurityEngineer"


entity EventBus

box Security Profile Manager #cc8888
    boundary spm #white
end box


box Software Defined Infrastructure #cccc88
            participant storageresource
    end box

box Security Profile Manager #cc8888
    end box


"SecurityEngineer" -> spm: Monitor Security Profile

    spm -> "storageresource": create (name: secProfileMSP,file: ./templates/secprofile.yml)

    "storageresource" --/ EventBus: securityprofile.create

    spm -> "securityprofile": status (name: secProfileMSP)

    "securityprofile" --/ EventBus: securityprofile.status



@enduml
```

_Prediction: no file on disk (provider/harness drop)._

#### `59a417a8d0d24bb5b3c5018d9d1c8bdb55cf68f9` — provider_drop (class, tier 1)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: aggregation
- chrF++: 0.00
- Files: GT `data/puml_files/59a417a8d0d24bb5b3c5018d9d1c8bdb55cf68f9.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/59a417a8d0d24bb5b3c5018d9d1c8bdb55cf68f9.puml` (MISSING) · input `data/puml_images_1568/59a417a8d0d24bb5b3c5018d9d1c8bdb55cf68f9.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/59a417a8d0d24bb5b3c5018d9d1c8bdb55cf68f9.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 59a417a8d0d24bb5b3c5018d9d1c8bdb55cf68f9
' Original Path: /diagrams/protelis-api.puml
' Source: World of Code

@startuml

skinparam dpi 250
hide empty members

ProtelisVM "1" o-- "1" ExecutionContext : uses
ProtelisVM "1" o- "1" ProtelisProgram : executes
interface ExecutionContext
interface ProtelisProgram
class ProtelisVM
@enduml
```

_Prediction: no file on disk (provider/harness drop)._

#### `69016c1560c26e4302d199133e6a4d0aba5d2465` — provider_drop (class, tier 4)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=9 F1=0.000; missed: composition, aggregation, association
- chrF++: 0.00
- Files: GT `data/puml_files/69016c1560c26e4302d199133e6a4d0aba5d2465.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/69016c1560c26e4302d199133e6a4d0aba5d2465.puml` (MISSING) · input `data/puml_images_1568/69016c1560c26e4302d199133e6a4d0aba5d2465.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/69016c1560c26e4302d199133e6a4d0aba5d2465.png` (MISSING)

#### `6defcd5ebcfd4504c58707f937babebfcde55a16` — provider_drop (class, tier 2)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=1 F1=0.000; missed: aggregation
- chrF++: 0.00
- Files: GT `data/puml_files/6defcd5ebcfd4504c58707f937babebfcde55a16.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/6defcd5ebcfd4504c58707f937babebfcde55a16.puml` (MISSING) · input `data/puml_images_1568/6defcd5ebcfd4504c58707f937babebfcde55a16.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/6defcd5ebcfd4504c58707f937babebfcde55a16.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 6defcd5ebcfd4504c58707f937babebfcde55a16
' Original Path: /exercise43/Diagram.puml
' Source: World of Code

@startuml
class Solution43{
+String name
+String author
+String CSS
+String JS
}

class SiteGenerator{
+String name
+String author
+String path
+website()
+JSFolder()
+CSSFolder()
+HTML()
}

Solution43 --o SiteGenerator
@enduml
```

_Prediction: no file on disk (provider/harness drop)._

#### `8ff76367f1b5e8f112876c5677d2babebb109437_01` — provider_drop (class, tier 3)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=7 F1=0.000; missed: inheritance, dependency, association
- chrF++: 0.00
- Files: GT `data/puml_files/8ff76367f1b5e8f112876c5677d2babebb109437_01.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/8ff76367f1b5e8f112876c5677d2babebb109437_01.puml` (MISSING) · input `data/puml_images_1568/8ff76367f1b5e8f112876c5677d2babebb109437_01.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/8ff76367f1b5e8f112876c5677d2babebb109437_01.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 8ff76367f1b5e8f112876c5677d2babebb109437
' Original Path: /doc/diagrams/drivers.puml
' Source: World of Code

@startuml

interface IMutationCommand
class StudyAdapter <<(C, HotPink) Proxy>> {
  start(command, ...args)
  getInterviewItems(pageSet)
  apply(interviewItems)
}
class PatientAdapter <<(C, HotPink) Proxy>> {
  interviews
}
class UpdateItemCommand {
  start(study, page, index)
  getInterviewItems(pageSet)
  apply(study, interviewItems)
}
class InterviewStudioDriver {
  save(study, patient, interview)
}

left to right direction
PatientStudioDriver -> PatientAdapter
StudyStudioDriver -> StudyAdapter
StudyAdapter::start ..> UpdateItemCommand::start : start(...)
StudyAdapter::apply ..> UpdateItemCommand::apply : apply(...)
PatientAdapter::interviews ..> StudyAdapter::getInterviewItems : getInterviewItems(pageSet)
InterviewStudioDriver::save ..> StudyAdapter::apply : apply(interviewItems)
UpdateItemCommand .u|> IMutationCommand

hide members
show UpdateItemCommand methods
show StudyAdapter methods
show PatientAdapter fields
show InterviewStudioDriver methods
@enduml
```

_Prediction: no file on disk (provider/harness drop)._

#### `df9a59b4a945a69a041fb2167b2fe7d7e5449b3f` — provider_drop (class, tier 4)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: dependency, association
- chrF++: 0.00
- Files: GT `data/puml_files/df9a59b4a945a69a041fb2167b2fe7d7e5449b3f.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/df9a59b4a945a69a041fb2167b2fe7d7e5449b3f.puml` (MISSING) · input `data/puml_images_1568/df9a59b4a945a69a041fb2167b2fe7d7e5449b3f.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/df9a59b4a945a69a041fb2167b2fe7d7e5449b3f.png` (MISSING)

#### `e085686b714ba51c8e8edf95c3733eb607eaf2f4` — provider_drop (class, tier 1)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 0.00
- Files: GT `data/puml_files/e085686b714ba51c8e8edf95c3733eb607eaf2f4.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/e085686b714ba51c8e8edf95c3733eb607eaf2f4.puml` (MISSING) · input `data/puml_images_1568/e085686b714ba51c8e8edf95c3733eb607eaf2f4.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/e085686b714ba51c8e8edf95c3733eb607eaf2f4.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: e085686b714ba51c8e8edf95c3733eb607eaf2f4
' Original Path: /cdm-distribution-1.1.30/cdm-distribution-1.1.30/documentation/java/org/isda/cdm/validation/choicerule/OptionSettlementChoice2ChoiceRule.puml
' Source: World of Code

@startuml

    class OptionSettlementChoice2ChoiceRule [[OptionSettlementChoice2ChoiceRule.html]] {
        +validate(OptionSettlement): ValidationResult<OptionSettlement>
    }

@enduml
```

_Prediction: no file on disk (provider/harness drop)._

#### `edbee8f129d67ba11c25b6993825553e1b4f090b` — provider_drop (sequence, tier 3)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/edbee8f129d67ba11c25b6993825553e1b4f090b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/edbee8f129d67ba11c25b6993825553e1b4f090b.puml` (MISSING) · input `data/puml_images_1568/edbee8f129d67ba11c25b6993825553e1b4f090b.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/edbee8f129d67ba11c25b6993825553e1b4f090b.png` (MISSING)

#### `f2cafbf3bb480a82f70c0d09afbfa66f58776b10` — provider_drop (class, tier 3)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=22 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=11 F1=0.000; missed: dependency
- chrF++: 0.00
- Files: GT `data/puml_files/f2cafbf3bb480a82f70c0d09afbfa66f58776b10.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/f2cafbf3bb480a82f70c0d09afbfa66f58776b10.puml` (MISSING) · input `data/puml_images_1568/f2cafbf3bb480a82f70c0d09afbfa66f58776b10.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/f2cafbf3bb480a82f70c0d09afbfa66f58776b10.png` (MISSING)

#### `f8e33eb7867f26e2b938030fd5039eb3b251e9fb` — provider_drop (sequence, tier 3)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/f8e33eb7867f26e2b938030fd5039eb3b251e9fb.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/f8e33eb7867f26e2b938030fd5039eb3b251e9fb.puml` (MISSING) · input `data/puml_images_1568/f8e33eb7867f26e2b938030fd5039eb3b251e9fb.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/f8e33eb7867f26e2b938030fd5039eb3b251e9fb.png` (MISSING)

#### outcome: compile_fail

#### `1067b9cef0f7617223a7f9ea212a6c7aa62e70cc` — compile_fail (class, tier 3)

- CSR: `Error line 3 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.puml`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 50.26
- Files: GT `data/puml_files/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.puml` (yes) · input `data/puml_images_1568/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/1067b9cef0f7617223a7f9ea212a6c7aa62e70cc.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 1067b9cef0f7617223a7f9ea212a6c7aa62e70cc
' Original Path: /UML/Character.puml
' Source: World of Code

@startuml
skinparam class{
    BorderColor black
    BackgroundColor #a3a3a3
}

class Character{
-GameDataRef _data;
-sf::Sprite sprite;
-sf::Vector2f position;
-sf::Texture texture;
-sf::Texture texture_flip;
-sf::Texture run_right1;
-sf::Texture run_right2;
-sf::Texture run_left1;
-sf::Texture run_left2;
-bool flip = false;
-sf::Clock animationClock;
-int animationRun = 0;
-bool air_texture = false;

+sf::Vector2f velocity = {0,0};
+float speed = 400.0f;
+float jump_speed = 600.0f;
+float slow_down = 0.0f, slow_down_ground = 40.0f, slow_down_air = 5.0f;
+float speed_up = 0.0f, speed_up_ground = 40.0f, speed_up_air = 30.0f;
+int max_jump =1, jump = 0;
+bool jump_done = false, on_ground = false;


-void flipTexture();

+Character(GameDataRef data);
+void update();
+void setTexture(6 Textures);
+void setPosition(const sf::Vector2f& position_);
+void setPosition(const float& x, const float& y);
+sf::Vector2f getPosition();
+void draw(sf::RenderWindow& renderWindow);
+void move(sf::Vector2f movement);
+void move(const float& x, const float& y);
+sf::Vector2f nextPosition(sf::Vector2f movement);
+sf::Sprite nextSprite(sf::Vector2f movement);
+sf::Sprite& getSprite();
+bool objectCollisionAndFalling(const sf::Sprite &object, const float& dt);
+void updateVelocity(const float& dt);
+void respawn(sf::Vector2f spawn);
+void characterKeyboardInput();
}

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
class Character
as Character

participant "Character" as C

C <<interface>>
    include "Character.h"

    C -- "GameDataRef" : _data
    C -- "Sprite" : sprite
    C -- "Vector2f" : position
    C -- "Texture" : texture
    C -- "Texture" : texture_flip
    C -- "Texture" : run_right1
    C -- "Texture" : run_right2
    C -- "Texture" : run_left1
    C -- "Texture" : run_left2
    C -- "bool" : flip
    C -- "Clock" : animationClock
    C -- "int" : animationRun
    C -- "bool" : air_texture

    C -- "Vector2f" : velocity
    C -- "float" : speed
    C -- "float" : jump_speed
    C -- "float" : slow_down
    C -- "float" : slow_down_ground
    C -- "float" : slow_down_air
    C -- "float" : speed_up
    C -- "float" : speed_up_ground
    C -- "float" : speed_up_air
    C -- "int" : max_jump
    C -- "int" : jump
    C -- "bool" : jump_done
    C -- "bool" : on_ground

    C -- "void" : flipTexture()

    C -- "Character" : (GameDataRef data)
    C -- "void" : update()
    C -- "void" : setTexture(6 Textures)
    C -- "void" : setPosition(const Vector2f& position_)
    C -- "void" : setPosition(const float& x, const float& y)
    C -- "Vector2f" : getPosition()
    C -- "void" : draw(sf::RenderWindow& renderWindow)
    C -- "void" : move(sf::Vector2f movement)
    C -- "void" : move(const float& x, const float& y)
    C -- "Vector2f" : nextPosition(sf::Vector2f movement)
    C -- "Sprite" : nextSprite(sf::Vector2f movement)
    C -- "Sprite" : getSprite()
    C -- "bool" : objectCollisionAndFalling(const Sprite& object, const float& dt)
    C -- "void" : updateVelocity(const float& dt)
    C -- "void" : respawn(sf::Vector2f spawn)
    C -- "void" : characterKeyboardInput()

@enduml
```

#### `187969222acbadebd6c579b9d33481b9440c76dc` — compile_fail (class, tier 4)

- CSR: `Error line 82 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/187969222acbadebd6c579b9d33481b9440c76dc.puml`
- Element: tp=0 fp=0 fn=14 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=13 F1=0.000; missed: inheritance, dependency, association
- chrF++: 65.27
- Files: GT `data/puml_files/187969222acbadebd6c579b9d33481b9440c76dc.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/187969222acbadebd6c579b9d33481b9440c76dc.puml` (yes) · input `data/puml_images_1568/187969222acbadebd6c579b9d33481b9440c76dc.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/187969222acbadebd6c579b9d33481b9440c76dc.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 187969222acbadebd6c579b9d33481b9440c76dc
' Original Path: /test6/src/类图.puml
' Source: World of Code

@startuml
top to bottom direction
title 类图
abstract class User{
    int id
    string name
    string github（github地址）
    string sex
    string picture
}
User<|--Student
class Student{
    int studentNumber（学号）
    string class（班级）
}
User<|--Teacher
class Teacher{
    int teacherNumber（工号）
    string office（办公室）
    string phone
}
class Login{
    int id
    int username（学生账号就是学号，老师账号是工号）
    string password
    int role（角色）
}
class Scoreitem{
    int id
    int completeScore (完成度得分）
    int complexScore（复杂度得分）
    int answerScore (答辩得分)
}
note right:一个scoreitem实例就表示了一个\n学生的一个实验成绩
class Course{
    int id
    int courseNum
    string name
    string term
    float credit（学分）
}
class Experiment{
    int id
    string name（实验名）
    Date date（实验发布时间）
    string github（实验的github地址）
    int courseId（与Course类的id关联）
}
class Experimentcore{
    int id
    int studentId (与学生关联)
    int scoreitemId (与scoreitem关联)
}
class StudentCourse{
    int id
    int studentId
    int courseId
}
note right:“学生选课”类
class TeacherCourse{
    int id
    int teacherId
    int courseId
}
note right:“老师选课”类
Student "1" -- "n" StudentCourse
StudentCourse "n" -- "1" Course
Teacher "1" -- "n" TeacherCourse
TeacherCourse "n" -- "1" Course
Experiment  "n" -- "1" Course
Scoreitem "n" -- "1" Experiment
Experimentscore "n" -- "1" Scoreitem
Experimentscore "n" -- "1" Student
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
class User {
    int id
    string name
    string github (github地址)
    string sex
    string picture
}

class Login {
    int id
    int username (学生账号就是学号，老师账号是工号)
    string password
    int role (角色)
}

class Experimentcore {
    int id
    int studentId (与学生关联)
    int scoreitemId (与scoreitem关联)
}

class Scoreitem {
    int id
    int complexScore (复杂度得分)
    int completeScore (完成度得分)
    int answerScore (答辩得分)
}

class Experiment {
    int id
    string name (实验名)
    Date date (实验发布时间)
    string github (实验的github地址)
    int courseld (与Course类的id关联)
}

class Course {
    int id
    int courseNum
    string name
    string term
    float credit (学分)
}

class Teacher {
    int teacherNumber (工号)
    string office (办公室)
    string phone
}

class Student {
    int studentNumber (学号)
    string class (班级)
}

class TeacherCourse {
    int id
    int teacherId
    int courseld
}

class StudentCourse {
    int id
    int studentId
    int courseld
}

class Experimentscore {
    int id
    int username (学生账号就是学号，老师账号是工号)
    string password
    int role (角色)
}

class Experimentscore {
    int id
    int studentId (与学生关联)
    int scoreitemId (与scoreitem关联)
}
```

#### `308a1f6f92b3b9683bfddf272a2ae3210d8c8635` — compile_fail (sequence, tier 3)

- CSR: `Error line 7 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/308a1f6f92b3b9683bfddf272a2ae3210d8c8635.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=9 F1=0.000; missed: message
- chrF++: 40.52
- Files: GT `data/puml_files/308a1f6f92b3b9683bfddf272a2ae3210d8c8635.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/308a1f6f92b3b9683bfddf272a2ae3210d8c8635.puml` (yes) · input `data/puml_images_1568/308a1f6f92b3b9683bfddf272a2ae3210d8c8635.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/308a1f6f92b3b9683bfddf272a2ae3210d8c8635.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 308a1f6f92b3b9683bfddf272a2ae3210d8c8635
' Original Path: /sequence_code/professor/professor.pontuation.wsd
' Source: World of Code

@startuml
actor Professor
boundary "tela principal" as home <<client page>>
control DocumentController as documents <<server page>>
entity DocumenteEntity as model <<server page>>

activate Professor
Professor ->> home: visualizar lista de alunos
deactivate Professor
activate home
home ->> documents: requisitar lista de alunos
activate documents
documents -> model: buscar por lista de alunos
activate model
model --> documents: retorna lista de alunos
deactivate model
documents -->> home: responder com lista de alunos
deactivate documents
deactivate home
home --> Professor: exibir lista de alunos
activate home
activate Professor
Professor ->> home: selecionar aluno da lista
deactivate home 
deactivate Professor
home -> home: calcular pontuação do aluno
activate home
home -->> Professor: exibir pontuação do aluno
deactivate home
activate Professor
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
participant "Professor" as P
participant "«client page» tela principal" as C
participant "«server page» DocumentController" as D
participant "«server page» DocumentoEntity" as E

P ..> C : visualizar lista de alunos
C ..> D : requisitar lista de alunos
D ..> E : buscar por lista de alunos
E ..> D : retorna lista de alunos
D ..> C : responder com lista de alunos
C ..> P : exibir lista de alunos
P ..> C : selecionar aluno da lista
C ..> D : calcular pontuação do aluno
D ..> C : exibir pontuação do aluno

@enduml
```

#### `37a255909b1aeb49264ef0593b9a9e1f5773ee23` — compile_fail (class, tier 1)

- CSR: `Error line 3 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/37a255909b1aeb49264ef0593b9a9e1f5773ee23.puml`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 24.36
- Files: GT `data/puml_files/37a255909b1aeb49264ef0593b9a9e1f5773ee23.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/37a255909b1aeb49264ef0593b9a9e1f5773ee23.puml` (yes) · input `data/puml_images_1568/37a255909b1aeb49264ef0593b9a9e1f5773ee23.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/37a255909b1aeb49264ef0593b9a9e1f5773ee23.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 37a255909b1aeb49264ef0593b9a9e1f5773ee23
' Original Path: /app/src/androidTest/java/com/example/justy/DataFromSensors/DataFromSensors.plantuml
' Source: World of Code

@startuml

title __DATAFROMSENSORS's Class Diagram__\n

  package com.example.justy.DataFromSensors {
    class ExampleInstrumentedTest {
        + useAppContext()
    }
  }
  



right footer


PlantUML diagram generated by SketchIt! (https://bitbucket.org/pmesmeur/sketch.it)
For more information about this tool, please contact philippe.mesmeur@gmail.com
endfooter

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
package com
    example
        justy
            DataFromSensors
                ExampleInstrumentedTest
                    useAppContext()
@enduml
```

#### `4dc97fd76002a99da5ddf57b1d44a80dcba69757` — compile_fail (sequence, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: message
- chrF++: 1.36
- Files: GT `data/puml_files/4dc97fd76002a99da5ddf57b1d44a80dcba69757.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/4dc97fd76002a99da5ddf57b1d44a80dcba69757.puml` (yes) · input `data/puml_images_1568/4dc97fd76002a99da5ddf57b1d44a80dcba69757.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/4dc97fd76002a99da5ddf57b1d44a80dcba69757.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 4dc97fd76002a99da5ddf57b1d44a80dcba69757
' Original Path: /doc/profiles/alias/discovery.puml
' Source: World of Code

@startuml
title Discovery
actor Client
participant "<&share> Alias" as Alias

Client -> Alias: HEAD
Alias --> Client: 307 Temporary Redirect / 308 Permanent Redirect
rnote left #lightgreen
  <#lightgreen,lightgreen>|= Header |= Value |
  | ""Profile"" | ""<http://level3.rest/profiles/alias>"", |
  | | ""<target-profile>"" |
  | ""Allow"" | //target's ""Allow"" values// |
  | ""Location"" | //target URL// |
end note
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam UMLClassDiagram labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
skinparam UMLActor labelStyle "bold"
```

#### `5062b6c354eb5e7d4350b93465d61c1c2b628ec7` — compile_fail (class, tier 3)

- CSR: `Error line 17 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: inheritance, association
- chrF++: 34.64
- Files: GT `data/puml_files/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.puml` (yes) · input `data/puml_images_1568/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 5062b6c354eb5e7d4350b93465d61c1c2b628ec7
' Original Path: /E-R/_diagrams/reference-data/PressureMeasurementType.1.0.0.ref.puml
' Source: World of Code

@startuml
hide methods
skinparam groupInheritance 2
skinparam class {
    ArrowColor Black
    BorderColor Black
    BackgroundColor<<master-data>> LightSalmon
    BackgroundColor<<work-product-component>> Gold
    BackgroundColor<<abstract>> LightSteelBlue
    BackgroundColor<<dataset>> Ivory
    BackgroundColor<<reference-data>> Turquoise
    BackgroundColor<<Abstraction>> LightSkyBlue
    BackgroundColor<<error>> Red
    BackgroundColor<<Activity>> LightSkyBlue
    BackgroundColor<<ReferenceType>> LightSkyBlue
    BackgroundColor<<WorkProductComponent>> LightSkyBlue
    BackgroundColor<<Project>> LightSkyBlue
    BackgroundColor<<File>> LightSkyBlue
    BackgroundColor<<FileCollection>> LightSkyBlue
    BackgroundColor<<MasterData>> LightSkyBlue
    BackgroundColor<<nested array>> WhiteSmoke
    BackgroundColor<<nested>> WhiteSmoke
    packageStyle rectangle
}
package "PressureMeasurementType Referenced-by View" <<rectangle>>
{
class "<size:16>PressureMeasurementType</size>" as PressureMeasurementType <<reference-data>>
left to right direction
class "PressureMeasurementType" <<reference-data>>
package "work-product-component Entities" as WorkProductComponent <<frame>>
{
class "RockSampleAnalysis" <<work-product-component>> {
RCAMeasurements[].Conditions.PressureMeasurementTypeID
}
}
"WorkProductComponent" -->  "PressureMeasurementType" 
abstract "AbstractReferenceType" <<Abstraction>>
"PressureMeasurementType" -right-|>  "AbstractReferenceType"
}
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
package "work-product-component Entities" as WorkProductComponent {
    class RockSampleAnalysis {
        <<work-product-component>>
        RCAMeasurements[].Conditions.PressureMeasurementTypeID
    }
}

class AbstractReferenceType {
    <<Abstraction>>
}

class PressureMeasurementType {
    <<reference-data>>
}

class PressureMeasurementTypeReferenced-by View {
    title "PressureMeasurementType Referenced-by View"
}

WorkProductComponent.RockSampleAnalysis --> AbstractReferenceType
WorkProductComponent.RockSampleAnalysis --> PressureMeasurementType

AbstractReferenceType --> PressureMeasurementType
@enduml
```

#### `7409cf40c00dfe3b5efd16bff9b188b1f767574b` — compile_fail (sequence, tier 1)

- CSR: `Error line 5 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/7409cf40c00dfe3b5efd16bff9b188b1f767574b.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: message
- chrF++: 44.96
- Files: GT `data/puml_files/7409cf40c00dfe3b5efd16bff9b188b1f767574b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/7409cf40c00dfe3b5efd16bff9b188b1f767574b.puml` (yes) · input `data/puml_images_1568/7409cf40c00dfe3b5efd16bff9b188b1f767574b.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/7409cf40c00dfe3b5efd16bff9b188b1f767574b.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 7409cf40c00dfe3b5efd16bff9b188b1f767574b
' Original Path: /wxh-note/src/main/uml/record/员工画像维护.puml
' Source: World of Code

@startuml

group 按门店维度批量执行
ehr -> attendance: 查询员工累计考勤工时
attendance --> ehr: 返回员工累计考勤工时
end

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
participant "ehr" as EHR
participant "attendance" as ATTENDANCE

rectangle "按门店维度批量执行" {
    EHR -> ATTENDANCE: 查询员工累计考勤工时
    ATTENDANCE <- EHR: 返回员工累计考勤工时
}

@enduml
```

#### `836fc1be71c455412e94cfec349f181ac525ab0f` — compile_fail (class, tier 2)

- CSR: `Error line 42 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/836fc1be71c455412e94cfec349f181ac525ab0f.puml`
- Element: tp=0 fp=0 fn=8 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: dependency, association
- chrF++: 53.71
- Files: GT `data/puml_files/836fc1be71c455412e94cfec349f181ac525ab0f.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/836fc1be71c455412e94cfec349f181ac525ab0f.puml` (yes) · input `data/puml_images_1568/836fc1be71c455412e94cfec349f181ac525ab0f.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/836fc1be71c455412e94cfec349f181ac525ab0f.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 836fc1be71c455412e94cfec349f181ac525ab0f
' Original Path: /figure/chap1/frontend_pascal.uml
' Source: World of Code

@startuml



package "frontend" #DDDDDD {
  Parser .[hidden]r Scanner
}

class "Parser" as Parser {
+ paser ()
+ getDErrorCount () : int
}

class "Scanner" as Scanner {
# ExactToken ()
}

package "frontend.pascal" #DDDDDD {
  PascalParserTd .[hidden]r PascalScanner
}

class "PascalParserTd" as PascalParserTd {
+ paser ()
+ getDErrorCount () : int
}

class "PascalScanner" as PascalScanner {
# ExactToken ()
}

PascalParserTd -u-> Parser
PascalScanner -u-> Scanner

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
package frontend {
    class Scanner {
        attribute ExactToken exactToken
    }

    class Parser {
        method paser()
        method getDErrorCount() : int
    }

    class PascalScanner {
        attribute ExactToken exactToken
    }

    class PascalParserTd {
        method paser()
        method getDErrorCount() : int
    }
}

package pascal {
    class PascalParserTd {
        method paser()
        method getDErrorCount() : int
    }

    class PascalScanner {
        attribute ExactToken exactToken
    }

    class Parser {
        method paser()
        method getDErrorCount() : int
    }

    class Scanner {
        attribute ExactToken exactToken
    }
}

class Scanner <-..> PascalScanner
class PascalScanner <-..> PascalParserTd
class PascalParserTd <-..> Parser
class Parser <-..> Scanner
@enduml
```

#### `89def1e0af84fe4771e9c3c068197ee8be3d1b32_02` — compile_fail (sequence, tier 3)

- CSR: `Error line 29 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/89def1e0af84fe4771e9c3c068197ee8be3d1b32_02.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=20 F1=0.000; missed: message
- chrF++: 54.51
- Files: GT `data/puml_files/89def1e0af84fe4771e9c3c068197ee8be3d1b32_02.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/89def1e0af84fe4771e9c3c068197ee8be3d1b32_02.puml` (yes) · input `data/puml_images_1568/89def1e0af84fe4771e9c3c068197ee8be3d1b32_02.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/89def1e0af84fe4771e9c3c068197ee8be3d1b32_02.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 89def1e0af84fe4771e9c3c068197ee8be3d1b32
' Original Path: /Capture/3_1_GroupVsSingleUserEvent.puml
' Source: World of Code

@startuml
title Scheduled Events
actor "Recording Staff" as user
actor "Coach" as coach
collections "IP/Mobile Cams" as cam
collections "Consumer Apps" as ch
ch -> "Security Gateway" as security: authenticate(ID)
security --> ch: return(token)
control "Control Domain\n(win10/linux)" as ctrl
create "Streaming Service\n(encoder)" as strm
ctrl -> strm: host(sources{endpoints})
cam -> ctrl: register(endpoint)
ch -> ctrl: register(token, priority)
user -> ctrl: createEvent(configuration{description, sources, consumers{priorities}})
ctrl --> ctrl: create(newEvent)
activate ctrl
user -> ctrl: start(newEvent)
ctrl -> strm: encode()
ctrl --> ch: notify(recording)
user -> ctrl: stop(newEvent)
deactivate ctrl
ctrl -> strm: saveAs(mediaID)
create entity "Media\n(mediaID)" as media
strm -> media: save(mediaID)
create "Transfer Service" as transfer
ctrl -> transfer: host(mediaID, consumers{token, priority})
ctrl --> ch: notify(newMediaAvailable, mediaID, transferServiceEndpoint)
alt auto-download enabled
    ch -> transfer: fetchMedia(token, mediaID)
    transfer --> ch: returnByPriority(mediaStream)
else manual-download enabled 
    coach -> ch: showMedia(token)
    ch -> transfer: fetchMedia(token, mediaID)
    transfer --> ch: returnByPriority(mediaStream)
end




@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam UMLSequenceDiagram arrowStyle solid
skinparam ActorActorStyle circle

title "Scheduled Events"

participant "Recording Staff" as RecordingStaff
participant "Coach" as Coach
participant "IP/Mobile Cams" as IPMobileCams
participant "Consumer Apps" as ConsumerApps
participant "Security Gateway" as SecurityGateway
participant "Control Domain (win10/linux)" as ControlDomain
participant "Streaming Service (encoder)" as StreamingService
participant "Media (medialID)" as Media
participant "Transfer Service" as TransferService

actor RecordingStaff
actor Coach

participant IPMobileCams
participant ConsumerApps
participant SecurityGateway
participant ControlDomain
participant StreamingService
participant Media
participant TransferService

RecordingStaff ->> ControlDomain : authenticate(ID)
ControlDomain -- ConsumerApps : return(token)

ConsumerApps ->> SecurityGateway : register(endpoint)
SecurityGateway ->> ControlDomain : register(token, priority)
ControlDomain ->> StreamingService : host(sources{endpoints})
StreamingService ->> ControlDomain : create(newEvent)

ControlDomain ->> RecordingStaff : start(newEvent)
RecordingStaff ->> ControlDomain : stop(newEvent)

ControlDomain ->> StreamingService : encode()
StreamingService ->> ControlDomain : notify(recording)

ControlDomain ->> StreamingService : saveAs(medialID)
StreamingService ->> Media : save(medialID)
Media -- ControlDomain : host(medialID, consumers{token, priority})
ControlDomain ->> TransferService : host(medialID, consumers{token, priority})
TransferService ->> ControlDomain : notify(newMediaAvailable, medialID, transferServiceEndpoint)

ControlDomain alt [auto-download enabled]
ControlDomain ->> TransferService : fetchMedia(token, medialID)
TransferService ->> ControlDomain : returnByPriority(mediaStream)
ControlDomain else [manual-download enabled]
ControlDomain ->> ConsumerApps : showMedia(token)
ConsumerApps ->> ControlDomain : fetchMedia(token, medialID)
ControlDomain ->> StreamingService : returnByPriority(mediaStream)
@endalt

@enduml
```

#### `a05ace8d6d55270205796fa7011e2f5e552ba0da` — compile_fail (class, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: aggregation, association
- chrF++: 1.52
- Files: GT `data/puml_files/a05ace8d6d55270205796fa7011e2f5e552ba0da.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/a05ace8d6d55270205796fa7011e2f5e552ba0da.puml` (yes) · input `data/puml_images_1568/a05ace8d6d55270205796fa7011e2f5e552ba0da.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/a05ace8d6d55270205796fa7011e2f5e552ba0da.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a05ace8d6d55270205796fa7011e2f5e552ba0da
' Original Path: /2-SoftwareDesign/2.7-PlantUML/UML-ConceptClasses.puml
' Source: World of Code

@startuml
title Concept Classes Diagram

Class User
Class Music
Class Music_Recomendation
Class API_Music_Recomendation

User"1" -up-> "+"Music : review
Music_Recomendation"+" o-- "1"Music
User"1" -up-> "+"Music_Recomendation: review
API_Music_Recomendation"1" -up-> "+"Music_Recomendation: provide
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam UMLClassBoxStyle fillcolor: #f5f5f5
skinparam UMLClassBoxStyleBorderStyle solid
skinparam UMLClassBoxStyleBorderWidth 1
skinparam UMLClassBoxStyleBorderDash 0 2
skinparam UMLClassBoxStyleBorderDashColor #000000
skinparam UMLClassBoxStyleFillColor #f5f5f5
skinparam UMLClassBoxStyleFillColor2 #f5f5f5
skinparam UMLClassBoxStyleFillColor3 #f5f5f5
skinparam UMLClassBoxStyleFillColor4 #f5f5f5
skinparam UMLClassBoxStyleFillColor5 #f5f5f5
skinparam UMLClassBoxStyleFillColor6 #f5f5f5
skinparam UMLClassBoxStyleFillColor7 #f5f5f5
skinparam UMLClassBoxStyleFillColor8 #f5f5f5
skinparam UMLClassBoxStyleFillColor9 #f5f5f5
skinparam UMLClassBoxStyleFillColor10 #f5f5f5
skinparam UMLClassBoxStyleFillColor11 #f5f5f5
skinparam UMLClassBoxStyleFillColor12 #f5f5f5
skinparam UMLClassBoxStyleFillColor13 #f5f5f5
skinparam UMLClassBoxStyleFillColor14 #f5f5f5
skinparam UMLClassBoxStyleFillColor15 #f5f5f5
skinparam UMLClassBoxStyleFillColor16 #f5f5f5
skinparam UMLClassBoxStyleFillColor17 #f5f5f5
skinparam UMLClassBoxStyleFillColor18 #f5f5f5
skinparam UMLClassBoxStyleFillColor19 #f5f5f5
skinparam UMLClassBoxStyleFillColor20 #f5f5f5
skinparam UMLClassBoxStyleFillColor21 #f5f5f5
skinparam UMLClassBoxStyleFillColor22 #f5f5f5
skinparam UMLClassBoxStyleFillColor23 #f5f5f5
skinparam UMLClassBoxStyleFillColor24 #f5f5f5
skinparam UMLClassBoxStyleFillColor25 #f5f5f5
skinparam UMLClassBoxStyleFillColor26 #f5f5f5
skinparam UMLClassBoxStyleFillColor27 #f5f5f5
skinparam UMLClassBoxStyleFillColor28 #f5f5f5
skinparam UMLClassBoxStyleFillColor29 #f5f5f5
skinparam UMLClassBoxStyleFillColor30 #f5f5f5
skinparam UMLClassBoxStyleFillColor31 #f5f5f5
skinparam UMLClassBoxStyleFillColor32 #f5f5f5
skinparam UMLClassBoxStyleFillColor33 #f5f5f5
skinparam UMLClassBoxStyleFillColor34 #f5f5f5
skinparam UMLClassBoxStyleFillColor35 #f5f5f5
skinparam UMLClassBoxStyleFillColor36 #f5f5f5
skinparam UMLClassBoxStyleFillColor37 #f5f5f5
skinparam UMLClassBoxStyleFillColor38 #f5f5f5
skinparam UMLClassBoxStyleFillColor39 #f5f5f5
skinparam UMLClassBoxStyleFillColor40 #f5f5f5
skinparam UMLClassBoxStyleFillColor41 #f5f5f5
skinparam UMLClassBoxStyleFillColor42 #f5f5f5
skinparam UMLClassBoxStyleFillColor43 #f5f5f5
skinparam UMLClassBoxStyleFillColor44 #f5f5f5
skinparam UMLClassBoxStyleFillColor45 #f5f5f5
skinparam UMLClassBoxStyleFillColor46 #f5f5f5
skinparam UMLClassBoxStyleFillColor47 #f5f5f5
skinparam UMLClassBoxStyleFillColor48 #f5f5f5
skinparam UMLClassBoxStyleFillColor49 #f5f5f5
skinparam UMLClassBoxStyleFillColor50 #f5f5f5
skinparam UMLClassBoxStyleFillColor51 #f5f5f5
skinparam UMLClassBoxStyleFillColor52 #f5f5f5
skinparam UMLClassBoxStyleFillColor53 #f5f5f5
skinparam UMLClassBoxStyleFillColor54 #f5f5f5
skinparam UMLClassBoxStyleFillColor55 #f5f5f5
skinparam UMLClassBoxStyleFillColor56 #f5f5f5
skinparam UMLClassBoxStyleFillColor57 #f5f5f5
skinparam UMLClassBoxStyleFillColor58 #f5f5f5
skinparam UMLClassBoxStyleFillColor59 #f5f5f5
skinparam UMLClassBoxStyleFillColor60 #f5f5f5
skinparam UMLClassBoxStyleFillColor61 #f5f5f5
skinparam UMLClassBoxStyleFillColor62 #f5f5f5
skinparam UMLClassBoxStyleFillColor63 #f5f5f5
skinparam UMLClassBoxStyleFillColor64 #f5f5f5
skinparam UMLClassBoxStyleFillColor65 #f5f5f5
skinparam UMLClassBoxStyleFillColor66 #f5f5f5
skinparam UMLClassBoxStyleFillColor67 #f5f5f5
skinparam UMLClassBoxStyleFillColor68 #f5f5f5
skinparam UMLClassBoxStyleFillColor69 #f5f5f5
skinparam UMLClassBoxStyleFillColor70 #f5f5f5
skinparam UMLClassBoxStyleFillColor71 #f5f5f5
skinparam UMLClassBoxStyleFillColor72 #f5f5f5
skinparam UMLClassBoxStyleFillColor73 #f5f5f5
skinparam UMLClassBoxStyleFillColor74 #f5f5f5
```

#### `a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43` — compile_fail (sequence, tier 2)

- CSR: `Error line 6 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: message
- chrF++: 49.97
- Files: GT `data/puml_files/a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43.puml` (yes) · input `data/puml_images_1568/a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a8a9d9ecd9fc8e805f9867c12316cfd53ae83c43
' Original Path: /TrainSystem/UML/Sequence Diagrams/MBO/GetAuthority.pu
' Source: World of Code

@startuml

title Get Authority

skinparam sequence {
  BackgroundColor transparent
  ParticipantBackgroundColor #e6ffcc
  ParticipantBorderColor 	#049595
  PackageBorderCOlor  #049595
  ArrowColor #006666
  LifeLineBorderColor #c09cd9
}

participant MBO

== MBO Receives Position and Transmits Authority ==
activate TrainController
activate MBO
MBO -> MBO : receiveTrainPosition(String)
MBO -> TrainController : getPosition(String)
TrainController -> MBO : trainPosition[2]
MBO -> MBO : calculateAuthority(String)
MBO -> MBO : transmitMboAuthority(String, double[2])
MBO -> TrainController : setMboAuthority(String, double)

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Get Authority
participant MBO as MBO
participant TrainController as TrainController

rectangle MBO Receives Position and Transmits Authority {
    receiveTrainPosition(String)
    getPosition(String)
    trainPosition[2]
    calculateAuthority(String)
    transmitMboAuthority(String, double[2])
    setMboAuthority(String, double)
}

MBO
TrainController

@enduml
```

#### `c2156696b5385583de2e134297e95e6dfc4465e3` — compile_fail (sequence, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=35 F1=0.000; missed: message
- chrF++: 19.34
- Files: GT `data/puml_files/c2156696b5385583de2e134297e95e6dfc4465e3.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/c2156696b5385583de2e134297e95e6dfc4465e3.puml` (yes) · input `data/puml_images_1568/c2156696b5385583de2e134297e95e6dfc4465e3.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/c2156696b5385583de2e134297e95e6dfc4465e3.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: c2156696b5385583de2e134297e95e6dfc4465e3
' Original Path: /docs/sequence.uml
' Source: World of Code

@startuml
participant Client
box "Master"
  participant Dispatcher
  database Database
  participant RSyncServer
  participant Arbiter
end box
box "Worker"
  participant Slave
  participant Worker
end box
activate Worker

Client->Database : Create a taskset
Client->Database : Enqueue tasks
Client->Dispatcher : Taskset request
Dispatcher->Worker : Taskset dispatch
Worker->Database : Log the worker participation

== RSync ==

Worker<->RSyncServer : RSync

== Setup ==

Worker->Worker : Worker setup
Worker->Database : Add a worker setup log

alt setup failed
  Worker->Arbiter : Fail request
  Arbiter->Database : Mark the taskset as failed
  Database->Worker : Notify the taskset is marked as failed
end alt

== Testing ==

create Slave
Worker->Slave : Spawn slaves
activate Slave
Slave->Slave : Slave setup

...

Slave->Database : Dequeue a task
Database-->Slave : Return a task

Slave->Database : Add a trial
Slave->Slave : Execute a task
Slave->Database : Add a trial result
Slave->Arbiter : Notify the trial result

Arbiter->Database : Query the trial result
Database-->Arbiter : Respond to the query

alt passed or pending
  Arbiter->Database : Mark the task as finished
else retry needed
  Arbiter->Database : Enqueue the task
else no more retries
  Arbiter->Database : Mark the task as failed
end alt

...

Slave->Database : Dequeue a task
Database-->Slave : No tasks left
Slave->Arbiter : Check request

Arbiter->Arbiter : Check whether all tasks are finished
alt some tasks are left
  Arbiter->Database : Enqueue the tasks
end alt
Arbiter->Database : Mark the taskset as finished
Database->Worker : Notify the taskset is marked as finished
Worker->Slave : Kill slaves
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam sequenceDiagram

participant Client
participant Dispatcher
participant Database
participant RSyncServer
participant Arbiter
participant Worker

actor Client
participant Dispatcher
participant Database
participant RSyncServer
participant Arbiter
participant Worker

Client->>Dispatcher: Create a taskset
Client->>Dispatcher: Enqueue tasks
Client->>Dispatcher: Taskset request

Dispatcher->>Database: Taskset dispatch
Dispatcher->>Worker: Log the worker participation

Worker->>RSyncServer: RSync
RSyncServer->>Worker: RSync

Worker->>Dispatcher: Setup
Dispatcher->>Worker: Add a worker setup log

alt [setup failed]
    Worker->>Arbiter: Fail request
    Arbiter->>Dispatcher: Mark the taskset as failed
    Arbiter->>Worker: Notify the taskset is marked as failed
end

alt [some tasks are left]
    Worker->>Arbiter: Enqueue the tasks
    Arbiter->>Dispatcher: Mark the taskset as finished
    Arbiter->>Worker: Notify the taskset is marked as finished
end

alt [passed or pending]
    Worker->>Arbiter: Mark the task as finished
    alt [retry needed]
        Worker->>Arbiter: Enqueue the task
    else [no more retries]
        Worker->>Arbiter: Mark the task as failed
    end
end

alt [passed or pending]
    Worker->>Arbiter: Mark the task as finished
    alt [retry needed]
        Worker->>Arbiter: Enqueue the task
    else [no more retries]
        Worker->>Arbiter: Mark the task as failed
    end
end

alt [some tasks are left]
    Worker->>Arbiter: Enqueue the tasks
    Arbiter->>Dispatcher: Mark the taskset as finished
    Arbiter->>Worker: Notify the taskset is marked as finished
end

alt [some tasks are left]
    Worker->>Arbiter: Enqueue the tasks
    Arbiter->>Dispatcher: Mark the taskset as finished
    Arbiter->>Worker: Notify the taskset is marked as finished
end

alt [some tasks are left]
    Worker->>Arbiter: Enqueue the tasks
    Arbiter->>Dispatcher: Mark the taskset as finished
    Arbiter->>Worker: Notify the taskset is marked as finished
end

alt [some tasks are left]
    Worker->>Arbiter: Enqueue the tasks
```

#### `ccc5b290f6b06a02cfab19d91dd6c611a1e6cb10` — compile_fail (sequence, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=11 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=61 F1=0.000; missed: message
- chrF++: 33.31
- Files: GT `data/puml_files/ccc5b290f6b06a02cfab19d91dd6c611a1e6cb10.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/ccc5b290f6b06a02cfab19d91dd6c611a1e6cb10.puml` (yes) · input `data/puml_images_1568/ccc5b290f6b06a02cfab19d91dd6c611a1e6cb10.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/ccc5b290f6b06a02cfab19d91dd6c611a1e6cb10.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: ccc5b290f6b06a02cfab19d91dd6c611a1e6cb10
' Original Path: /SprintD/US017/US017_SD.puml
' Source: World of Code



@startuml

autonumber
actor "CenterCoordinator" as CC
participant ":DataFromLegacySystemUI" as UI
participant ":DataFromLegacySystemController" as CTRL
participant ":ReadLegacyDataFile" as RDLF
participant ":Company" as Comp
participant ":SNSUserStore" as SNSStore
participant ":App" as App
participant ":VaccinationCenter" as VC
participant ":Arrival" as AR
participant ":Departure" as DR
participant ":vaccinationCentersStore" as VCS

activate CC
CC -> UI : Asks to load a CSV file with legacy data
activate UI
UI -> CTRL** : DataFromLegacySystemController()
activate CTRL
CTRL -> Comp : getVaccinationCentersStore()
activate Comp
Comp --> CTRL : returns the store
deactivate Comp
CTRL -> VCS : getVaccinationCenterAssociatedToCoordinator(id)
activate VCS
VCS --> CTRL : returns the vaccination center
deactivate VCS
CTRL --> RDLF **: ReadLegacyDataFile(center)
deactivate CTRL



UI --> CC : request path of the CSV file
deactivate UI

CC -> UI : types path
activate UI


UI -> CTRL: readFile(path)

activate CTRL
CTRL -> RDLF : readFile(Sring path)


activate RDLF


loop#Red while csv has new lines
RDLF -> RDLF : validateFileLegacy(SNSUserNumber,\nfirstDate,secondDate,thirdDate,fourthDate)

RDLF -> RDLF : Saves data into an ArrayList<String> called\n legacyDataList

end loop


RDLF -> Comp : getSNSUserList()
activate Comp
Comp -> SNSStore : getSNSUserList()
activate SNSStore
SNSStore -> Comp : returns list
deactivate SNSStore
Comp -> RDLF : returns list
RDLF -> Comp : getVaccineList()
Comp -> RDLF : returns list
deactivate Comp
loop#Red while legacyDataList has new lines

RDLF -> RDLF : findPosOfSNSUser(snsUsersList,\n values,positionInSnsUserList)



deactivate Comp
```

Prediction PlantUML (truncated):
```plantuml
@startuml
participant "CenterCoordinator" as CenterCoordinator
participant "DataFromLegacySystemUI" as DataFromLegacySystemUI
participant "DataFromLegacySystemController" as DataFromLegacySystemController
participant "Company" as Company
participant "SNSUserStore" as SNSUserStore
participant "App" as App
participant "VaccinationCenter" as VaccinationCenter
participant "Arrival" as Arrival
participant "Departure" as Departure
participant "vaccinationCentersStore" as vaccinationCentersStore

participant "DataFromLegacySystemUI" as DataFromLegacySystemUI

CenterCoordinator -> DataFromLegacySystemUI: 1 Asks to load a CSV file with legacy data
DataFromLegacySystemUI -> DataFromLegacySystemController: 2 DataFromLegacySystemController
DataFromLegacySystemController -> vaccinationCentersStore: 3 getVaccinationCentersStore()
DataFromLegacySystemController -> vaccinationCentersStore: 4 returns the store
DataFromLegacySystemController -> vaccinationCentersStore: 5 getVaccinationCenter(AssociatedToCoordinator(id))
DataFromLegacySystemController -> vaccinationCentersStore: 6 returns the vaccination center
DataFromLegacySystemUI -> ReadLegacyDataFile: 7 ReadLegacyDataFile(center)
DataFromLegacySystemUI -> ReadLegacyDataFile: 8 request path of the CSV file
DataFromLegacySystemUI -> ReadLegacyDataFile: 9 types path
DataFromLegacySystemUI -> ReadLegacyDataFile: 10 readFile(path)
DataFromLegacyDataFile -> ReadLegacyDataFile: 11 readFile(String path)
DataFromLegacyDataFile -> ReadLegacyDataFile: 12 while csv has new lines
DataFromLegacyDataFile -> ReadLegacyDataFile: 13 validateFile(legacy(SNSUserNumber, firstName, secondDate, thirdDate, fourthDate))
DataFromLegacyDataFile -> ReadLegacyDataFile: 14 Saves data into an ArrayList<String> called legacyDataList
DataFromLegacyDataFile -> ReadLegacyDataFile: 15 getSNSUserList()
DataFromLegacyDataFile -> ReadLegacyDataFile: 16 returns list
DataFromLegacyDataFile -> ReadLegacyDataFile: 17 returns list
DataFromLegacyDataFile -> ReadLegacyDataFile: 18 getVaccineList()
DataFromLegacyDataFile -> ReadLegacyDataFile: 19 returns list
DataFromLegacyDataFile -> ReadLegacyDataFile: 20 while legacyDataList has new lines
DataFromLegacyDataFile -> ReadLegacyDataFile: 21 findPos(OTPax(vaccineList, values, positionInSNSUserList, values.positionInSNSUserList, positionInVaccinesList, lineOfTheData)
DataFromLegacyDataFile -> ReadLegacyDataFile: 22 checksDuplicates(updatedList, snsUsersList, vaccineList, positionInSNSUserList, positionInVaccinesList, lineOfTheData)
DataFromLegacyDataFile -> ReadLegacyDataFile: 23 Saves data into an ArrayList<String> called updatedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 24 createArrival()
DataFromLegacyDataFile -> ReadLegacyDataFile: 25 createArrival()
DataFromLegacyDataFile -> ReadLegacyDataFile: 26 returns Arrival
DataFromLegacyDataFile -> ReadLegacyDataFile: 27 Saves arrival into List<Arrival> called arrivalsList
DataFromLegacyDataFile -> ReadLegacyDataFile: 28 genericsArrivals.binaryFileWrite(Constants.FILE_PATH_ARRIVALS, arrivalsList)
DataFromLegacyDataFile -> ReadLegacyDataFile: 29 createDeparture()
DataFromLegacyDataFile -> ReadLegacyDataFile: 30 createDeparture()
DataFromLegacyDataFile -> ReadLegacyDataFile: 31 returns departure
DataFromLegacyDataFile -> ReadLegacyDataFile: 32 Saves departure into List<Departure> called departedDepartureList
DataFromLegacyDataFile -> ReadLegacyDataFile: 33 genericsDeparture.binaryFileWrite(Constants.FILE_PATH_DEPARTURES, departedDepartureList)
DataFromLegacyDataFile -> ReadLegacyDataFile: 34 returns updatedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 35 returns updatedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 36 requests the option to sort
DataFromLegacyDataFile -> ReadLegacyDataFile: 37 selects option
DataFromLegacyDataFile -> ReadLegacyDataFile: 38 chooseCriteriaToSort(option)
DataFromLegacyDataFile -> ReadLegacyDataFile: 39 setList(Option)
DataFromLegacyDataFile -> ReadLegacyDataFile: 40 while updatedList has new lines
DataFromLegacyDataFile -> ReadLegacyDataFile: 41 a List<LocalDateTime> called listToSort
DataFromLegacyDataFile -> ReadLegacyDataFile: 42 selects order
DataFromLegacyDataFile -> ReadLegacyDataFile: 43 getAlgorithm()
DataFromLegacyDataFile -> ReadLegacyDataFile: 44 getSortingAlgorithm()
DataFromLegacyDataFile -> ReadLegacyDataFile: 45 returns algorithm
DataFromLegacyDataFile -> ReadLegacyDataFile: 46 returns algorithm
DataFromLegacyDataFile -> ReadLegacyDataFile: 47 sortListWithAlgo(algorithmToBeUsed.option)
DataFromLegacyDataFile -> ReadLegacyDataFile: 48 insertionSortAscending()
DataFromLegacyDataFile -> ReadLegacyDataFile: 49 returns sortedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 50 returns sortedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 51 prints sortedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 52 selects order
DataFromLegacyDataFile -> ReadLegacyDataFile: 53 getAlgorithm()
DataFromLegacyDataFile -> ReadLegacyDataFile: 54 getSortingAlgorithm()
DataFromLegacyDataFile -> ReadLegacyDataFile: 55 returns algorithm
DataFromLegacyDataFile -> ReadLegacyDataFile: 56 returns algorithm
DataFromLegacyDataFile -> ReadLegacyDataFile: 57 sortListWithAlgo(algorithmToBeUsed.option)
DataFromLegacyDataFile -> ReadLegacyDataFile: 58 insertionSortDescending()
DataFromLegacyDataFile -> ReadLegacyDataFile: 59 returns sortedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 60 returns sortedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 61 prints sortedList
DataFromLegacyDataFile -> ReadLegacyDataFile: 62 while csv has new lines
DataFromLegacyDataFile -> ReadLegacyDataFile: 63 validateFile(legacy(SNSUserNumber, firstName, secondDate, thirdDate, fourthDate))
DataFromLegacyDataFile -> ReadLegacyDataFile: 64 Saves data into an ArrayList<String> called legacyDataList
DataFromLegacyDataFile -> ReadLegacyDataFile: 65 getSNSUserList()
DataFromLegacyDataFile -> ReadLegacyDataFile: 66 returns list
```

#### `ccff036df127af4a5880d98ee2d665b019028bd4` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=10 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: inheritance, aggregation, association
- chrF++: 20.28
- Files: GT `data/puml_files/ccff036df127af4a5880d98ee2d665b019028bd4.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/ccff036df127af4a5880d98ee2d665b019028bd4.puml` (yes) · input `data/puml_images_1568/ccff036df127af4a5880d98ee2d665b019028bd4.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/ccff036df127af4a5880d98ee2d665b019028bd4.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: ccff036df127af4a5880d98ee2d665b019028bd4
' Original Path: /docs/Class-Diagram.plantuml
' Source: World of Code

@startuml

class KindleNotesMarkdown {
+ {static} convert(notes: KindleNotes)
}

enum MarkdownFormatter {
+ TITLE
+ AUTHOR
+ SECTION
+ S_HEADING
+ S_TEXT
}

KindleNotesMarkdown -- MarkdownFormatter

abstract class KindleNotes<<abstract>> {
+title: String
+author: String
+notes: <<List>> NoteElement
+{abstract}parse()
}

class NoteElement{
+section
+heading
+text
}

enum Selector{
+ TITLE
+ AUTHOR
+ SECTIONS
+ S_HEADING
+ S_NOTE_HEADING
+ S_NOTE_TEXT
}

class KindleNotesHtml_1_21{
selector
}

class KindleNotesHtml_1_23{
selector
}

class KindleNotesHtml <<KindleNotes>>{
- _html
- _selector: <<Enum>>Selector
- _extract_notes()
}

class KindleNotesCsv <<KindleNotes>>{
- _csv
- _extract_notes()
}

class KindleNotesText <<KindleNotes>>{
- _text
- _extract_notes()
}

KindleNotesHtml -right- Selector
KindleNotesHtml_1_21 -up-|> KindleNotesHtml
KindleNotesHtml_1_23 -up-|> KindleNotesHtml
KindleNotesHtml .up.|> KindleNotes
KindleNotesCsv .up.|> KindleNotes
KindleNotesText .up.|> KindleNotes
NoteElement -left-o KindleNotes: has n notes

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam classDiagram
    class KindleNotes {
        <<abstract>>
        title: String
        author: String
        notes: <<List>> NoteElement
        parse()
    }

    class NoteElement {
        section
        heading
        text
    }

    class KindleNotesMarkdown {
        convert(notes: KindleNotes)
    }

    class MarkdownFormatter {
        TITLE
        AUTHOR
        SECTION
        S_HEADING
        S_TEXT
    }

    class KindleNotesCsv {
        _csv
        _extract_notes()
    }

    class KindleNotesText {
        _text
        _extract_notes()
    }

    class KindleNotesHtml {
        _html
        _selector: <<Enum>>Selector
        _extract_notes()
    }

    class Selector {
        TITLE
        AUTHOR
        SECTIONS
        S_HEADING
        S_NOTE_HEADING
        S_NOTE_TEXT
    }

    class KindleNotesHtml_1_21 {
        selector
    }

    class KindleNotesHtml_1_23 {
        selector
    }

    class KindleNotes {
        title: String
        author: String
        notes: <<List>> NoteElement
        parse()
    }

    class KindleNotesMarkdown {
        convert(notes: KindleNotes)
    }

    class MarkdownFormatter {
        TITLE
        AUTHOR
        SECTION
        S_HEADING
        S_TEXT
    }

```

#### `defb5523b1761bd4a179f706eaab0e5e6a774f08_04` — compile_fail (sequence, tier 2)

- CSR: `Error line 17 in file: data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/extracted/defb5523b1761bd4a179f706eaab0e5e6a774f08_04.puml`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 71.86
- Files: GT `data/puml_files/defb5523b1761bd4a179f706eaab0e5e6a774f08_04.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/defb5523b1761bd4a179f706eaab0e5e6a774f08_04.puml` (yes) · input `data/puml_images_1568/defb5523b1761bd4a179f706eaab0e5e6a774f08_04.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/defb5523b1761bd4a179f706eaab0e5e6a774f08_04.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: defb5523b1761bd4a179f706eaab0e5e6a774f08
' Original Path: /test6/sequence.pu
' Source: World of Code

@startuml
title 学生列表用例时序图
hide footbox
actor teacher
teacher --> courseClass: 根据工号以及默认学期获取\n所授课程开课班号及课程号
courseClass --> S_C: 获取学生成绩及学号
S_C --> student: 获取学生信息
student --> teacher: 每个所授学生信息及其已批改实验平均成绩列表
group 点击成绩详情
    teacher --> experimentscores: 根据学号,课程号开课班号查找试实验成绩单号
    experimentscores --> cexperiments: 获取实验及成绩信息
    cexperiments --> experimentclauses: 获取实验及成绩信息
    experimentclauses --> teacher: 返回所点击学生该课程所有相关实验成绩列表
end
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title 学生列表用例时序图

actor teacher
participant courseClass
participant S_C
participant student
participant experimentscores
participant cexperiments
participant experimentclauses

teacher -> courseClass: 根据工号以及默认学期获取所授课程开课班号及课程号
courseClass -> S_C: 获取学生成绩及学号
S_C -> student: 获取学生信息
student -> courseClass: 每个所授学生信息及其已批改实验平均成绩列表

section 点击成绩详情
    teacher -> experimentscores: 根据学号,课程号开课班号查找试实验成绩单号
    experimentscores -> cexperiments: 获取实验及成绩信息
    cexperiments -> experimentclauses: 获取实验及成绩信息
    experimentclauses -> student: 返回所点击学生该课程所有相关实验成绩列表
    student -> courseClass: 返回所点击学生该课程所有相关实验成绩列表
@endsection

@enduml
```

#### `e494004949c090dbccf0a82083800b6947b2fc32` — compile_fail (class, tier 2)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=6 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: inheritance
- chrF++: 8.84
- Files: GT `data/puml_files/e494004949c090dbccf0a82083800b6947b2fc32.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/e494004949c090dbccf0a82083800b6947b2fc32.puml` (yes) · input `data/puml_images_1568/e494004949c090dbccf0a82083800b6947b2fc32.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/e494004949c090dbccf0a82083800b6947b2fc32.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: e494004949c090dbccf0a82083800b6947b2fc32
' Original Path: /doc/package-architecture.puml
' Source: World of Code

@startuml

title Java Steganography API :: Packages

package "org.steg.jsa" #DDDDDD {
  interface SteganographyTechnique {
  + embed(Message, Key,Cover): Stego
     + extract(Stego, Key): Message
  }
  SteganographyTechnique <|. AbstractSteganography
}

package org.steg.audio {
  SteganographyTechnique <|... AdaptiveAudioSteganography
  SteganographyTechnique <|... AudioLSBSteganography
}

package org.steg.image {
  SteganographyTechnique <|... ImageLSBSteganography
}

package org.steg.video {
  SteganographyTechnique <|... VideoSteganography
}

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
package org {
    package steg {
        package jsa {
            interface SteganographyTechnique {
                method embed(Message, Key, Cover): Stego
                method extract(Stego, Key): Message
            }
            class AbstractSteganography {
            }
        }
        package audio {
            class AdaptiveAudioSteganography {
            }
            class AudioLSBSteganography {
            }
        }
        package image {
            class ImageLSBSteganography {
            }
        }
        package video {
            class VideoSteganography {
            }
        }
}

class SteganographyTechnique {
    label "I" as interfaceIcon
    label "SteganographyTechnique" as interfaceName
    label "embed(Message, Key, Cover): Stego" as method1
    label "extract(Stego, Key): Message" as method2
}

class AbstractSteganography {
    label "C" as classIcon
    label "AbstractSteganography" as className
}

class AdaptiveAudioSteganography {
    label "C" as classIcon
    label "AdaptiveAudioSteganography" as className
}

class AudioLSBSteganography {
    label "C" as classIcon
    label "AudioLSBSteganography" as className
}

class ImageLSBSteganography {
    label "C" as classIcon
    label "ImageLSBSteganography" as className
}

class VideoSteganography {
    label "C" as classIcon
    label "VideoSteganography" as className
}

class SteganographyTechnique {
    label "I" as interfaceIcon
    label "SteganographyTechnique" as interfaceName
    label "embed(Message, Key, Cover): Stego" as method1
    label "extract(Stego, Key): Message" as method2
}

class AbstractSteganography {
    label "C" as classIcon
    label "AbstractSteganography" as className
}

class AdaptiveAudioSteganography {
    label "C" as classIcon
    label "AdaptiveAudioSteganography" as className
}

class AudioLSBSteganography {
    label "C" as classIcon
    label "AudioLSBSteganography" as className
}
```

#### outcome: compiled_low_structural

#### `04a41abf900ab96464224a91e2f67aaf11011c89` — compiled_low_structural (sequence, tier 3)

- Element: tp=4 fp=2 fn=0 F1=0.800; type-acc matched=4 correct=0 excluded=0
- Relationship: tp=0 fp=12 fn=14 F1=0.000; missed: message; extra: association
- chrF++: 57.12
- Files: GT `data/puml_files/04a41abf900ab96464224a91e2f67aaf11011c89.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/04a41abf900ab96464224a91e2f67aaf11011c89.puml` (yes) · input `data/puml_images_1568/04a41abf900ab96464224a91e2f67aaf11011c89.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/04a41abf900ab96464224a91e2f67aaf11011c89.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 04a41abf900ab96464224a91e2f67aaf11011c89
' Original Path: /doc/uml/context-dynamic-apotektjenester.puml
' Source: World of Code

@startuml

title Inhalasjonsveiledning

actor Farmasøyt
participant Kjedesystem
participant DIFA
participant HELFO

group Dialog med Kjede Kjedesystem
Farmasøyt -> Kjedesystem: Velger Inhalasjonsveiledning
Farmasøyt <-- Kjedesystem: Redirect
end group
group Dialog med DIFA
Farmasøyt -> DIFA: Vis Personsøk skjema
Farmasøyt -> DIFA: Angi person (fødselsnummer eller navn + fødselsdato)
Farmasøyt <-- DIFA: Vis instrukser for behandlingen
Farmasøyt -> DIFA: Angi informasjon om behandlingen (eks: antall repetisjoner)
Farmasøyt -> DIFA: Fullfør behandling
activate DIFA
DIFA -> DIFA: Journalføre behandling
DIFA -> DIFA: Beregne refusjon og egenandel
DIFA -> HELFO: Refusjonskrav
Farmasøyt <-- DIFA: Redirect med varenummer og egenandel
deactivate DIFA
end group
group Dialog med Kjede Kjedesystem
Farmasøyt -> Kjedesystem: Legg til egenandel i handlekurv
Farmasøyt <-> Kjedesystem: Vis oppgjørsgrunnlag
Farmasøyt <-> Kjedesystem: Fullfør salg
end group

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Inhalasjonsveiledning

actor "Farmasøyt" as Farmer

interface "Kjedesystem" as Kjesystem

interface "DIFA" as Difa

interface "HELFO" as Helfo

rectangle "Dialog med Kjede Kjesystem" {
    Farmer -> Kjesystem : Velger Inhalasjonsveiledning
    Kjesystem -- Farmer : Redirect
}

rectangle "Dialog med DIFA" {
    Farmer -> Difa : Vis Personsøk skjema
    Difa -- Farmer : Vis instrukser for behandlingen
    Farmer -> Difa : Angi person (fødselsnummer eller navn + fødselsdato)
    Difa -- Farmer : Angi informasjon om behandlingen (eks: antall repetisjoner)
    Farmer -> Difa : Fullfør behandling
    Difa -> Helfo : Refusjonskrav
    Difa -- Farmer : Redirect med varenummer og egenandel
}

rectangle "Dialog med Kjede Kjesystem" {
    Farmer -> Kjesystem : Legg til egenandel i handlekurv
    Kjesystem -- Farmer : Vis oppgjørsgrunnlag
    Farmer -> Kjesystem : Fullfør salg
}

@enduml
```

#### `21b4a540ef036fcb31ecb8df572773b7cd602a22` — compiled_low_structural (sequence, tier 3)

- Element: tp=8 fp=2 fn=1 F1=0.842; type-acc matched=8 correct=4 excluded=0
- Relationship: tp=5 fp=9 fn=11 F1=0.333; missed: message; extra: message
- chrF++: 76.40
- Files: GT `data/puml_files/21b4a540ef036fcb31ecb8df572773b7cd602a22.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/21b4a540ef036fcb31ecb8df572773b7cd602a22.puml` (yes) · input `data/puml_images_1568/21b4a540ef036fcb31ecb8df572773b7cd602a22.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/21b4a540ef036fcb31ecb8df572773b7cd602a22.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 21b4a540ef036fcb31ecb8df572773b7cd602a22
' Original Path: /bank/diagrams/cqrs.puml
' Source: World of Code

@startuml

actor User
participant UIBFF
box DomainModel
  queue CommandBus
  participant Aggregate
  participant ProcessManager
  queue EventBus
  participant QueryManager
end box
participant Projectors
database ReadModels

User -> UIBFF : http commands
UIBFF -> CommandBus : commands
CommandBus -> Aggregate : commands
Aggregate -> EventBus : events
EventBus -> ProcessManager : events
ProcessManager -> CommandBus : commands
EventBus -> Projectors : events
Projectors -> ReadModels : write
EventBus -> UIBFF : events
UIBFF -> User : push

User -> UIBFF : http queries
UIBFF -> QueryManager : queries
QueryManager -> ReadModels : results
ReadModels ->  QueryManager : results
QueryManager -> UIBFF : results
UIBFF -> User : results

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
participant "User" as User
participant "UIFF" as UIBFF
participant "CommandBus" as CommandBus
participant "Aggregate" as Aggregate
participant "ProcessManager" as ProcessManager
participant "EventBus" as EventBus
participant "QueryManager" as QueryManager
participant "Projectors" as Projectors
participant "ReadModels" as ReadModels

User ->> UIBFF : http commands
UIFF -> CommandBus : commands
CommandBus -> Aggregate : commands
Aggregate -> EventBus : events
EventBus -> ProcessManager : events
ProcessManager -> CommandBus : events
CommandBus -> UIBFF : commands
UIFF -> User : push
User -> UIBFF : http queries
UIFF -> QueryManager : queries
QueryManager -> Projectors : results
Projectors -> ReadModels : write
QueryManager -> UIBFF : results
UIFF -> User : results

@enduml
```

#### `289412e14085f0e88a03028956a35b485378539f` — compiled_low_structural (class, tier 1)

- Element: tp=2 fp=0 fn=0 F1=1.000; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=1 fn=1 F1=0.000; missed: association; extra: dependency
- chrF++: 81.66
- Files: GT `data/puml_files/289412e14085f0e88a03028956a35b485378539f.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/289412e14085f0e88a03028956a35b485378539f.puml` (yes) · input `data/puml_images_1568/289412e14085f0e88a03028956a35b485378539f.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/289412e14085f0e88a03028956a35b485378539f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 289412e14085f0e88a03028956a35b485378539f
' Original Path: /Documents/Shos.Chatter.Server/Areas/HelpPage/ModelDescriptions/ParameterAnnotation.puml
' Source: World of Code

@startuml
class ParameterAnnotation {
    + Documentation : string <<get>> <<set>>
}
ParameterAnnotation --> "AnnotationAttribute" Attribute
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
class ParameterAnnotation {
    "C"
    Documentation : string <<get>> <<set>>
}

class Attribute {
    "C"
}

ParameterAnnotation ..> Attribute : AnnotationAttribute

@enduml
```

#### `31f9d300f7cbc62f736af6bdaa9541dc23087f14` — compiled_low_structural (class, tier 2)

- Element: tp=3 fp=0 fn=0 F1=1.000; type-acc matched=3 correct=3 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: inheritance; extra: dependency
- chrF++: 41.60
- Files: GT `data/puml_files/31f9d300f7cbc62f736af6bdaa9541dc23087f14.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/31f9d300f7cbc62f736af6bdaa9541dc23087f14.puml` (yes) · input `data/puml_images_1568/31f9d300f7cbc62f736af6bdaa9541dc23087f14.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/31f9d300f7cbc62f736af6bdaa9541dc23087f14.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 31f9d300f7cbc62f736af6bdaa9541dc23087f14
' Original Path: /JavaProg/src/main/java/javaprog/worksheet/ws0304/課題3.puml
' Source: World of Code

@startuml
skinparam classAttributeIconSize 0
skinparam monochrome true
skinparam classFontSize 18
skinparam classFontName Menlo
skinparam classAttributeFontSize 18
skinparam classAttributeFontName Menlo
skinparam shadowing false
skinparam arrowFontSize 18
skinparam arrowFontName Menlo

hide circle

class Diagram {
#x: float
#y: float
+set(x: float, y: float): void
}

class Rectangle {
+calc(): float
}

class Triangle {
+calc(): float
}

Diagram <|-r- Rectangle : "    "
Diagram <|-- Triangle
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
class Diagram {
  +#x: float
  +#y: float
  +set(x: float, y: float): void
}

class Rectangle {
  +calc(): float
}

class Triangle {
  +calc(): float
}

Diagram <.. Rectangle
Diagram <.. Triangle

@enduml
```

#### `47701f1f9b618cbf4dd05de9a20a69ba6b2de9c6` — compiled_low_structural (class, tier 2)

- Element: tp=3 fp=0 fn=1 F1=0.857; type-acc matched=3 correct=2 excluded=0
- Relationship: tp=0 fp=2 fn=3 F1=0.000; missed: inheritance, aggregation, association; extra: dependency
- chrF++: 58.77
- Files: GT `data/puml_files/47701f1f9b618cbf4dd05de9a20a69ba6b2de9c6.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/47701f1f9b618cbf4dd05de9a20a69ba6b2de9c6.puml` (yes) · input `data/puml_images_1568/47701f1f9b618cbf4dd05de9a20a69ba6b2de9c6.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/47701f1f9b618cbf4dd05de9a20a69ba6b2de9c6.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 47701f1f9b618cbf4dd05de9a20a69ba6b2de9c6
' Original Path: /MyProjects/Others/DesignPatterns/策略模式.puml
' Source: World of Code

@startuml

interface Strategy {
    + algorithm()
}

class ConcreteStrategy {
    + algorithm()
}

class Context {
    - strategy
    + operation()
}

ConcreteStrategy ..|> Strategy
Strategy --o "-strategy" Context

note right of Context::"operation()"
    strategy.algorithm();
end note

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
class ConcreteStrategy {
    "C"
    algorithm()
}

class Strategy {
    "I"
    algorithm()
}

class Context {
    "C"
    strategy
    operation()
}

ConcreteStrategy ..> Strategy : inherits
Strategy ..> Context : -strategy
@enduml
```

#### `549978ae505c2371e3d2a0fbef91df22093718b5` — compiled_low_structural (class, tier 3)

- Element: tp=6 fp=3 fn=1 F1=0.750; type-acc matched=6 correct=4 excluded=0
- Relationship: tp=1 fp=17 fn=7 F1=0.077; missed: composition, aggregation, dependency; extra: dependency
- chrF++: 62.59
- Files: GT `data/puml_files/549978ae505c2371e3d2a0fbef91df22093718b5.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/549978ae505c2371e3d2a0fbef91df22093718b5.puml` (yes) · input `data/puml_images_1568/549978ae505c2371e3d2a0fbef91df22093718b5.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/549978ae505c2371e3d2a0fbef91df22093718b5.png` (yes)

#### `5ffc89fc72b1e274a4fcb2b6ee0b39ab8fb1e527` — compiled_low_structural (class, tier 4)

- Element: tp=7 fp=1 fn=0 F1=0.933; type-acc matched=7 correct=7 excluded=0
- Relationship: tp=0 fp=7 fn=6 F1=0.000; missed: composition, aggregation, association; extra: composition, dependency, association
- chrF++: 76.64
- Files: GT `data/puml_files/5ffc89fc72b1e274a4fcb2b6ee0b39ab8fb1e527.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/5ffc89fc72b1e274a4fcb2b6ee0b39ab8fb1e527.puml` (yes) · input `data/puml_images_1568/5ffc89fc72b1e274a4fcb2b6ee0b39ab8fb1e527.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/5ffc89fc72b1e274a4fcb2b6ee0b39ab8fb1e527.png` (yes)

#### `6f12ad3e5c0100e4b2adf9d45f67dda7f2c7e15b` — compiled_low_structural (sequence, tier 1)

- Element: tp=0 fp=4 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=4 fn=1 F1=0.000; missed: message; extra: inheritance, dependency
- chrF++: 63.86
- Files: GT `data/puml_files/6f12ad3e5c0100e4b2adf9d45f67dda7f2c7e15b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/6f12ad3e5c0100e4b2adf9d45f67dda7f2c7e15b.puml` (yes) · input `data/puml_images_1568/6f12ad3e5c0100e4b2adf9d45f67dda7f2c7e15b.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/6f12ad3e5c0100e4b2adf9d45f67dda7f2c7e15b.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 6f12ad3e5c0100e4b2adf9d45f67dda7f2c7e15b
' Original Path: /DossierConception/old/SeqChangerEtat.pu
' Source: World of Code

@startuml

title Diagramme Séquence du Changement d'etat d'un dossier

actor User as U
U -> Dossier:ChangerEtat(Etat e)
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Diagramme Séquence du Changement d'état d'un dossier

actor User1 as User1
actor User2 as User2

rectangle Dossier1 as Dossier1
rectangle Dossier2 as Dossier2

User1 --|> Dossier1
User2 --|> Dossier2

User1 ..> Dossier1 : ChangerEtat(Etat e)
User2 ..> Dossier2 : ChangerEtat(Etat e)

@enduml
```

#### `8c8654017838296bafee2adff60937211799aae3` — compiled_low_structural (sequence, tier 1)

- Element: tp=4 fp=2 fn=0 F1=0.800; type-acc matched=4 correct=0 excluded=0
- Relationship: tp=0 fp=6 fn=2 F1=0.000; missed: message; extra: association
- chrF++: 55.08
- Files: GT `data/puml_files/8c8654017838296bafee2adff60937211799aae3.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/8c8654017838296bafee2adff60937211799aae3.puml` (yes) · input `data/puml_images_1568/8c8654017838296bafee2adff60937211799aae3.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/8c8654017838296bafee2adff60937211799aae3.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 8c8654017838296bafee2adff60937211799aae3
' Original Path: /uml/CanelOffer.pu
' Source: World of Code

@startuml
hide footbox
title Cancel Offer
skinparam monochrome true

actor Merchant
collections MarketContract
collections Inventory

Merchant -> Market : Merchant calls settle()
MarketContract -> Inventory : Market unlocks offered funds in inventory

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Cancel Offer

actor Merchant
rectangle MarketContract
rectangle Inventory
rectangle Market

rectangle MarketContract
rectangle Inventory
rectangle Market

"Merchant calls settle()" as M1
M1 --> MarketContract
M1 --> Inventory
M1 --> Market

"Market unlocks offered funds in inventory" as M2
M2 --> MarketContract
M2 --> Inventory
M2 --> Market

@enduml
```

#### `9f191261deed646fe29bfdbe79135b223f66136e` — compiled_low_structural (class, tier 3)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=1 fp=6 fn=5 F1=0.154; missed: aggregation, association; extra: association
- chrF++: 69.05
- Files: GT `data/puml_files/9f191261deed646fe29bfdbe79135b223f66136e.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/9f191261deed646fe29bfdbe79135b223f66136e.puml` (yes) · input `data/puml_images_1568/9f191261deed646fe29bfdbe79135b223f66136e.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/9f191261deed646fe29bfdbe79135b223f66136e.png` (yes)

#### `a3ad23d50dbe8e3469b0409e193eabac4c6b96c4` — compiled_low_structural (class, tier 1)

- Element: tp=2 fp=0 fn=0 F1=1.000; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=2 fn=1 F1=0.000; missed: inheritance; extra: association
- chrF++: 71.22
- Files: GT `data/puml_files/a3ad23d50dbe8e3469b0409e193eabac4c6b96c4.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/a3ad23d50dbe8e3469b0409e193eabac4c6b96c4.puml` (yes) · input `data/puml_images_1568/a3ad23d50dbe8e3469b0409e193eabac4c6b96c4.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/a3ad23d50dbe8e3469b0409e193eabac4c6b96c4.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: a3ad23d50dbe8e3469b0409e193eabac4c6b96c4
' Original Path: /Documentação/v2/plantuml/Application.Sales/Controllers/TesteController.puml
' Source: World of Code

@startuml
class TesteController {
    + TesteController()
    + Get() : void
}
ControllerBase <|-- TesteController
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
package "C" as C {
    class ControllerBase {
        +C
    }
    class TesteController {
        +C
        -TesteController()
        -Get() : void
    }
}

C --> ControllerBase
C --> TesteController

@enduml
```

#### `ae6873b5bca0613bb74894f77a2ccdf505b9e329` — compiled_low_structural (sequence, tier 2)

- Element: tp=4 fp=0 fn=0 F1=1.000; type-acc matched=4 correct=4 excluded=0
- Relationship: tp=4 fp=12 fn=0 F1=0.400; extra: message
- chrF++: 54.17
- Files: GT `data/puml_files/ae6873b5bca0613bb74894f77a2ccdf505b9e329.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/ae6873b5bca0613bb74894f77a2ccdf505b9e329.puml` (yes) · input `data/puml_images_1568/ae6873b5bca0613bb74894f77a2ccdf505b9e329.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/ae6873b5bca0613bb74894f77a2ccdf505b9e329.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: ae6873b5bca0613bb74894f77a2ccdf505b9e329
' Original Path: /mero-halon/doc/diagrams/sns-operation-abort.uml
' Source: World of Code

@startuml
participant halon
participant ios1
participant ios2
participant client

activate ios1
activate ios2
... SNS operation ...
halon -> ios2: m0_spiel_repair_abort
destroy ios1
destroy ios2
loop until all IOS are in [IDLE,FAILED]
  halon -> ios2: repair status request
  ios2  -> halon: repair status reply
end
halon -> client: notify [(pool, PREVIOUS_STATE), (disk, PREVIOUS_STATE)]

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
participant "halon" as Halon
participant "ios1" as IOS1
participant "ios2" as IOS2
participant "client" as Client

Halon --> IOS1 : m0_spiel_repair_abort
Halon --> IOS2 : m0_spiel_repair_abort

Halon --> IOS1 : repair status request
Halon --> IOS2 : repair status request

IOS1 --> IOS2 : repair status reply
IOS2 --> IOS1 : repair status reply

Halon --> Client : notify [(pool, PREVIOUS_STATE), (disk, PREVIOUS_STATE)]

Halon --> IOS1 : loop
loop [until all IOS are in [IDLE,FAILED]]
Halon --> IOS1 : repair status request
IOS1 --> Halon : repair status reply
Halon --> IOS2 : repair status request
IOS2 --> Halon : repair status reply
end loop

Halon --> IOS1 : SNS operation
Halon --> IOS2 : SNS operation

Halon --> IOS1 : X
Halon --> IOS2 : X

@enduml
```

#### `b6e8396cacc10977e676c9aff6c9598b4ea1a934` — compiled_low_structural (sequence, tier 2)

- Element: tp=0 fp=9 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=7 fn=3 F1=0.000; missed: message; extra: association
- chrF++: 73.90
- Files: GT `data/puml_files/b6e8396cacc10977e676c9aff6c9598b4ea1a934.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/b6e8396cacc10977e676c9aff6c9598b4ea1a934.puml` (yes) · input `data/puml_images_1568/b6e8396cacc10977e676c9aff6c9598b4ea1a934.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/b6e8396cacc10977e676c9aff6c9598b4ea1a934.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: b6e8396cacc10977e676c9aff6c9598b4ea1a934
' Original Path: /stock-market-seq (SELL).wsd
' Source: World of Code

@startuml
skinparam Monochrome true
skinparam Shadowing false

participant TraderClient 
participant CommandBuilder
participant TransactionManager  
participant StockBroker 
participant TraderAccount 
participant SellStockCommand
participant Mediator 
participant TraderPolicy
participant PriceProvider 

TraderClient -> CommandBuilder: create_command(SellStockCommand)
CommandBuilder -> TraderClient: SellStockCommand
TraderClient ->o TransactionManager: command_signal(SellStockCommand)

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
participant as TraderClient
participant as CommandBuilder
participant as TransactionManager
participant as StockBroker
participant as TraderAccount
participant as SellStockCommand
participant as Mediator
participant as TraderPolicy
participant as PriceProvider

TraderClient --> CommandBuilder : create_command(SellStockCommand)
CommandBuilder --> TraderClient : SellStockCommand
TraderClient --> TransactionManager : command_signal(SellStockCommand)
TransactionManager --> StockBroker : execute
StockBroker --> TraderAccount : execute
TraderAccount --> TraderPolicy : execute
TraderPolicy --> PriceProvider : execute

@enduml
```

#### `bc5d8adf0f76950c65189a4fe9d08c956c22e8a6` — compiled_low_structural (sequence, tier 4)

- Element: tp=9 fp=0 fn=0 F1=1.000; type-acc matched=9 correct=8 excluded=0
- Relationship: tp=9 fp=13 fn=8 F1=0.462; missed: message; extra: message
- chrF++: 58.43
- Files: GT `data/puml_files/bc5d8adf0f76950c65189a4fe9d08c956c22e8a6.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/bc5d8adf0f76950c65189a4fe9d08c956c22e8a6.puml` (yes) · input `data/puml_images_1568/bc5d8adf0f76950c65189a4fe9d08c956c22e8a6.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/bc5d8adf0f76950c65189a4fe9d08c956c22e8a6.png` (yes)

#### `c8c2c241aac85edf063c91907252641d60d12c1e` — compiled_low_structural (sequence, tier 4)

- Element: tp=2 fp=4 fn=4 F1=0.333; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=0 fn=17 F1=0.000; missed: message
- chrF++: 67.59
- Files: GT `data/puml_files/c8c2c241aac85edf063c91907252641d60d12c1e.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/c8c2c241aac85edf063c91907252641d60d12c1e.puml` (yes) · input `data/puml_images_1568/c8c2c241aac85edf063c91907252641d60d12c1e.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/c8c2c241aac85edf063c91907252641d60d12c1e.png` (yes)

#### `f60a13a24f73eed9f20b65111e100cf8d048403b` — compiled_low_structural (class, tier 4)

- Element: tp=15 fp=1 fn=1 F1=0.938; type-acc matched=15 correct=11 excluded=0
- Relationship: tp=2 fp=16 fn=13 F1=0.121; missed: inheritance, composition, association; extra: association
- chrF++: 74.09
- Files: GT `data/puml_files/f60a13a24f73eed9f20b65111e100cf8d048403b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-2B_20260613T153655Z/f60a13a24f73eed9f20b65111e100cf8d048403b.puml` (yes) · input `data/puml_images_1568/f60a13a24f73eed9f20b65111e100cf8d048403b.png` (yes) · render `data/csr/Qwen_Qwen3.5-2B_20260613T153655Z/png/f60a13a24f73eed9f20b65111e100cf8d048403b.png` (yes)

### Qwen3.5-9B

#### outcome: compile_fail

#### `01325068fa93284336d6055e819ad4dd59251533` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=8 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: inheritance, aggregation, association
- chrF++: 4.11
- Files: GT `data/puml_files/01325068fa93284336d6055e819ad4dd59251533.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/01325068fa93284336d6055e819ad4dd59251533.puml` (yes) · input `data/puml_images_1568/01325068fa93284336d6055e819ad4dd59251533.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/01325068fa93284336d6055e819ad4dd59251533.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 01325068fa93284336d6055e819ad4dd59251533
' Original Path: /plantUml.puml
' Source: World of Code

@startuml
abstract class Transaccion{
  getTipo()
  getCantidad()
  getdescripcion()
  getFecha()

}

class Gasto {
  Valor: float
  Fecha: Date
  Descripcion: str

  getTipo()
  getCantidad()
  getdescripcion()
  getFecha()
}

class Movimiento {
  NomCat: str
  Mod: str
  Valor: float
  Fecha: Date
  Descripcion: str

  getTipo()
  getMod()
  getCantidad()
  getNomCat()
  getdescripcion()
  getFecha()
}



class Ingreso {
  Valor: float
  Fecha: Date
  Descripcion: str

  getTipo()
  getCantidad()
  getdescripcion()
  getFecha()
}

class GHormiga {
  Valor: float
  Fecha: Date
  Descripcion: str

  getCantidad()
  getdescripcion()
  getFecha()
}

class Registro {
  Registros: List[Transaccion]
 

  addTransaccion()
  getRegistros()
}

class Categoria {
  parent
  Nombre: str
  Descripcion: str
  Saldo: float

  nwIngreso()
  nwGasto()
  getRegistro()
  
```

Prediction PlantUML (truncated):
```plantuml
@startuml
left to right direction
skinparam classAttributeIconSize 0
skinparam classFontName "Arial"
skinparam classFontColor #000000
skinparam classBackgroundColor #F5F5F5
skinparam classBorderColor #CCCCCC
skinparam classBorderThickness 1
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
skinparam classIconBorderThickness 1
skinparam classIconFontName "Arial"
skinparam classIconFontColor #000000
skinparam classIconBackgroundColor #E0E0E0
skinparam classIconBorderColor #999999
```

#### `0533cd1adbc17c8b92f9e1b95610057e64b52489` — compile_fail (class, tier 2)

- CSR: `Error line 18 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/0533cd1adbc17c8b92f9e1b95610057e64b52489.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=1 F1=0.000; missed: association
- chrF++: 62.29
- Files: GT `data/puml_files/0533cd1adbc17c8b92f9e1b95610057e64b52489.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/0533cd1adbc17c8b92f9e1b95610057e64b52489.puml` (yes) · input `data/puml_images_1568/0533cd1adbc17c8b92f9e1b95610057e64b52489.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/0533cd1adbc17c8b92f9e1b95610057e64b52489.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 0533cd1adbc17c8b92f9e1b95610057e64b52489
' Original Path: /uml.puml
' Source: World of Code

@startuml

class NumbersStack {
    + <<constructor>> NumbersStack()
    + <<constructor>> NumbersStack(int)
    + peak(): int
    + pop(): int
    + push(int): void
    + empty(): void
}

note left of NumbersStack::peak() {
    trả về phần tử cuối cùng
    được push vào ngăn xếp
}

note left of NumbersStack::pop() {
    trả về phần tử cuối cùng
    được push vào ngăn xếp và
    bỏ nó ra khỏi ngăn xếp
}
note left of NumbersStack::push(int) {
    thêm một phần tử vào
    ngăn xếp
}

note left of NumbersStack::empty() {
    làm rỗng ngăn xếp
}

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam noteStyle rectangle
skinparam noteBackgroundColor #FFFFE0
skinparam noteBorderColor #D4D4D4
skinparam noteFontColor #000000

package "NumbersStack" as NumbersStack {
  [«constructor» NumbersStack()]
  [«constructor» NumbersStack(int)]
  [peak(): int]
  [pop(): int]
  [push(int): void]
  [empty(): void]
}

note "làm rỗng ngăn xếp"
NumbersStack -> empty(): void

note "thêm một phần tử vào ngăn xếp"
NumbersStack -> push(int): void

note "trả về phần tử cuối cùng được push vào ngăn xếp"
NumbersStack -> peak(): int

note "trả về phần tử cuối cùng được push vào ngăn xếp và bỏ nó ra khỏi ngăn xếp"
NumbersStack -> pop(): int

@enduml
```

#### `2a0b046e572d01ab0ffe5240a016073e59a5e595` — compile_fail (sequence, tier 1)

- CSR: `Error line 3 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/2a0b046e572d01ab0ffe5240a016073e59a5e595.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 71.12
- Files: GT `data/puml_files/2a0b046e572d01ab0ffe5240a016073e59a5e595.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/2a0b046e572d01ab0ffe5240a016073e59a5e595.puml` (yes) · input `data/puml_images_1568/2a0b046e572d01ab0ffe5240a016073e59a5e595.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/2a0b046e572d01ab0ffe5240a016073e59a5e595.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 2a0b046e572d01ab0ffe5240a016073e59a5e595
' Original Path: /core/JsonData/Doc/PermissionSequence.uml
' Source: World of Code

@startuml
JsonData -> Permission1: hasAccess
Permission1 -> Callback: execute
Callback -> JsonData2: execute
JsonData2 -> Permission2: hasAccess
JsonData2 <-- Permission2: false
Callback <-- JsonData2: Session expired
Permission1 <-- Callback: Throw exception
JsonData <-- Permission1: false
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
autonumber
left to right direction
skinparam sequenceMessageAlign center

participant "JsonData" as JsonData
participant "Permission1" as Permission1
participant "Callback" as Callback
participant "JsonData2" as JsonData2
participant "Permission2" as Permission2

JsonData -> Permission1 : hasAccess
Permission1 -> Callback : execute
Callback -> JsonData2 : execute
JsonData2 -> Permission2 : hasAccess
Permission2 --> JsonData2 : false
JsonData2 --> Callback : Session expired
Callback --> Permission1 : Throw exception
Permission1 --> JsonData : false

@enduml
```

#### `4d55d9c17b48517f603b4236d9eea9bb07d7ab17` — compile_fail (sequence, tier 3)

- CSR: `Error line 10 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/4d55d9c17b48517f603b4236d9eea9bb07d7ab17.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=16 F1=0.000; missed: message
- chrF++: 83.93
- Files: GT `data/puml_files/4d55d9c17b48517f603b4236d9eea9bb07d7ab17.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/4d55d9c17b48517f603b4236d9eea9bb07d7ab17.puml` (yes) · input `data/puml_images_1568/4d55d9c17b48517f603b4236d9eea9bb07d7ab17.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/4d55d9c17b48517f603b4236d9eea9bb07d7ab17.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 4d55d9c17b48517f603b4236d9eea9bb07d7ab17
' Original Path: /plantuml/C4/C4-Level4/SequenceDiagrams/RegisterUserSequenceDiagram.wsd
' Source: World of Code

@startuml


actor User as User
participant LoginPartialView as LoginPartialView
participant MicrosoftIdentityLibrary as  MicrosoftIdentityLibrary
participant HomeController as HomeController
database StudieTipsDB as Database

User -> LoginPartialView : clicks on "Register"
activate LoginPartialView

LoginPartialView -> MicrosoftIdentityLibrary : sends action
deactivate LoginPartialView
activate MicrosoftIdentityLibrary

MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Creates RegisterView
loop While user not registered
    User -> MicrosoftIdentityLibrary : inputs e-mail, password and password confirmation


    alt E-mail is invalid
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'The Email field is not a valid e-mail address'.

    else Password is less than 6 or greater than 100 characters
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'The password must be at least 6 and at max 100 chracters long.'

    else Password and confirmation password do not match
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'The password and confirmation password do not match'

    end

    User -> MicrosoftIdentityLibrary : User clicks register button


    alt Password does not contain at least one symbol
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'Passwords must have at least one non alphanumeric character'.

    else Passord does not contain at least one digit
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'Passwords must have at least one digit ('0'-'9')'.

    else Password does not contain uppercase letters
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'Passwords must have at least one uppercase ('A'-'Z').'

    else Password does not contain 4 different characters
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'Passwords must use at least 4 different characters.'

    else E-mail is already in use 
        MicrosoftIdentityLibrary -> MicrosoftIdentityLibrary : Display 'Username 'E-mail' is already taken.'

    end

    MicrosoftIdentityLibrary -> Database : Creates user with e-mail and password

end


MicrosoftIdentityLibrary -> HomeController : returns action
deactivate MicrosoftIdentityLibrary

activate HomeController
HomeController -> HomeController : Create home view
deactivate HomeController

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
actor "User" as User
rectangle "LoginPartialView" as LoginPartialView
rectangle "MicrosoftIdentityLibrary" as MicrosoftIdentityLibrary
rectangle "HomeController" as HomeController
database "StudieTipsDB" as StudieTipsDB

User -> LoginPartialView: clicks on "Register"
activate LoginPartialView
LoginPartialView -> MicrosoftIdentityLibrary: sends action
activate MicrosoftIdentityLibrary
MicrosoftIdentityLibrary: Creates RegisterView
deactivate MicrosoftIdentityLibrary

loop [While user not registered]
  User -> MicrosoftIdentityLibrary: inputs e-mail, password and password confirmation
  activate MicrosoftIdentityLibrary
  alt [E-mail is invalid]
    MicrosoftIdentityLibrary: Display 'The Email field is not a valid e-mail address'.
  else [Password is less than 6 or greater than 100 characters]
    MicrosoftIdentityLibrary: Display 'The password must be at least 6 and at max 100 chracters long.'
  else [Password and confirmation password do not match]
    MicrosoftIdentityLibrary: Display 'The password and confirmation password do not match'
  end
  deactivate MicrosoftIdentityLibrary

  User -> MicrosoftIdentityLibrary: User clicks register button
  activate MicrosoftIdentityLibrary
  alt [Password does not contain at least one symbol]
    MicrosoftIdentityLibrary: Display 'Passwords must have at least one non alphanumeric character'.
  else [Passord does not contain at least one digit]
    MicrosoftIdentityLibrary: Display 'Passwords must have at least one digit ('0'-'9')'.
  else [Password does not contain uppercase letters]
    MicrosoftIdentityLibrary: Display 'Passwords must have at least one uppercase ('A'-'Z').
  else [Password does not contain 4 different characters]
    MicrosoftIdentityLibrary: Display 'Passwords must use at least 4 different characters.'
  else [E-mail is already in use]
    MicrosoftIdentityLibrary: Display 'Username 'E-mail' is already taken.'
  end
  deactivate MicrosoftIdentityLibrary

  MicrosoftIdentityLibrary -> StudieTipsDB: Creates user with e-mail and password
  activate StudieTipsDB
  deactivate StudieTipsDB
end

MicrosoftIdentityLibrary -> HomeController: returns action
activate HomeController
HomeController: Create home view
deactivate HomeController

@enduml
```

#### `60a722852250f7770ba344356915d9dea211674b` — compile_fail (sequence, tier 3)

- CSR: `Error line 9 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/60a722852250f7770ba344356915d9dea211674b.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=10 F1=0.000; missed: message
- chrF++: 58.98
- Files: GT `data/puml_files/60a722852250f7770ba344356915d9dea211674b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/60a722852250f7770ba344356915d9dea211674b.puml` (yes) · input `data/puml_images_1568/60a722852250f7770ba344356915d9dea211674b.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/60a722852250f7770ba344356915d9dea211674b.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 60a722852250f7770ba344356915d9dea211674b
' Original Path: /sequence - analysis/rollcall/updateRollCall.plantuml
' Source: World of Code

@startuml

actor ": Teacher"
boundary ": UpdateRollCallForm"
control ": StudentController"
entity ": RollCall"
entity ": ClassroomMember"

activate ": Teacher"

": Teacher" -> ": UpdateRollCallForm": 1 // request update roll call
activate ": UpdateRollCallForm"
": UpdateRollCallForm" -> ": StudentController": 2 // request update roll call
activate ": StudentController"
": StudentController" -> ": ClassroomMember": 3 // checking information is valid
activate ": ClassroomMember"
alt information is valid
    ": ClassroomMember" -->> ": StudentController": 5 // Information is valid
    ": StudentController" ->> ": RollCall": 6 // Request make roll call
    activate ": RollCall"
    ": StudentController" -->> ": UpdateRollCallForm": 8 // Roll call update done
    deactivate ": RollCall"
    ": UpdateRollCallForm" -->> ": Teacher": 9 // Roll call done
else information is not valid
    ": ClassroomMember" -->> ": StudentController": 5.1 // Information is not valid
    deactivate ": ClassroomMember"
    ": StudentController" -->> ": UpdateRollCallForm": 5.2 // Roll call update failed
    deactivate ": StudentController"
    ": UpdateRollCallForm" -->> ": Teacher": 5.3 // Roll call failed,\n check information again
end

deactivate ": UpdateRollCallForm"
deactivate ": Teacher"



@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
actor "Teacher" as teacher
interface "UpdateRollCallForm" as updateForm
boundary "StudentController" as studentController
boundary "RollCall" as rollCall
boundary "ClassroomMember" as classroomMember

activate teacher
activate updateForm
activate studentController
activate rollCall
activate classroomMember

teacher -> updateForm : 1 // request update roll call
updateForm -> studentController : 2 // request update roll call
studentController -> classroomMember : 3 // checking information is valid

alt [information is valid]
classroomMember --> studentController : 5 // Information is valid
studentController -> rollCall : 6 // Request make roll call
activate rollCall
deactivate rollCall
rollCall --> studentController : 8 // Roll call update done
studentController --> updateForm : 8 // Roll call update done
updateForm --> teacher : 9 // Roll call done
deactivate updateForm
deactivate teacher
else [information is not valid]
classroomMember --> studentController : 5.1 // Information is not valid
studentController --> updateForm : 5.2 // Roll call update failed
updateForm --> teacher : 5.3 // Roll call failed, check information again
deactivate updateForm
deactivate teacher
end

deactivate studentController
deactivate classroomMember
@enduml
```

#### `66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8` — compile_fail (sequence, tier 4)

- CSR: `Error line 7 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8.puml`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=20 F1=0.000; missed: message
- chrF++: 48.81
- Files: GT `data/puml_files/66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8.puml` (yes) · input `data/puml_images_1568/66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 66a6dbf50cde09d030b4e2d1fa36a2c31fe129a8
' Original Path: /searchProduct.puml
' Source: World of Code

@startuml
 
' style tweaks to make the diagram a little more readable
skinparam {
	Style strictuml
	RoundCorner 8
 
	Sequence {
		' make activations yellow too
		LifeLineBackgroundColor #FDFDCD
 
		' make stereotypes less ugly
		Stereotype {
			Font {
				Size 11
				Style plain
			}
		}
	}
 
	DatabaseBorderColor #A80036
 
}
 
title Search for Products by ID (using DB dao)
 
actor User as user
participant "Administration" as main << main >>
participant "MainMenu" as menu << frame >>
participant "ProductReportDialog" as dialog << dialog >>
participant "ProductDatabaseDAO" as dao << ProductDAO >>
participant "SimpleListModel\n:model" as model
database "Database" as db
 
main++
create menu
main -> menu : « construct »
 
 
user ->> menu : clicks 'View Products'
menu++
 
 
create dialog
menu -> dialog++ : « construct »
 
 
create dao
dialog -> dao : « construct »
 
dialog -> dao++ : getProducts()
dao -> db++ : select * from product
return ResultSet
dao -> dao : reconstruct products\nfrom ResultSet
return products
 
create model
dialog -> model : « construct »
dialog -> model++ : updateItems(products)
model--
dialog -> dialog : lstProducts.setModel(model)
 
note left : products now\nvisible to user

user -> dialog : enters product id into search bar
dialog -> dialog : txtId.getText : id
user -> dialog : clicks "Search"

dialog -> dao : search(id)

dao -> db++ : select * from product where product_id = id
return product

dialog -> model++ : updateItems(product)
dialog -> dialog : lstProducts.getModel(model)
model--
```

Prediction PlantUML:
```plantuml
@startuml
title Search for Products by ID (using DB dao)

actor "User" as User
rectangle "«main» Administration" as Administration
frame "«frame» MainMenu" as MainMenu
dialog "«dialog» ProductReportDialog" as ProductReportDialog
database "Database" as Database
rectangle "«ProductDAO» ProductDatabaseDAO" as ProductDatabaseDAO
rectangle "SimpleListModel :model" as SimpleListModel

User -> Administration : clicks 'View Products'
Administration -> MainMenu : «construct»
MainMenu -> ProductReportDialog : «construct»
ProductReportDialog -> ProductDatabaseDAO : «construct»
ProductDatabaseDAO -> Database : getProducts()
Database --> ProductDatabaseDAO : select * from product
ProductDatabaseDAO --> ProductReportDialog : ResultSet
activate ProductDatabaseDAO
ProductDatabaseDAO -> ProductDatabaseDAO : reconstruct products from ResultSet
ProductDatabaseDAO --> ProductReportDialog : products
deactivate ProductDatabaseDAO

ProductReportDialog -> SimpleListModel : «construct»
ProductReportDialog -> SimpleListModel : updateItems(products)
activate SimpleListModel
deactivate SimpleListModel

ProductReportDialog -> ProductReportDialog : IstProducts.setModel(model)
activate ProductReportDialog
deactivate ProductReportDialog

note right of ProductReportDialog
  products now visible to user
end note

User -> ProductReportDialog : enters product id into search bar
ProductReportDialog -> ProductReportDialog : txtId.getText : id
activate ProductReportDialog
deactivate ProductReportDialog

User -> ProductReportDialog : clicks "Search"
ProductReportDialog -> ProductDatabaseDAO : search(id)
activate ProductDatabaseDAO
ProductDatabaseDAO -> Database : select * from product where product_id = id
Database --> ProductDatabaseDAO : product
deactivate ProductDatabaseDAO

ProductReportDialog -> SimpleListModel : updateItems(product)
activate SimpleListModel
deactivate SimpleListModel

ProductReportDialog -> ProductReportDialog : IstProducts.getModel(model)
activate ProductReportDialog
deactivate ProductReportDialog

note right of ProductReportDialog
  only searched product now visible to user
end note

@enduml
```

#### `6b9fdfa3aa1c44fe114ad772eb3bd7cf0809f79c` — compile_fail (sequence, tier 2)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=11 F1=0.000; missed: message
- chrF++: 1.21
- Files: GT `data/puml_files/6b9fdfa3aa1c44fe114ad772eb3bd7cf0809f79c.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/6b9fdfa3aa1c44fe114ad772eb3bd7cf0809f79c.puml` (yes) · input `data/puml_images_1568/6b9fdfa3aa1c44fe114ad772eb3bd7cf0809f79c.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/6b9fdfa3aa1c44fe114ad772eb3bd7cf0809f79c.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 6b9fdfa3aa1c44fe114ad772eb3bd7cf0809f79c
' Original Path: /Scenario /doc/UML/DeleteClass.uml
' Source: World of Code

@startuml

actor User
entity UI
entity Application
database Database

User -> UI: go to Tables page
UI -> Application: Dump Tables
Application -> Database: Dump Tables
Application <- Database: Tables
UI <- Application: Tables
User -> UI: Click "Delete" on a Class
UI -> Application: DeleteClass(ClassID)
Application -> Database: DeleteClass(ClassID)
Application <- Database: Success
UI <- Application: Success
UI -> UI: Update table

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
' Define the style for the diagram
skinparam sequenceMessageLineColor black
skinparam sequenceMessageLineColor black
skinparam sequenceMessageLineWidth 1
skinparam sequenceMessageFontName "Helvetica"
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontWeight normal
skinparam sequenceMessageFontSlant normal
skinparam sequenceMessageFontFamily "Helvetica"
skinparam sequenceMessageFontColor black
skinparam sequenceMessageFontSize 12
```

#### `6e0e78745d3694cd2ea39f463c45e5cf6dc644c4` — compile_fail (sequence, tier 2)

- CSR: `Error line 4 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/6e0e78745d3694cd2ea39f463c45e5cf6dc644c4.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=9 F1=0.000; missed: message
- chrF++: 62.81
- Files: GT `data/puml_files/6e0e78745d3694cd2ea39f463c45e5cf6dc644c4.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/6e0e78745d3694cd2ea39f463c45e5cf6dc644c4.puml` (yes) · input `data/puml_images_1568/6e0e78745d3694cd2ea39f463c45e5cf6dc644c4.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/6e0e78745d3694cd2ea39f463c45e5cf6dc644c4.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 6e0e78745d3694cd2ea39f463c45e5cf6dc644c4
' Original Path: /rapport/img/sequence_click2call.uml
' Source: World of Code

@startuml

actor Caller as caller
participant ServeurDynamease as dyn
participant Asterisk as ast
actor CalledDynamease as called

caller -> dyn : clickButton

activate dyn

dyn -> dyn : Verification
dyn -> ast : Create conference room
activate ast
ast --> dyn
dyn --> caller : Ask_to_call_the_trunk_number
dyn --> called : Ask_to_call_the_trunk_number_with information_of_the _caller

deactivate dyn

caller -> ast : Call_With_Trunk_Number
called -> ast : Call_With_Trunk_Number

...When the communication is ending...
ast --> dyn : communication ending
deactivate ast


@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
actor Caller
participant "ServeurDynamease" as SD
participant "Asterisk" as AS
actor CalledDynamease

Caller -> SD : clickButton
activate SD
SD -> SD : Verification
SD -> AS : Create conference room
activate AS
SD --> Caller : Ask_to_call_the_trunk_number
SD --> AS : Ask_to_call_the_trunk_number_with information_of_the_caller
Caller -> AS : Call_With_Trunk_Number
AS -> CalledDynamease : Call_With_Trunk_Number
CalledDynamease -> AS : Call_With_Trunk_Number
AS --> SD : communication ending
deactivate AS
deactivate SD

note right of SD : When the communication is ending
note left of CalledDynamease : CalledDynamease
note left of Caller : Caller

@enduml
```

#### `81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583` — compile_fail (class, tier 3)

- CSR: `Error line 9 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=3 F1=0.000; missed: dependency, association
- chrF++: 24.57
- Files: GT `data/puml_files/81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583.puml` (yes) · input `data/puml_images_1568/81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 81687d3f4b7ac594ccb96e9e3d6ca7ce22a1e583
' Original Path: /DDI-CDI/DDI-CDI_2022-07-20b/doc/_rst/DDICDILibrary/Classes/DataDescription/Components/ComponentPosition.pu
' Source: World of Code

/'
PLEASE DO NOT EDIT THIS CODE!
 This code was generated by the Eclipse Acceleo module UCMIS M2T.
 Target language is 'Plantuml' generated on the basis of the model 'DDICDIModels'.
'/


@startuml
!pragma ratio 0.5625
' HD display aspect ratio 16:9
' hyperlinkColor and pathHoverColor do not seem to work with class diagrams
' working approach: colors per item
' default font size for class names is 14

hide circle
hide empty members
scale 0.9

skinparam {
  ArrowThickness 1.5
  MinClassWidth 150
}

skinparam legend {
  BackgroundColor white
  FontSize 10
}

skinparam note {
  BackgroundColor white
}

skinparam class {
  ArrowColor #404040
  BorderColor #404040
}

skinparam package {
  FontColor lightgrey
  BorderColor lightgrey
}

title <size:20>UML Diagram: Class ComponentPosition in Context\n
footer \n\nDDI Cross Domain Integration (DDI-CDI) \
  1.0 - Components::ComponentPosition

legend top left
**Hints**
<color:grey>- Move the mouse cursor over a name to see more information.
<color:grey>- Click on a name to go to the corresponding page.
endlegend

' Core class of diagram
class DDICDIModels::DDICDILibrary::Classes::DataDescription::Components::ComponentPosition as "<size:10>Components::\n<color:black>ComponentPosition" #FFD700 {
  value : Integer
}

' Class definitions for associated classes without superclass (might have also an association)
' This would be too many constraints for Graphviz. 
together {
  class DDICDIModels::DDICDILibrary::Classes::DataDescription::DataStructure as "<size:10>DataDescription::\n<color:blue>DataStructure" [[../DDICDILibrary/Classes/DataDescription/DataStructure.html#super-class-hierarchy-generalization{ <U+2015> DataStructure:\nData organization based on reusable data structure components.}]]
  class DDICDIModels::DDICDILibrary::Classes::DataDescription::Components::DataStructureComponent as "<size:10>Components::\n<color:blue>DataStructureComponent" [[../DDICDILibrary/Classes/DataDescription/Components/DataStructureComponent.html#super-class-hierarchy-generalization{ <U+2015> DataStructureComponent:\nRole given to a represented variable in the context of a data structure.}]]
}

' Class definitions for suppliers of abstractions
together {
  abstract class DDICDIModels::DesignPatterns::CollectionsPattern::Position as "<size:10>CollectionsPattern::\n<color:blue>Position" [[../DesignPatterns/CollectionsPattern/Position.html#super-class-hierarchy-generalization{ <U+2015> Position:\nPosition of the associated member within the associated List.}]]
}

' Rest of class definitions, without associated classes of core class and abstraction supplier classes



' Associations
DDICDIModels::DDICDILibrary::Classes::DataDescription::Components::ComponentPosition <-[#grey]- DDICDIModels::DDICDILibrary::Classes::DataDescription::DataStructure [[{ <U+2015> has:\n}]] : has
DDICDIModels::DDICDILibrary::Classes::DataDescription::Components::ComponentPosition -[#grey]-> DDICDIModels::DDICDILibrary::Classes::DataDescription::Components::DataStructureComponent [[{ <U+2015> indexes:\n}]] : indexes
```

Prediction PlantUML:
```plantuml
@startuml
title UML Diagram: Class ComponentPosition in Context

' Hints box
note left of Components::ComponentPosition
  **Hints**
  - Move the mouse cursor over a name to see more information.
  - Click on a name to go to the corresponding page.
end note

' Main class: ComponentPosition
class Components::ComponentPosition {
  value : Integer
}

' Related classes
class DataDescription::DataStructure
class Components::DataStructureComponent
class CollectionsPattern::Position

' Relationships
DataDescription::DataStructure --> Components::ComponentPosition : has
Components::ComponentPosition --> Components::DataStructureComponent : indexes
Components::ComponentPosition ..> CollectionsPattern::Position : «Refine»

' Footer note
note bottom
  DDI Cross Domain Integration (DDI-CDI) 1.0 – Components::ComponentPosition
end note

@enduml
```

#### `a5f6d7abf8c4651c51308f5c1487e94e5d00ec90` — compile_fail (class, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 0.56
- Files: GT `data/puml_files/a5f6d7abf8c4651c51308f5c1487e94e5d00ec90.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/a5f6d7abf8c4651c51308f5c1487e94e5d00ec90.puml` (yes) · input `data/puml_images_1568/a5f6d7abf8c4651c51308f5c1487e94e5d00ec90.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/a5f6d7abf8c4651c51308f5c1487e94e5d00ec90.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a5f6d7abf8c4651c51308f5c1487e94e5d00ec90
' Original Path: /Livrables/Diagrammes/Composants/UML/Client.plantuml
' Source: World of Code

@startuml
class Client {
    + appetizer : Command <<get>> <<set>>
    + dish : Command <<get>> <<set>>
    + desert : Command <<get>> <<set>>
    + CurrentCommand : Command <<get>> <<set>>
}
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_TITLE_TEXT
!define CLASS_TITLE_TEXT_COLOR
!define CLASS_TITLE_TEXT_SIZE
!define CLASS_TITLE_TEXT_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE
!define CLASS_TITLE_TEXT_UNDERLINE_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_COLOR
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_STYLE
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_WIDTH
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_HEIGHT
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_OFFSET
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_PADDING
!define CLASS_TITLE_TEXT_UNDERLINE_BORDER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER_CORNER
```

#### `a7d13afb8d9821c057a30fc94c8cb6020bd2e826` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=8 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=9 F1=0.000; missed: inheritance, composition, aggregation, association
- chrF++: 1.30
- Files: GT `data/puml_files/a7d13afb8d9821c057a30fc94c8cb6020bd2e826.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/a7d13afb8d9821c057a30fc94c8cb6020bd2e826.puml` (yes) · input `data/puml_images_1568/a7d13afb8d9821c057a30fc94c8cb6020bd2e826.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/a7d13afb8d9821c057a30fc94c8cb6020bd2e826.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a7d13afb8d9821c057a30fc94c8cb6020bd2e826
' Original Path: /Lab6_Proxy/Diagrams/Class diagram.puml
' Source: World of Code

@startuml

Sensor -|> Component
Actuator -|> Component
ComponentStore -|> IComponent
Proxy -|> IComponent
Program --* Proxy
Sensor --o ComponentContext
Actuator --o ComponentContext
Component -- ComponentStore
ComponentStore -- ComponentContext

class ComponentContext {
    Components: List<Component>
    
    ComponentContext()
}

class Component {
    id: int
    name: string
    date: DateTime
    
    Component(id int, name string, date DateTime)
    GetFunction()
}

class Sensor {
    TypesOfSensors: List<string>
    TypesOfSignal: List<string>
    TypeOfSensor: string
    TypeOfSignal: string
    
    Component(id int, name string, date DateTime, string typeOfSensor, string typeOfSignal)
    GetFunction()
}

class Actuator {
    TypesOfActuators: List<string>
    StatusesOfActuators: List<string>
    TypeOfActuator: string
    StatusOfActuator: string
    
    Component(id int, name string, date DateTime, string typeOfActuator, string statusOfActuator)
    GetFunction()
}

class IComponent {
    
    GetComponent(id int) Component
}

class Proxy {
    components: List<Component>
    componentStore: ComponentStore
    
    Proxy()
    GetComponent(id int) Component
}

class ComponentStore {
    container: ComponentContext
    
    ComponentStore()
    GetComponent(id int) Component
}

class Program {
 
    Main(args[] string)
}


@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_TITLE_ICON
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
```

#### `cff9c8f0856b2a71cec7a566494746db29317e7c` — compile_fail (sequence, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 1.22
- Files: GT `data/puml_files/cff9c8f0856b2a71cec7a566494746db29317e7c.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/cff9c8f0856b2a71cec7a566494746db29317e7c.puml` (yes) · input `data/puml_images_1568/cff9c8f0856b2a71cec7a566494746db29317e7c.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/cff9c8f0856b2a71cec7a566494746db29317e7c.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: cff9c8f0856b2a71cec7a566494746db29317e7c
' Original Path: /src/test/UpdateOrder.puml
' Source: World of Code

@startuml
AppUser -> Webserver: Update https://xxx/orders/{OrderId}?uuid=123
Webserver --> OrderController: OrderId
OrderController --> OrderService: OrderId
OrderService --> OrderDao: OrderId
OrderDao --> OrderService: OrderPO
OrderService --> OrderController: OrderVO
OrderController --> Webserver: OrderVO
AppUser <-- Webserver
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
left to right direction
skinparam sequenceMessageAlign center
skinparam sequenceMessageFontName Courier
skinparam sequenceMessageFontSize 12
skinparam sequenceMessageFontStyle plain
skinparam sequenceMessageFontColor black
skinparam sequenceMessageBackgroundColor white
skinparam sequenceMessageBorderColor black
skinparam sequenceMessageBorderWidth 1
skinparam sequenceMessageBorderRadius 5
skinparam sequenceMessageBorderDashArray 0
skinparam sequenceMessageBorderDashStyle solid
skinparam sequenceMessageBorderDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
skinparam sequenceMessageBorderDashPatternHeight 0
skinparam sequenceMessageBorderDashPatternColor black
skinparam sequenceMessageBorderDashPatternStyle solid
skinparam sequenceMessageBorderDashPatternDashArray 0
skinparam sequenceMessageBorderDashPatternDashStyle solid
skinparam sequenceMessageBorderDashPatternDashPattern 0
skinparam sequenceMessageBorderDashPatternLength 0
skinparam sequenceMessageBorderDashPatternWidth 0
```

#### `d23836a3fe74fedc9a9718a3a92792087c41a87c` — compile_fail (class, tier 3)

- CSR: `Error line 2 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/d23836a3fe74fedc9a9718a3a92792087c41a87c.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: inheritance, aggregation, dependency, association
- chrF++: 43.54
- Files: GT `data/puml_files/d23836a3fe74fedc9a9718a3a92792087c41a87c.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/d23836a3fe74fedc9a9718a3a92792087c41a87c.puml` (yes) · input `data/puml_images_1568/d23836a3fe74fedc9a9718a3a92792087c41a87c.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/d23836a3fe74fedc9a9718a3a92792087c41a87c.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: d23836a3fe74fedc9a9718a3a92792087c41a87c
' Original Path: /uml-class/util/gui/github.weichware10.util.gui.puml
' Source: World of Code

@startuml
title github.weichware10.util.gui

package github.weichware10.util.gui {

    ' -=- classes (github.weichware10.util.gui) -=-
    class github.weichware10.util.gui.AbsScene {
        ' --- values (github.weichware10.util.gui.AbsScene) ---

        ' --- methods (github.weichware10.util.gui.AbsScene) ---
        {static}+ InitResult initialize(URL fxml)
        {static}+ void setMenuBar(MenuBar menuBar, Parent root)
        {static}+ InitResult start(Stage primaryStage, URL fxml, Parent root, AbsSceneController controller, String title, MenuBar menuBar, Integer width, Integer height, String icon)
    }
    class github.weichware10.util.gui.AbsScene$InitResult {
        ' --- values (github.weichware10.util.gui.AbsScene$InitResult) ---

        ' --- fields (github.weichware10.util.gui.AbsScene$InitResult) ---
        + Parent root
        + AbsSceneController controller

        ' --- methods (github.weichware10.util.gui.AbsScene$InitResult) ---
        #  InitResult(Parent root, AbsSceneController controller)
    }
    github.weichware10.util.gui.AbsScene +-- github.weichware10.util.gui.AbsScene$InitResult

    class github.weichware10.util.gui.AbsSceneController {
        ' --- values (github.weichware10.util.gui.AbsSceneController) ---

        ' --- fields (github.weichware10.util.gui.AbsSceneController) ---
        # ResourceBundle resources
        # URL location

        ' --- methods (github.weichware10.util.gui.AbsSceneController) ---
        {abstract}# void initialize()
    }

    class github.weichware10.util.gui.Log {
        ' --- values (github.weichware10.util.gui.Log) ---

        ' --- fields (github.weichware10.util.gui.Log) ---
        {static}- Stage logStage
        {static}- Parent root
        {static}- SimpleBooleanProperty visibleProperty
        {static}+ ObservableBooleanValue visible

        ' --- methods (github.weichware10.util.gui.Log) ---
        {static}+ void start(String icon)
        {static}+ boolean isVisible()
        {static}+ void show()
        {static}+ void hide()
        {static}+ void close()
        {static}+ void log(String content, String type)
    }

    class github.weichware10.util.gui.LogController {
        ' --- values (github.weichware10.util.gui.LogController) ---

        ' --- fields (github.weichware10.util.gui.LogController) ---
        - ResourceBundle resources
        - URL location
        - TextField logInput
        - TextArea logArea
        - Pane logPane
        - MenuButton logMenuButton

        ' --- methods (github.weichware10.util.gui.LogController) ---
        # void initialize()
        ~ void setLogType(ActionEvent event)
        ~ void inputKeyPress(KeyEvent event)
        ~ void log()
    }

}

' autogenerated field links, may be faulty.
```

Prediction PlantUML:
```plantuml
@startuml
!theme base
title github.weichware10.util.gui

package "github" {
  package "weichware10" {
    package "util" {
      package "gui" {
        class "AbsScene" {
          +InitResult initialize(URL fxml)
          +void setMenuBar(MenuBar menuBar, Parent root)
          +InitResult start(Stage primaryStage, URL fxml, Parent root, AbsSceneController controller, String title, MenuBar menuBar, Integer width, Integer height, String icon)
        }

        class "AbsScene$InitResult" {
          -Parent root
          -AbsSceneController controller
          +InitResult(Parent root, AbsSceneController controller)
        }

        class "AbsSceneController" {
          +ResourceBundle resources
          +URL location
          +void initialize()
        }

        class "Log" {
          -Stage logStage
          -Parent root
          -SimpleBooleanProperty visibleProperty
          -ObservableBooleanValue visible
          +void start(String icon)
          +boolean isVisible()
          +void show()
          +void hide()
          +void close()
          +void log(String content, String type)
        }

        class "LogController" {
          -ResourceBundle resources
          -URL location
          -TextField logInput
          -TextArea logArea
          -Pane logPane
          -MenuButton logMenuButton
          +void initialize()
          +void setLogType(ActionEvent event)
          +void inputKeyPress(KeyEvent event)
          +void log()
        }

        "AbsScene" --o "AbsScene$InitResult" : composition
        "AbsScene" <|-- "Log" : inheritance
        "AbsScene$InitResult" --o "AbsSceneController" : aggregation
        "LogController" --|> "AbsSceneController" : inheritance
        "LogController" ..> "Log" : "Verbindung über Bindings"
      }
    }
  }
}

@enduml
```

#### `d794b09cb87451a09b2848a1443e887f529f8a93` — compile_fail (sequence, tier 4)

- CSR: `Error line 11 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/d794b09cb87451a09b2848a1443e887f529f8a93.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=21 F1=0.000; missed: message
- chrF++: 43.08
- Files: GT `data/puml_files/d794b09cb87451a09b2848a1443e887f529f8a93.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/d794b09cb87451a09b2848a1443e887f529f8a93.puml` (yes) · input `data/puml_images_1568/d794b09cb87451a09b2848a1443e887f529f8a93.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/d794b09cb87451a09b2848a1443e887f529f8a93.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: d794b09cb87451a09b2848a1443e887f529f8a93
' Original Path: /reference-code/lambda/cm-premembers-setting/SequenceDiagram/BATCH/Batch_組織_プロジェクト遅延削除.pu
' Source: World of Code

@startuml
title [組織_プロジェクト遅延削除]
hide footbox

participant タスクコントローラ as controller <<lambda>> #violet
participant プロジェクト削除バッチ as batch_prj_delete <<lambda>> #violet
database 組織タスクキュー as queue_org_task <<sqs>> #gold
database 組織タスク as table_org_task <<dynamodb>> #royalblue
database プロジェクト as table_projects <<dynamodb>> #royalblue
database AWSアカウント連携 as table_awsac_coops <<dynamodb>> #royalblue

box "レポート"
database レポート as table_reports <<dynamodb>> #royalblue
database レポートジョブ履歴 as table_report_joblog <<dynamodb>> #royalblue
database レポートストレージ as storage <<s3>> #crimson
end box

controller ->> batch_prj_delete :invoke (InvocationType='Event')
note right :タスクID、メッセージのメッセージIDと受信ハンドルを渡す
activate batch_prj_delete
    batch_prj_delete -> table_org_task :query
    note right :タスクIDをキーとしてタスク情報を取得
    table_org_task --> batch_prj_delete
    alt ステータス=0（待機中）
        batch_prj_delete -> table_org_task :更新
        note right :タスクのステータスを1（実行中）に更新（更新条件：ステータスが0）
        table_org_task --> batch_prj_delete
        |||
    else ステータス=1（実行中）
        note over batch_prj_delete: 処理終了
    else ステータス=2（完了）
        note over batch_prj_delete: 処理終了
    else ステータス=-1（エラー）、かつリトライ回数=最大リトライ回数
        note over batch_prj_delete: 処理終了
    else ステータス=-1（エラー）、かつリトライ回数<最大リトライ回数
        batch_prj_delete -> table_org_task :更新
        note right :タスクのステータスを1（実行中）、リトライ回数+1に更新（更新条件：ステータスが-1）
        table_org_task --> batch_prj_delete
        |||
    end
    |||
    batch_prj_delete -> batch_prj_delete :タスク情報から処理対象（プロジェクトID）を取得
    group プロジェクト削除処理
        batch_prj_delete -> table_awsac_coops :レコード削除
        note right :親プロジェクトがプロジェクトIDに該当するAWSアカウント連携を削除
        table_awsac_coops --> batch_prj_delete
        batch_prj_delete -> table_reports :query
        note right :親プロジェクトがプロジェクトIDに該当するレポート情報を取得
        table_reports --> batch_prj_delete
        |||
        loop , レポート数
            batch_prj_delete -> batch_prj_delete :レポートIDを取得
            batch_prj_delete -> table_reports :レポート情報を削除
            table_reports --> batch_prj_delete
            |||
            ref over batch_prj_delete, storage :レポート削除処理
            |||
        end
        |||
    end
    alt 削除処理成功
        batch_prj_delete -> table_org_task :更新
        note right :タスクのステータスを2（完了）に更新（更新条件：ステータスが1）
        table_org_task --> batch_prj_delete
        batch_prj_delete -> queue_org_task :処理済みのメッセージを削除
        queue_org_task --> batch_prj_delete
        |||
    else 削除処理エラー
        batch_prj_delete -> table_org_task :更新
        note right :タスクのステータスを-1（エラー）に更新（更新条件：ステータスが1）
        table_org_task --> batch_prj_delete
        |||
    end
deactivate batch_prj_delete
|||

```

Prediction PlantUML (truncated):
```plantuml
@startuml
left to right direction
skinparam sequenceMessageAlign center
skinparam note {
  BackgroundColor #FFFFE0
  BorderColor #FFD700
}

title [組織_プロジェクト遅延削除]

participant "«lambda» タスクコントローラ" as taskController
participant "«lambda» プロジェクト削除バッチ" as projectBatch
participant "«sqs» 組織タスクキュー" as taskQueue
participant "«dynamodb» 組織タスク" as orgTask
participant "«dynamodb» プロジェクト" as project
participant "«dynamodb» AWSアカウント連携" as awsAccount
participant "«dynamodb» レポート" as report
participant "«dynamodb» レポートジョブ履歴" as reportJobHistory
participant "«s3» レポートストレージ" as reportStorage

taskController -> projectBatch: invoke (InvocationType='Event')
activate projectBatch

note right of projectBatch
  タスクID、メッセージのメッセージIDと受信ハンドルを渡す
end note

projectBatch -> orgTask: query
note right of orgTask
  タスクIDをキーとしてタスク情報を取得
end note

alt [ステータス=0（待機中）]
  projectBatch -> orgTask: 更新
  note right of orgTask
    タスクのステータスを1（実行中）に更新（更新条件：ステータスが0）
  end note
  orgTask --> projectBatch: ...
else [ステータス=1（実行中）]
  note right of projectBatch
    処理終了
  end note
else [ステータス=2（完了）]
  note right of projectBatch
    処理終了
  end note
else [ステータス=-1（エラー）、かつリトライ回数=最大リトライ回数]
  note right of projectBatch
    処理終了
  end note
else [ステータス=-1（エラー）、かつリトライ回数<最大リトライ回数]
  projectBatch -> orgTask: 更新
  note right of orgTask
    タスクのステータスを1（実行中）、リトライ回数+1に更新（更新条件：ステータスが-1）
  end note
  orgTask --> projectBatch: ...
end

deactivate projectBatch

projectBatch -> projectBatch: タスク情報から処理対象（プロジェクトID）を取得

alt [削除処理成功]
  projectBatch -> projectBatch: プロジェクト削除処理
  activate projectBatch

  projectBatch -> awsAccount: レコード削除
  note right of awsAccount
    親プロジェクトがプロジェクトIDに該当するAWSアカウント連携を削除
  end note
  awsAccount --> projectBatch: ...

  projectBatch -> report: query
  note right of report
    親プロジェクトがプロジェクトIDに該当するレポート情報を取得
  end note
  report --> projectBatch: ...

  loop [レポート数]
    projectBatch -> projectBatch: レポートIDを取得
```

#### `e422bd4ed1591e46fadbabe9fb6cd85de4891749` — compile_fail (class, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=1 F1=0.000; missed: inheritance
- chrF++: 0.61
- Files: GT `data/puml_files/e422bd4ed1591e46fadbabe9fb6cd85de4891749.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/e422bd4ed1591e46fadbabe9fb6cd85de4891749.puml` (yes) · input `data/puml_images_1568/e422bd4ed1591e46fadbabe9fb6cd85de4891749.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/e422bd4ed1591e46fadbabe9fb6cd85de4891749.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: e422bd4ed1591e46fadbabe9fb6cd85de4891749
' Original Path: /WasteWatcherApp/WasteWatcherApp/UML/Waste/Persistance/LocalWasteStorage.puml
' Source: World of Code

@startuml
class LocalWasteStorage {
    + GetData(productId:string) : Task<WasteCollection>
    + <<async>> SaveData(productId:string, wasteCollection:WasteCollection) : Task
    RemoveWasteValue(wasteKey:string) : void
    SetWasteValue(wasteKey:string, value:int) : void
    GetWasteValue(wasteKey:string) : int?
    GetWasteValue(productId:string, wasteType:WasteType) : WasteAmount
}
IWasteStore <|-- LocalWasteStorage
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
!define CLASS_BODY
!define CLASS_HEADER
!define CLASS_TITLE
!define CLASS_ICON
!define CLASS_STEREOTYPE
!define CLASS_VISIBILITY
!define CLASS_TYPE
!define CLASS_NAME
!define CLASS_METHODS
!define CLASS_FIELDS
!define CLASS_CONSTANTS
!define CLASS_OPERATORS
!define CLASS_EXCEPTIONS
!define CLASS_DEPENDENCIES
!define CLASS_IMPLEMENTATIONS
!define CLASS_ABSTRACT
!define CLASS_FINAL
!define CLASS_INTERFACE
!define CLASS_ENUM
!define CLASS_ANONYMOUS
!define CLASS_LOCAL
!define CLASS_STATIC
!define CLASS_TRANSIENT
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
!define CLASS_VOLATILE
!define CLASS_SYNCHRONIZED
```

#### `eff76e684b657103a5b9a074acbaf89a607557e1` — compile_fail (class, tier 2)

- CSR: `Error line 11 in file: data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/extracted/eff76e684b657103a5b9a074acbaf89a607557e1.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 63.04
- Files: GT `data/puml_files/eff76e684b657103a5b9a074acbaf89a607557e1.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/eff76e684b657103a5b9a074acbaf89a607557e1.puml` (yes) · input `data/puml_images_1568/eff76e684b657103a5b9a074acbaf89a607557e1.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/eff76e684b657103a5b9a074acbaf89a607557e1.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: eff76e684b657103a5b9a074acbaf89a607557e1
' Original Path: /Singleton/singleton.pu
' Source: World of Code

@startuml

note as N1
  Singleton (シングルトン)
  <概要>
  システム内に存在するオブジェクトが1つであることを保証する。
  このパターンでは外部からのオブジェクトを生成を禁止する。
  システムの起動中はオブジェクト1つだけ制限したいときに使う
  <メリット>
  ・オブジェクトが1つしかないことが保証されている
end note

class FileFormatter {
  - singleton : Singleton
  - Singleton()
  + GetInstance() : Singleton
}

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
skinparam noteBackgroundColor #FFFFE0
skinparam noteBorderColor #000000
skinparam noteBorderThickness 1
skinparam classBorderColor #000000
skinparam classBorderThickness 1
skinparam classFontColor #000000
skinparam classBackgroundColor #F5F5F5

note "Singleton (シングルトン)\n\n<概要>\nシステム内に存在するオブジェクトが1つであることを保証する。\nこのパターンでは外部からのオブジェクトを生成を禁止する。\nシステムの起動中はオブジェクト1つだけ制限したいときに使う\n\n<メリット>\n・オブジェクトが1つしかないことが保証されている"
end note

class "FileFormatter" as FileFormatter {
  [C]
  singleton : Singleton
  Singleton()
  +GetInstance() : Singleton
}

@enduml
```

#### outcome: compiled_low_structural

#### `0806d963c5e7a8c33333d600ef648945bd34e3a3` — compiled_low_structural (class, tier 2)

- Element: tp=1 fp=19 fn=0 F1=0.095; type-acc matched=1 correct=0 excluded=0
- Relationship: tp=0 fp=19 fn=0 F1=0.000; extra: association
- chrF++: 60.68
- Files: GT `data/puml_files/0806d963c5e7a8c33333d600ef648945bd34e3a3.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/0806d963c5e7a8c33333d600ef648945bd34e3a3.puml` (yes) · input `data/puml_images_1568/0806d963c5e7a8c33333d600ef648945bd34e3a3.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/0806d963c5e7a8c33333d600ef648945bd34e3a3.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 0806d963c5e7a8c33333d600ef648945bd34e3a3
' Original Path: /puFileV7TMS/Enum_Algorithm18Code.pu
' Source: World of Code

@startuml
skinparam classBackgroundColor<<Codeset>> Azure 
enum Algorithm18Code <<Codeset>> {
UKPT : UKPT
E3DC : DES112CBC
EA2C : AES128CBC
DKP9 : DUKPT2009
UKA1 : UKPTwithAES128
EA5C : AES256CBC
EA9C : AES192CBC
DA12 : AESDUKPT128ECB
DA25 : AESDUKPT256ECB
DA19 : AESDUKPT192ECB
N108 : Nist800-108KeyDerivation
EA2R : AES128CTR
EA9R : AES192CTR
EA5R : AES256CTR
E3DR : DES112CTR
E36C : DES168CBC
E36R : DES168CTR
SD5C : SDE056CBC
}
@enduml 
```

Prediction PlantUML:
```plantuml
@startuml
!define CODESET "Codeset"
!define ALGORITHM18CODE "Algorithm18Code"

class "Algorithm18Code" as A18 {
  <<Codeset>>
  "E" as E
  "UKPT : UKPT" as UKPT
  "E3DC : DES112CBC" as E3DC
  "EA2C : AES128CBC" as EA2C
  "DKP9 : DUKPT2009" as DKP9
  "UKA1 : UKPTwithAES128" as UKA1
  "EA5C : AES256CBC" as EA5C
  "EA9C : AES192CBC" as EA9C
  "DA12 : AESDUKPT128ECB" as DA12
  "DA25 : AESDUKPT256ECB" as DA25
  "DA19 : AESDUKPT192ECB" as DA19
  "N108 : Nist800-108KeyDerivation" as N108
  "EA2R : AES128CTR" as EA2R
  "EA9R : AES192CTR" as EA9R
  "EA5R : AES256CTR" as EA5R
  "E3DR : DES112CTR" as E3DR
  "E36C : DES168CBC" as E36C
  "E36R : DES168CTR" as E36R
  "SD5C : SDE056CBC" as SD5C
}

A18 --> E
A18 --> UKPT
A18 --> E3DC
A18 --> EA2C
A18 --> DKP9
A18 --> UKA1
A18 --> EA5C
A18 --> EA9C
A18 --> DA12
A18 --> DA25
A18 --> DA19
A18 --> N108
A18 --> EA2R
A18 --> EA9R
A18 --> EA5R
A18 --> E3DR
A18 --> E36C
A18 --> E36R
A18 --> SD5C

@enduml
```

#### `08e3416ffa684d3ace7a399d6e46d9e7c513483a` — compiled_low_structural (class, tier 2)

- Element: tp=7 fp=0 fn=0 F1=1.000; type-acc matched=7 correct=4 excluded=0
- Relationship: tp=3 fp=4 fn=4 F1=0.429; missed: inheritance, association; extra: aggregation, dependency
- chrF++: 54.89
- Files: GT `data/puml_files/08e3416ffa684d3ace7a399d6e46d9e7c513483a.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/08e3416ffa684d3ace7a399d6e46d9e7c513483a.puml` (yes) · input `data/puml_images_1568/08e3416ffa684d3ace7a399d6e46d9e7c513483a.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/08e3416ffa684d3ace7a399d6e46d9e7c513483a.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 08e3416ffa684d3ace7a399d6e46d9e7c513483a
' Original Path: /doc/RxContract2.puml
' Source: World of Code

@startuml
interface Publisher<T> {
{abstract} void subscribe(Subscriber<? super T> s)
}
abstract class Flowable<T> {
{abstract} void subscribeActual(Subscriber<? super T> s)
}

interface Subscription<T> {
{abstract}void request(long n)
{abstract}void cancel()
}

Publisher <|.. Flowable

class FlowableFilter<T>
class FlowableMap<T, U>
class FilterSubscriber<T>
class MapSubscriber<T, U>

Flowable <|-- FlowableFilter
Flowable <|-- FlowableMap

FlowableFilter +-- FilterSubscriber
FlowableMap +-- MapSubscriber

Subscription <|.. FilterSubscriber
Subscription <|.. MapSubscriber


@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
' UML diagram for Reactive Streams Publisher/Subscriber pattern

class Publisher {
  <<interface>>
  +subscribe(Subscriber<? super T> s)
}

class Flowable {
  <<abstract>>
  +subscribeActual(Subscriber<? super T> s)
}

class FlowableFilter {
  <<class>>
  +filter()
}

class FilterSubscriber {
  <<class>>
  +onNext(T item)
  +onError(Throwable t)
  +onComplete()
}

class FlowableMap {
  <<class>>
  +map()
}

class MapSubscriber {
  <<class>>
  +onNext(T item)
  +onError(Throwable t)
  +onComplete()
}

class Subscription {
  <<interface>>
  +request(long n)
  +cancel()
}

' Relationships
Publisher <|.. Flowable
Flowable <|-- FlowableFilter
Flowable <|-- FlowableMap
FlowableFilter o-- FilterSubscriber
FlowableMap o-- MapSubscriber
FilterSubscriber ..> Subscription
MapSubscriber ..> Subscription

' Styling
class Publisher {
  background-color: #f0f0f0;
  border: 1px solid #333;
}

class Flowable {
  background-color: #f0f0f0;
  border: 1px solid #333;
}

class FlowableFilter {
  background-color: #f0f0f0;
  border: 1px solid #333;
}

class FilterSubscriber {
  background-color: #f0f0f0;
  border: 1px solid #333;
}

class FlowableMap {
  background-color: #f0f0f0;
  border: 1px solid #333;
}

class MapSubscriber {
  background-color: #f0f0f0;
```

#### `21b4a540ef036fcb31ecb8df572773b7cd602a22` — compiled_low_structural (sequence, tier 3)

- Element: tp=9 fp=0 fn=0 F1=1.000; type-acc matched=9 correct=0 excluded=0
- Relationship: tp=0 fp=16 fn=16 F1=0.000; missed: message; extra: association
- chrF++: 81.29
- Files: GT `data/puml_files/21b4a540ef036fcb31ecb8df572773b7cd602a22.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/21b4a540ef036fcb31ecb8df572773b7cd602a22.puml` (yes) · input `data/puml_images_1568/21b4a540ef036fcb31ecb8df572773b7cd602a22.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/21b4a540ef036fcb31ecb8df572773b7cd602a22.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 21b4a540ef036fcb31ecb8df572773b7cd602a22
' Original Path: /bank/diagrams/cqrs.puml
' Source: World of Code

@startuml

actor User
participant UIBFF
box DomainModel
  queue CommandBus
  participant Aggregate
  participant ProcessManager
  queue EventBus
  participant QueryManager
end box
participant Projectors
database ReadModels

User -> UIBFF : http commands
UIBFF -> CommandBus : commands
CommandBus -> Aggregate : commands
Aggregate -> EventBus : events
EventBus -> ProcessManager : events
ProcessManager -> CommandBus : commands
EventBus -> Projectors : events
Projectors -> ReadModels : write
EventBus -> UIBFF : events
UIBFF -> User : push

User -> UIBFF : http queries
UIBFF -> QueryManager : queries
QueryManager -> ReadModels : results
ReadModels ->  QueryManager : results
QueryManager -> UIBFF : results
UIBFF -> User : results

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
actor "User" as User
rectangle "DomainModel" as DomainModel {
  rectangle "UIBFF" as UIBFF
  rectangle "CommandBus" as CommandBus
  rectangle "Aggregate" as Aggregate
  rectangle "ProcessManager" as ProcessManager
  rectangle "EventBus" as EventBus
  rectangle "QueryManager" as QueryManager
  rectangle "Projectors" as Projectors
}
database "ReadModels" as ReadModels

User -> UIBFF : http commands
UIBFF -> CommandBus : commands
CommandBus -> Aggregate : commands
Aggregate -> EventBus : events
EventBus -> ProcessManager : events
ProcessManager -> CommandBus : commands
EventBus -> Projectors : events
Projectors -> ReadModels : write
EventBus -> UIBFF : events
UIBFF -> User : push
User -> UIBFF : http queries
UIBFF -> QueryManager : queries
QueryManager -> ReadModels : results
ReadModels -> QueryManager : results
QueryManager -> UIBFF : results
UIBFF -> User : results

@enduml
```

#### `2399ddf66f2df14f2110eb29e444cc1f617e7810` — compiled_low_structural (class, tier 1)

- Element: tp=3 fp=0 fn=0 F1=1.000; type-acc matched=3 correct=3 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: composition; extra: inheritance
- chrF++: 36.36
- Files: GT `data/puml_files/2399ddf66f2df14f2110eb29e444cc1f617e7810.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/2399ddf66f2df14f2110eb29e444cc1f617e7810.puml` (yes) · input `data/puml_images_1568/2399ddf66f2df14f2110eb29e444cc1f617e7810.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/2399ddf66f2df14f2110eb29e444cc1f617e7810.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 2399ddf66f2df14f2110eb29e444cc1f617e7810
' Original Path: /tema5/imgs/composicionuml.pu
' Source: World of Code

@startuml

Fruta *-- Tallo
Fruta *-- Piel

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
class "Fruta" {
  C
}
class "Tallo" {
  C
}
class "Piel" {
  C
}
"Fruta" --|> "Tallo"
"Fruta" --|> "Piel"
@enduml
```

#### `3557f9e92c32096bc4472986fb49f9d25c95bdcf` — compiled_low_structural (class, tier 4)

- Element: tp=9 fp=0 fn=0 F1=1.000; type-acc matched=9 correct=9 excluded=0
- Relationship: tp=2 fp=4 fn=4 F1=0.333; missed: aggregation; extra: dependency, association
- chrF++: 48.49
- Files: GT `data/puml_files/3557f9e92c32096bc4472986fb49f9d25c95bdcf.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/3557f9e92c32096bc4472986fb49f9d25c95bdcf.puml` (yes) · input `data/puml_images_1568/3557f9e92c32096bc4472986fb49f9d25c95bdcf.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/3557f9e92c32096bc4472986fb49f9d25c95bdcf.png` (yes)

#### `377a42f35cc2d674f45cb52402a572bda269ac83` — compiled_low_structural (class, tier 4)

- Element: tp=10 fp=0 fn=0 F1=1.000; type-acc matched=10 correct=7 excluded=0
- Relationship: tp=0 fp=8 fn=7 F1=0.000; missed: inheritance; extra: dependency
- chrF++: 58.00
- Files: GT `data/puml_files/377a42f35cc2d674f45cb52402a572bda269ac83.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/377a42f35cc2d674f45cb52402a572bda269ac83.puml` (yes) · input `data/puml_images_1568/377a42f35cc2d674f45cb52402a572bda269ac83.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/377a42f35cc2d674f45cb52402a572bda269ac83.png` (yes)

#### `7e0e0e3379e4f346233ea39b20fa7408fb452111` — compiled_low_structural (sequence, tier 2)

- Element: tp=3 fp=2 fn=1 F1=0.667; type-acc matched=3 correct=0 excluded=0
- Relationship: tp=0 fp=9 fn=9 F1=0.000; missed: message; extra: dependency, association
- chrF++: 55.19
- Files: GT `data/puml_files/7e0e0e3379e4f346233ea39b20fa7408fb452111.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/7e0e0e3379e4f346233ea39b20fa7408fb452111.puml` (yes) · input `data/puml_images_1568/7e0e0e3379e4f346233ea39b20fa7408fb452111.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/7e0e0e3379e4f346233ea39b20fa7408fb452111.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 7e0e0e3379e4f346233ea39b20fa7408fb452111
' Original Path: /assets/initial-adapter-proxy-sequence.puml
' Source: World of Code

@startuml
title Initialization
box "service process" #LightBlue
participant ConcreteImpl #Wheat
participant DBusAdapter #PaleGreen
end box

ConcreteImpl -[hidden]> DBusAdapter
DBusAdapter -> DBusAdapter: Init(ConcreteImpl) 
DBusAdapter -> DBus: Export 

box "client process" #Lavender
participant DBusProxy #PaleGreen
end box

DBusProxy -> DBusProxy: Init 
DBusProxy -> DBus: ConnectToRemoteObject
note right: Tries to fetch all properties \n including "ready" property 
DBusProxy -> DBus: GetAllProperties
DBus -> DBusAdapter: GetAllProperties
DBusAdapter --> DBus: return properties
DBus --> DBusProxy: return properties
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam sequenceStyle rectangle

package "service process" as service {
  [ConcretImpl] as concreteImpl
  [DBusAdapter] as dbusAdapter
}

package "client process" as client {
  [DBusProxy] as dbusProxy
}

[DBus] as dbus

note right of dbusProxy
  Tries to fetch all properties
  including "ready" property
end note

dbusProxy -> dbus: ConnectToRemoteObject
dbusProxy -> dbus: GetAllProperties
dbus -> dbusAdapter: GetAllProperties
dbusAdapter -> dbus: return properties
dbus -> dbusProxy: return properties

dbusAdapter -> dbusAdapter: Init(ConcretImpl)
dbusAdapter -> dbus: Export
dbusProxy -> dbusProxy: Init

@enduml
```

#### `82fd0908b0de00ad974a0518092896435c86f09b` — compiled_low_structural (class, tier 3)

- Element: tp=5 fp=1 fn=1 F1=0.833; type-acc matched=5 correct=3 excluded=1
- Relationship: tp=2 fp=4 fn=3 F1=0.364; missed: composition, aggregation, dependency; extra: inheritance, composition, aggregation, dependency
- chrF++: 72.80
- Files: GT `data/puml_files/82fd0908b0de00ad974a0518092896435c86f09b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/82fd0908b0de00ad974a0518092896435c86f09b.puml` (yes) · input `data/puml_images_1568/82fd0908b0de00ad974a0518092896435c86f09b.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/82fd0908b0de00ad974a0518092896435c86f09b.png` (yes)

#### `84229a2f3146a5612be77dc49bc84ef4e68d6371` — compiled_low_structural (sequence, tier 1)

- Element: tp=4 fp=1 fn=0 F1=0.889; type-acc matched=4 correct=0 excluded=0
- Relationship: tp=0 fp=8 fn=4 F1=0.000; missed: message; extra: dependency
- chrF++: 42.83
- Files: GT `data/puml_files/84229a2f3146a5612be77dc49bc84ef4e68d6371.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/84229a2f3146a5612be77dc49bc84ef4e68d6371.puml` (yes) · input `data/puml_images_1568/84229a2f3146a5612be77dc49bc84ef4e68d6371.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/84229a2f3146a5612be77dc49bc84ef4e68d6371.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 84229a2f3146a5612be77dc49bc84ef4e68d6371
' Original Path: /docs/UseCases/Manage-Pipeline/Destroy-Pipeline.puml
' Source: World of Code

@startuml
Actor "actorName" as A

box "Manage-Pipeline" #lightblue
participant CLI as CLI
participant Web as Web
participant "caade" as S
A -> CLI : caade-pipeline-destroy()
CLI -> S : pipeline/destroy()
A -> Web : pipeline/destroy()
Web -> S : pipeline/destroy()
end box

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
actor actorName as actor1
actor actorName as actor2

rectangle "Manage-Pipeline" as managePipeline {
  [CLI] as cli
  [Web] as web
  [caade] as caade
}

actor1 ..> cli : caade-pipeline-destroy()
cli ..> caade : pipeline/destroy()
actor1 ..> web : pipeline/destroy()
web ..> caade : pipeline/destroy()

actor2 ..> cli : caade-pipeline-destroy()
cli ..> caade : pipeline/destroy()
actor2 ..> web : pipeline/destroy()
web ..> caade : pipeline/destroy()

@enduml
```

#### `8db937ff1aa2482e25096ce400100023484400be` — compiled_low_structural (sequence, tier 4)

- Element: tp=4 fp=6 fn=0 F1=0.571; type-acc matched=4 correct=0 excluded=0
- Relationship: tp=0 fp=11 fn=4 F1=0.000; missed: message; extra: dependency, association
- chrF++: 82.05
- Files: GT `data/puml_files/8db937ff1aa2482e25096ce400100023484400be.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/8db937ff1aa2482e25096ce400100023484400be.puml` (yes) · input `data/puml_images_1568/8db937ff1aa2482e25096ce400100023484400be.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/8db937ff1aa2482e25096ce400100023484400be.png` (yes)

#### `9f8b8b5e51ee53edb67eba0d97eb9e0fdde90351` — compiled_low_structural (sequence, tier 1)

- Element: tp=2 fp=0 fn=0 F1=1.000; type-acc matched=2 correct=0 excluded=0
- Relationship: tp=0 fp=3 fn=3 F1=0.000; missed: message; extra: dependency
- chrF++: 55.73
- Files: GT `data/puml_files/9f8b8b5e51ee53edb67eba0d97eb9e0fdde90351.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/9f8b8b5e51ee53edb67eba0d97eb9e0fdde90351.puml` (yes) · input `data/puml_images_1568/9f8b8b5e51ee53edb67eba0d97eb9e0fdde90351.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/9f8b8b5e51ee53edb67eba0d97eb9e0fdde90351.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 9f8b8b5e51ee53edb67eba0d97eb9e0fdde90351
' Original Path: /nockenwellen_pruefstand/pruefstand_software/main_motor_message_activity.plantuml
' Source: World of Code

@startuml

' Messages between main and motor actor
Main -> Motor: Set Speed

Main -> Motor: Get Speed
Motor -> Main: Motor Speed Respone


@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam class {
  BackgroundColor #E6E6FA
  BorderColor #999999
  FontColor #000000
}

class "Main" {
}

class "Motor" {
}

Main ..> Motor : Set Speed
Main ..> Motor : Get Speed
Motor ..> Main : Motor Speed Response

@enduml
```

#### `bec9b6e0cd05a21e2c28a157001b3c273c9b1510` — compiled_low_structural (sequence, tier 2)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=0 excluded=0
- Relationship: tp=0 fp=9 fn=10 F1=0.000; missed: message; extra: association
- chrF++: 47.00
- Files: GT `data/puml_files/bec9b6e0cd05a21e2c28a157001b3c273c9b1510.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/bec9b6e0cd05a21e2c28a157001b3c273c9b1510.puml` (yes) · input `data/puml_images_1568/bec9b6e0cd05a21e2c28a157001b3c273c9b1510.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/bec9b6e0cd05a21e2c28a157001b3c273c9b1510.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: bec9b6e0cd05a21e2c28a157001b3c273c9b1510
' Original Path: /app/src/main/java/uml/display_setting_diagram.puml
' Source: World of Code

@startuml
box "host" #fff
participant MultiDisplayService
end box
box "rcv" #fff
participant IMultipleDisplaysUiController
participant IMultipleDisplaysDelegate
end box
box "controller" #fff
participant DisplaysSwapViewController
participant DisplaysSwapPresenter
end box

MultiDisplayService -> MultiDisplayService: onDisplayAdded
MultiDisplayService -> IMultipleDisplaysUiController: updateDisplayInfos
MultiDisplayService -> MultiDisplayService: onDisplayRemoved
MultiDisplayService -> IMultipleDisplaysUiController: updateDisplayInfos
DisplaysSwapViewController -> DisplaysSwapPresenter: swap()
DisplaysSwapPresenter -> IMultipleDisplaysUiController: swap()
IMultipleDisplaysDelegate -> DisplaysSwapPresenter: onUpdateDisplayInfo(IMultipleDisplaysUiController var1, EMultipleDisplaysAction var2)
DisplaysSwapPresenter -> DisplaysSwapPresenter: loadMonitorsIndicator()
IMultipleDisplaysDelegate -> MultiDisplayService: onUpdateDisplayInfo(IMultipleDisplaysUiController var1, EMultipleDisplaysAction var2)
MultiDisplayService -> MultiDisplayService: notifyMultiDisplayChanged(type: MultiDisplayChangeType,displayId: Int)
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
left to right direction
skinparam sequenceMessageAlign center

package "host" as host {
  [MultiDisplayService] as mds
}

package "rcv" as rcv {
  [IMultipleDisplaysUiController] as imd_uc
  [IMultipleDisplaysDelegate] as imd_dl
}

package "controller" as controller {
  [DisplaysSwapViewController] as dsvvc
  [DisplaysSwapPresenter] as dsvp
}

mds -> imd_uc : updateDisplayInfos
mds -> imd_uc : updateDisplayInfos

imd_uc -> dsvp : swap()
dsvp -> imd_dl : onUpdateDisplayInfo(MultipleDisplaysUiController var1, EMultipleDisplaysAction var2)
imd_dl -> mds : onUpdateDisplayInfo(MultipleDisplaysUiController var1, EMultipleDisplaysAction var2)
mds -> mds : notifyMultiDisplayChanged(type: MultiDisplayChangeType, displayId: Int)

mds -> mds : onDisplayAdded
mds -> mds : onDisplayRemoved

dsvp -> dsvp : loadMonitorsIndicator()

@enduml
```

#### `c2056417614836054c507c50f98bd814afb43d88` — compiled_low_structural (sequence, tier 3)

- Element: tp=3 fp=2 fn=2 F1=0.600; type-acc matched=3 correct=3 excluded=0
- Relationship: tp=1 fp=9 fn=6 F1=0.118; missed: message; extra: message
- chrF++: 36.05
- Files: GT `data/puml_files/c2056417614836054c507c50f98bd814afb43d88.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/c2056417614836054c507c50f98bd814afb43d88.puml` (yes) · input `data/puml_images_1568/c2056417614836054c507c50f98bd814afb43d88.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/c2056417614836054c507c50f98bd814afb43d88.png` (yes)

#### `f3577068d1cdb0d8093b087519559ea632920802` — compiled_low_structural (sequence, tier 4)

- Element: tp=4 fp=2 fn=0 F1=0.800; type-acc matched=4 correct=0 excluded=0
- Relationship: tp=0 fp=9 fn=9 F1=0.000; missed: message; extra: association
- chrF++: 23.01
- Files: GT `data/puml_files/f3577068d1cdb0d8093b087519559ea632920802.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/f3577068d1cdb0d8093b087519559ea632920802.puml` (yes) · input `data/puml_images_1568/f3577068d1cdb0d8093b087519559ea632920802.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/f3577068d1cdb0d8093b087519559ea632920802.png` (yes)

#### `f61b8e6740f27fd7ccccb669844d09ac0159f39c` — compiled_low_structural (class, tier 3)

- Element: tp=6 fp=0 fn=0 F1=1.000; type-acc matched=6 correct=5 excluded=0
- Relationship: tp=0 fp=7 fn=7 F1=0.000; missed: inheritance, composition, aggregation; extra: inheritance, association
- chrF++: 69.31
- Files: GT `data/puml_files/f61b8e6740f27fd7ccccb669844d09ac0159f39c.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/f61b8e6740f27fd7ccccb669844d09ac0159f39c.puml` (yes) · input `data/puml_images_1568/f61b8e6740f27fd7ccccb669844d09ac0159f39c.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/f61b8e6740f27fd7ccccb669844d09ac0159f39c.png` (yes)

#### `f9b87c78f652ee63cd07d4a0e4a54cb09852e58a` — compiled_low_structural (class, tier 1)

- Element: tp=2 fp=0 fn=0 F1=1.000; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=1 fn=0 F1=0.000; extra: dependency
- chrF++: 65.23
- Files: GT `data/puml_files/f9b87c78f652ee63cd07d4a0e4a54cb09852e58a.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-9B_20260613T202001Z/f9b87c78f652ee63cd07d4a0e4a54cb09852e58a.puml` (yes) · input `data/puml_images_1568/f9b87c78f652ee63cd07d4a0e4a54cb09852e58a.png` (yes) · render `data/csr/Qwen_Qwen3.5-9B_20260613T202001Z/png/f9b87c78f652ee63cd07d4a0e4a54cb09852e58a.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: f9b87c78f652ee63cd07d4a0e4a54cb09852e58a
' Original Path: /BinaryTrees/binary_tree_class.puml
' Source: World of Code

@startuml
class Node<T>{
-Node* Left
-Node* Right
-T value
}

class BinaryTree<T> {
-Node** root
+void insert(T value)
+void remove(T value)
+void search(T value)
}
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
!theme plain

class "Node" as Node {
  [C]
  Node* Left
  Node* Right
  T value
}

class "BinaryTree" as BinaryTree {
  [C]
  Node** root
  void insert(T value)
  void remove(T value)
  void search(T value)
}

Node ..> BinaryTree : T

@enduml
```

### Qwen3.5-27B

#### outcome: provider_drop

#### `938e9cc0e6b8dda26422f35f30282f7d202efb9d_02` — provider_drop (sequence, tier 4)

- CSR: `no prediction (missing/timeout)`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=20 F1=0.000; missed: message
- chrF++: 0.00
- Files: GT `data/puml_files/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (MISSING) · input `data/puml_images_1568/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (MISSING)

#### outcome: compile_fail

#### `2b81c26799a6f7c76f023689f2fec36e30d18c05` — compile_fail (sequence, tier 4)

- CSR: `Error line 12 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/2b81c26799a6f7c76f023689f2fec36e30d18c05.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=21 F1=0.000; missed: message
- chrF++: 54.52
- Files: GT `data/puml_files/2b81c26799a6f7c76f023689f2fec36e30d18c05.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/2b81c26799a6f7c76f023689f2fec36e30d18c05.puml` (yes) · input `data/puml_images_1568/2b81c26799a6f7c76f023689f2fec36e30d18c05.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/2b81c26799a6f7c76f023689f2fec36e30d18c05.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 2b81c26799a6f7c76f023689f2fec36e30d18c05
' Original Path: /docs/SprintB/US/US13/US013_SD.puml
' Source: World of Code

@startuml
autonumber
'hide footbox
actor "Administrator" as Administrator

participant ":SpecifyNewVaccineUI" as NewVaccineUI
participant ":SpecifyNewVaccineController" as NewVaccineController
participant ":Company" as Company
participant ":VaccineStore" as VaccineStore
participant "vc:Vaccine" as Vaccine
participant "admPro:AdministrationProcess" as AdministrationProcess
participant ":VaccineTypeStore" as VaccineTypeStore
participant ":VaccineType" as VaccineType


activate Administrator

Administrator -> NewVaccineUI : starts specifying a new vaccine and its administration process
activate NewVaccineUI

NewVaccineUI -> NewVaccineController : createVaccine()
activate NewVaccineController

NewVaccineController -> Company : typeList = getVaccineTypeList()
activate Company

Company -> VaccineTypeStore : getVaccineTypeList()
activate VaccineTypeStore

loop for all known vaccineTypes
VaccineTypeStore -> VaccineType : VaccineType(code,name)
activate VaccineType
deactivate VaccineTypeStore
deactivate VaccineType
end

NewVaccineUI --> Administrator : request data (name, manufacturer, type, age groups,doses,elapsing interval, dosage) and show vaccineType list
deactivate NewVaccineUI
deactivate NewVaccineController
deactivate Company
deactivate VaccineTypeStore


Administrator -> NewVaccineUI : types requested data
activate NewVaccineUI

NewVaccineUI -> NewVaccineController : createVaccine(id,name,manufacturer,type,administrationProcess)
activate NewVaccineController

NewVaccineController -> Company : createVaccine(id,name,manufacturer,type,administrationProcess)
activate Company

Company -> VaccineStore : createVaccine(id,name,manufacturer,type,administrationProcess)
activate VaccineStore
deactivate Company

create Vaccine
VaccineStore -> Vaccine** : vc = createVaccine(id,name,manufacturer,type,administrationProcess)
activate Vaccine

loop for all age groups
Vaccine -> AdministrationProcess** : administrationProcess(minAge,maxAge,numberOfDoses,dosage,timeElapsed)
activate AdministrationProcess
end
deactivate AdministrationProcess

Vaccine -> Vaccine : validateVaccine()

VaccineStore -> VaccineStore : validateVaccine(vc)
deactivate Vaccine

NewVaccineUI --> Administrator : shows data and request confirmation
deactivate VaccineStore

Administrator -> NewVaccineUI : confirms data

```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
left to right direction
skinparam sequence {
    ArrowColor black
    ActorBorderColor black
    ActorBackgroundColor white
    LifeLineBorderColor black
    LifeLineBackgroundColor white
}

actor Administrator as admin
participant "SpecifyNewVaccineUI" as ui
participant "SpecifyNewVaccineController" as controller
participant "Company" as company
participant "VaccineStore" as store
database "vc.Vaccine" as vaccineDB
rectangle "admPro.AdministrationProcess" as admProcess
database "VaccineTypeStore" as typeStore
database "VaccineType" as vType

admin -> ui : 1 starts specifying a new vaccine and its administration process
activate ui
ui -> controller : 2 createVaccine()
activate controller
controller -> company : 3 typeList = getVaccineTypeList()
activate company
company -> typeStore : 4 getVaccineTypeList()
activate typeStore
loop for all known vaccineTypes
    typeStore -> vType : 5 VaccineType(code, name)
end
deactivate typeStore
deactivate company
typeStore --> controller : 6 request data (name, manufacturer, type, age groups,doses,elapsing interval, dosage) and show vaccineType list
controller --> ui : 7 types requested data
ui -> controller : 8 createVaccine(id, name, manufacturer, type, administrationProcess)
controller -> company : 9 createVaccine(id, name, manufacturer, type, administrationProcess)
company -> store : 10 createVaccine(id, name, manufacturer, type, administrationProcess)
activate store
store -> vaccineDB : 11 vc = createVaccine(id, name, manufacturer, type, administrationProcess)
activate vaccineDB
loop For all age groups
    vaccineDB -> admProcess : 12 administrationProcess(minAge, maxAge, numberOfDoses, dosage, timeElapsed)
    activate admProcess
    admProcess --> vaccineDB : 13 validateVaccine()
    deactivate admProcess
end
vaccineDB --> store : 14 updateVaccine()
deactivate store
deactivate vaccineDB
store --> ui : 15 shows data and request confirmation
ui --> controller : 16 confirms data
controller -> company : 17 saveVaccine()
company -> store : 18 saveVaccine()
store -> vaccineDB : 19 saveVaccine()
vaccineDB --> store : 20 addVaccine()
deactivate store
deactivate company
deactivate controller
deactivate ui
ui --> admin : 21 informs operation (in)succcess

@enduml
```
```

#### `2ba4e7f17f9f45f359569c1285dafccb3b4f54ab` — compile_fail (sequence, tier 2)

- CSR: `Error line 10 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=5 F1=0.000; missed: message
- chrF++: 62.92
- Files: GT `data/puml_files/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.puml` (yes) · input `data/puml_images_1568/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/2ba4e7f17f9f45f359569c1285dafccb3b4f54ab.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 2ba4e7f17f9f45f359569c1285dafccb3b4f54ab
' Original Path: /docs/edgemere/sa/spm/usecases/managesecurityprofiles/MonitorSecurityProfile.puml
' Source: World of Code

@startuml

actor "SecurityEngineer"


entity EventBus

box Security Profile Manager #cc8888
    boundary spm #white
end box


box Software Defined Infrastructure #cccc88
            participant storageresource
    end box

box Security Profile Manager #cc8888
    end box


"SecurityEngineer" -> spm: Monitor Security Profile

    spm -> "storageresource": create (name: secProfileMSP,file: ./templates/secprofile.yml)

    "storageresource" --/ EventBus: securityprofile.create

    spm -> "securityprofile": status (name: secProfileMSP)

    "securityprofile" --/ EventBus: securityprofile.status



@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam componentStyle rectangle

actor "SecurityEngineer" as se1
circle "EventBus" as eb1
rectangle "Security Profile Manager" as spm {
  interface "spm" as spm_interface
}
rectangle "Software Defined Infrastructure" as sdi {
  box "storageresource" as sr1
  box "securityprofile" as sp1
}

se1 -> spm : Monitor Security Profile
activate spm
spm -> sdi : create (name: secProfileMSP, file: ./templates/secprofile.yml)
deactivate spm
sdi --> eb1 : securityprofile.create

spm -> sdi : status (name: secProfileMSP)
sdi --> eb1 : securityprofile.status

actor "SecurityEngineer" as se2
circle "EventBus" as eb2
rectangle "Security Profile Manager" as spm2 {
  interface "spm" as spm_interface2
}
rectangle "Software Defined Infrastructure" as sdi2 {
  box "storageresource" as sr2
  box "securityprofile" as sp2
}

@enduml
```
```

#### `3742b10891bd50981fd7c438979c2a63ef66aa44` — compile_fail (class, tier 4)

- CSR: `Error line 85 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/3742b10891bd50981fd7c438979c2a63ef66aa44.puml`
- Element: tp=0 fp=0 fn=14 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=16 F1=0.000; missed: composition, aggregation, dependency
- chrF++: 91.53
- Files: GT `data/puml_files/3742b10891bd50981fd7c438979c2a63ef66aa44.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/3742b10891bd50981fd7c438979c2a63ef66aa44.puml` (yes) · input `data/puml_images_1568/3742b10891bd50981fd7c438979c2a63ef66aa44.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/3742b10891bd50981fd7c438979c2a63ef66aa44.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 3742b10891bd50981fd7c438979c2a63ef66aa44
' Original Path: /Project/docs/Sprint3/US027/US027-CD.puml
' Source: World of Code

@startuml

hide circle
skinparam classAttributeIconSize 0

title "US027 - As Director, I want to define the Product Owner of a project."

class AssignProductOwnerUI {
}

class AssignProductOwnerController {
    +AssignProductOwnerController
    +getProject(code)
    +getResource(name)
    +assignRole(resourceName, roleName)
}

class ProjectsMapper {
    +toDTO(project)
    }

class ProjectTeamMapper {
    +toDto(resource)
}

class ProjectDTO {
    +ProjectDTO(code, projectName, startDate, endDate)
}

class ResourceDTO {
    +ResourceDTO(name, role, startDate, endDate, costPerHour, percentageOfAllocation)
}

class Company {
    +Company()
    +getProjectStore()
    +getProjectRoleStore()
}

class ProjectTeam {
    +ProjectTeam()
    +getResourceByName()
    +assignProjectRole(resource,startDate,sprintDuration,role)
    +saveResource(newResource)
    +checkIfRoleCurrentExistInTheProjectTeam(role,startDate)
}

class Resource {
    +Resource()
    +Resource(originalResource)
    +isYourName(name)
    +isCurrent()
    +setRole(role)
    +setStartDate(startDate)
    +setEndDate(startDate)
    +isAvailableToSprint(startDate, sprintDuration)
    +copyUpdateProjectRoleOfAResource(originalResource, startDateNewRole, role)
}

class ProjectStore {
    +ProjectStore()
    +getProjectByCode()
}

class ProjectRoleStore {
    +ProjectRoleStore()
    +getProjectRole(roleName)
}

class Project {
    +Project()
    +getProjectTeam()
    +getSprintDuration()
    +getSprints()
    +hasCode()
}
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
title US027 - As Director, I want to define the Product Owner of a project.

class AssignProductOwnerUI {
}

class AssignProductOwnerController {
    +AssignProductOwnerController()
    +getProject(code)
    +getResource(name)
    +assignRole(resourceName, roleName)
}

class ProjectsMapper {
    +toDTO(project)
}

class ProjectDTO {
    +ProjectDTO(code, projectName, startDate, endDate)
}

class ProjectTeamMapper {
    +toDto(resource)
}

class ResourceDTO {
    +ResourceDTO(name, role, startDate, endDate, costPerHour, percentageOfAllocation)
}

class Company {
    +Company()
    +getProjectStore()
    +getProjectRoleStore()
}

class ProjectStore {
    +ProjectStore()
    +getProjectByCode()
}

class ProjectRoleStore {
    +ProjectRoleStore()
    +getProjectRole(roleName)
}

class Project {
    +Project()
    +getProjectTeam()
    +getSprintDuration()
    +getSprints()
    +hasCode()
}

class ProjectTeam {
    +ProjectTeam()
    +getResourceByName()
    +assignProjectRole(resource, startDate, sprintDuration, role)
    +saveResource(newResource)
    +checkIfRoleCurrentExistInTheProjectTeam(role, startDate)
}

class Resource {
    +Resource()
    +Resource(originalResource)
    +isYourName(name)
    +isCurrent()
    +setRole(role)
    +setStartDate(startDate)
    +setEndDate(startDate)
    +isAvailableToSprint(startDate, sprintDuration)
    +copyUpdateProjectRoleOfAResource(originalResource, startDateNewRole, role)
}

class SprintList {
    +SprintList()
    +getCurrentSprint()
}

class Sprint {
```

#### `4ee70296687473b2dc89dddc2bd8f00e9aaf2b44` — compile_fail (sequence, tier 3)

- CSR: `Error line 6 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/4ee70296687473b2dc89dddc2bd8f00e9aaf2b44.puml`
- Element: tp=0 fp=0 fn=6 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 61.92
- Files: GT `data/puml_files/4ee70296687473b2dc89dddc2bd8f00e9aaf2b44.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/4ee70296687473b2dc89dddc2bd8f00e9aaf2b44.puml` (yes) · input `data/puml_images_1568/4ee70296687473b2dc89dddc2bd8f00e9aaf2b44.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/4ee70296687473b2dc89dddc2bd8f00e9aaf2b44.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 4ee70296687473b2dc89dddc2bd8f00e9aaf2b44
' Original Path: /docs/io_pulling_crd_seq_diagram_1.uml
' Source: World of Code

//
// vim:syntax=plantuml
//
// Copyright © 2020 Red Hat, Inc.
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Generate PNG image with sequence diagram by using the following command:
// java -jar plantuml.jar io_pulling_crd_seq_diagram.uml
//
// Generate SVG drawing with sequence diagram by using the following command:
// java -jar plantuml.jar -tsvg io_pulling_crd_seq_diagram.uml

@startuml

!include <cloudinsight/kafka>
!include <kubernetes/k8s-sprites-unlabeled-25pct>

header Sequence diagram for the whole CCX (external) data pipeline
footer Copyright © 2020 Red Hat, Inc. Author: Pavel Tisnovsky

participant "Smart\nProxy" as smart_proxy #a0a0ff
participant "3Scale" as 3scale
box "Insights operator" #ddffdd
participant "<$master>\nControl logic" as operator
database "IO memory cache" as cache
end box
entity "CRD" as crd
collections "OCP\nWebConsole" as console

== Pulling data from Smart Proxy ==
operator -> 3scale: Get\nrecommendations\norg ID\ncluster ID
3scale -> smart_proxy: Get\nrecommendations\norg ID\ncluster ID
smart_proxy -> 3scale: Recommendations\nfor cluster
3scale -> operator: Recommendations\nfor cluster

== Exposing recommendations ==
operator -> cache: Store\nrecommendations
cache -> crd: Expose\nrecommendations

== Pulling from OCP WebConsole ==
console -> crd: Read\nrecommendations
crd -> console: Here are\nrequired data

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title Sequence diagram for the whole CCX (external) data pipeline

actor "Smart Proxy" as SmartProxy
participant "3Scale" as ThreeScale
package "Insights operator" {
    participant "Control logic" as ControlLogic
    database "IO memory cache" as Cache
}
participant "CRD" as CRD
participant "OCP WebConsole" as OCPWebConsole

== Pulling data from Smart Proxy ==
ControlLogic -> ThreeScale: Get recommendations\norg ID\ncluster ID
ThreeScale -> SmartProxy: Get recommendations\norg ID\ncluster ID
SmartProxy --> ThreeScale: Recommendations for cluster
ThreeScale --> ControlLogic: Recommendations for cluster

== Exposing recommendations ==
ControlLogic -> Cache: Store recommendations
Cache -> CRD: Expose recommendations

== Pulling from OCP WebConsole ==
OCPWebConsole -> CRD: Read recommendations
CRD --> OCPWebConsole: Here are required data

note bottom: Copyright © 2020 Red Hat, Inc. Author: Pavel Tisnovsky
@enduml
```
```

#### `5062b6c354eb5e7d4350b93465d61c1c2b628ec7` — compile_fail (class, tier 3)

- CSR: `Error line 8 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: inheritance, association
- chrF++: 33.70
- Files: GT `data/puml_files/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.puml` (yes) · input `data/puml_images_1568/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/5062b6c354eb5e7d4350b93465d61c1c2b628ec7.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 5062b6c354eb5e7d4350b93465d61c1c2b628ec7
' Original Path: /E-R/_diagrams/reference-data/PressureMeasurementType.1.0.0.ref.puml
' Source: World of Code

@startuml
hide methods
skinparam groupInheritance 2
skinparam class {
    ArrowColor Black
    BorderColor Black
    BackgroundColor<<master-data>> LightSalmon
    BackgroundColor<<work-product-component>> Gold
    BackgroundColor<<abstract>> LightSteelBlue
    BackgroundColor<<dataset>> Ivory
    BackgroundColor<<reference-data>> Turquoise
    BackgroundColor<<Abstraction>> LightSkyBlue
    BackgroundColor<<error>> Red
    BackgroundColor<<Activity>> LightSkyBlue
    BackgroundColor<<ReferenceType>> LightSkyBlue
    BackgroundColor<<WorkProductComponent>> LightSkyBlue
    BackgroundColor<<Project>> LightSkyBlue
    BackgroundColor<<File>> LightSkyBlue
    BackgroundColor<<FileCollection>> LightSkyBlue
    BackgroundColor<<MasterData>> LightSkyBlue
    BackgroundColor<<nested array>> WhiteSmoke
    BackgroundColor<<nested>> WhiteSmoke
    packageStyle rectangle
}
package "PressureMeasurementType Referenced-by View" <<rectangle>>
{
class "<size:16>PressureMeasurementType</size>" as PressureMeasurementType <<reference-data>>
left to right direction
class "PressureMeasurementType" <<reference-data>>
package "work-product-component Entities" as WorkProductComponent <<frame>>
{
class "RockSampleAnalysis" <<work-product-component>> {
RCAMeasurements[].Conditions.PressureMeasurementTypeID
}
}
"WorkProductComponent" -->  "PressureMeasurementType" 
abstract "AbstractReferenceType" <<Abstraction>>
"PressureMeasurementType" -right-|>  "AbstractReferenceType"
}
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam classAttributeIconSize 0

title PressureMeasurementType Referenced-by View

package "work-product-component Entities" {
    package "«work-product-component»\nRockSampleAnalysis" as RockSampleAnalysis {
        RCAMeasurements[].Conditions.PressureMeasurementTypeID
    }
}

abstract class "«Abstraction»\nAbstractReferenceType" as AbstractReferenceType {
}

class "«reference-data»\nPressureMeasurementType" as PressureMeasurementType {
}

AbstractReferenceType <|-- PressureMeasurementType

RockSampleAnalysis --> PressureMeasurementType

note "A" as A
note "C" as C1
note "C" as C2

hide circle
A -[hidden]down- AbstractReferenceType
C1 -[hidden]right- RockSampleAnalysis
C2 -[hidden]right- PressureMeasurementType
@enduml
```
```

#### `5922ccf81ce292fdd445209df90f8035c5b34c23` — compile_fail (class, tier 1)

- CSR: `Error line 6 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/5922ccf81ce292fdd445209df90f8035c5b34c23.puml`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 67.41
- Files: GT `data/puml_files/5922ccf81ce292fdd445209df90f8035c5b34c23.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/5922ccf81ce292fdd445209df90f8035c5b34c23.puml` (yes) · input `data/puml_images_1568/5922ccf81ce292fdd445209df90f8035c5b34c23.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/5922ccf81ce292fdd445209df90f8035c5b34c23.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 5922ccf81ce292fdd445209df90f8035c5b34c23
' Original Path: /РегистрыСведений/РегистрСведенийВзаимозависимыеЛица.wsd
' Source: World of Code

﻿@startuml
'!include templates.wsd
'..\include templates.wsd
class РегистрСведений.ВзаимозависимыеЛица as "Взаимозависимые лица" <<РегистрыСведений>>
{
..Измерения..
Организация : Справочник.Организация
Контрагент : Справочник.Организация\rСправочник.Контрагент
..Ресурсы..
ТипВзаимозависимости : Типы взаимозависимости
}
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam packageStyle rectangle

package "РегистрСведений" {
    package «РегистрыСведений» Взаимозависимые лица as C {
        [C]
        ..Измерения..
        Организация : Справочник.Организация
        Контрагент : Справочник.Организация
        Справочник.Контрагент
        ..Ресурсы..
        ТипВзаимозависимости : Типы взаимозависимости
    }
}
@enduml
```
```

#### `704b783235640f12565d250b751599d621aff349` — compile_fail (sequence, tier 1)

- CSR: `Error line 9 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/704b783235640f12565d250b751599d621aff349.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 49.06
- Files: GT `data/puml_files/704b783235640f12565d250b751599d621aff349.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/704b783235640f12565d250b751599d621aff349.puml` (yes) · input `data/puml_images_1568/704b783235640f12565d250b751599d621aff349.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/704b783235640f12565d250b751599d621aff349.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 704b783235640f12565d250b751599d621aff349
' Original Path: /docs/activity_diagram.puml
' Source: World of Code

@startuml

title Activity Diagram

participant "Bot Service" as svc
participant "Listener" as lsn
participant "Worker" as wrk
participant "Publisher" as pub


@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title Activity Diagram

package "Bot Service" as BotService {
    [Bot Service]
}

package "Listener" as Listener {
    [Listener]
}

package "Worker" as Worker {
    [Worker]
}

package "Publisher" as Publisher {
    [Publisher]
}

BotService -down-> BotService
Listener -down-> Listener
Worker -down-> Worker
Publisher -down-> Publisher

@enduml
```
```

#### `7409cf40c00dfe3b5efd16bff9b188b1f767574b` — compile_fail (sequence, tier 1)

- CSR: `Error line 5 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/7409cf40c00dfe3b5efd16bff9b188b1f767574b.puml`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: message
- chrF++: 62.19
- Files: GT `data/puml_files/7409cf40c00dfe3b5efd16bff9b188b1f767574b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/7409cf40c00dfe3b5efd16bff9b188b1f767574b.puml` (yes) · input `data/puml_images_1568/7409cf40c00dfe3b5efd16bff9b188b1f767574b.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/7409cf40c00dfe3b5efd16bff9b188b1f767574b.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 7409cf40c00dfe3b5efd16bff9b188b1f767574b
' Original Path: /wxh-note/src/main/uml/record/员工画像维护.puml
' Source: World of Code

@startuml

group 按门店维度批量执行
ehr -> attendance: 查询员工累计考勤工时
attendance --> ehr: 返回员工累计考勤工时
end

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam packageStyle rectangle

package "按门店维度批量执行" as batch {
    participant "ehr" as ehr
    participant "attendance" as attendance

    ehr -> attendance : 查询员工累计考勤工时
    attendance ..> ehr : 返回员工累计考勤工时
}
@enduml
```
```

#### `8e4456a2565edb67be4b5ca865e478ae5df47a50` — compile_fail (class, tier 3)

- CSR: `Error line 29 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/8e4456a2565edb67be4b5ca865e478ae5df47a50.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: inheritance, composition, aggregation
- chrF++: 81.90
- Files: GT `data/puml_files/8e4456a2565edb67be4b5ca865e478ae5df47a50.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/8e4456a2565edb67be4b5ca865e478ae5df47a50.puml` (yes) · input `data/puml_images_1568/8e4456a2565edb67be4b5ca865e478ae5df47a50.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/8e4456a2565edb67be4b5ca865e478ae5df47a50.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 8e4456a2565edb67be4b5ca865e478ae5df47a50
' Original Path: /.history/ginasio_20200903220406.wsd
' Source: World of Code

@startuml
abstract class Pessoa {
  # nome: String
}

Pessoa <|-- Clients

class Clients {
  - id: Int
  - nome: String
  - locaçao: List<Aluguel>
}

Clients "1" -r---* "0..*" Aluguel

class Aluguel {
  - cliente: Client
  - tempo: Int
  - quadra: Quadra
}

Aluguel "1" o-l-- "1..*" Quadra

class Quadra {
  - numero: Int
  - aluguel: Aluguel
  - ginasio: Ginasio
}

Quadra *-u- Ginasio

class Ginasio {
  - nome: String
  - quadra: List<Quadra>
}
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
class Ginasio {
    - nome: String
    - quadra: List<Quadra>
}

class Quadra {
    - numero: Int
    - aluguel: Aluguel
    - ginasio: Ginasio
}

class Pessoa {
    + nome: String
}

class Clients {
    - id: Int
    - nome: String
    - locação: List<Aluguel>
}

class Aluguel {
    - cliente: Client
    - tempo: Int
    - quadra: Quadra
}

Ginasio *-- "1..*" Quadra : 
Pessoa <|-- Clients
Clients --* "0..*" Aluguel : 
Pessoa "1" o-- Aluguel

skinparam classAttributeIconSize 0
@enduml
```
```

#### `a5898ca01b395eebbf7c8a3ed6666f10652c5f85` — compile_fail (class, tier 1)

- CSR: `Error line 2 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/a5898ca01b395eebbf7c8a3ed6666f10652c5f85.puml`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 80.43
- Files: GT `data/puml_files/a5898ca01b395eebbf7c8a3ed6666f10652c5f85.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/a5898ca01b395eebbf7c8a3ed6666f10652c5f85.puml` (yes) · input `data/puml_images_1568/a5898ca01b395eebbf7c8a3ed6666f10652c5f85.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/a5898ca01b395eebbf7c8a3ed6666f10652c5f85.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a5898ca01b395eebbf7c8a3ed6666f10652c5f85
' Original Path: /doc/E_LCD_Config_Font.puml
' Source: World of Code

@startuml

enum E_LCD_Config_Font <<Enumerated_Data_Type>>
{
  Allows to define a data representing
  a font size on LCD.
  --
  LCD_CONFIG_FONT_5x8
  LCD_CONFIG_FONT_5x10
}

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
enumerated "E_LCD_Config_Font" as E {
  Allows to define a data representing a font size on LCD.
  LCD_CONFIG_FONT_5x8
  LCD_CONFIG_FONT_5x10
}
@enduml
```
```

#### `b2fe8e9f55ef708f52eccce505c3b4ea0eeff6d7` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=10 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=11 F1=0.000; missed: aggregation, association
- chrF++: 2.37
- Files: GT `data/puml_files/b2fe8e9f55ef708f52eccce505c3b4ea0eeff6d7.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/b2fe8e9f55ef708f52eccce505c3b4ea0eeff6d7.puml` (yes) · input `data/puml_images_1568/b2fe8e9f55ef708f52eccce505c3b4ea0eeff6d7.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/b2fe8e9f55ef708f52eccce505c3b4ea0eeff6d7.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: b2fe8e9f55ef708f52eccce505c3b4ea0eeff6d7
' Original Path: /puml/class-diagram.puml
' Source: World of Code

@startuml

Team "1" o-- "0..n" Topic
Team "1" o-- "0..n" Participant
Team "1" o-- "1" User
Topic "1" o-- "0..n" Subtopic
Subtopic "1" o-- "0..n" Challenge
Participant "1" o-- "1" User
Participant --> ParticipantStatus : + status
Challenge --> ChallengeType : + type
User --> EducationalBackground : + educationalBackground
ChallengeReport "1" o-- "1" User
ChallengeReport "1" o-- "1" Challenge

class Challenge {
    + name: string
    + body: string
    + type: ChallengeType
    + selection: string[]
    + correct: string[]
    + points: number
    + feedback: string
}

class ChallengeReport {
    + userId: User
    + challengeId: Challenge
    + answer: string[]
    + answeredCorrectly: boolean
}

class Participant {
    + userId: User
    + points: number
    + status: ParticipantStatus
}

class Subtopic {
    + name: string
    + description: string
    + challenges: Challenge[]
}

class Team {
    + name: string
    + description: string
    + ownerId: User
    + participants: Participant[]
    + topics: Topic[]
}

class Topic {
    + name: string
    + icon: string
    + isSequential: boolean
    + subtopics: Subtopic[]
}

class User {
    + name: string
    + email: string
    + educationalInstitution: string
    + educationalBackground: EducationalBackground
    + birthDate: Date
    + points: number
}

enum ChallengeType {
    INPUT
    RADIO
    CHECKBOX
}

enum EducationalBackground {
    MIDDLE_INCOMPLETE
    MIDDLE_ONGOING
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
' in: https://www.plantuml.com/plantuml/uml/XP11JiCm48Rt-Er3jD90b5726d0f8a933e91053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c6181053c61
```

#### `b7d4eaff896dfce2a97656b676679dcfa0198292` — compile_fail (class, tier 2)

- CSR: `Error line 4 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/b7d4eaff896dfce2a97656b676679dcfa0198292.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=3 F1=0.000; missed: association
- chrF++: 72.79
- Files: GT `data/puml_files/b7d4eaff896dfce2a97656b676679dcfa0198292.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/b7d4eaff896dfce2a97656b676679dcfa0198292.puml` (yes) · input `data/puml_images_1568/b7d4eaff896dfce2a97656b676679dcfa0198292.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/b7d4eaff896dfce2a97656b676679dcfa0198292.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: b7d4eaff896dfce2a97656b676679dcfa0198292
' Original Path: /plantuml/Library/PackageCache/com.unity.mathematics@1.1.0/Unity.Mathematics/bool3x3.gen.puml
' Source: World of Code

@startuml
class bool3x3 <<struct>> {
    + bool3x3(c0:bool3, c1:bool3, c2:bool3)
    + bool3x3(m00:bool, m01:bool, m02:bool, m10:bool, m11:bool, m12:bool, m20:bool, m21:bool, m22:bool)
    + bool3x3(v:bool)
    + Equals(rhs:bool3x3) : bool
    + <<override>> Equals(o:object) : bool
    + <<override>> GetHashCode() : int
    + <<override>> ToString() : string
}
class math <<static>> <<partial>> {
    + {static} bool3x3(c0:bool3, c1:bool3, c2:bool3) : bool3x3
    + {static} bool3x3(m00:bool, m01:bool, m02:bool, m10:bool, m11:bool, m12:bool, m20:bool, m21:bool, m22:bool) : bool3x3
    + {static} bool3x3(v:bool) : bool3x3
    + {static} transpose(v:bool3x3) : bool3x3
    + {static} hash(v:bool3x3) : uint
    + {static} hashwide(v:bool3x3) : uint3
}
class "IEquatable`1"<T> {
}
bool3x3 --> "c0" bool3
bool3x3 --> "c1" bool3
bool3x3 --> "c2" bool3
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
namespace C {
  namespace math {
    class "«static»\n«partial»" #fff as math {
        +bool3x3(c0:bool3, c1:bool3, c2:bool3) : bool3x3
        +bool3x3(m00:bool, m01:bool, m02:bool, m10:bool, m11:bool, m12:bool, m20:bool, m21:bool, m22:bool) : bool3x3
        +bool3x3(v:bool) : bool3x3
        +transpose(v:bool3x3) : bool3x3
        +hash(v:bool3x3) : uint
        +hashwide(v:bool3x3) : uint3
    }
  }
}

class "«struct»" #fff as bool3x3 {
    +bool3x3(c0:bool3, c1:bool3, c2:bool3)
    +bool3x3(m00:bool, m01:bool, m02:bool, m10:bool, m11:bool, m12:bool, m20:bool, m21:bool, m22:bool)
    +bool3x3(v:bool)
    +Equals(rhs:bool3x3) : bool
    +«override» Equals(o:object) : bool
    +«override» GetHashCode() : int
    +«override» ToString() : string
}

class "«Equatable`1»" #fff as IEquatable_1 {
}

class "«struct»" #fff as bool3 {
}

math ..> bool3x3 : extends
bool3x3 ..> IEquatable_1 : implements
bool3x3 --> bool3 : c0
bool3x3 --> bool3 : c1
bool3x3 --> bool3 : c2

@enduml
```
```

#### `e19a66584de809e23cbb78abef6cf806b7903906` — compile_fail (sequence, tier 4)

- CSR: `Error line 6 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/e19a66584de809e23cbb78abef6cf806b7903906.puml`
- Element: tp=0 fp=0 fn=11 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=25 F1=0.000; missed: message
- chrF++: 64.81
- Files: GT `data/puml_files/e19a66584de809e23cbb78abef6cf806b7903906.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/e19a66584de809e23cbb78abef6cf806b7903906.puml` (yes) · input `data/puml_images_1568/e19a66584de809e23cbb78abef6cf806b7903906.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/e19a66584de809e23cbb78abef6cf806b7903906.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: e19a66584de809e23cbb78abef6cf806b7903906
' Original Path: /.idea/docs/(Templates)/USExample/US6_SD.puml
' Source: World of Code

@startuml
autonumber
'hide footbox
actor "Organization Employee" as ADM

participant ":CreateTaskUI" as UI
participant ":CreateTaskController" as CTRL
participant "ApplicationPOT" as _APP
participant "app\n:ApplicationPOT" as APP
participant "session\n:UserSession" as SESSAO
participant ":Platform" as PLAT
participant "org\n:Organization" as ORG
participant "task\n:Task" as TAREFA
participant "cat\n:Category" as CAT
participant "lc\n:List<Category>" as LIST_CAT

activate ADM
ADM -> UI : asks to create a new task
activate UI
UI --> ADM : requests data (reference, designation,  informal \n description, technical description, duration, cost)
deactivate UI

ADM -> UI : types requested data
activate UI

UI -> CTRL : lc=getTaskCategories()
activate CTRL

CTRL -> PLAT : lc=getTaskCategories()
activate PLAT
|||
deactivate PLAT
deactivate CTRL

UI --> ADM : shows task categories list and ask to select one
deactivate PLAT
deactivate UI

ADM -> UI : selects a task category
activate UI

UI -> CTRL : createTask(ref,designation,informalDesc,technicalDesc,duration,cost,categoryId)
activate CTRL

CTRL -> PLAT : cat=getCategoryById(categoryId)
activate PLAT
|||
deactivate PLAT

CTRL -> _APP: app = getInstance()
activate _APP
|||
deactivate _APP

CTRL -> APP: session = getCurrentSession()
activate APP
|||
deactivate APP

CTRL -> SESSAO: email = getUserEmail()
activate SESSAO
|||
deactivate SESSAO

CTRL -> PLAT: org = getOrganizationByUserEmail(email)
activate PLAT
|||
deactivate PLAT

CTRL -> ORG: task=createTask(ref,designation,informalDesc,technicalDesc,duration,cost,cat)
activate ORG

ORG --> TAREFA**: create(ref,designation,informalDesc,technicalDesc,duration,cost,cat)
ORG -> ORG: validateTask(task)

CTRL --> UI: result
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Organization Employee" as User
participant ":CreateTaskUI" as UI
participant ":CreateTaskController" as Controller
participant "ApplicationPOT" as POT
participant "app :ApplicationPOT" as App
participant "session :UserSession" as Session
participant ":Platform" as Platform
participant "org :Organization" as Org
participant "cat :Category" as Category
participant "lc :List<Category>" as LC
participant "task :Task" as Task

User -> UI: 1 asks to create a new task
activate UI
UI --> User: 2 requests data (reference, designation, informal description, technical description, duration, cost)
User -> UI: 3 types requested data
UI -> Controller: 4 lc=getTaskCategories()
activate Controller
Controller -> Platform: 5 lc=getTaskCategories()
activate Platform
deactivate Platform
deactivate Controller
UI --> User: 6 shows task categories list and ask to select one
User -> UI: 7 selects a task category
UI -> Controller: 8 createTask(ref,designation,informalDesc,technicalDesc,duration,cost,categoryId)
activate Controller
Controller -> Platform: 9 cat=getCategoryId(categoryId)
activate Platform
deactivate Platform
Controller -> App: 10 app = getInstance()
activate App
deactivate App
Controller -> Session: 11 session = getCurrentSession()
activate Session
deactivate Session
Controller -> Session: 12 email = getUserEmail()
activate Session
deactivate Session
Controller -> Platform: 13 org = getOrganizationByUserEmail(email)
activate Platform
deactivate Platform
Controller -> Org: 14 task=createTask(ref,designation,informalDesc,technicalDesc,duration,cost,cat)
activate Org
Org -> Task: 15 create(ref,designation,informalDesc,technicalDesc,duration,cost,cat)
activate Task
deactivate Task
Org -> Org: 16 validateTask(task)
Org --> Controller: 17 result
deactivate Org
deactivate Controller
UI --> User: 18 shows all data and requests confirmation
User -> UI: 19 confirms the data
UI -> Controller: 20 saveTask()
activate Controller
Controller -> Org: 21 saveTask(task)
activate Org
Org -> Org: 22 validateTask(task)
Org -> Org: 23 addTask(task)
Org --> Controller: 24 result
deactivate Org
deactivate Controller
UI --> User: 25 informs operation success
deactivate UI

@enduml
```
```

#### `f6581486698109da74a3436a4c52c27a478e7980` — compile_fail (class, tier 2)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=6 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=6 F1=0.000; missed: composition
- chrF++: 5.69
- Files: GT `data/puml_files/f6581486698109da74a3436a4c52c27a478e7980.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/f6581486698109da74a3436a4c52c27a478e7980.puml` (yes) · input `data/puml_images_1568/f6581486698109da74a3436a4c52c27a478e7980.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/f6581486698109da74a3436a4c52c27a478e7980.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: f6581486698109da74a3436a4c52c27a478e7980
' Original Path: /docs/development/backend/regards/processing/puml/domain-entities.puml
' Source: World of Code

@startuml

interface PProject
class PBatch
class PExecution
class PStep
class PInputFile
class POutputFile

PProject *-- PBatch
PBatch *-- PExecution
PExecution *-- PStep
PExecution *-- PInputFile
PExecution *-- POutputFile
POutputFile *-- PInputFile

@enduml
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
class PProject {
}

class PBatch {
}

class PExecution {
}

class PStep {
}

class PInputFile {
}

class POutputFile {
}

PProject *-- PBatch : 
PBatch *-- PExecution : 
PExecution *-- PStep : 
PExecution *-- PInputFile : 
PExecution *-- POutputFile : 
POutputFile *-- PInputFile : 

skinparam classAttributeIconSize 0
hide circle
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 10
skinparam class {
  BackgroundColor White
  BorderColor Black
  ArrowColor Black
}
skinparam note {
  BackgroundColor White
  BorderColor Black
}
skinparam mindmap {
  BackgroundColor White
  BorderColor Black
}
skinparam component {
  BackgroundColor White
  BorderColor Black
}
skinparam actor {
  BackgroundColor White
  BorderColor Black
}
skinparam usecase {
  BackgroundColor White
  BorderColor Black
}
skinparam card {
  BackgroundColor White
  BorderColor Black
}
skinparam state {
  BackgroundColor White
  BorderColor Black
}
skinparam participant {
  BackgroundColor White
  BorderColor Black
}
skinparam agent {
  BackgroundColor White
  BorderColor Black
}
skinparam database {
  BackgroundColor White
  BorderColor Black
}
skinparam folder {
  BackgroundColor White
  BorderColor Black
```

#### `f8525f10938208a65f6de3e1a78e31a16a4deb67` — compile_fail (sequence, tier 3)

- CSR: `Error line 16 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/f8525f10938208a65f6de3e1a78e31a16a4deb67.puml`
- Element: tp=0 fp=0 fn=9 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=21 F1=0.000; missed: message
- chrF++: 64.61
- Files: GT `data/puml_files/f8525f10938208a65f6de3e1a78e31a16a4deb67.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/f8525f10938208a65f6de3e1a78e31a16a4deb67.puml` (yes) · input `data/puml_images_1568/f8525f10938208a65f6de3e1a78e31a16a4deb67.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/f8525f10938208a65f6de3e1a78e31a16a4deb67.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: f8525f10938208a65f6de3e1a78e31a16a4deb67
' Original Path: /Project/docs/Sprint3/US029/US029-SD-Reengenharia-v2.puml
' Source: World of Code

@startuml

title US029 - As Project Manager, I want to start a sprint.

autoactivate on
'autonumber

actor "Project Manager" as projectManager
participant ": StartSprintRoute" as UI
participant ": StartSprintController" as Ctrl
participant ": StartSprintService" as startSprintService
participant "dto : SprintDTO" as sprintDTO
participant " : Project" as project
participant " : SprintDomainService" as sprintDomainService
participant " : SprintStore" as sprintStore
participant " : ResourceStore" as resourceStore


activate projectManager


projectManager -> UI: Asks to start a Sprint
UI --> Ctrl: startSprint(sprintDTO)
Ctrl -> startSprintService: startSprint(sprintDTO)
startSprintService -> project: getProjectTeam()
project --> startSprintService: projectTeam
startSprintService -> project: getSprintDuration()
project --> startSprintService: sprintDuration
startSprintService -> sprintStore: startSprint(dto.projectID, dto.sprintID, dto.startDate, \n projectTeam, sprintDuration)
sprintStore -> sprintStore: findAllSprintByProjectID (projectID)
deactivate
sprintStore -> sprintStore: findSprintByID (sprintID)
deactivate
sprintStore -> sprintDomainService: validateStartDate(startDate)
sprintDomainService --> sprintStore: true
resourceStore -> sprintDomainService: validateProjectTeam(startDate, sprintDuration)
sprintDomainService -> sprintDomainService: getProductOwnerByStartDate(startDate, sprintDuration)
deactivate
sprintDomainService -> sprintDomainService: getScrumMasterByStartDate(startDate, sprintDuration)
deactivate
sprintDomainService --> sprintStore: true
sprintStore -> sprintStore: setStartDate(startDate)
deactivate
sprintStore --> startSprintService: true
startSprintService --> Ctrl: true
Ctrl --> UI: true
UI --> projectManager: Informs Operation Success
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title US029 – As Project Manager, I want to start a sprint.

actor "Project Manager" as PM
participant "StartSprintRoute" as Route
participant "StartSprintController" as Controller
participant "StartSprintService" as Service
participant "dto : SprintDTO" as DTO
participant ": Project" as Project
participant ": SprintDomainService" as DomainService
participant ": SprintStore" as Store
participant ": ResourceStore" as ResStore

PM -> Route: Asks to start a Sprint
activate Route
Route ..> Controller: startSprint(sprintDTO)
deactivate Route
activate Controller
Controller -> Service: startSprint(sprintDTO)
activate Service
Service -> Project: getProjectTeam()
activate Project
Project ..> Service: projectTeam
deactivate Project
Service -> Project: getSprintDuration()
activate Project
Project ..> Service: sprintDuration
deactivate Project
Service -> Store: startSprint(dto.projectID, dto.sprintID, dto.startDate,\nprojectTeam, sprintDuration)
activate Store
Store -> Store: findAllSprintByProjectID (projectID)
activate Store
deactivate Store
Store -> Store: findSprintByID (sprintID)
activate Store
deactivate Store
Store -> DomainService: validateStartDate(startDate)
activate DomainService
DomainService ..> Store: true
deactivate DomainService
Store -> ResStore: validateProjectTeam(startDate, sprintDuration)
activate ResStore
ResStore -> ResStore: getProductOwnerByStartDate(startDate, sprintDuration)
activate ResStore
deactivate ResStore
ResStore -> ResStore: getScrumMasterByStartDate(startDate, sprintDuration)
activate ResStore
deactivate ResStore
ResStore ..> Store: true
deactivate ResStore
Store -> Store: setStartDate(startDate)
activate Store
deactivate Store
Store ..> Service: true
deactivate Store
deactivate Service
Controller ..> Route: true
deactivate Controller
Route ..> PM: Informs Operation Success
@enduml
```
```

#### `ffd0a552b452557d64ae34c6f0baa93f1b97ef47` — compile_fail (sequence, tier 2)

- CSR: `Error line 19 in file: data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/extracted/ffd0a552b452557d64ae34c6f0baa93f1b97ef47.puml`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=8 F1=0.000; missed: message
- chrF++: 38.37
- Files: GT `data/puml_files/ffd0a552b452557d64ae34c6f0baa93f1b97ef47.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/ffd0a552b452557d64ae34c6f0baa93f1b97ef47.puml` (yes) · input `data/puml_images_1568/ffd0a552b452557d64ae34c6f0baa93f1b97ef47.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/ffd0a552b452557d64ae34c6f0baa93f1b97ef47.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: ffd0a552b452557d64ae34c6f0baa93f1b97ef47
' Original Path: /uml/demo/design/scm/新流程/欧美区印度区-运单路由流程-新.puml
' Source: World of Code

@startuml
actor Time
control tradecenter as xman
control wms
boundary 合作商仓储系统 as TPL
boundary Aftership

autonumber 10 10 "<b>[000]"
TPL --> wms: 回传发货信息imei运单号等
wms --> wms: 生成运单信息
Time --> wms: 定时推送运单
wms --> Aftership: 推送运单至aftership
Aftership --> wms: 推送路由轨迹信息
wms --> wms: 轨迹处理和封装
wms --> wms: 记录运单信息更新状态

alt 路由最终状态
    autonumber resume "<font color=red><b> [000]  "
    wms --> xman: 通知订单发货单的路由状态
else 非最终状态
end
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title 运单推送与轨迹更新流程

actor "Time" as Time
participant "tradecenter" as TC
participant "wms" as WMS
boundary "合作商仓储系统" as PartnerWMS
boundary "Aftership" as Aftership

== 发货信息回传 ==
PartnerWMS ->> WMS: [010] 回传发货信息imei运单号等

== 运单生成与推送 ==
activate WMS
WMS ->> WMS: [020] 生成运单信息
deactivate WMS

activate Time
Time -x> WMS: [030] 定时推送运单
deactivate Time

activate WMS
WMS -x> Aftership: [040] 推送运单至aftership
deactivate WMS

== 轨迹信息处理 ==
activate Aftership
Aftership -x> WMS: [050] 推送路由轨迹信息
deactivate Aftership

activate WMS
WMS ->> WMS: [060] 轨迹处理和封装
WMS ->> WMS: [070] 记录运单信息更新状态
deactivate WMS

== 状态通知 ==
alt 路由最终状态
    WMS -x> TC: [080] 通知订单发货单的路由状态
else 非最终状态
end alt

@enduml
```
```

#### outcome: compiled_low_structural

#### `013f262fafb9cce412d05966af0aca59982ed3f2` — compiled_low_structural (class, tier 4)

- Element: tp=11 fp=17 fn=6 F1=0.489; type-acc matched=11 correct=9 excluded=0
- Relationship: tp=0 fp=26 fn=18 F1=0.000; missed: inheritance, composition, aggregation, association; extra: inheritance, dependency
- chrF++: 42.94
- Files: GT `data/puml_files/013f262fafb9cce412d05966af0aca59982ed3f2.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/013f262fafb9cce412d05966af0aca59982ed3f2.puml` (yes) · input `data/puml_images_1568/013f262fafb9cce412d05966af0aca59982ed3f2.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/013f262fafb9cce412d05966af0aca59982ed3f2.png` (yes)

#### `0b185a3b2c5e97ab0a5a8e498f41117b5d8a0c04` — compiled_low_structural (sequence, tier 4)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=0 fp=0 fn=34 F1=0.000; missed: message
- chrF++: 36.50
- Files: GT `data/puml_files/0b185a3b2c5e97ab0a5a8e498f41117b5d8a0c04.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/0b185a3b2c5e97ab0a5a8e498f41117b5d8a0c04.puml` (yes) · input `data/puml_images_1568/0b185a3b2c5e97ab0a5a8e498f41117b5d8a0c04.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/0b185a3b2c5e97ab0a5a8e498f41117b5d8a0c04.png` (yes)

#### `18a145261879ea7d3dcb19eeaa0efb33e36d678c` — compiled_low_structural (sequence, tier 3)

- Element: tp=2 fp=4 fn=4 F1=0.333; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=10 fn=10 F1=0.000; missed: message; extra: message
- chrF++: 55.17
- Files: GT `data/puml_files/18a145261879ea7d3dcb19eeaa0efb33e36d678c.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/18a145261879ea7d3dcb19eeaa0efb33e36d678c.puml` (yes) · input `data/puml_images_1568/18a145261879ea7d3dcb19eeaa0efb33e36d678c.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/18a145261879ea7d3dcb19eeaa0efb33e36d678c.png` (yes)

#### `40e703ca80bef393871251b173d566585f60dd37` — compiled_low_structural (class, tier 3)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=4 excluded=0
- Relationship: tp=0 fp=4 fn=4 F1=0.000; missed: inheritance; extra: inheritance, dependency
- chrF++: 75.34
- Files: GT `data/puml_files/40e703ca80bef393871251b173d566585f60dd37.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/40e703ca80bef393871251b173d566585f60dd37.puml` (yes) · input `data/puml_images_1568/40e703ca80bef393871251b173d566585f60dd37.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/40e703ca80bef393871251b173d566585f60dd37.png` (yes)

#### `4788cbabec3c97afb5ecc1f2ea825d8e9bcd1461` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=3 fn=3 F1=0.250; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=9 fn=9 F1=0.000; missed: message; extra: message
- chrF++: 41.62
- Files: GT `data/puml_files/4788cbabec3c97afb5ecc1f2ea825d8e9bcd1461.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/4788cbabec3c97afb5ecc1f2ea825d8e9bcd1461.puml` (yes) · input `data/puml_images_1568/4788cbabec3c97afb5ecc1f2ea825d8e9bcd1461.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/4788cbabec3c97afb5ecc1f2ea825d8e9bcd1461.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 4788cbabec3c97afb5ecc1f2ea825d8e9bcd1461
' Original Path: /WebPult/WebZulu/documents/UML/Validation_Tocken.puml
' Source: World of Code

@startuml

title <b><size:45>Validation Tocken</size></b>

participant "RemoteServiceServlet" as rss << (C, #ADD1B2) >>
participant "HttpSessionCollector" as hsc << (C, #ADD1B2) >>
participant "SysLog" as sl << (L, Orange) >>

[-[#Green]> rss: Data Request
activate rss
	
	rss -[#Green]> rss: Get Session ID_client
	
        rss -[#Green]> hsc: Get Session by ID_client
	activate hsc
	hsc -[#Green]> rss: Session
	deactivate hsc
	
	rss -[#Green]> rss: <b><color:#777777> Validation Tockens </color></b> \n <b><color:#Green> True </color></b>
	activate rss #Green
		create Validation_User
		rss -[#Green]> Validation_User : Access success
	deactivate rss
	
	rss -[#Red]> rss: <b><color:#777777> Validation Tockens </color></b> \n <b><color:#Red> False </color></b>
	activate rss #Red
		rss -[#Orange]> sl : Tocken Failure (Name, Time)
		[<[#Red]- rss: Access denied
	deactivate rss
	
deactivate rss

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
title Validation Tocken

actor "RemoteServiceServlet" as RemoteServiceServlet
participant "HttpSessionCollector" as HttpSessionCollector
participant "SysLog" as SysLog
participant "Validation_User" as Validation_User

activate RemoteServiceServlet

RemoteServiceServlet -> RemoteServiceServlet: Data Request
RemoteServiceServlet -> RemoteServiceServlet: Get Session ID_client
RemoteServiceServlet -> HttpSessionCollector: Get Session by ID_client
activate HttpSessionCollector
HttpSessionCollector --> RemoteServiceServlet: Session
deactivate HttpSessionCollector

alt Validation Tocken = True
    RemoteServiceServlet -> RemoteServiceServlet: Access success
    RemoteServiceServlet -> Validation_User: Access success
else Validation Tocken = False
    RemoteServiceServlet -> RemoteServiceServlet: Tocken Failure (Name, Time)
    RemoteServiceServlet -> SysLog: Tocken Failure (Name, Time)
    RemoteServiceServlet --> RemoteServiceServlet: Access denied
end

deactivate RemoteServiceServlet

@enduml
```
```

#### `578f8ee18ea64ed4e206fa31c1e5aa0fe694e69f` — compiled_low_structural (class, tier 2)

- Element: tp=2 fp=0 fn=2 F1=0.667; type-acc matched=2 correct=1 excluded=0
- Relationship: tp=1 fp=2 fn=2 F1=0.333; missed: inheritance; extra: inheritance
- chrF++: 57.50
- Files: GT `data/puml_files/578f8ee18ea64ed4e206fa31c1e5aa0fe694e69f.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/578f8ee18ea64ed4e206fa31c1e5aa0fe694e69f.puml` (yes) · input `data/puml_images_1568/578f8ee18ea64ed4e206fa31c1e5aa0fe694e69f.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/578f8ee18ea64ed4e206fa31c1e5aa0fe694e69f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 578f8ee18ea64ed4e206fa31c1e5aa0fe694e69f
' Original Path: /Forelesning17_Uke11_JSON_Collections/AfterLecture/01_FilSkriving_JSON/src/main/resources/klasser.puml
' Source: World of Code

@startuml

abstract class Klasse {
    navn: String
    beskrivelse: String
    terning: int
}

Klasse <|-- Trollmann
Klasse <|-- Barbar
Klasse <-- Karakter

class Karakter {
    navn: String
    klasse : Klasse
    level: int
}

class Barbar {
    raseriAnfall: int
}

class Trollmann {
    trylleformler: ArrayList<String>
}

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
class "Klasse" as A {
    +navn: String
    +beskrivelse: String
    +terning: int
}

class "Trollmann" as C {
    +trylleformler: ArrayList<String>
}

class "Barbar" as C {
    +raseriAnfall: int
}

class "Karakter" as C {
    +navn: String
    +klasse : Klasse
    +level: int
}

C --|> A
C --|> A
C --> A

skinparam classAttributeIconSize 0
@enduml
```
```

#### `7be4f7f9591cb2862f012abdc29a495a70c77fee` — compiled_low_structural (class, tier 3)

- Element: tp=8 fp=0 fn=0 F1=1.000; type-acc matched=8 correct=0 excluded=0
- Relationship: tp=0 fp=12 fn=13 F1=0.000; missed: inheritance, association; extra: inheritance, dependency, association
- chrF++: 44.44
- Files: GT `data/puml_files/7be4f7f9591cb2862f012abdc29a495a70c77fee.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/7be4f7f9591cb2862f012abdc29a495a70c77fee.puml` (yes) · input `data/puml_images_1568/7be4f7f9591cb2862f012abdc29a495a70c77fee.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/7be4f7f9591cb2862f012abdc29a495a70c77fee.png` (yes)

#### `7f03d6628c26b835983153776640390596fedf5b` — compiled_low_structural (sequence, tier 2)

- Element: tp=4 fp=0 fn=0 F1=1.000; type-acc matched=4 correct=0 excluded=0
- Relationship: tp=0 fp=10 fn=10 F1=0.000; missed: message; extra: association
- chrF++: 53.13
- Files: GT `data/puml_files/7f03d6628c26b835983153776640390596fedf5b.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/7f03d6628c26b835983153776640390596fedf5b.puml` (yes) · input `data/puml_images_1568/7f03d6628c26b835983153776640390596fedf5b.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/7f03d6628c26b835983153776640390596fedf5b.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 7f03d6628c26b835983153776640390596fedf5b
' Original Path: /docs/blue/1150344/sp3/analysis2.puml
' Source: World of Code

@startuml
skinparam handwritten false
skinparam monochrome true
skinparam packageStyle rect
skinparam defaultFontName FG Virgil
skinparam shadowing false

actor SuperUser

SuperUser -> Browser : navigate to profile
 
Browser ->> Server : loadAllUsers()

database Database 

Server -> Database : fetch

Server -->> Browser : return

Browser -> Browser : display

SuperUser -> Browser : enable/disable user

Browser ->> Server : changeStatus(user)

Server -> Database : save

Server -->> Browser : return

Browser -> Browser : display

@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "SuperUser" as user
rectangle "Browser" as browser
rectangle "Server" as server
database "Database" as db

user -> browser : navigate to profile
browser -> server : loadAllUsers()
server -> db : fetch
db -->> server : return
browser -> browser : display

user -> browser : enable/disable user
browser -> server : changeStatus(user)
server -> db : save
db -->> server : return
browser -> browser : display

@enduml
```
```

#### `8b3d0798463a9167895a0489a54bc9fae4cc6736` — compiled_low_structural (sequence, tier 1)

- Element: tp=2 fp=2 fn=0 F1=0.667; type-acc matched=2 correct=0 excluded=0
- Relationship: tp=0 fp=2 fn=1 F1=0.000; missed: message; extra: dependency
- chrF++: 42.39
- Files: GT `data/puml_files/8b3d0798463a9167895a0489a54bc9fae4cc6736.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/8b3d0798463a9167895a0489a54bc9fae4cc6736.puml` (yes) · input `data/puml_images_1568/8b3d0798463a9167895a0489a54bc9fae4cc6736.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/8b3d0798463a9167895a0489a54bc9fae4cc6736.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 8b3d0798463a9167895a0489a54bc9fae4cc6736
' Original Path: /example.puml
' Source: World of Code

@startuml
lice -> Bob: 日本語
@enduml
```

Prediction PlantUML:
```plantuml
```@startuml
class "lice" as C1
class "Bob" as C2
class "lice" as C3
class "Bob" as C4

C1 ..> C3 : 日本語
C2 ..> C4 : 日本語

@enduml
```
```

#### `9dcbe3ca2a480347bdc97c962c0f9ac2c349f1c5` — compiled_low_structural (sequence, tier 3)

- Element: tp=0 fp=5 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=11 fn=8 F1=0.000; missed: message; extra: dependency, association
- chrF++: 77.04
- Files: GT `data/puml_files/9dcbe3ca2a480347bdc97c962c0f9ac2c349f1c5.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/9dcbe3ca2a480347bdc97c962c0f9ac2c349f1c5.puml` (yes) · input `data/puml_images_1568/9dcbe3ca2a480347bdc97c962c0f9ac2c349f1c5.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/9dcbe3ca2a480347bdc97c962c0f9ac2c349f1c5.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 9dcbe3ca2a480347bdc97c962c0f9ac2c349f1c5
' Original Path: /ssi/certified-gs1-ids-1-GCP.plantuml
' Source: World of Code

@startuml
skinparam responseMessageBelowArrow true

actor "did:...:GS1" as GS1
actor "did:...:Manufacturer" as Manufacturer

group Ausstellungsprozess der GCP
    Manufacturer -> GS1 : GCP Anfrage
    GS1 -> Manufacturer : Berechtigung Prüfen
    GS1 -> Manufacturer : ISSUE
    note right of GS1
        <b>GCP Credential</b>
        gcp: 4047111
    end note
    Manufacturer -> Manufacturer : ISSUE
    note right of GS1
        <b>Party GLN Credential</b>
        urn:epc:id:pgln:4047111.00000
    end note
end

group Ausstellungsprozess zertifizierter Stammdaten
    Manufacturer -> GS1 : PRESENT GCP
    Manufacturer -> GS1 : Anfrage + Nachweis der Stammdaten
    GS1 -> GS1: Prüfung der Stammdaten basierend auf\nDokumenten oder eigener Recherche
    
    GS1 -> Manufacturer : ISSUE
    note right of GS1
        <b>Stammdaten Credential (e.g.)</b>
        name: European EPC Competence Center,
        legal_form: GmbH,
        trade_register_number: Köln HBR 61026,
        . . .
    end note
end
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
skinparam sequence {
  ArrowColor Black
  ActorBorderColor Black
  ActorBackgroundColor LightGray
  LifeLineBorderColor Black
  LifeLineBackgroundColor White
}

actor "did:....GS1" as GS1
actor "did:....Manufacturer" as Manufacturer

rectangle "Ausstellungsprozess der GCP" {
  Manufacturer -> GS1 : GCP Anfrage
  GS1 -> Manufacturer : Berechtigung Prüfen
  GS1 -> Manufacturer : ISSUE
  note right of GS1: GCP Credential\ngcp: 4047111
  Manufacturer -> Manufacturer : ISSUE
  note left of Manufacturer: Party GLN Credential\nurn:epc:id:pgln:4047111.00000
}

rectangle "Ausstellungsprozess zertifizierter Stammdaten" {
  Manufacturer -> GS1 : PRESENT GCP
  Manufacturer -> GS1 : Anfrage + Nachweis der Stammdaten
  GS1 -> GS1 : Prüfung der Stammdaten basierend auf Dokumenten oder eigener Recherche
  GS1 -> Manufacturer : ISSUE
  note right of GS1: Stammdaten Credential (e.g.)\nname: European EPC Competence Center,\nlegal_form: GmbH,\ntrade_register_number: Köln HBR 61026,\n...
}

@enduml
```
```

#### `a33039e4fbdeb76d8d991f13075eb6aabf979e31` — compiled_low_structural (class, tier 2)

- Element: tp=0 fp=1 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 50.16
- Files: GT `data/puml_files/a33039e4fbdeb76d8d991f13075eb6aabf979e31.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/a33039e4fbdeb76d8d991f13075eb6aabf979e31.puml` (yes) · input `data/puml_images_1568/a33039e4fbdeb76d8d991f13075eb6aabf979e31.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/a33039e4fbdeb76d8d991f13075eb6aabf979e31.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: a33039e4fbdeb76d8d991f13075eb6aabf979e31
' Original Path: /northernwind/1.2-ALPHA-10/apidocs/it/tidalwave/northernwind/frontend/ui/component/gallery/spi/GalleryAdapter.puml
' Source: World of Code

@startuml
    set namespaceSeparator none
    hide empty fields
    hide empty methods

    interface "<size:14>GalleryAdapter\n<size:10>it.tidalwave.northernwind.frontend.ui.component.gallery.spi" as it.tidalwave.northernwind.frontend.ui.component.gallery.spi.GalleryAdapter [[GalleryAdapter.html]] {
        {abstract} +getExtraViewProperties(Id): ResourceProperties
        {abstract} +getInlinedScript(): String
        {abstract} +prepareCatalog(List<? extends GalleryItem>): void
        {abstract} +prepareGallery(GalleryItem, List<? extends GalleryItem>): void
        {abstract} +prepareFallbackGallery(GalleryItem, List<? extends GalleryItem>): void
        {abstract} +prepareFallbackLightbox(List<? extends GalleryItem>): void
        {abstract} +render(RenderContext): void
    }

    center footer UMLDoclet 2.0.12, PlantUML 1.2020.16
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
interface GalleryAdapter {
    + getExtraViewProperties(Id): ResourceProperties
    + getInlinedScript(): String
    + prepareCatalog(List<? extends GalleryItem>): void
    + prepareGallery(GalleryItem, List<? extends GalleryItem>): void
    + prepareFallbackGallery(GalleryItem, List<? extends GalleryItem>): void
    + prepareFallbackLightbox(List<? extends GalleryItem>): void
    + render(RenderContext): void
}
@enduml
```
```

#### `ac4ce0ed5d931589d8926d76d4481f9cd2bcaef6` — compiled_low_structural (class, tier 1)

- Element: tp=2 fp=0 fn=0 F1=1.000; type-acc matched=2 correct=2 excluded=0
- Relationship: tp=0 fp=1 fn=1 F1=0.000; missed: aggregation; extra: aggregation
- chrF++: 46.44
- Files: GT `data/puml_files/ac4ce0ed5d931589d8926d76d4481f9cd2bcaef6.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/ac4ce0ed5d931589d8926d76d4481f9cd2bcaef6.puml` (yes) · input `data/puml_images_1568/ac4ce0ed5d931589d8926d76d4481f9cd2bcaef6.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/ac4ce0ed5d931589d8926d76d4481f9cd2bcaef6.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: ac4ce0ed5d931589d8926d76d4481f9cd2bcaef6
' Original Path: /exercise41/docs/NameSorter.puml
' Source: World of Code

@startuml

class Solution41 {
    +main(String[])
    ' NameSorter ns = new NameSorter()
    ' ArrayList<String> names = ns.readNames()
    ' ns.sortNames(names)
    ' ns.writeNames(names)
}

class NameSorter {
    -ArrayList<String> names;

    ' init name list
    ' store values from readNames() in name list
    ' sort the name list
    ' use writeNames to write the list
    +readNames(String fileName)
    +sortNames()
    +writeNames(String fileName)
}

Solution41 --o NameSorter

@enduml
```

Prediction PlantUML:
```plantuml
```
@startuml
class Solution41 {
    +main(String[])
}

class NameSorter {
    -ArrayList<String> names
    +readNames(String fileName)
    +sortNames()
    +writeNames(String fileName)
}

Solution41 o-- NameSorter : aggregation
@enduml
```
```

#### `b98c5fc6649e2bb3ceff143dbc060d141396ff62` — compiled_low_structural (sequence, tier 4)

- Element: tp=14 fp=2 fn=1 F1=0.903; type-acc matched=14 correct=13 excluded=0
- Relationship: tp=2 fp=120 fn=96 F1=0.018; missed: message; extra: message
- chrF++: 46.78
- Files: GT `data/puml_files/b98c5fc6649e2bb3ceff143dbc060d141396ff62.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/b98c5fc6649e2bb3ceff143dbc060d141396ff62.puml` (yes) · input `data/puml_images_1568/b98c5fc6649e2bb3ceff143dbc060d141396ff62.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/b98c5fc6649e2bb3ceff143dbc060d141396ff62.png` (yes)

#### `ba9090f76db6fbde5872bc8f24d23e890049aca6` — compiled_low_structural (sequence, tier 1)

- Element: tp=3 fp=3 fn=0 F1=0.667; type-acc matched=3 correct=0 excluded=0
- Relationship: tp=0 fp=6 fn=4 F1=0.000; missed: message; extra: association
- chrF++: 73.31
- Files: GT `data/puml_files/ba9090f76db6fbde5872bc8f24d23e890049aca6.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/ba9090f76db6fbde5872bc8f24d23e890049aca6.puml` (yes) · input `data/puml_images_1568/ba9090f76db6fbde5872bc8f24d23e890049aca6.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/ba9090f76db6fbde5872bc8f24d23e890049aca6.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: ba9090f76db6fbde5872bc8f24d23e890049aca6
' Original Path: /springboot-mybatis-demo2/aop代理对象生成过程分析.puml
' Source: World of Code

@startuml
Actor actor

Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: another authentication Response
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
actor "actor" as A1
rectangle "Alice" as Alice
rectangle "Bob" as Bob

A1 -[hidden]down-> Alice
Alice -> Bob : Authentication Request
Bob --> Alice : Authentication Response
Alice -> Bob : Another authentication Request
Bob --> Alice : another authentication Response

rectangle "Alice" as Alice2
rectangle "Bob" as Bob2
actor "actor" as A2

A2 -[hidden]up-> Alice2
@enduml
```
```

#### `baf5a2b62c2e718307ef947700d775b69f4a2f61` — compiled_low_structural (class, tier 4)

- Element: tp=22 fp=0 fn=0 F1=1.000; type-acc matched=22 correct=22 excluded=0
- Relationship: tp=6 fp=16 fn=21 F1=0.245; missed: composition, dependency, association; extra: dependency, association
- chrF++: 59.14
- Files: GT `data/puml_files/baf5a2b62c2e718307ef947700d775b69f4a2f61.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/baf5a2b62c2e718307ef947700d775b69f4a2f61.puml` (yes) · input `data/puml_images_1568/baf5a2b62c2e718307ef947700d775b69f4a2f61.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/baf5a2b62c2e718307ef947700d775b69f4a2f61.png` (yes)

#### `fcd65f7d8920511a96fcffe53538f6014bb6f64f` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=2 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=1 fn=1 F1=0.000; missed: inheritance; extra: inheritance
- chrF++: 16.98
- Files: GT `data/puml_files/fcd65f7d8920511a96fcffe53538f6014bb6f64f.puml` (yes) · pred `data/runs/Qwen_Qwen3.5-27B_20260613T202731Z/fcd65f7d8920511a96fcffe53538f6014bb6f64f.puml` (yes) · input `data/puml_images_1568/fcd65f7d8920511a96fcffe53538f6014bb6f64f.png` (yes) · render `data/csr/Qwen_Qwen3.5-27B_20260613T202731Z/png/fcd65f7d8920511a96fcffe53538f6014bb6f64f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: fcd65f7d8920511a96fcffe53538f6014bb6f64f
' Original Path: /northernwind/1.2-ALPHA-10/it-tidalwave-northernwind-modules/it-tidalwave-northernwind-core-default/testapidocs/it/tidalwave/northernwind/frontend/ui/spi/mock/MockRequestProcessor3.puml
' Source: World of Code

@startuml
    set namespaceSeparator none
    hide empty fields
    hide empty methods

    class "<size:14>MockRequestProcessor3\n<size:10>it.tidalwave.northernwind.frontend.ui.spi.mock" as it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessor3 [[MockRequestProcessor3.html]]

    class "<size:14>MockRequestProcessorSupport\n<size:10>it.tidalwave.northernwind.frontend.ui.spi.mock" as it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessorSupport [[MockRequestProcessorSupport.html]]

    it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessorSupport <|-- it.tidalwave.northernwind.frontend.ui.spi.mock.MockRequestProcessor3

    center footer UMLDoclet 2.0.12, PlantUML 1.2020.16
@enduml
```

Prediction PlantUML:
```plantuml
```plantuml
@startuml
class MockRequestProcessorSupport {
}

class MockRequestProcessor3 {
}

MockRequestProcessor3 --|> MockRequestProcessorSupport
@enduml
```
```

### Qwen3.5-397B-A17B

#### outcome: compile_fail

#### `2830a2eabd8ada9ad42a0d10eeeacad0dc53a202` — compile_fail (sequence, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=14 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=40 F1=0.000; missed: message
- chrF++: 12.16
- Files: GT `data/puml_files/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.puml` (yes) · input `data/puml_images_1568/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/2830a2eabd8ada9ad42a0d10eeeacad0dc53a202.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 2830a2eabd8ada9ad42a0d10eeeacad0dc53a202
' Original Path: /.models/api/openc2/sequences-proxy.plantuml
' Source: World of Code

@startuml

!pragma teoz true

skinparam sequenceArrowThickness 2
skinparam roundcorner 20
skinparam maxmessagesize 200


skinparam ParticipantPadding 30
skinparam BoxPadding 30
skinparam SequenceBoxBackgroundColor AliceBlue
skinparam ActorBorderColor SaddleBrown
skinparam sequenceMessageAlign left

box Upstream
participant "Producer" as UpstreamProducer << (C,#ADD1B2) >> order 0
participant "Adapter" as UpstreamProducerAdapter << (C,#ADD1B2) >> order 1
end box

participant "Tansport" as UpstreamTransport << (S, LightBlue) >> order 2

box "Gateway"
participant "Adapter" as GatewayConsumerAdapter << (C,#ADD1B2) >> order 3
participant "Consumer" as GatewayConsumer << (C,#ADD1B2) >> order 4
box JobExecution #LightCyan
participant GatewayJobHandler << (C,#ADD1B2) >> order 5
end box
participant "Gateway" as Gateway << (C,#ADD1B2) >> order 6
participant "Producer" as GatewayProducer << (C,#ADD1B2) >> order 7
participant "Adapter" as GatewayProducerAdapter << (C,#ADD1B2) >> order 8
end box

participant "Tansport" as DownstreamTransport << (S, LightBlue) >> order 9

box Downstream
participant "Adapter" as DownstreamConsumerAdapter << (C,#ADD1B2) >> order 10
participant "Consumer" as DownstreamConsumer << (C,#ADD1B2) >> order 11
end box

box JobExecution #LightCyan
participant DownstreamJobHandler << (C,#ADD1B2) >> order 12
end box

participant "Lower Layer" as Lower << (S, LightBlue) >> order 13


activate UpstreamProducer
UpstreamProducer -> UpstreamProducerAdapter : publish(command)
activate UpstreamProducerAdapter
UpstreamProducerAdapter -> UpstreamTransport : publish(command)
UpstreamTransport -> GatewayConsumerAdapter: execute(command)
UpstreamTransport -> UpstreamProducerAdapter : resolves()
activate GatewayConsumerAdapter
& GatewayConsumerAdapter -> GatewayConsumer : handler(command, done)
activate GatewayConsumer
create GatewayJobHandler
GatewayConsumer --> GatewayJobHandler : subscribe("done")
activate GatewayJobHandler
& UpstreamProducerAdapter -> UpstreamProducer : resolves()
GatewayConsumer --> Gateway : emit("command", GatewayJobHandler)
activate Gateway
& {UpstreamStart} UpstreamProducer -> UpstreamProducerAdapter : subscribe(handler)
UpstreamProducerAdapter -> UpstreamTransport : subscribe("response")
& Gateway -> GatewayProducer : publish(command)
activate GatewayProducer
GatewayProducer -> GatewayProducerAdapter : publish(command)
activate GatewayProducerAdapter
GatewayProducerAdapter -> DownstreamTransport : publish(command)
DownstreamTransport -> DownstreamConsumerAdapter: execute(command)
DownstreamTransport -> GatewayProducerAdapter : resolves()
activate DownstreamConsumerAdapter
& DownstreamConsumerAdapter -> DownstreamConsumer : handler(command, done)
activate DownstreamConsumer
create DownstreamJobHandler
DownstreamConsumer --> DownstreamJobHandler : subscribe("done")
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
skinparam sequence {
    ArrowColor #333333
    ArrowThickness 1
    LifeLineBorderColor #CCCCCC
    LifeLineBackgroundColor #FFFFFF
    ParticipantBorderColor #CCCCCC
    ParticipantBackgroundColor #F5F5F5
    ParticipantPadding 10
    BoxPadding 10
    NoteBackgroundColor #FFFFCC
    NoteBorderColor #CCCCCC
}

skinparam packageStyle rectangle
skinparam rectangle {
    BackgroundColor<<Group>> #E6F3FF
    BorderColor #99CCFF
}

skinparam actor {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam database {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam interface {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam participant {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam control {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam entity {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam boundary {
    BackgroundColor #FFFFFF
    BorderColor #333333
}

skinparam note {
    BackgroundColor #FFFFCC
    BorderColor #CCCCCC
}

skinparam legend {
    BackgroundColor #FFFFFF
    BorderColor #CCCCCC
}

skinparam title {
    FontSize 16
    FontColor #333333
}

skinparam header {
    FontSize 14
    FontColor #333333
}

skinparam footer {
    FontSize 12
    FontColor #666666
}
```

#### `3b84f043b6bebeb57b16145d55b6be38a244e0be` — compile_fail (class, tier 3)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: inheritance, aggregation
- chrF++: 4.15
- Files: GT `data/puml_files/3b84f043b6bebeb57b16145d55b6be38a244e0be.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/3b84f043b6bebeb57b16145d55b6be38a244e0be.puml` (yes) · input `data/puml_images_1568/3b84f043b6bebeb57b16145d55b6be38a244e0be.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/3b84f043b6bebeb57b16145d55b6be38a244e0be.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 3b84f043b6bebeb57b16145d55b6be38a244e0be
' Original Path: /Homework/Android/homework/Simple Chat/src/main/java/com/example/simple_chat/recycler_view_adapter/recycler_view_adapter.plantuml
' Source: World of Code

@startuml

title __RECYCLER_VIEW_ADAPTER's Class Diagram__\n

  namespace com.example.simple_chat {
    namespace recycler_view_adapter {
      class com.example.simple_chat.recycler_view_adapter.ChatAdapter {
          + mData : List<RecordInfo>
          - headerOfMy : Bitmap
          - headerOfSystem : Bitmap
          - intent : Intent
          - mapOfImage : HashMap<String, Bitmap>
          - settingInfo : SharedPreferences
          + ChatAdapter()
          + getItemCount()
          + getItemViewType()
          + onBindViewHolder()
          + onCreateViewHolder()
          + updateHeader()
          - setHeaderImage()
      }
    }
  }
  

  com.example.simple_chat.recycler_view_adapter.ChatAdapter -up-|> androidx.recyclerview.widget.RecyclerView.Adapter
  com.example.simple_chat.recycler_view_adapter.ChatAdapter o-- com.example.simple_chat.MyService.MusicInfoBinder : binder


right footer


PlantUML diagram generated by SketchIt! (https://bitbucket.org/pmesmeur/sketch.it)
For more information about this tool, please contact philippe.mesmeur@gmail.com
endfooter

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
title RECYCLER_VIEW_ADAPTER's Class Diagram
skinparam packageStyle rectangle
skinparam classAttributeIconSize 0
skinparam classBackgroundColor #F0F0F0
skinparam classBorderColor #000000
skinparam classFontColor #000000
skinparam classFontName Arial
skinparam classFontSize 12
skinparam classStereotypeFontColor #000000
skinparam classStereotypeFontName Arial
skinparam classStereotypeFontSize 12
skinparam classStereotypeFontStyle bold
skinparam classStereotypeFontStyle italic
skinparam classStereotypeFontStyle underline
skinparam classStereotypeFontStyle strikethrough
skinparam classStereotypeFontStyle overline
skinparam classStereotypeFontStyle blink
skinparam classStereotypeFontStyle shadow
skinparam classStereotypeFontStyle outline
skinparam classStereotypeFontStyle fill
skinparam classStereotypeFontStyle gradient
skinparam classStereotypeFontStyle radial
skinparam classStereotypeFontStyle linear
skinparam classStereotypeFontStyle conic
skinparam classStereotypeFontStyle diamond
skinparam classStereotypeFontStyle square
skinparam classStereotypeFontStyle circle
skinparam classStereotypeFontStyle triangle
skinparam classStereotypeFontStyle star
skinparam classStereotypeFontStyle heart
skinparam classStereotypeFontStyle cross
skinparam classStereotypeFontStyle plus
skinparam classStereotypeFontStyle minus
skinparam classStereotypeFontStyle equal
skinparam classStereotypeFontStyle not
skinparam classStereotypeFontStyle and
skinparam classStereotypeFontStyle or
skinparam classStereotypeFontStyle xor
skinparam classStereotypeFontStyle nand
skinparam classStereotypeFontStyle nor
skinparam classStereotypeFontStyle xnor
skinparam classStereotypeFontStyle implies
skinparam classStereotypeFontStyle equivalent
skinparam classStereotypeFontStyle subset
skinparam classStereotypeFontStyle superset
skinparam classStereotypeFontStyle properSubset
skinparam classStereotypeFontStyle properSuperset
skinparam classStereotypeFontStyle disjoint
skinparam classStereotypeFontStyle intersect
skinparam classStereotypeFontStyle union
skinparam classStereotypeFontStyle difference
skinparam classStereotypeFontStyle symmetricDifference
skinparam classStereotypeFontStyle complement
skinparam classStereotypeFontStyle emptySet
skinparam classStereotypeFontStyle universalSet
skinparam classStereotypeFontStyle naturalNumbers
skinparam classStereotypeFontStyle integers
skinparam classStereotypeFontStyle rationalNumbers
skinparam classStereotypeFontStyle realNumbers
skinparam classStereotypeFontStyle complexNumbers
skinparam classStereotypeFontStyle quaternions
skinparam classStereotypeFontStyle octonions
skinparam classStereotypeFontStyle sedenions
skinparam classStereotypeFontStyle trigintaduonions
skinparam classStereotypeFontStyle pathions
skinparam classStereotypeFontStyle chingons
skinparam classStereotypeFontStyle routons
skinparam classStereotypeFontStyle wagdys
skinparam classStereotypeFontStyle gargantua
skinparam classStereotypeFontStyle googol
skinparam classStereotypeFontStyle googolplex
skinparam classStereotypeFontStyle infinity
skinparam classStereotypeFontStyle alephNull
skinparam classStereotypeFontStyle alephOne
skinparam classStereotypeFontStyle alephTwo
skinparam classStereotypeFontStyle alephThree
skinparam classStereotypeFontStyle alephFour
skinparam classStereotypeFontStyle alephFive
skinparam classStereotypeFontStyle alephSix
```

#### `474f517555452d09a886e20bf68de11fa0890f9b` — compile_fail (sequence, tier 2)

- CSR: `Error line 115 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/474f517555452d09a886e20bf68de11fa0890f9b.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=10 F1=0.000; missed: message
- chrF++: 37.82
- Files: GT `data/puml_files/474f517555452d09a886e20bf68de11fa0890f9b.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/474f517555452d09a886e20bf68de11fa0890f9b.puml` (yes) · input `data/puml_images_1568/474f517555452d09a886e20bf68de11fa0890f9b.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/474f517555452d09a886e20bf68de11fa0890f9b.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 474f517555452d09a886e20bf68de11fa0890f9b
' Original Path: /Modification_1/mod_1-seq-diagrams/DefenseInGloves.puml
' Source: World of Code

@startuml
'https://plantuml.com/sequence-diagram
mainframe Virologist wear gloves


participant "attackerVirologist:Virologist" as attackerVirologist
participant "v: Virologist" as Virologist
participant "glovesOnVirologist:Gloves" as Gloves

attackerVirologist->Virologist++:attack(forgetAgent:Agent, attackerVirologist:Virologist)
Virologist->Gloves++:defense(forgetAgent:Agent,v:Virologist, attackerVirologist:Virologist)


Gloves->attackerVirologist++:attack(forgetAgent:Agent, attackerVirologist:Virologist,v:Virologist)
attackerVirologist-->Gloves--
Gloves->Gloves++:decreaseTTL()
Gloves-->Gloves--
opt life==0
Gloves->Gloves++:discard(v:Virologist)
Gloves-->Gloves--
end opt
Gloves-->Virologist--
Virologist-->attackerVirologist--

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam sequenceMessageAlign center
skinparam lifelineStrategy solid
skinparam participantStyle rectangle
skinparam participantPadding 10
skinparam notePadding 10
skinparam noteBackgroundColor #F0F0F0
skinparam noteBorderColor #CCCCCC
skinparam noteFontColor #333333
skinparam noteFontSize 12
skinparam noteFontStyle plain
skinparam noteFontName Arial
skinparam noteBorderThickness 1
skinparam noteCornerRadius 5
skinparam noteShadowing false
skinparam noteTextAlignment center
skinparam noteVerticalAlignment middle
skinparam noteHorizontalAlignment center
skinparam noteMargin 5
skinparam noteSpacing 5
skinparam noteZIndex 100
skinparam noteLayer front
skinparam notePosition top
skinparam noteDirection horizontal
skinparam noteOrientation horizontal
skinparam noteRotation 0
skinparam noteScale 1
skinparam noteOpacity 100
skinparam noteTransparency 0
skinparam noteVisibility visible
skinparam noteDisplay true
skinparam noteShow true
skinparam noteEnable true
skinparam noteActive true
skinparam noteEnabled true
skinparam noteVisible true
skinparam noteShown true
skinparam notePresent true
skinparam noteExisting true
skinparam noteAvailable true
skinparam noteAccessible true
skinparam noteReachable true
skinparam noteDetectable true
skinparam noteObservable true
skinparam notePerceivable true
skinparam noteSensible true
skinparam noteResponsive true
skinparam noteReactive true
skinparam noteInteractive true
skinparam noteEngaging true
skinparam noteInvolving true
skinparam noteParticipating true
skinparam noteContributing true
skinparam noteCollaborating true
skinparam noteCooperating true
skinparam noteWorking together
skinparam noteTeamwork true
skinparam noteSynergy true
skinparam noteHarmony true
skinparam noteBalance true
skinparam noteEquilibrium true
skinparam noteStability true
skinparam noteConsistency true
skinparam noteReliability true
skinparam noteDependability true
skinparam noteTrustworthiness true
skinparam noteCredibility true
skinparam noteAuthenticity true
skinparam noteIntegrity true
skinparam noteHonesty true
skinparam noteTruthfulness true
skinparam noteAccuracy true
skinparam notePrecision true
skinparam noteExactness true
skinparam noteCorrectness true
skinparam noteValidity true
skinparam noteLegitimacy true
skinparam noteAuthority true
skinparam notePower true
skinparam noteControl true
```

#### `578ffe267d2c971e91dd1753716f3ebe87d7328c` — compile_fail (class, tier 3)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: dependency, association
- chrF++: 3.84
- Files: GT `data/puml_files/578ffe267d2c971e91dd1753716f3ebe87d7328c.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/578ffe267d2c971e91dd1753716f3ebe87d7328c.puml` (yes) · input `data/puml_images_1568/578ffe267d2c971e91dd1753716f3ebe87d7328c.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/578ffe267d2c971e91dd1753716f3ebe87d7328c.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 578ffe267d2c971e91dd1753716f3ebe87d7328c
' Original Path: /10.Facade外观/facade.puml
' Source: World of Code

@startuml
class Computer{
   - Cpu cpu
   - Disk disk
   - Memory memory
   + void start()
   + void stop()
}
class Cpu{
   + void start()
   + void stop()
}
class Disk{
   + void start()
   + void stop()
}
class Memory{
   + void start()
   + void stop()
}
class Client{
    +{static}void main(String[] args)
}
Computer --> Cpu
Computer --> Disk
Computer --> Memory
Client ..> Computer
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontName Arial
skinparam classFontSize 14
skinparam classBackgroundColor #F5F5F5
skinparam classBorderColor #333333
skinparam classHeaderBackgroundColor #E8E8E8
skinparam classHeaderFontColor #333333
skinparam classHeaderFontSize 16
skinparam classHeaderFontStyle bold
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline......
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
skinparam classAttributeUnderline false
skinparam classAttributeFontStyle normal
skinparam classAttributeFontColor #333333
skinparam classMethodFontColor #333333
skinparam classMethodFontStyle italic
skinparam classMethodUnderline true
```

#### `6a34c869757f4e32cf9f81c687ee0236b2b19532` — compile_fail (class, tier 1)

- CSR: `Error line 101 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/6a34c869757f4e32cf9f81c687ee0236b2b19532.puml`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 6.48
- Files: GT `data/puml_files/6a34c869757f4e32cf9f81c687ee0236b2b19532.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/6a34c869757f4e32cf9f81c687ee0236b2b19532.puml` (yes) · input `data/puml_images_1568/6a34c869757f4e32cf9f81c687ee0236b2b19532.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/6a34c869757f4e32cf9f81c687ee0236b2b19532.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 6a34c869757f4e32cf9f81c687ee0236b2b19532
' Original Path: /puFileV7TMS/Enum_AttributeType2Code.pu
' Source: World of Code

@startuml
skinparam classBackgroundColor<<Codeset>> Azure 
enum AttributeType2Code <<Codeset>> {
EMAL : EmailAddress
CHLG : ChallengePassword
}
@enduml 
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontName Courier New
skinparam classFontSize 14
skinparam classBackgroundColor #F0FFFF
skinparam classBorderColor black
skinparam classFontColor black
skinparam classStereotypeFontName Courier New
skinparam classStereotypeFontSize 14
skinparam classStereotypeFontColor black
skinparam classStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderColor black
skinparam classStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontSize 14
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBackgroundColor #F0FFFF
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderColor black
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderThickness 1
skinparam classStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeBorderStereotypeFontName Courier New
```

#### `7e0e0e3379e4f346233ea39b20fa7408fb452111` — compile_fail (sequence, tier 2)

- CSR: `Error line 3 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/7e0e0e3379e4f346233ea39b20fa7408fb452111.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=9 F1=0.000; missed: message
- chrF++: 54.64
- Files: GT `data/puml_files/7e0e0e3379e4f346233ea39b20fa7408fb452111.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/7e0e0e3379e4f346233ea39b20fa7408fb452111.puml` (yes) · input `data/puml_images_1568/7e0e0e3379e4f346233ea39b20fa7408fb452111.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/7e0e0e3379e4f346233ea39b20fa7408fb452111.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 7e0e0e3379e4f346233ea39b20fa7408fb452111
' Original Path: /assets/initial-adapter-proxy-sequence.puml
' Source: World of Code

@startuml
title Initialization
box "service process" #LightBlue
participant ConcreteImpl #Wheat
participant DBusAdapter #PaleGreen
end box

ConcreteImpl -[hidden]> DBusAdapter
DBusAdapter -> DBusAdapter: Init(ConcreteImpl) 
DBusAdapter -> DBus: Export 

box "client process" #Lavender
participant DBusProxy #PaleGreen
end box

DBusProxy -> DBusProxy: Init 
DBusProxy -> DBus: ConnectToRemoteObject
note right: Tries to fetch all properties \n including "ready" property 
DBusProxy -> DBus: GetAllProperties
DBus -> DBusAdapter: GetAllProperties
DBusAdapter --> DBus: return properties
DBus --> DBusProxy: return properties
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Initialization
participant "service process" as SP {
    participant "ConcreteImpl" as CI
    participant "DBusAdapter" as DA
}
participant "DBus" as DB
participant "client process" as CP {
    participant "DBusProxy" as DP
}

DA -> DA: Init(ConcreteImpl)
DA -> DB: Export
DP -> DP: Init
DP -> DB: ConnectToRemoteObject
note right of DP: Tries to fetch all properties\nincluding "ready" property
DP -> DB: GetAllProperties
DB -> DA: GetAllProperties
DA --> DB: return properties
DB --> DP: return properties
@enduml
```

#### `84229a2f3146a5612be77dc49bc84ef4e68d6371` — compile_fail (sequence, tier 1)

- CSR: `Error line 6 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/84229a2f3146a5612be77dc49bc84ef4e68d6371.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: message
- chrF++: 57.26
- Files: GT `data/puml_files/84229a2f3146a5612be77dc49bc84ef4e68d6371.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/84229a2f3146a5612be77dc49bc84ef4e68d6371.puml` (yes) · input `data/puml_images_1568/84229a2f3146a5612be77dc49bc84ef4e68d6371.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/84229a2f3146a5612be77dc49bc84ef4e68d6371.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 84229a2f3146a5612be77dc49bc84ef4e68d6371
' Original Path: /docs/UseCases/Manage-Pipeline/Destroy-Pipeline.puml
' Source: World of Code

@startuml
Actor "actorName" as A

box "Manage-Pipeline" #lightblue
participant CLI as CLI
participant Web as Web
participant "caade" as S
A -> CLI : caade-pipeline-destroy()
CLI -> S : pipeline/destroy()
A -> Web : pipeline/destroy()
Web -> S : pipeline/destroy()
end box

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
actor "actorName" as actor1
actor "actorName" as actor2

package "Manage-Pipeline" {
    participant "CLI" as cli1
    participant "Web" as web1
    participant "caade" as caade1
    participant "CLI" as cli2
    participant "Web" as web2
    participant "caade" as caade2
}

actor1 -> cli1: caade-pipeline-destroy()
cli1 -> caade1: pipeline/destroy()
actor1 -> web1: pipeline/destroy()
web1 -> caade1: pipeline/destroy()

@enduml
```

#### `922bf6a56d7cde0d054a7a6c27786000e3979ae6` — compile_fail (class, tier 1)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=2 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=1 F1=0.000; missed: inheritance
- chrF++: 2.63
- Files: GT `data/puml_files/922bf6a56d7cde0d054a7a6c27786000e3979ae6.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/922bf6a56d7cde0d054a7a6c27786000e3979ae6.puml` (yes) · input `data/puml_images_1568/922bf6a56d7cde0d054a7a6c27786000e3979ae6.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/922bf6a56d7cde0d054a7a6c27786000e3979ae6.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: 922bf6a56d7cde0d054a7a6c27786000e3979ae6
' Original Path: /docs/stages/RetryOnError/class.uml
' Source: World of Code

@startuml

	Class Stage
	Class Sequential{
		+constructor:function(cfg)
===
		-stage:Stage
===		
		+retry:function(err, ctx, iter)|Number
	}

 	Stage <|-- Sequential

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontName Courier New
skinparam classFontSize 14
skinparam classBackgroundColor #F5F5F5
skinparam classBorderColor black
skinparam classHeaderBackgroundColor #E8E8E8
skinparam classHeaderFontColor black
skinparam classHeaderFontSize 16
skinparam classHeaderFontStyle bold
skinparam classAttributeFontColor black
skinparam classAttributeFontSize 14
skinparam classMethodFontColor black
skinparam classMethodFontSize 14
skinparam classMethodFontStyle italic
skinparam classMethodVisibilityColor green
skinparam classAttributeVisibilityColor red
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold......
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibility......
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
skinparam classAttributeVisibilityFontStyle bold
skinparam classMethodVisibilityFontStyle bold
skinparam classAttributeVisibilityFontColor red
skinparam classMethodVisibilityFontColor green
```

#### `92d8301974977c07e4b1c27bfb8bf2c21e227b7a` — compile_fail (class, tier 4)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=6 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: inheritance, association
- chrF++: 4.69
- Files: GT `data/puml_files/92d8301974977c07e4b1c27bfb8bf2c21e227b7a.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/92d8301974977c07e4b1c27bfb8bf2c21e227b7a.puml` (yes) · input `data/puml_images_1568/92d8301974977c07e4b1c27bfb8bf2c21e227b7a.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/92d8301974977c07e4b1c27bfb8bf2c21e227b7a.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: 92d8301974977c07e4b1c27bfb8bf2c21e227b7a
' Original Path: /app/src/main/java/il/ac/afeka/tomco/cookingapp/Entities/Entities.plantuml
' Source: World of Code

@startuml

title __ENTITIES's Class Diagram__\n

  package il.ac.afeka.tomco.cookingapp {
    package il.ac.afeka.tomco.cookingapp.Entities {
      class CategoriesContent {
          {static} + CATEGORIES : List<Category>
          {static} + clear()
          {static} + addCategory()
      }
    }
  }
  

  package il.ac.afeka.tomco.cookingapp {
    package il.ac.afeka.tomco.cookingapp.Entities {
      class Category {
          - title : String
          - imageURL : String
          {static} + CREATOR : Creator<Category>
          + Category()
          + Category()
          # Category()
          + setTitle()
          + setImageURL()
          + getTitle()
          + getImageURL()
          + describeContents()
          + writeToParcel()
      }
    }
  }
  

  package il.ac.afeka.tomco.cookingapp {
    package il.ac.afeka.tomco.cookingapp.Entities {
      class Recipe {
          - title : String
          - ingredients : String
          - cookingOperations : String
          - category : String
          - imageURL : String
          - uploadingUser : String
          {static} + CREATOR : Creator<Recipe>
          + Recipe()
          + Recipe()
          # Recipe()
          + getTitle()
          - setTitle()
          + getIngredients()
          - setIngredients()
          + getCookingOperations()
          - setCookingOperations()
          + getImageURL()
          + setImageURL()
          + getCategory()
          + setCategory()
          + getUploadingUser()
          + setUploadingUser()
          + describeContents()
          + writeToParcel()
      }
    }
  }
  

  package il.ac.afeka.tomco.cookingapp {
    package il.ac.afeka.tomco.cookingapp.Entities {
      class RecipesContent {
          {static} + RECIPES : List<Recipe>
          {static} + clear()
          {static} + addRecipe()
      }
    }
  }
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml
title ENTITIES's Class Diagram
skinparam classAttributeIconSize 0
skinparam classFontStyle bold
skinparam classBackgroundColor #F0F0F0
skinparam classBorderColor #000000
skinparam classArrowColor #000000
skinparam classStereotypeStyle none
skinparam packageStyle folder
skinparam packageBackgroundColor #FFFFFF
skinparam packageBorderColor #000000
skinparam packageFontStyle bold
skinparam packageHeaderAlignment left
skinparam packageBodyAlignment left
skinparam packagePadding 10
skinparam packageMargin 10
skinparam packageBorderThickness 2
skinparam packageHeaderBackgroundColor #FFFFFF
skinparam packageHeaderBorderColor #000000
skinparam packageHeaderFontStyle bold
skinparam packageHeaderFontSize 12
skinparam packageBodyBackgroundColor #FFFFFF
skinparam packageBodyBorderColor #000000
skinparam packageBodyFontStyle normal
skinparam packageBodyFontSize 10
skinparam packageBodyPadding 5
skinparam packageBodyMargin 5
skinparam packageBodyBorderThickness 1
skinparam packageBodyHeaderBackgroundColor #FFFFFF
skinparam packageBodyHeaderBorderColor #000000
skinparam packageBodyHeaderFontStyle bold
skinparam packageBodyHeaderFontSize 11
skinparam packageBodyHeaderPadding 3
skinparam packageBodyHeaderMargin 3
skinparam packageBodyHeaderBorderThickness 1
skinparam packageBodyHeaderAlignment left
skinparam packageBodyHeaderBodyAlignment left
skinparam packageBodyHeaderBodyPadding 2
skinparam packageBodyHeaderBodyMargin 2
skinparam packageBodyHeaderBodyBorderThickness 1
skinparam packageBodyHeaderBodyBackgroundColor #FFFFFF
skinparam packageBodyHeaderBodyBorderColor #000000
skinparam packageBodyHeaderBodyFontStyle normal
skinparam packageBodyHeaderBodyFontSize 9
skinparam packageBodyHeaderBodyPadding 1
skinparam packageBodyHeaderBodyMargin 1
skinparam packageBodyHeaderBodyBorderThickness 1
skinparam packageBodyHeaderBodyHeaderBackgroundColor #FFFFFF
skinparam packageBodyHeaderBodyHeaderBorderColor #000000
skinparam packageBodyHeaderBodyHeaderFontStyle bold
skinparam packageBodyHeaderBodyHeaderFontSize 10
skinparam packageBodyHeaderBodyHeaderPadding 2
skinparam packageBodyHeaderBodyHeaderMargin 2
skinparam packageBodyHeaderBodyHeaderBorderThickness 1
skinparam packageBodyHeaderBodyHeaderAlignment left
skinparam packageBodyHeaderBodyHeaderBodyAlignment left
skinparam packageBodyHeaderBodyHeaderBodyPadding 1
skinparam packageBodyHeaderBodyHeaderBodyMargin 1
skinparam packageBodyHeaderBodyHeaderBodyBorderThickness 1
skinparam packageBodyHeaderBodyHeaderBodyBackgroundColor #FFFFFF
skinparam packageBodyHeaderBodyHeaderBodyBorderColor #000000
skinparam packageBodyHeaderBodyHeaderBodyFontStyle normal
skinparam packageBodyHeaderBodyHeaderBodyFontSize 8
skinparam packageBodyHeaderBodyHeaderBodyPadding 0
skinparam packageBodyHeaderBodyHeaderBodyMargin 0
skinparam packageBodyHeaderBodyHeaderBodyBorderThickness 1
skinparam packageBodyHeaderBodyHeaderBodyHeaderBackgroundColor #FFFFFF
skinparam packageBodyHeaderBodyHeaderBodyHeaderBorderColor #000000
skinparam packageBodyHeaderBodyHeaderBodyHeaderFontStyle bold
skinparam packageBodyHeaderBodyHeaderBodyHeaderFontSize 9
skinparam packageBodyHeaderBodyHeaderBodyHeaderPadding 1
skinparam packageBodyHeaderBodyHeaderBodyHeaderMargin 1
skinparam packageBodyHeaderBodyHeaderBodyHeaderBorderThickness 1
skinparam packageBodyHeaderBodyHeaderBodyHeaderAlignment left
skinparam packageBodyHeaderBodyHeaderBodyHeaderBodyAlignment left
skinparam packageBodyHeaderBodyHeaderBodyHeaderBodyPadding 0
skinparam packageBodyHeaderBodyHeaderBodyHeaderBodyMargin 0
skinparam packageBodyHeaderBodyHeaderBodyHeaderBodyBorderThickness 1
skinparam packageBodyHeaderBodyHeaderBodyHeaderBodyBackgroundColor #FFFFFF
```

#### `a6345d1b606990db509338edf787ebdf90c825ef` — compile_fail (sequence, tier 3)

- CSR: `Error line 7 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/a6345d1b606990db509338edf787ebdf90c825ef.puml`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=2 F1=0.000; missed: message
- chrF++: 68.95
- Files: GT `data/puml_files/a6345d1b606990db509338edf787ebdf90c825ef.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/a6345d1b606990db509338edf787ebdf90c825ef.puml` (yes) · input `data/puml_images_1568/a6345d1b606990db509338edf787ebdf90c825ef.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/a6345d1b606990db509338edf787ebdf90c825ef.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: a6345d1b606990db509338edf787ebdf90c825ef
' Original Path: /PB-351 - Mimos 2.0/Package 2/UC23 - View Offers Details on System Management.puml
' Source: World of Code

@startuml
'diagram parameters'
autonumber
'skinparam dpi 300
skinparam LegendBackgroundColor #white

'diagram title'
title PB-351 UC23 - View Offers Details on System Management
'a list of the actors and participants'
actor "UI (System Admin and Manager - System Management)" as UI
box "Partners and Offers Platform"
participant "Next Platform" as Next
database "Next Database" as DB
end box

'a brief description of the diagram'
legend top
-- \t**Abstract:**\t --
This use case will retrieve details of a specific Offer. This endpoint already
exists on the Partners and Offers platform, but we have to add on response
the new fields.
end legend

UI -> Next: **HTTP** \nGET /offers/{offerId}
activate Next
note right Next #orange
**Note to developers**
Add these fields on response:
#. benefit
#. listImage
#. listImageVersion
#. partnerName


Also, change the type of:
#. startDate
#. endDate
To consider timestamp from now on.
end note

note right of Next #plum
For partnerName consider the field 'FANTASY_NAME' in PATNER table.
end note

Next->UI: response
deactivate Next
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title PB-351 UC23 – View Offers Details on System Management

actor "UI (System Admin and Manager – System Management)" as UI

rectangle "Partners and Offers Platform" as Platform {
    participant "Next Platform" as NP
    database "Next Database" as ND
}

note over Platform
**Abstract:**
This use case will retrieve details of a specific Offer. This endpoint already exists on the Partners and Offers platform, but we have to add on response the new fields.
end note

UI -> NP: 1 HTTP GET /offers/{offerId}

activate NP

note right of NP
**Note to developers**
Add these fields on response:
1. . benefit
2. . listImage
3. . listImageVersion
4. . partnerName

Also, change the type of:
5. . startDate
6. . endDate
To consider timestamp from now on.
end note

note right of ND
For partnerName consider the field 'FANTASY_NAME' in PATNER table.
end note

NP --> UI: 2 response

deactivate NP

@enduml
```

#### `b21a6faaf6a180c501e0aba4b0056672ede1ea2d` — compile_fail (class, tier 2)

- CSR: `Error line 55 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: inheritance, aggregation, association
- chrF++: 50.46
- Files: GT `data/puml_files/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.puml` (yes) · input `data/puml_images_1568/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/b21a6faaf6a180c501e0aba4b0056672ede1ea2d.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: b21a6faaf6a180c501e0aba4b0056672ede1ea2d
' Original Path: /Documentation/plantuml/Grid/BuildingTile.puml
' Source: World of Code

@startuml
class BuildingTile {
    + IsLocationValid : bool <<get>>
    + BuildingTile(type:StructureType, facing:Facing)
    + <<override>> ToString() : string
}
class "Dictionary`2"<T1,T2> {
}
enum StructureType {
    House= 0,
    Office= 1,
    TestStruct= 2,
}
Tile <|-- BuildingTile
BuildingTile o-> "ModelLookup<StructureType,string>" "Dictionary`2"
BuildingTile --> "structure" StructureType
BuildingTile +-- StructureType
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontColor black
skinparam classBackgroundColor white
skinparam classBorderColor black
skinparam classHeaderBackgroundColor #f0f0f0
skinparam classHeaderFontColor black
skinparam classHeaderBorderColor black
skinparam classHeaderBorderThickness 1
skinparam classHeaderPadding 5
skinparam classPadding 5
skinparam classMargin 10
skinparam classStereotypeStyle none
skinparam classStereotypeFontColor black
skinparam classStereotypeBackgroundColor #e0e0e0
skinparam classStereotypeBorderColor black
skinparam classStereotypeBorderThickness 1
skinparam classStereotypePadding 3
skinparam classStereotypeMargin 5
skinparam classStereotypeAlignment center
skinparam classStereotypeFontStyle bold
skinparam classStereotypeFontSize 10
skinparam classStereotypeFontName "Arial"
skinparam classStereotypeFontColor #333333
skinparam classStereotypeBackgroundColor #f8f8f8
skinparam classStereotypeBorderColor #cccccc
skinparam classStereotypeBorderThickness 1
skinparam classStereotypePadding 3
skinparam classStereotypeMargin 5
skinparam classStereotypeAlignment center
skinparam classStereotypeFontStyle bold
skinparam classStereotypeFontSize 10
skinparam classStereotypeFontName "Arial"

class Tile {
}

class BuildingTile {
  + IsLocationValid : bool «get»
  + BuildingTile(type:StructureType, facing:Facing)
  + «override» ToString() : string
}

class StructureType {
  House = 0,
  Office = 1,
  TestStruct = 2,
}

class Dictionary`2 {
}

Tile <|-- BuildingTile
BuildingTile --> StructureType : structure
BuildingTile o-- Dictionary`2
note right of Dictionary`2
  ModelLookup<StructureType,string>
  T1,T2
end note

@enduml
```

#### `b8328a277bb75f19a8707d0a11eced190879e5c8` — compile_fail (sequence, tier 3)

- CSR: `no PNG produced`
- Element: tp=0 fp=0 fn=3 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=14 F1=0.000; missed: message
- chrF++: 6.25
- Files: GT `data/puml_files/b8328a277bb75f19a8707d0a11eced190879e5c8.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/b8328a277bb75f19a8707d0a11eced190879e5c8.puml` (yes) · input `data/puml_images_1568/b8328a277bb75f19a8707d0a11eced190879e5c8.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/b8328a277bb75f19a8707d0a11eced190879e5c8.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: b8328a277bb75f19a8707d0a11eced190879e5c8
' Original Path: /docs/diagrams/sequence/LEA.puml
' Source: World of Code

@startuml

skinparam ActorBorderColor #Black
hide footbox

actor Programador

box LEA
    participant Front as "front: Ceed"
    participant Ceed as "agent: Ceed"
end box

autoactivate on
Front -> Front: see(addBrain, brain)
deactivate
Front -> Front: see('listen', port)
deactivate

Programador->Front: ws://lea
Front->Front: see('onSocketConnection', socket)
Front-->Programador: socket.emit(agents)
Programador -> Front: see(agent, action, args)
Front -> Ceed: see(action, args)
Ceed --> Front
Front --> Programador: resolve()
deactivate

Programador -> Front: http://lea/:agent/:action
Front -> Front: see('http', [req, res])
Front -> Ceed: see(action, [req, res])
Ceed --> Front
Front --> Programador: res.send()
deactivate

@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam sequenceMessageAlign center
skinparam participantStyle rectangle
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantFontName Arial
skinparam participantFontSize 14
skinparam participantFontStyle plain
skinparam participantFontColor #000000
skinparam participantBackgroundColor #......
skinparam participantBorderColor #000000
skinparam participantPadding 10
```

#### `bf0e4a69eec206028b6fbd8dfc1e9905986d987d` — compile_fail (class, tier 4)

- CSR: `Error line 106 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/bf0e4a69eec206028b6fbd8dfc1e9905986d987d.puml`
- Element: tp=0 fp=0 fn=27 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=33 F1=0.000; missed: inheritance, composition, dependency, association
- chrF++: 79.24
- Files: GT `data/puml_files/bf0e4a69eec206028b6fbd8dfc1e9905986d987d.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/bf0e4a69eec206028b6fbd8dfc1e9905986d987d.puml` (yes) · input `data/puml_images_1568/bf0e4a69eec206028b6fbd8dfc1e9905986d987d.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/bf0e4a69eec206028b6fbd8dfc1e9905986d987d.png` (MISSING)

GT PlantUML (truncated):
```plantuml
' Blob ID: bf0e4a69eec206028b6fbd8dfc1e9905986d987d
' Original Path: /old/mcd.uml
' Source: World of Code

@startuml
skinparam dpi 500
skinparam monochrome true
skinparam linetype ortho
hide circle

class Membre {
	numeroMembre : int{key}
	nom : string
	prenom : string
	adresse : string
	dateDeNaissance : date
	{field} tel : int(10)
    	createNumMembre()
	membreActif()
}
class Inscription {
	date : timestamp
	fraisIns()
	montantPayé : int
	statutInscription : {a,p}
	solde()
	setMontantPayé()
}
class Activité {
	numéroActivité : string {key}
	titre : string
    
}

class Financement {
	date : timestamp
	adresse : string
    
}
class Compétition {
	heure : timestamp
	adresse : string
}

class Epreuve {
	date : timestamp
    
}

class Discipline {
	nom : string {key}
    
}

class Spécialité {
	nom : string {key}
    
}

class Comité {
	nom : string {key}
    
    
}

class Participant {
	numéro : int {local key}
	nom : string
	prénom : string
	createNuméro()
}

class CompétitionExterne {
	nomClub : varchar
	responsableClub : varchar
	{field} tel : int(10)
}

class RésultatInterne {
	résultat : int
```

Prediction PlantUML (truncated):
```plantuml
```plantuml
@startuml

note "Sauf indication contraire, les héritages de cette MLD sont exclusifs, et les attributs doivent tous être non nuls." as Note1

class Membre {
    numeroMembre : int{key}
    nom : string
    prenom : string
    adresse : string
    dateDeNaissance : date
    tel : int(10)
    --
    createNumMembre()
    membreActif()
}

class Inscription {
    date : timestamp
    montantPayé : int
    statutInscription : {a,p}
    --
    fraisIns()
    solde()
    setMontantPayé()
}

class Comité {
    nom : string {key}
}

class Activité {
    numéroActivité : string {key}
    titre : string
}

class Financement {
    date : timestamp
    adresse : string
}

class Compétition {
    heure : timestamp
    adresse : string
}

class CompétitionInterne {
}

class CompétitionExterne {
    nomClub : varchar
    responsableClub : varchar
    tel : int(10)
}

class Participant {
    numéro : int {local key}
    nom : string
    prénom : string
    --
    createNuméro()
}

class Epreuve {
    date : timestamp
}

class Discipline {
    nom : string {key}
}

class Spécialité {
    nom : string {key}
}

class Amateur {
}

class Professionnel {
}
```

#### `c22af72a8329b4b5b474e1e7294a3e3d251bf753` — compile_fail (sequence, tier 1)

- CSR: `Error line 4 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/c22af72a8329b4b5b474e1e7294a3e3d251bf753.puml`
- Element: tp=0 fp=0 fn=1 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=0 F1=1.000
- chrF++: 63.75
- Files: GT `data/puml_files/c22af72a8329b4b5b474e1e7294a3e3d251bf753.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/c22af72a8329b4b5b474e1e7294a3e3d251bf753.puml` (yes) · input `data/puml_images_1568/c22af72a8329b4b5b474e1e7294a3e3d251bf753.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/c22af72a8329b4b5b474e1e7294a3e3d251bf753.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: c22af72a8329b4b5b474e1e7294a3e3d251bf753
' Original Path: /example/teste/arquivo.ts.sequence.puml
' Source: World of Code

@startuml 
 participant participant as Usuario
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
participant participant
participant participant
participant -- participant
@enduml
```

#### `e74eafa342207f6317773e0c8d1f8562842c9e97` — compile_fail (sequence, tier 4)

- CSR: `Error line 10 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/e74eafa342207f6317773e0c8d1f8562842c9e97.puml`
- Element: tp=0 fp=0 fn=7 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=20 F1=0.000; missed: message
- chrF++: 88.28
- Files: GT `data/puml_files/e74eafa342207f6317773e0c8d1f8562842c9e97.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/e74eafa342207f6317773e0c8d1f8562842c9e97.puml` (yes) · input `data/puml_images_1568/e74eafa342207f6317773e0c8d1f8562842c9e97.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/e74eafa342207f6317773e0c8d1f8562842c9e97.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: e74eafa342207f6317773e0c8d1f8562842c9e97
' Original Path: /GameCode/UML/UML_Seqüencia/PlantUML/Diagrama_Seq04.uml
' Source: World of Code

﻿@startuml
actor Jugador
boundary Telegram
control Gestor
entity Ranking
entity User
entity Timer
entity Options

group Guanyar Partida
    activate Jugador
      Jugador -> Telegram : Seleccionar_opcio()
    activate Telegram
      Telegram -> Gestor : Realitzar_jugada(self,bot,update)
    activate Gestor
	  ref over Gestor: Desplacar-se per l'escenari()
      Gestor -> User : GetTimer()
	  activate User
	  User -> Gestor : return(timer)
	  deactivate User
      Gestor -> Timer : RestarSeg()
	  activate Timer
      Timer -> Gestor : Return(bool)
    deactivate Timer
      Gestor -> Options : get_texts(ind)
    activate Options
      Options -> Gestor : Return(String)
    deactivate Options
      Gestor -> Options : get_options(ind)
    activate Options
      Options -> Gestor : Return(String)
    deactivate Options
      Gestor -> Options : get_realitzar_mod(ind)
    activate Options
      Options -> Gestor : Return(String)
    deactivate Options
	group Emmagatzemar Ranking
      Gestor -> Ranking : AddtoRanking(User)
    activate Ranking
	Ranking -> Gestor : return(bool)
	deactivate Ranking
end
group Mostrar Ranking
	  Gestor -> Ranking : FiveFirstRanking()
	  activate Ranking
      Ranking -> Gestor : return(bool)
	  deactivate Ranking
      Gestor -> Ranking : printRanking()
	  activate Ranking
	  Ranking -> Gestor : return(bool)
    deactivate Ranking
end
      Gestor -> Telegram : Return(String)
    deactivate Gestor
      Telegram -> Jugador : Return(String)
    deactivate Telegram
    deactivate Jugador
end

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
actor Jugador
participant Telegram
control Gestor
entity Ranking
entity User
entity Timer
entity Options

frame "Guanyar Partida" {
    Jugador -> Telegram: Seleccionar_opcio()
    activate Telegram
    Telegram -> Gestor: Realitzar_jugada(self,bot,update)
    activate Gestor
    
    ref over Gestor: Desplaçar-se per l'escenari()
    
    Gestor -> Timer: GetTimer()
    activate Timer
    Timer --> Gestor: return(timer)
    deactivate Timer
    
    Gestor -> Timer: RestarSeg()
    activate Timer
    Timer --> Gestor: Return(bool)
    deactivate Timer
    
    Gestor -> Options: get_texts(ind)
    activate Options
    Options --> Gestor: Return(String)
    deactivate Options
    
    Gestor -> Options: get_options(ind)
    activate Options
    Options --> Gestor: Return(String)
    deactivate Options
    
    Gestor -> Options: get_realitzar_mod(ind)
    activate Options
    Options --> Gestor: Return(String)
    deactivate Options
    
    frame "Emmagatzemar Ranking" {
        Gestor -> Ranking: AddtoRanking(User)
        activate Ranking
        Ranking --> Gestor: return(bool)
        deactivate Ranking
    }
    
    frame "Mostrar Ranking" {
        Gestor -> Ranking: FiveFirstRanking()
        activate Ranking
        Ranking --> Gestor: return(bool)
        deactivate Ranking
        
        Gestor -> Ranking: printRanking()
        activate Ranking
        Ranking --> Gestor: return(bool)
        deactivate Ranking
    }
    
    Gestor --> Telegram: Return(String)
    deactivate Gestor
    Telegram --> Jugador: Return(String)
    deactivate Telegram
}
@enduml
```

#### `e7bd74664407c0ec08fb1e90fbb1a40573b2afeb` — compile_fail (class, tier 2)

- CSR: `Error line 52 in file: data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/extracted/e7bd74664407c0ec08fb1e90fbb1a40573b2afeb.puml`
- Element: tp=0 fp=0 fn=4 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=0 fn=4 F1=0.000; missed: inheritance, aggregation, dependency
- chrF++: 29.14
- Files: GT `data/puml_files/e7bd74664407c0ec08fb1e90fbb1a40573b2afeb.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/e7bd74664407c0ec08fb1e90fbb1a40573b2afeb.puml` (yes) · input `data/puml_images_1568/e7bd74664407c0ec08fb1e90fbb1a40573b2afeb.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/e7bd74664407c0ec08fb1e90fbb1a40573b2afeb.png` (MISSING)

GT PlantUML:
```plantuml
' Blob ID: e7bd74664407c0ec08fb1e90fbb1a40573b2afeb
' Original Path: /src/main/java/com/master/chapter019/Composute-Pattern.puml
' Source: World of Code

@startuml
'https://plantuml.com/class-diagram
/'客户端'/
class client{

}

/'component为所有对象定义一个类，不管是叶子还是节点'/
class Component{
    void add();
    void remove();
    void print();
}
/'依赖'/
client ..> Component

/'叶子没有孩子，不能操作孩子，但其定义组合内元素的行为'/
class leaf{

}

/'组合可以操作子节点和叶子，但可能不具有叶子的某些行为'/
class Composite{

}

/'继承/扩展/泛化'/
Component <|-- leaf
Component <|-- Composite

/'聚合'/
Composite o-- Component
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontName Arial
skinparam classFontSize 14
skinparam classBackgroundColor #F5F5F5
skinparam classBorderColor #000000
skinparam classHeaderBackgroundColor #E8F5E9
skinparam classHeaderBorderColor #000000
skinparam classHeaderFontColor #000000
skinparam classHeaderFontSize 16
skinparam classHeaderFontStyle bold
skinparam classIconSize 20
skinparam classIconColor #4CAF50
skinparam classIconBackgroundColor #C8E6C9
skinparam classIconBorderColor #000000
skinparam classIconFontColor #000000
skinparam classIconFontSize 14
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skinparam classIconFontStyle bold
skinparam classIconFontName Arial
skinparam classIconFontWeight bold
skin......
class "client" as client {
}
class "Component" as Component {
+ void add();
+ void remove();
+ void print();
}
class "leaf" as leaf {
}
class "Composite" as Composite {
}
client --> Component
Component <|-- leaf
Component <|-- Composite
Composite o-- Component
@enduml
```

#### outcome: compiled_low_structural

#### `013f262fafb9cce412d05966af0aca59982ed3f2` — compiled_low_structural (class, tier 4)

- Element: tp=13 fp=16 fn=4 F1=0.565; type-acc matched=13 correct=13 excluded=0
- Relationship: tp=4 fp=25 fn=14 F1=0.170; missed: inheritance, composition, aggregation, association; extra: dependency, association
- chrF++: 41.71
- Files: GT `data/puml_files/013f262fafb9cce412d05966af0aca59982ed3f2.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/013f262fafb9cce412d05966af0aca59982ed3f2.puml` (yes) · input `data/puml_images_1568/013f262fafb9cce412d05966af0aca59982ed3f2.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/013f262fafb9cce412d05966af0aca59982ed3f2.png` (yes)

#### `0c347826efa0a235f71c95b3d79310d14e6bcf57` — compiled_low_structural (class, tier 2)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=1 excluded=2
- Relationship: tp=2 fp=2 fn=4 F1=0.400; missed: dependency; extra: dependency
- chrF++: 70.77
- Files: GT `data/puml_files/0c347826efa0a235f71c95b3d79310d14e6bcf57.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/0c347826efa0a235f71c95b3d79310d14e6bcf57.puml` (yes) · input `data/puml_images_1568/0c347826efa0a235f71c95b3d79310d14e6bcf57.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/0c347826efa0a235f71c95b3d79310d14e6bcf57.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 0c347826efa0a235f71c95b3d79310d14e6bcf57
' Original Path: /src/main/java/com/shengsiyuan/dp/principle/segregation/泛化-实现关系.puml
' Source: World of Code

@startuml




abstract class DaoSupport {

  + void save(Object e)
  + void delete(Integer id)
}

class PersonServiceBean {
    + void delete(Integer id)
}

DaoSupport <|-- PersonServiceBean

note "泛化即继承关系" as N1
DaoSupport ..N1
N1 ..PersonServiceBean

interface PersonService {
  + void delete(Integer id)
}

PersonService <|.. PersonServiceBean

note "实现关系" as N2
PersonService ..N2
N2 ..PersonServiceBean


@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam noteBackgroundColor #FFFFE0
skinparam noteBorderColor #000000
skinparam class {
  BackgroundColor #F5F5F5
  BorderColor #000000
  ArrowColor #000000
}

class "DaoSupport" as DaoSupport {
  + void save(Object e)
  + void delete(Integer id)
}

class "PersonService" as PersonService {
  + void delete(Integer id)
}

class "PersonServiceBean" as PersonServiceBean {
  + void delete(Integer id)
}

note "泛化即继承关系" as Note1
note "实现关系" as Note2

DaoSupport <|-- PersonServiceBean
PersonService <|.. PersonServiceBean

PersonServiceBean -[dashed]-> Note1
PersonServiceBean -[dashed]-> Note2

@enduml
```

#### `119e0cad229d01b262f56304e78948d18db5b2f4` — compiled_low_structural (class, tier 1)

- Element: tp=1 fp=1 fn=0 F1=0.667; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=1 fn=0 F1=0.000; extra: dependency
- chrF++: 20.19
- Files: GT `data/puml_files/119e0cad229d01b262f56304e78948d18db5b2f4.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/119e0cad229d01b262f56304e78948d18db5b2f4.puml` (yes) · input `data/puml_images_1568/119e0cad229d01b262f56304e78948d18db5b2f4.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/119e0cad229d01b262f56304e78948d18db5b2f4.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 119e0cad229d01b262f56304e78948d18db5b2f4
' Original Path: /РегистрыСведений/РегистрСведенийФИОФизическихЛиц.wsd
' Source: World of Code

﻿@startuml
'!include templates.wsd
'..\include templates.wsd
class РегистрСведений.ФИОФизическихЛиц as "Фамилия, имя, отчество физического лица" <<РегистрыСведений>>
{
..Измерения..
ФизическоеЛицо : Справочник.Организация\rСправочник.Физическое лицо
..Ресурсы..
Фамилия : Строка
Имя : Строка
Отчество : Строка
ИнициалыИмени : Строка
}
@enduml
```

Prediction PlantUML (truncated):
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontName Arial
skinparam classFontSize 14
skinparam classBackgroundColor #F0F0F0
skinparam classBorderColor #000000
skinparam classHeaderBackgroundColor #FFFFFF
skinparam classHeaderFontColor #000000
skinparam classHeaderFontSize 16
skinparam classHeaderFontStyle bold
skinparam classStereotypeFontStyle italic
skinparam classStereotypeFontColor #000000
skinparam classStereotypeFontSize 12
skinparam classStereotypeFontName Arial
skinparam classStereotypeBackgroundColor #FFFFFF
skinparam classStereotypeBorderColor #000000
skinparam classStereotypeBorderThickness 1
skinparam classStereotypeBorderRadius 0
skinparam classStereotypeBorderPadding 0
skinparam classStereotypeBorderMargin 0
skinparam classStereotypeBorderSpacing 0
skinparam classStereotypeBorderGap 0
skinparam classStereotypeBorderOffset 0
skinparam classStereotypeBorderShift 0
skinparam classStereotypeBorderSkew 0
skinparam classStereotypeBorderRotate 0
skinparam classStereotypeBorderScale 1
skinparam classStereotypeBorderOpacity 1
skinparam classStereotypeBorderDashed false
skinparam classStereotypeBorderDotted false
skinparam classStereotypeBorderDouble false
skinparam classStereotypeBorderGroove false
skinparam classStereotypeBorderInset false
skinparam classStereotypeBorderOutset false
skinparam classStereotypeBorderRidge false
skinparam classStereotypeBorderSolid true
skinparam classStereotypeBorderWidth 1
skinparam classStereotypeBorderHeight 1
skinparam classStereotypeBorderDepth 1
skinparam classStereotypeBorderShadow false
skinparam classStereotypeBorderReflection false
skinparam classStereotypeBorderGradient false
skinparam classStereotypeBorderGradientAngle 0
skinparam classStereotypeBorderGradientStartColor #FFFFFF
skinparam classStereotypeBorderGradientEndColor #FFFFFF
skinparam classStereotypeBorderGradientMiddleColor #FFFFFF
skinparam classStereotypeBorderGradientMiddlePosition 50
skinparam classStereotypeBorderGradientMiddleSize 0
skinparam classStereotypeBorderGradientMiddleOpacity 1
skinparam classStereotypeBorderGradientMiddleDashed false
skinparam classStereotypeBorderGradientMiddleDotted false
skinparam classStereotypeBorderGradientMiddleDouble false
skinparam classStereotypeBorderGradientMiddleGroove false
skinparam classStereotypeBorderGradientMiddleInset false
skinparam classStereotypeBorderGradientMiddleOutset false
skinparam classStereotypeBorderGradientMiddleRidge false
skinparam classStereotypeBorderGradientMiddleSolid true
skinparam classStereotypeBorderGradientMiddleWidth 1
skinparam classStereotypeBorderGradientMiddleHeight 1
skinparam classStereotypeBorderGradientMiddleDepth 1
skinparam classStereotypeBorderGradientMiddleShadow false
skinparam classStereotypeBorderGradientMiddleReflection false
skinparam classStereotypeBorderGradientMiddleGradient false
skinparam classStereotypeBorderGradientMiddleGradientAngle 0
skinparam classStereotypeBorderGradientMiddleGradientStartColor #FFFFFF
skinparam classStereotypeBorderGradientMiddleGradientEndColor #FFFFFF
skinparam classStereotypeBorderGradientMiddleGradientMiddleColor #FFFFFF
skinparam classStereotypeBorderGradientMiddleGradientMiddlePosition 50
skinparam classStereotypeBorderGradientMiddleGradientMiddleSize 0
skinparam classStereotypeBorderGradientMiddleGradientMiddleOpacity 1
skinparam classStereotypeBorderGradientMiddleGradientMiddleDashed false
skinparam classStereotypeBorderGradientMiddleGradientMiddleDotted false
skinparam classStereotypeBorderGradientMiddleGradientMiddleDouble false
skinparam classStereotypeBorderGradientMiddleGradientMiddleGroove false
skinparam classStereotypeBorderGradientMiddleGradientMiddleInset false
skinparam classStereotypeBorderGradientMiddleGradientMiddleOutset false
skinparam classStereotypeBorderGradientMiddleGradientMiddleRidge false
skinparam classStereotypeBorderGradientMiddleGradientMiddleSolid true
skinparam classStereotypeBorderGradientMiddleGradientMiddleWidth 1
skinparam classStereotypeBorderGradientMiddleGradientMiddleHeight 1
```

#### `13535b2cbd8a085a55557cd59dee9ac4e2096202_20` — compiled_low_structural (sequence, tier 1)

- Element: tp=5 fp=0 fn=0 F1=1.000; type-acc matched=5 correct=5 excluded=0
- Relationship: tp=0 fp=4 fn=0 F1=0.000; extra: message
- chrF++: 51.68
- Files: GT `data/puml_files/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.puml` (yes) · input `data/puml_images_1568/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/13535b2cbd8a085a55557cd59dee9ac4e2096202_20.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 13535b2cbd8a085a55557cd59dee9ac4e2096202
' Original Path: /apex-Walle钱包系统.wsd
' Source: World of Code

@startuml
scale 3
title uc2_6活动执行时序图
actor 管理员 as adm
participant web 
participant sever as se 
database 活动快照表 as kz
database 活动结果表 as jg
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title uc2_6活动执行时序图

actor "管理员" as admin
participant "web" as web
participant "sever" as sever
database "活动快照表" as snapshot
database "活动结果表" as result

admin -> web: 
web -> sever: 
sever -> snapshot: 
sever -> result: 

@enduml
```

#### `159a02c8f268bf0088c99b6596ab6513270fe85f` — compiled_low_structural (class, tier 1)

- Element: tp=0 fp=5 fn=5 F1=0.000; type-acc matched=0 correct=0 excluded=0
- Relationship: tp=0 fp=4 fn=4 F1=0.000; missed: inheritance; extra: inheritance
- chrF++: 49.89
- Files: GT `data/puml_files/159a02c8f268bf0088c99b6596ab6513270fe85f.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/159a02c8f268bf0088c99b6596ab6513270fe85f.puml` (yes) · input `data/puml_images_1568/159a02c8f268bf0088c99b6596ab6513270fe85f.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/159a02c8f268bf0088c99b6596ab6513270fe85f.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 159a02c8f268bf0088c99b6596ab6513270fe85f
' Original Path: /M3UF5/1-estructures_emmagatzematge/uml/collection.puml
' Source: World of Code

@startuml
interface Collection
interface Set
interface List
interface Queue
interface SortedSet
Collection <|.. Set
Collection <|.. List
Collection <|.. Queue
Set <|.. SortedSet
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam classFontStyle italic
skinparam classBackgroundColor #F5F5F5
skinparam classBorderColor black
skinparam classArrowColor black
skinparam classStereotypeStyle none

interface "I Collection" as Collection {
}

interface "I Set" as Set {
}

interface "I List" as List {
}

interface "I Queue" as Queue {
}

interface "I SortedSet" as SortedSet {
}

Collection <|-- Set
Collection <|-- List
Collection <|-- Queue
Set <|-- SortedSet

@enduml
```

#### `42fc85c2e1d580aedd56311d963ecb8df37a5cb1` — compiled_low_structural (class, tier 2)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=1 fn=0 F1=0.000; extra: dependency
- chrF++: 84.01
- Files: GT `data/puml_files/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.puml` (yes) · input `data/puml_images_1568/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/42fc85c2e1d580aedd56311d963ecb8df37a5cb1.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 42fc85c2e1d580aedd56311d963ecb8df37a5cb1
' Original Path: /shacl-diagram/src/specs/07-maxCount/expected.iuml
' Source: World of Code

@startuml
class "ex:MyShapemaxCount" 
"ex:MyShapemaxCount" : age : integer : maxCount[0..1]


note as N1
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.org/ns#> .

ex:MyShapemaxCount a sh:NodeShape ;
sh:targetClass ex:Person ;
sh:property[
  sh:path ex:age ;
  sh:maxCount 1 ;
  sh:datatype xsd:integer ;
] .
end note


hide circle
hide empty members
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam note {
  BackgroundColor LightYellow
  BorderColor Black
}
skinparam class {
  BackgroundColor LightGray
  BorderColor Black
}

class "ex:MyShapemaxCount" as MyClass {
  age : integer : maxCount[0..1]
}

note right of MyClass
  @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
  @prefix schema: <http://schema.org/> .
  @prefix sh: <http://www.w3.org/ns/shacl#> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
  @prefix ex: <http://example.org/ns#> .

  ex:MyShapemaxCount a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property[
      sh:path ex:age ;
      sh:maxCount 1 ;
      sh:datatype xsd:integer ;
    ] .
end note

@enduml
```

#### `5a0aae7871f32620048d5024b1c31f35ff539948` — compiled_low_structural (sequence, tier 4)

- Element: tp=9 fp=0 fn=0 F1=1.000; type-acc matched=9 correct=9 excluded=0
- Relationship: tp=9 fp=10 fn=15 F1=0.419; missed: message; extra: message
- chrF++: 48.17
- Files: GT `data/puml_files/5a0aae7871f32620048d5024b1c31f35ff539948.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/5a0aae7871f32620048d5024b1c31f35ff539948.puml` (yes) · input `data/puml_images_1568/5a0aae7871f32620048d5024b1c31f35ff539948.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/5a0aae7871f32620048d5024b1c31f35ff539948.png` (yes)

#### `6c7324c7eaeb23cd5644654ea022ca212ecd24ea` — compiled_low_structural (sequence, tier 1)

- Element: tp=1 fp=1 fn=1 F1=0.500; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=4 fn=4 F1=0.000; missed: message; extra: message
- chrF++: 61.08
- Files: GT `data/puml_files/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.puml` (yes) · input `data/puml_images_1568/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/6c7324c7eaeb23cd5644654ea022ca212ecd24ea.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 6c7324c7eaeb23cd5644654ea022ca212ecd24ea
' Original Path: /Documentação/1201384/US1005/US1005_SSD.puml
' Source: World of Code

@startuml
actor SalesClerk as adm
participant "//<<presentation>>//\nDefineNewCategoryUI" as ui

autonumber

adm-->ui: Define new category

activate ui

ui-->adm: asks user information

adm-->ui: Code, Description

ui-->adm: displayCategoryInfo

deactivate ui
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
actor SalesClerk
participant "«presentation»\nDefineNewCategoryUI" as UI

SalesClerk -> UI: 1 Define new category
activate UI
UI --> SalesClerk: 2 asks user information
SalesClerk -> UI: 3 Code, Description
UI --> SalesClerk: 4 displayCategoryInfo
deactivate UI
@enduml
```

#### `75d17323e3f57e506be51b5455aa97ae89d8c5cc` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=3 fn=3 F1=0.250; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=6 fn=6 F1=0.000; missed: message; extra: message
- chrF++: 46.95
- Files: GT `data/puml_files/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/75d17323e3f57e506be51b5455aa97ae89d8c5cc.puml` (yes) · input `data/puml_images_1568/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/75d17323e3f57e506be51b5455aa97ae89d8c5cc.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: 75d17323e3f57e506be51b5455aa97ae89d8c5cc
' Original Path: /input/images-source/Implementing-PDQm-as-a-gateway.plantuml
' Source: World of Code

@startuml
hide footbox

Participant "Patient\nDemographics\nConsumer" as Client1
box "PDQm Implementation\ngrouped as a façade "
    Participant "Patient\n Demographics\nSupplier" as Server1
    Participant "Patient\n Demographics\nConsumer" as Client2
endbox
Participant "Patient\n Demographics\nSupplier" as Server2

Client1 -> Server1: Mobile Patient\nDemographics\nQuery [ITI-78]
activate Client1
activate Server1
Server1 --> Client2: Internal processing
activate Client2
activate Server2
Client2 -> Server2: Patient Demographics\nQuery [ITI-21]\nor Patient Demographics\nQuery for HL7v3 [ITI-47]
Client2 <- Server2: [ITI-21] or [ITI-47] Response
Server1 <-- Client2: Internal processing
deactivate Client2
deactivate Server2
Client1 <- Server1: [ITI-78] Response
deactivate Client2
deactivate Server1

@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam sequenceMessageAlign center
skinparam participantStyle rectangle
skinparam participantBackgroundColor #E6E6FA
skinparam participantBorderColor #000000
skinparam participantFontColor #000000
skinparam participantFontSize 14
skinparam participantFontStyle bold
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantBorderRadius 5
skinparam participantBorderDashed false
skinparam participantBorderDotted false
skinparam participantBorderSolid true
skinparam participantBorderWidth 1
skinparam participantBorderColor #000000
skinparam participantBackgroundColor #E6E6FA
skinparam participantFontColor #000000
skinparam participantFontSize 14
skinparam participantFontStyle bold
skinparam participantPadding 10
skinparam participantMargin 10
skinparam participantBorderThickness 1
skinparam participantBorderRadius 5
skinparam participantBorderDashed false
skinparam participantBorderDotted false
skinparam participantBorderSolid true
skinparam participantBorderWidth 1

participant "Patient Demographics Consumer" as PDC1
participant "Patient Demographics Supplier" as PDS1
participant "Patient Demographics Consumer" as PDC2
participant "Patient Demographics Supplier" as PDS2

box "PDQm Implementation grouped as a façade" #DDDDDD
    participant "Patient Demographics Supplier" as PDS1
    participant "Patient Demographics Consumer" as PDC2
end box

PDC1 -> PDS1: Mobile Patient Demographics Query [ITI-78]
activate PDS1
PDS1 -> PDC2: Internal processing
activate PDC2
PDC2 -> PDS2: Patient Demographics Query [ITI-21] or Patient Demographics Query for HL7v3 [ITI-47]
activate PDS2
PDS2 --> PDC2: [ITI-21] or [ITI-47] Response
deactivate PDS2
PDC2 --> PDS1: Internal processing
deactivate PDC2
PDS1 --> PDC1: [ITI-78] Response
deactivate PDS1

@enduml
```

#### `938e9cc0e6b8dda26422f35f30282f7d202efb9d_02` — compiled_low_structural (sequence, tier 4)

- Element: tp=1 fp=4 fn=4 F1=0.200; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=20 fn=20 F1=0.000; missed: message; extra: message
- chrF++: 62.82
- Files: GT `data/puml_files/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.puml` (yes) · input `data/puml_images_1568/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/938e9cc0e6b8dda26422f35f30282f7d202efb9d_02.png` (yes)

#### `b1bfedf152eefbba6b408c7ffbc16e5cd01cd904` — compiled_low_structural (sequence, tier 3)

- Element: tp=3 fp=1 fn=1 F1=0.750; type-acc matched=3 correct=3 excluded=0
- Relationship: tp=4 fp=15 fn=15 F1=0.211; missed: message; extra: message
- chrF++: 63.27
- Files: GT `data/puml_files/b1bfedf152eefbba6b408c7ffbc16e5cd01cd904.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/b1bfedf152eefbba6b408c7ffbc16e5cd01cd904.puml` (yes) · input `data/puml_images_1568/b1bfedf152eefbba6b408c7ffbc16e5cd01cd904.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/b1bfedf152eefbba6b408c7ffbc16e5cd01cd904.png` (yes)

#### `b54faa73ac4f11af7993db28cc8d2eb8866801fc` — compiled_low_structural (class, tier 4)

- Element: tp=13 fp=1 fn=1 F1=0.929; type-acc matched=13 correct=13 excluded=0
- Relationship: tp=0 fp=16 fn=12 F1=0.000; missed: inheritance, aggregation; extra: association
- chrF++: 31.91
- Files: GT `data/puml_files/b54faa73ac4f11af7993db28cc8d2eb8866801fc.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/b54faa73ac4f11af7993db28cc8d2eb8866801fc.puml` (yes) · input `data/puml_images_1568/b54faa73ac4f11af7993db28cc8d2eb8866801fc.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/b54faa73ac4f11af7993db28cc8d2eb8866801fc.png` (yes)

#### `c5bb3816232672cc44f741e2b5d82d69ebdf932c` — compiled_low_structural (sequence, tier 2)

- Element: tp=1 fp=2 fn=1 F1=0.400; type-acc matched=1 correct=1 excluded=0
- Relationship: tp=0 fp=2 fn=2 F1=0.000; missed: message; extra: message
- chrF++: 62.18
- Files: GT `data/puml_files/c5bb3816232672cc44f741e2b5d82d69ebdf932c.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/c5bb3816232672cc44f741e2b5d82d69ebdf932c.puml` (yes) · input `data/puml_images_1568/c5bb3816232672cc44f741e2b5d82d69ebdf932c.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/c5bb3816232672cc44f741e2b5d82d69ebdf932c.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: c5bb3816232672cc44f741e2b5d82d69ebdf932c
' Original Path: /doc/profiles/representation/minimal.puml
' Source: World of Code

@startuml
title Omit Representation
actor Client
participant "<&transfer> Representation" as Representation

Client -> Representation: PUT / POST / PATCH
rnote right #lightblue
  <#lightblue,lightblue>|= Header |= Value |
  | ""Prefer"" | ""return=minimal"" |
end note
Representation --> Client: 204 No Content / 201 Created
rnote left #lightgreen
  <#lightgreen,lightgreen>|= Header |= Value |
  | ""Preference-Applied"" | ""return=minimal"" |
end note
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
title Omit Representation
actor Client
participant "⇄ Representation" as Representation

Client -> Representation: PUT / POST / PATCH
note right of Client
  <b>Header</b>  <b>Value</b>
  Prefer  return=minimal
end note

Representation --> Client: 204 No Content / 201 Created
note left of Client
  <b>Header</b>  <b>Value</b>
  Preference-Applied  return=minimal
end note

actor Client
participant "⇄ Representation" as Representation2
@enduml
```

#### `ca4d115d35fbb40dbae3bfb4e2db6b8089a36eba` — compiled_low_structural (class, tier 3)

- Element: tp=3 fp=1 fn=1 F1=0.750; type-acc matched=3 correct=3 excluded=0
- Relationship: tp=0 fp=1 fn=1 F1=0.000; missed: association; extra: dependency
- chrF++: 74.91
- Files: GT `data/puml_files/ca4d115d35fbb40dbae3bfb4e2db6b8089a36eba.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/ca4d115d35fbb40dbae3bfb4e2db6b8089a36eba.puml` (yes) · input `data/puml_images_1568/ca4d115d35fbb40dbae3bfb4e2db6b8089a36eba.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/ca4d115d35fbb40dbae3bfb4e2db6b8089a36eba.png` (yes)

GT PlantUML:
```plantuml
' Blob ID: ca4d115d35fbb40dbae3bfb4e2db6b8089a36eba
' Original Path: /view-diagram.plantuml
' Source: World of Code

@startuml
class ItemViews {
    create_item()
    get_item()
    catalog()
    get_category()
    submit_offer()
    search()
    get_all_sales()
    get_sale()
}
note right of ItemViews::get_all_sales
All sales for the logged in user
Both where he is buyer and seller.
end note
class UserViews {
    frontpage()
    register()
    profile()
    update_profile()
}
class MessagingViews {
    send_message()
    get_all_messages()
    get_message()
}
@enduml
```

Prediction PlantUML:
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam noteBackgroundColor #FFFFCC
skinparam noteBorderColor #000000
skinparam class {
  BackgroundColor #F5F5F5
  BorderColor #000000
  HeaderBackgroundColor #E8E8E8
}

class ItemViews {
  + create_item()
  + get_item()
  + catalog()
  + get_category()
  + submit_offer()
  + search()
  + get_all_sales()
  + get_sale()
}

class UserViews {
  + frontpage()
  + register()
  + profile()
  + update_profile()
}

class MessagingViews {
  + send_message()
  + get_all_messages()
  + get_message()
}

note right of ItemViews
  All sales for the logged in user
  Both where he is buyer and seller.
end note

@enduml
```

#### `de434622c1f498168c9bccf95ceb52a9dc1ef385` — compiled_low_structural (sequence, tier 3)

- Element: tp=4 fp=1 fn=1 F1=0.800; type-acc matched=4 correct=2 excluded=0
- Relationship: tp=3 fp=5 fn=4 F1=0.400; missed: message; extra: message
- chrF++: 37.89
- Files: GT `data/puml_files/de434622c1f498168c9bccf95ceb52a9dc1ef385.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/de434622c1f498168c9bccf95ceb52a9dc1ef385.puml` (yes) · input `data/puml_images_1568/de434622c1f498168c9bccf95ceb52a9dc1ef385.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/de434622c1f498168c9bccf95ceb52a9dc1ef385.png` (yes)

#### `fff389a2f264c9d5a71da3c2e50c05082884a074` — compiled_low_structural (class, tier 3)

- Element: tp=6 fp=0 fn=0 F1=1.000; type-acc matched=6 correct=6 excluded=0
- Relationship: tp=0 fp=5 fn=5 F1=0.000; missed: inheritance; extra: inheritance
- chrF++: 45.06
- Files: GT `data/puml_files/fff389a2f264c9d5a71da3c2e50c05082884a074.puml` (yes) · pred `data/runs/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/fff389a2f264c9d5a71da3c2e50c05082884a074.puml` (yes) · input `data/puml_images_1568/fff389a2f264c9d5a71da3c2e50c05082884a074.png` (yes) · render `data/csr/qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z/png/fff389a2f264c9d5a71da3c2e50c05082884a074.png` (yes)

