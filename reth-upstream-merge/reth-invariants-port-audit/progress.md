# Progress

## 2026-05-12 Initial Production Setup

- Fetched Atlas bundle generated `2026-05-10`.
- Built `queue.current-invariants.jsonl` with `1954` current refined invariants.
- Recorded repo branch/commit metadata in `run-metadata.json`.
- Initialized `invariants/`, `index.jsonl`, and `confirmed-gaps.md`.
- Launched read-only investigator subagents for invariant indices `1` through `12`.
- Completed artifacts: `0/1954`.


## Completed invariant-0013

- `cur-4cf8ab2d0d-obligation-scans-honor-supplied-deadlines`: `mapped_in_port` in `crates/ritual-scheduled-verification/src/lib.rs` (`compute_obligations`).
- Completed artifacts: `1/1954`.

## Completed invariant-0014

- `cur-bbd9fcfd1c-passkey-async-originals-convert-back-signed`: `mapped_in_port` in `crates/transaction-pool/src/pool/async_pool.rs` (`convert_original_to_signed`).
- Completed artifacts: `2/1954`.

## Completed invariant-0015

- `cur-fed39041e2-scheduled-replay-checks-overflow-bitmap-after-index`: `mapped_in_port` in `crates/ritual-scheduled-verification/src/lib.rs` and `src/slots.rs`.
- Completed artifacts: `3/1954`.

## Completed invariant-0016

- `cur-4ef2525863-canonical-scheduler-submits-next-block-calls`: `mapped_in_port` structurally through payload-builder obligation synthesis and scheduled candidate insertion.
- Completed artifacts: `4/1954`.

## Completed invariant-0017

- `cur-5eef00d37e-generated-scheduled-preserve-system-fields`: `mapped_in_port` structurally across scheduled transaction generation and Alloy `TxScheduled` timing fields.
- Completed artifacts: `5/1954`.

## Completed invariant-0018

- `cur-4a8b295707-scheduler-channel-size-configurable`: `confirmed_gap`; no `RITUAL_SCHEDULER_CHANNEL_SIZE` / `ScheduledTxService` implementation found in audited repos.
- Completed artifacts: `6/1954`.

## Completed invariant-0019

- `cur-c172a5245e-scheduler-monitor-share-state`: `confirmed_gap`; `SchedulerContract` / shared `SchedulerServiceState` construction is absent.
- Completed artifacts: `7/1954`.

## Completed invariant-0020

- `cur-61aca19161-scheduled-index-window-bounded-exact`: `mapped_in_port` through `due_index_bounds` and shared block-building usage.
- Completed artifacts: `8/1954`.

## Completed invariant-0021

- `cur-ba621aff7e-scheduled-async-sender-address-original-caller`: `mapped_in_port` structurally through payload-builder sender selection and commitment encoding.
- Completed artifacts: `9/1954`.

## Completed invariant-0022

- `cur-cb91e0ade5-scheduled-calls-active-bounds`: `mapped_in_port` through `verify_scheduled_transactions` C2/C3 checks.
- Completed artifacts: `10/1954`.

## Launched additional investigators

- Launched read-only investigator subagents for invariant indices `23` through `26`.
- Completed artifacts remain `10/1954`; in-flight investigator indices are `1-12` and `23-26`.

## Integrated returned investigator batch 1-12

- Wrote completed artifacts for invariant indices `1` through `12` from returned investigator evidence.
- Completed artifacts: `22/1954`.

## Launched replacement investigators after batch 1-12

- Launched read-only investigator subagents for invariant indices `39` through `45`.
- Completed artifacts: `22/1954`.

## Integrated returned investigator batch 23-26, 29, 31, 36, 37

- Wrote completed artifacts for invariant indices `23`, `24`, `25`, `26`, `29`, `31`, `36`, and `37`.
- Completed artifacts: `30/1954`.

## Launched replacement investigators after batch 23-37 partial

- Launched read-only investigator subagents for invariant indices `46` through `53`.
- Completed artifacts: `30/1954`.

## Integrated returned investigator batch 27-41 partial

- Wrote completed artifacts for invariant indices `27`, `28`, `30`, `32`, `33`, `34`, `35`, `38`, `39`, `40`, and `41`.
- Completed artifacts: `41/1954`.

## Launched replacement investigator batch 54-63

- Launched read-only investigators for invariant indices `54` through `63`.
- Checkpoint: completed artifacts remain `41/1954`; continuing.

## Integrated returned investigator invariant-0042

- Wrote completed artifact for invariant index `42`.
- Completed artifacts: `42/1954`.

## Direct parent audit batch 42-45

- Wrote completed artifacts for invariant indices `42`, `43`, `44`, and `45`.
- Completed artifacts: `45/1954`.

## Direct parent audit batch 46-53

- Wrote completed artifacts for invariant indices `46` through `53`.
- Completed artifacts: `53/1954`.

## Launched replacement investigator batch 64-73

- Launched read-only investigators for invariant indices `64` through `73`.
- Checkpoint: completed artifacts `53/1954`; continuing.

## Direct parent audit batch 54-63

- Wrote completed artifacts for invariant indices `54` through `63`.
- Completed artifacts: `63/1954`.

## Launched replacement investigator batch 74-83

- Launched read-only investigators for invariant indices `74` through `83`.
- Checkpoint: completed artifacts `63/1954`; continuing.

## Direct parent audit batch 64-73

- Wrote completed artifacts for invariant indices `64` through `73`.
- Completed artifacts: `73/1954`.

## Subagent permission correction

- Interrupted duplicate investigators for invariant indices `64` through `73`
  after local artifacts were already completed, to prevent further permission
  prompts.
- Re-issued invariant indices `74` through `83` with a strict local-only
  constraint: no SSH, no remote hosts, no network access, and no elevated or
  dangerous permission requests.
- Updated `orchestrator-prompt.md` so future child investigator prompts inherit
  the same local-only execution rule.

## Direct parent audit batch 74-83

- Wrote completed artifacts for invariant indices `74` through `83`.
- Mapped in port/dependency: `74`, `77`, `78`, `79`.
- Confirmed gaps: `75`, `76`, `80`, `81`, `82`, `83`.
- Completed artifacts: `83/1954`.

## Launched replacement investigator batch 84-93

- Stopped duplicate investigators for invariant indices `74` through `83`
  after parent artifacts were written.
- Launched read-only local-only investigators for invariant indices `84`
  through `93`.
- Checkpoint: completed artifacts `83/1954`; continuing.

## Direct parent audit batch 84-93

- Wrote completed artifacts for invariant indices `84` through `93`.
- Mapped in port/dependency: `85`, `86`, `87`, `89`, `90`, `91`, `93`.
- Confirmed gaps: `84`, `88`, `92`.
- Completed artifacts: `93/1954`.

## Launched replacement investigator batch 94-103

- Stopped duplicate investigators for invariant indices `84` through `93` after parent artifacts were written.
- Launched read-only local-only investigators for invariant indices `94` through `103`.
- Checkpoint: completed artifacts `93/1954`; continuing.

## Direct parent audit batch 94-103

- Wrote completed artifacts for invariant indices `94` through `103`.
- Mapped in port/dependency: `96`, `98`, `102`, `103`.
- Confirmed gaps: `94`, `95`, `97`, `99`, `100`, `101`.
- Completed artifacts: `103/1954`.

## Launched replacement investigator batch 104-113

- Launched read-only local-only investigators for invariant indices `104` through `113`.
- Checkpoint: completed artifacts `103/1954`; continuing.

## Direct parent audit batch 104-113

- Wrote completed artifacts for invariant indices `104` through `113`.
- Mapped in port/dependency: `105`, `106`, `108`, `110`, `111`, `112`, `113`.
- Confirmed gaps: `104`, `107`, `109`.
- Completed artifacts: `113/1954`.

## Launched replacement investigator batch 114-123

- Launched read-only local-only investigators for invariant indices `114` through `123`.
- Checkpoint: completed artifacts `113/1954`; continuing.

## Direct parent audit batch 114-123

- Wrote completed artifacts for invariant indices `114` through `123`.
- Mapped in port/dependency: `114`, `115`, `117`, `118`, `119`.
- Confirmed gaps: `116`, `120`, `121`, `122`, `123`.
- Completed artifacts: `123/1954`.

## Direct parent audit batch 124-133

- Wrote completed artifacts for invariant indices `124` through `133`.
- Mapped in port/dependency: `126`, `127`, `128`, `130`, `131`, `133`.
- Confirmed gaps: `124`, `125`, `129`, `132`.
- Completed artifacts: `133/1954`.

## Launched replacement investigator batch 134-143

- Launched read-only local-only investigators for invariant indices `134` through `143`.
- Checkpoint: completed artifacts `133/1954`; continuing.

## Direct parent audit batch 134-143

- Wrote completed artifacts for invariant indices `134` through `143`.
- Mapped in port/dependency: `135`, `138`, `142`.
- Confirmed gaps: `134`, `136`, `137`, `139`, `140`, `141`, `143`.
- Completed artifacts: `143/1954`.

## Launched replacement investigator batch 144-153

- Launched read-only local-only investigators for invariant indices `144` through `153`.
- Checkpoint: completed artifacts `143/1954`; continuing.

## Direct parent audit invariant 144

- `cur-e8aeac2d46-async-fulfillment-metadata-comes-system`: `mapped_in_port` in `crates/ethereum/payload/src/lib.rs` with supporting async metadata validation in `crates/ethereum/payload/src/ritual_async.rs` and `crates/transaction-pool/src/pool`.
- Completed artifacts: `144/1954`.

## Direct parent audit batch 145-154

- Wrote completed artifacts for invariant indices `145` through `154`.
- Mapped in port/dependency: `145`, `146`, `150`, `151`, `152`, `153`, `154`.
- Confirmed gaps: `147`, `148`, `149`.
- Completed artifacts: `154/1954`.

## Direct parent audit batch 155-164

- Wrote completed artifacts for invariant indices `155` through `164`.
- Mapped in port/dependency: `155`, `156`, `157`, `158`.
- Confirmed gaps: `159`, `160`, `161`, `162`, `163`, `164`.
- Completed artifacts: `164/1954`.



## Direct parent audit batch 165-174

- Wrote completed artifacts for invariant indices `165` through `174`.
- Mapped in port/dependency: `166`, `168`, `169`, `171`, `173`, `174`.
- Confirmed gaps: `165`, `167`, `170`, `172`.
- Completed artifacts: `174/1954`.

## Direct parent audit batch 165-174

- Wrote completed artifacts for invariant indices `165` through `174`.
- Mapped in port/dependency: `166`, `167`, `168`, `169`, `171`, `173`, `174`.
- Confirmed gaps: `165`, `170`, `172`.
- Completed artifacts: `174/1954`.

## Direct parent audit batch 175-184

- Wrote completed artifacts for invariant indices `175` through `184`.
- Mapped in port/dependency: `175`, `178`, `182`, `184`.
- Confirmed gaps: `176`, `177`, `179`, `180`, `181`, `183`.
- Completed artifacts: `184/1954`.

## Direct parent audit batch 185-194

- Wrote completed artifacts for invariant indices `185` through `194`.
- Mapped in port/dependency: `186`, `187`, `188`, `190`, `194`.
- Confirmed gaps: `185`, `189`, `191`, `192`, `193`.
- Completed artifacts: `194/1954`.

## Direct parent audit batch 195-214

- Wrote completed artifacts for invariant indices `195` through `214`.
- Mapped in port/dependency: `195`, `197`, `200`, `201`, `204`, `205`, `206`, `212`, `213`.
- Confirmed gaps: `196`, `198`, `199`, `202`, `203`, `207`, `208`, `209`, `210`, `211`, `214`.
- Completed artifacts: `214/1954`.

## Direct parent audit batch 215-234

- Wrote completed artifacts for invariant indices `215` through `234`.
- Mapped in port/dependency: `216`, `217`, `219`, `223`, `224`, `225`, `226`, `228`, `230`, `231`, `233`, `234`.
- Confirmed gaps: `215`, `218`, `220`, `221`, `222`, `227`, `229`, `232`.
- Completed artifacts: `234/1954`.

## Direct parent audit batch 235-254

- Wrote completed artifacts for invariant indices `235` through `254`.
- Mapped in port/dependency: `235`, `237`, `243`, `245`, `246`, `247`, `248`, `249`.
- Confirmed gaps: `236`, `238`, `239`, `240`, `241`, `242`, `244`, `250`, `251`, `252`, `253`, `254`.
- Completed artifacts: `254/1954`.

## Direct parent audit batch 255-274

- Completed at: 2026-05-13T18:10:06.420960Z
- Mapped: 255, 256, 260, 261, 263, 264, 266, 268, 270, 271, 272, 273
- Confirmed gaps: 257, 258, 259, 262, 265, 267, 269, 274
- Completed artifacts: 274/1954

## Direct parent audit batch 275-294

- Completed at: 2026-05-13T18:16:42.851958Z
- Mapped: 275, 277, 278, 280, 281, 282, 283, 284, 285, 286, 288, 289, 291, 292, 293, 294
- Confirmed gaps: 276, 279, 287, 290
- Completed artifacts: 294/1954

## Direct parent audit batch 295-314

- Completed at: 2026-05-13T18:23:07.092532Z
- Mapped: 295, 296, 297, 298, 300, 301, 302, 304, 307, 309, 310, 312, 313, 314
- Confirmed gaps: 299, 303, 305, 306, 308, 311
- Completed artifacts: 314/1954

## Direct parent audit batch 315-334

- Completed at: 2026-05-13T19:31:49.562829Z
- Mapped: 315, 319, 326, 327, 329, 330, 331, 332, 333, 334
- Confirmed gaps: 316, 317, 318, 320, 321, 322, 323, 324, 325, 328
- Completed artifacts: 334/1954

## Direct parent audit batch 335-354

- Completed at: 2026-05-13T19:39:32.940812Z
- Mapped: 335, 336, 337, 338, 339, 340, 341, 343, 344, 345, 346, 347, 349, 350, 352, 353
- Confirmed gaps: 342, 348, 351, 354
- Completed artifacts: 354/1954

## Direct parent audit batch 355-374

- Completed at: 2026-05-13T19:44:52.483808Z
- Mapped: 356, 357, 358, 359, 360, 361, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374
- Confirmed gaps: 355, 362
- Completed artifacts: 374/1954

## Direct parent audit batch 375-394

- Completed at: 2026-05-13T19:50:48.836831Z
- Mapped: 378, 379, 380, 381, 382, 383, 384, 386, 387, 388, 392, 393, 394
- Confirmed gaps: 375, 376, 377, 385, 389, 390, 391
- Completed artifacts: 394/1954

## Direct parent audit batch 395-414

- Completed at: 2026-05-13T19:55:56.617071Z
- Mapped: 396, 398, 401, 402, 403, 404, 405, 406, 409, 410, 411, 412, 413
- Confirmed gaps: 395, 397, 399, 400, 407, 408, 414
- Completed artifacts: 414/1954

## Direct parent audit batch 415-434

- Completed at: 2026-05-13T20:01:11.273760Z
- Mapped: 415, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434
- Confirmed gaps: 416, 417, 418, 419
- Completed artifacts: 434/1954

## Direct parent audit batch 435-454

- Completed at: 2026-05-13T20:08:11.943540Z
- Mapped: 435, 436, 438, 439, 440, 441, 442, 444, 446, 453, 454
- Confirmed gaps: 437, 443, 445, 447, 448, 449, 450, 451, 452
- Completed artifacts: 454/1954

## Direct parent audit batch 455-474

- Completed at: 2026-05-13T20:13:51.299255Z
- Mapped: 460, 461, 462, 463, 464, 465, 466, 470, 473, 474
- Confirmed gaps: 455, 456, 457, 458, 459, 467, 468, 469, 471, 472
- Completed artifacts: 474/1954

## Direct parent audit batch 475-494

- Completed at: 2026-05-13T20:17:56.568383Z
- Mapped: 475, 477, 479, 480, 481, 482, 485, 486, 487, 488, 489, 491, 492, 493, 494
- Confirmed gaps: 476, 478, 483, 484, 490
- Completed artifacts: 494/1954

## Direct parent audit batch 495-514

- Completed at: 2026-05-13T20:24:16.217346Z
- Mapped: 495, 496, 498, 502, 503, 505, 508, 510, 511, 514
- Confirmed gaps: 497, 499, 500, 501, 504, 506, 507, 509, 512, 513
- Completed artifacts: 514/1954

## Direct parent audit batch 515-534

- Completed at: 2026-05-13T20:29:37.310193Z
- Mapped: 515, 516, 518, 519, 520, 521, 522, 523, 524, 525, 527, 529, 532, 533, 534
- Confirmed gaps: 517, 526, 528, 530, 531
- Completed artifacts: 534/1954

## Direct parent audit batch 535-554

- Completed at: 2026-05-13T20:39:36.912818Z
- Mapped: 535, 536, 537, 538, 540, 541, 542, 544, 545, 548, 549, 550, 552
- Confirmed gaps: 539, 543, 546, 547, 551, 553, 554
- Completed artifacts: 554/1954

## Direct parent audit batch 555-574

- Completed at: 2026-05-13T20:45:58.207715Z
- Mapped: 556, 558, 559, 561, 563, 564, 568, 569, 572
- Confirmed gaps: 555, 557, 560, 562, 565, 566, 567, 570, 571, 573, 574
- Completed artifacts: 574/1954
