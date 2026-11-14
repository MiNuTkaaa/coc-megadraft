# CoC Megadraft

A website for running **Megadraft tournaments in Clash of Clans**. It borrows the format of Clash Royale's Mega Draft.

Two players snake-draft troops, super troops, spells, siege machines and epic equipment from a shared random pool. Then each player attacks the other's own base in a friendly challenge, using only what they drafted. The site runs the draft live: rooms, turns, timer, auto-pick, a practice bot, results, and an army builder that makes an in-game army link.

- Owner: Mikhail (GitHub `MiNuTkaaa`), who runs a community tournament in his clan.
- Repo: https://github.com/MiNuTkaaa/coc-megadraft (branch `main`)
- Live site (GitHub Pages, once enabled in the repo settings): https://minutkaaa.github.io/coc-megadraft/
- Local working copy: `C:\CoC\Megadraft`
- Firebase project: `coc-megadraft` (console: https://console.firebase.google.com/project/coc-megadraft)
- Older Claude-artifact copy (Claude db backend, out of date): https://claude.ai/artifact/ShiLdW5vRZZDatcWeLAnQ8
- Design doc: https://claude.ai/artifact/D5pszXAhwc3vTzms3wDomb
- Tournament rulebook: https://claude.ai/artifact/YD6SijgHtwFndnoMJWhYDD

## Working rules

- **Do not commit or push to GitHub unless Mikhail explicitly asks.** Make changes in the local folder and check them on localhost first.
- Edit `tools/template.html`, never `index.html` directly. `index.html` is generated (see Build).
- Keep it a single static page with no framework and no build step beyond injecting the data. GitHub Pages serves the files as they are.
- Before calling a change done, test it: run a full draft locally, and use the Firebase emulator for anything that touches rooms (see Testing).

## Run it locally

Double-click `start-local.bat`. It serves the folder and opens the browser. Or run it by hand:

```
cd C:\CoC\Megadraft
python -m http.server 8000
```

Open http://localhost:8000/. Use a server rather than opening the file, because the page loads the Firebase SDK and the icons over HTTP.

The local copy uses the **real** Firebase config in `firebase-config.js`, so rooms created locally show up on the live site too. To test with rooms kept in the browser only, temporarily empty `firebase-config.js`. The header then shows "This device only" and one screen plays both seats.

## Files

| Path | What it is |
|---|---|
| `tools/template.html` | **The source.** All HTML, CSS and JS for the app. Contains the placeholder `/*__DATA__*/{}`. |
| `index.html` | Built output: the template with `data.json` injected. This is what Pages serves. |
| `data.json` | Game data: `items` (troops, supers, spells, sieges, epics), `heroes`, `commons` (common equipment), `pets`. |
| `icons/` | 112px WebP icons for every item, hero, pet and equipment, from ClashKingAssets. |
| `firebase-config.js` | Firebase web config (`window.MEGADRAFT_FIREBASE`). These values are public by design; security comes from `firestore.rules`. |
| `firestore.rules` | Firestore access rules (deployed in the Firebase console). |
| `firebase.json` | Emulator ports (Firestore 8085, Auth 9099) and the rules path. |
| `tools/data.py` | Builds `data.json` and the icons from a ClashKingAssets checkout. |
| `tools/build.sh` | Full rebuild: clones ClashKingAssets, runs `data.py`, resizes icons, builds `index.html`. |
| `tools/inject.py` | Quick rebuild of `index.html` from the template and `data.json` (no network). |
| `README.md` | Public setup guide (Firebase, Pages, limits). |
| `start-local.bat` | Windows: serves the folder on http://localhost:8000 and opens it. |

## Build

After editing the template:

```
python tools/inject.py
```

To refresh the game data after a CoC update (new troops or equipment), run `bash tools/build.sh` on Linux, macOS or WSL. It needs `git`, Python 3 and Pillow.

## Game data (`tools/data.py`)

Source: https://github.com/ClashKingInc/ClashKingAssets (`assets/static_data/*.json` plus icons). The CoC fandom wiki is blocked from Claude's cloud environment, so use this repo.

- **Unlock Town Hall**: the production building level that unlocks the item (barracks, dark barracks, workshop, spell factories), mapped to that building level's `required_townhall` in `buildings.json`. Super troops use max(TH11, the base troop's TH). Heroes: BK 7, AQ 8, MP 9, GW 11, RC 13, DD 15.
- **`aid`**: the in-game id minus its base (troops 4000000, spells 26000000, heroes 28000000, pets 73000000, equipment 90000000). The army link uses it.
- `hs` is housing space. `fly` marks air troops, so the pool can guarantee some air and some ground.
- The data has 19 epic equipment across 6 heroes (BK, AQ, GW, RC, MP, DD). The Angry spell is real.

## How the app works (`tools/template.html`)

### Store (where rooms live)

The `Store` object picks a backend at startup:

1. **Claude artifact db**, when `window.claude.use` exists (the artifact copy only).
2. **Firebase Firestore**, when `window.MEGADRAFT_FIREBASE.apiKey` is set. It signs in anonymously, listens to the `rooms` collection with `onSnapshot`, and every write is a `runTransaction`, so two players can't take the same pick. The SDK (11.0.2) is imported from gstatic. Setting `emulatorHost` in the config points the app at the local emulators.
3. **localStorage**, when neither is available. Labeled "This device only".

Rendering: `app` and `#lockbar` have an `innerHTML` setter that patches the DOM in place (`morph`), so taps and picks don't rebuild the page and icons don't flash. It clears `onclick`/`onchange`/`oninput`/`onsubmit` on reused elements, so views must bind handlers with those properties after each render (not `addEventListener`).

`Store.mutate(id, fn)` takes a pure function that returns the new room, or `null` to abort. All game logic goes through it.

### Room document

```
{ v, name, th, createdAt, hostUid, phase: "lobby"|"draft"|"attack"|"done", practice,
  players: { A: {name, uid, lacks[], ready}, B: {...} | {name:"Bot", uid:"bot", bot:true, ready:true} | null },
  settings: { troops, supers, spells, sieges, epics, timer },   // picks per player; timer in s (0 = none)
  size: { troop, super, spell, siege, epic },                   // pool size per category (autoSize)
  pool: [itemId], picks: [{id, seat, auto, at, slot}],
  first, turn, done: {A?, B?}, turnStart, paused, pausedLeft,
  previewUntil, armyUntil,
  rerolls, reroll: {by, at} | null, results: {A: {stars, pct, time}, B} }
```

### Look and home page (`renderHome`)

- Every page uses the navy sticker-album style (Bowlby One + Rubik), rolled out to the whole site on 2026-11-14. The `--h*` and `--c-*` tokens live on `body`. The older tokens (`--fg`, `--panel`, `--line`, ...) mean "on the navy" at `:root`, and the light cards (`.panel`, `.status`, `.dock`, `.mrow`, `.hpanel`, `.hrooms`, ...) flip them back to dark ink. Pool tiles, roster chips and builder units get a category-coloured underline through `--cc`. The "sticker-album theme for every page" CSS block holds the overrides.
- The top shows one draft (`featured`): a room the visitor tapped in the list (`ui.hsel`), else a live draft (the visitor's own first, then the most recently active), else the last finished draft, else an empty, dimmed board ("No drafts right now", `emptyHero`). There is no example draft (Mikhail removed it, 2026-11-13).
- Tapping a room row pins its board at the top without leaving the page, and that room leaves the list until it's unpinned (Unpin button). The pinned board has a button that opens the room (Watch live, View room, Open room or Join).
- Each row's button comes from `roomAction`: Open (your room), Join (open seat), Watch (someone else's lobby or draft) or View (attacks or finished). Watch opens the room page read-only, updating live. Signed-in admins also get Delete on every row.
- Each row's strip is the whole snake, one cell per pick, coloured by what was taken: troop yellow, super troop orange-red, spell blue, siege green, epic equipment purple (`--c-*` tokens). The next pick blinks navy.
- Actions: Create room, Join, Practice (opens Create with the bot ticked via `ui.practice`). The free army builder (`#builder`) was removed from the menu and the route; the per-room builder (`#army-<room>-<seat>`) stays.

### Flow

1. **Create** (`renderCreate`): name, Town Hall chips (default 18), +/- steppers for picks per player and the timer (default 20 s, 5 s steps, 0 = off), and a live summary card (each player's slots, the pool). The form state lives in `ui.cr`, so live re-renders don't reset it. There is no bot checkbox: the home Practice button sets `ui.practice`, which opens the same screen as "Practice draft" with the bot seated. Pool sizes come from `autoSize`: about 1.5x what both players draft, plus at least 2 spare (1.25x for epics), capped at what exists at that TH. The defaults (7 troops, 2 supers, 4 spells, 1 siege, 4 epics) give 15 / 6 / 12 / 4 / 10.
2. **Lobby** (`lobbyView`): the opponent joins. Each seated player sees the rules, ticks the epic equipment they don't own (`lacks`, remembered in localStorage) and presses **Ready**. When both are ready, `startDraft` deals the pool, flips a coin for first pick and starts the draft. The pool doesn't exist before this point.
   - **Board preview**: the first 30 s (`PREVIEW_MS`) are for looking only. `previewUntil` is set and `turnStart` equals it, so the pick timer starts after the preview. `applyPick` refuses picks while `inPreview(r)`. A new pool from Change pool gets a fresh preview.
3. **Draft** (`draftView`/`bindDraft`): only the board. Rules and checkboxes are gone.
   - Snake order (`seqSeat`): F, O, O, F, F, O, O, ... `curSlot` skips seats that are full or finished, and `turnSeat` gives whose turn it is.
   - Legality is checked by `whyIllegal`: slot caps, max 2 supers, max 2 epics per hero, no epics the player lacks, no item already taken.
   - **Finish drafting**: available once a player has the minimum (`minsOf`: troops-2, spells-1, epics-2, all sieges, so 5/3/2/1 by default). That player's remaining turns are skipped. `finishStuck` also ends a seat that has nothing legal left.
   - **Change pool**: either player asks, the timer pauses, and the other must Accept or Decline. Accepting deals a new pool and restarts the picks. The limit is `MAX_REROLLS` = 2 per room. In practice or one-screen mode it happens straight away.
   - **Timer**: at 0, the picker's own device auto-picks a random legal item, then the opponent's device after 3 s, then a spectator's after 8 s (`setInterval` tick). The bot is driven by the host's device (`botChoice`).
   - A bottom dock shows the clock, whose turn it is, Lock in and Finish drafting. The tab title says "Your turn".
4. **Attack** (`attackView`): `checkEnd` sets `armyUntil` = now + 3 min (`ARMY_MS`). A countdown shows on the room page and in the builder, and the builder locks when it reaches 0. The link can still be copied.
   Also on this page: both rosters, "Build army link", a results form (stars, %, seconds left; `winner` compares them in that order), rematch, and close room.

### Epic pool rule

**Epic race with flex picks** (Mikhail's choice, 2026-11-14): both players keep the full epic cap (4). Once the pool has no epic a seat could still take (`epicsOpenFor` counts untaken, owned epics under the 2-per-hero limit), each of that seat's unfilled epic slots becomes a flex pick (`flexOf`/`flexLeft`): one more troop or spell over the 7/4 caps. The super, siege and per-hero limits don't change. So with 6 epics split 4 and 2, both players still make 16 picks. The roster shows unused flex slots as purple "flex" chips, and the lobby rules explain it. `seatSlots`/`shownPicks` show fewer slots only for a seat that finished early.

`genPool` deals epics **only from those every (non-bot) player owns**, up to `size.epic` (10). If fewer qualify, it deals all of them, rounded down to an even number so both players can take the same amount. Example: 8 shared gives 8, 7 shared gives 6.

Every category is dealt purely at random with a plain shuffle. There's no air/ground guarantee.

### Army builder (`renderBuilder`, route `#army-<roomId>-<seat>`)

- Built in the in-game style: Army and Clan Castle tabs, capacity bars, and a tray of chosen units (tap one to remove it). Tapping a unit below adds one.
- A unit that doesn't fit the remaining space is greyed out and can't be added, so capacity is a hard limit.
- In a room, only that player's drafted troops, spells and epics are offered, for the army and the Clan Castle. Regular and super troops sit in separate sections.
- Siege machines never go in the army. In a room, the drafted siege is placed in the Clan Castle automatically and can't be removed.
- Heroes: 4 fixed slots. Tap an empty slot to choose a hero. Tap a filled slot to pick 2 equipment and a pet from icon grids, change the hero, or remove it. Heroes, pets (one per hero) and common equipment are free.
- `CAP[th]` = [army camps, spells, CC troops, CC spells, CC sieges]. TH18 = 352 / 11 / 55 / 4 / 2 (from Mikhail). TH12-17 were researched in 2026-11 (coc.guide, cocmap, clasher.us); TH16+ allow 2 CC sieges.
- The army itself takes 1 siege. The saved army lives in localStorage per room and seat.
- `armyLink` builds `https://link.clashofclans.com/en?action=CopyArmy&army=` + `h<heroes>` `i<CC troops>` `d<CC spells>` `u<troops incl. siege>` `s<spells>`. Units are written `countxaid`, joined by `-`.
  - A hero is written `heroAid[p<petAid>][e<eq1>_<eq2>]`, and heroes are joined by `-`.
  - This format comes from the coc.py library and **hasn't been verified in-game yet**.

### Admin panel (`#admin`, `renderAdmin`)

- Username `admin` maps to the Firebase email/password account `admin@coc-megadraft.app` (`ADMIN_EMAIL`). Firebase checks the password; it is not stored in the page.
- When signed in, the admin sees every room (including ones older than a day), can watch any room, delete one, or delete all rooms older than a day. The admin can also delete from inside a room.
- `firestore.rules` has `isAdmin()` (auth email = the admin email), which allows update and delete on any room.
- Setup in the Firebase console:
  1. Authentication > Sign-in method: enable Email/Password.
  2. Authentication > Users: add `admin@coc-megadraft.app` with the admin password.
  3. Firestore > Rules: publish the repo's `firestore.rules`.
- The admin signs in on a second Firebase app instance (`Store.adm`, app name "admin"), separate from the player's anonymous session (`Store.fb`). That lets the same browser play and administer at once. Deletes go through the admin session when `Store.isAdmin`.

### Roles

- `mySeats(r)`: the seats this browser controls. In local mode that's both non-bot seats.
- `isHost`: the room creator.
- `isMod`: the Claude artifact owner, or local mode. It shows Pause and Undo.
- In Firebase mode, nobody is a mod.

## Firestore rules

- **Read:** anyone.
- **Create:** a signed-in user who sets themselves as `hostUid` and as player A.
- **Update:** the host, the seated player B, or a newcomer taking the empty B seat. `hostUid` can't change.
- **Delete:** the host or the admin. The admin can also update any room.
- Draft legality is checked in the browser only. That's fine among friends. A public ladder would need a Cloud Function.
- Rooms older than 24 h are hidden from the lists but not deleted.

## Testing

- **Local mode:** serve a copy with an empty `firebase-config.js`, then drive it with Playwright. Create a room with the bot, tick some epics, press Ready, change the pool twice, play to the end, then fill the army builder to its caps.
- **Firebase emulator:** `npx firebase emulators:start --only firestore,auth --project demo-megadraft`, using the repo's `firestore.rules`. Inject a config with `emulatorHost: "127.0.0.1"`. Then run two browser contexts (host and opponent) through join, the epics both players own, Ready, change pool (decline, then accept twice) and the full draft. Also check that a spectator's write is denied.
- In Claude's cloud container, Playwright and Chromium are preinstalled. The test scripts from earlier sessions are not in the repo.

## Defaults and decisions (agreed with Mikhail)

- Picks per player: 7 troops (max 2 supers), 4 spells, 1 siege, 4 epics. 6 vs 7 troops is still to be settled in testing.
- Only drafted items may be used, Clan Castle included. Heroes, pets and common equipment are free.
- Players attack each other's own bases in friendly challenges, both attacks within 15 minutes. Mighty Morsels and potions are allowed.
- The create menu deliberately has no pool-size or finish-early settings; both are derived automatically.
- Still open: the defense-level rule, and whether boosts work in friendly challenges.
