# CoC Megadraft

A draft board for running Clash of Clans Megadraft matches, modeled on Clash Royale's Mega Draft.

Two players snake-draft (A, BB, AA, …, A) an army from a random, limited pool dealt for the room's Town Hall level:

- **Troops:** 7 picks per player, at most 2 of them super troops
- **Spells:** 4 picks
- **Siege machine:** 1 pick
- **Epic equipment:** 4 picks, at most 2 per hero

Heroes, pets and common equipment are free for everyone. Attacks are played as friendly challenges in a clan, and results go back into the board: stars, then destruction %, then time left.

## Features

- Create a room (Town Hall, pick limits, timer, pool sizes) or join one, with a Town Hall filter
- Pool sizes default to about 1.5× what both players draft, capped at what exists at that Town Hall
- Practice mode against a bot
- Timer with random auto-pick, pick log, army export, results and winner

## Running it

It's one static page: `index.html` plus the `icons/` folder. Open it locally or serve it with GitHub Pages (Settings → Pages → deploy from branch `main`, folder `/`).

**Multiplayer:** live shared rooms only work when the page runs as a Claude artifact. Anywhere else, including GitHub Pages, it falls back to **this device only** mode, where rooms are saved in the browser and one screen plays both seats. That mode still works for practice against the bot and for a draft run on a single shared screen. Open rooms on GitHub Pages need a shared backend, such as Firebase or Supabase, plugged into the `Store` object in `tools/template.html`.

## Updating game data

`tools/build.sh` pulls the latest game data and official icons from [ClashKingInc/ClashKingAssets](https://github.com/ClashKingInc/ClashKingAssets), then rebuilds `index.html` (needs Python 3 and Pillow).

The UI and logic live in `tools/template.html`. Edit that file, not `index.html`.

## Credits

Clash of Clans art and data © Supercell. This is an unofficial fan tool, made under Supercell's Fan Content Policy: https://supercell.com/en/fan-content-policy/. It is not affiliated with, endorsed, sponsored or specifically approved by Supercell, and Supercell is not responsible for it.
