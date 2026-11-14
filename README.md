# CoC Megadraft

A draft board for running Clash of Clans Megadraft matches, modeled on Clash Royale's Mega Draft.

Two players snake-draft (A, BB, AA, …, A) an army from a random, limited pool dealt for the room's Town Hall level:

- **Troops:** 7 picks per player, at most 2 of them super troops
- **Spells:** 4 picks
- **Siege machine:** 1 pick
- **Epic equipment:** 4 picks, at most 2 per hero

Heroes, pets and common equipment are free for everyone. Attacks are played as friendly challenges in a clan, and results go back into the board: stars, then destruction %, then time left.

## Features

- Create a room (Town Hall, default TH18; picks per player; timer) or join one, with a Town Hall filter
- Pool size follows the picks: about 1.5x what both players draft (15 troops, 6 supers, 12 spells, 4 sieges, 10 epics for the defaults)
- Both players read the rules, mark the epic equipment they don't own and press Ready. The pool is dealt then, with only epics both players own
- Either player can ask for a new pool during the draft; the other must accept, at most twice per room
- 20-second pick timer by default, with a random auto-pick; a bottom bar shows the clock and whose turn it is
- Finish drafting early once you have 5 troops, 3 spells, 1 siege and 2 epics
- Practice mode against a bot
- In-game style army builder with hard capacity limits, which makes an in-game "copy army" link. Each player builds from their own drafted picks.
- 30-second board preview before the first pick; 3-minute army-building timer after the draft
- Admin panel at `#admin` (Firebase email/password account) to watch and delete any room
- Home page shows one draft at the top (tap any room to show its board there), with each room's picks as a coloured strip by troop, spell, siege and epic
- Pick log, results and winner

## Running it

It's a static site (`index.html`, `icons/`, `firebase-config.js`) that keeps rooms on a Firebase server. Firestore stores the rooms and pushes live updates, and anonymous sign-in gives each browser a player id. Rooms live on the server, not in the browser. Picks are written in server-side transactions, so two players can't take the same item.

### 1. Set up Firebase (free Spark plan, about 5 minutes)

1. Go to https://console.firebase.google.com and add a project. Analytics isn't needed.
2. Open **Build → Firestore Database → Create database**. Pick production mode and a region near your players.
3. On Firestore's **Rules** tab, replace everything with the contents of [`firestore.rules`](firestore.rules) and click **Publish**.
4. Open **Build → Authentication → Get started → Sign-in method**, then enable **Anonymous**.
5. Open **Project settings → General → Your apps**, add a **Web app** (`</>`) and copy the config values into [`firebase-config.js`](firebase-config.js): `apiKey`, `authDomain`, `projectId`, `appId`. These values are safe to commit, because Firebase web keys are public and the rules protect the data.
6. Open **Authentication → Settings → Authorized domains** and add `minutkaaa.github.io`.

### 2. Turn on GitHub Pages

Go to the repo's **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, and select `main`, folder `/ (root)`. The site goes live at https://minutkaaa.github.io/coc-megadraft/.

If `firebase-config.js` is left empty, the app runs in **this device only** mode: rooms stay in the browser and one screen plays both seats. Practice against the bot still works.

### Access rules (`firestore.rules`)

- Anyone can see rooms and watch drafts.
- Only the host and the seated opponent can change a room, and a newcomer can only take an empty seat.
- Only the host can delete a room.

### Known limits

- Draft rules (slot caps, turn order) are checked in the browser, not by the server, so a player who edits the page code could cheat. That's fine among friends. A public ladder would need a Cloud Function to validate picks.
- Army capacities per Town Hall are in `CAP` in `tools/template.html`. TH12-17 were researched in November 2026 and may need updating after game changes.
- Old rooms aren't deleted, only hidden from the lists after 24 hours. Delete them from the Firebase console now and then.

### Local testing

Install the Firebase CLI, then run `firebase emulators:start --only firestore,auth --project demo-megadraft` and serve the folder with `python3 -m http.server`. In `firebase-config.js`, set `apiKey: "demo-key"`, `projectId: "demo-megadraft"`, `emulatorHost: "127.0.0.1"`.

## Updating game data

`tools/build.sh` pulls the latest game data and official icons from [ClashKingInc/ClashKingAssets](https://github.com/ClashKingInc/ClashKingAssets), then rebuilds `index.html` (needs Python 3 and Pillow).

The UI and logic live in `tools/template.html`. Edit that file, not `index.html`.

## Credits

Clash of Clans art and data © Supercell. This is an unofficial fan tool, made under Supercell's Fan Content Policy: https://supercell.com/en/fan-content-policy/. It is not affiliated with, endorsed, sponsored or specifically approved by Supercell, and Supercell is not responsible for it.
