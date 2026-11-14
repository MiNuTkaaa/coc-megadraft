# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Clash of Clans players in Mikhail's clan community, casual-competitive, mostly on phones, often with the game open on the same device or a second one. A tournament organiser (Mikhail) runs rooms, spectates and administers. Players meet in Discord or clan chat, then open the site together to draft before attacking each other in friendly challenges.

## Product Purpose
A live two-player Megadraft for Clash of Clans, borrowing Clash Royale's Mega Draft format. Two players snake-draft troops, super troops, spells, siege machines and epic hero equipment from a shared random pool, then attack each other's own base using only what they drafted. Success: a full draft runs in a few minutes with no disputes about whose turn it is, what was picked, or what is legal, and players leave with a usable army link.

## Positioning
The only draft tool built around Clash of Clans' own army rules: Town Hall caps, max 2 supers, max 2 epics per hero, a pool restricted to equipment both players own, and an in-game style army builder that outputs a CopyArmy link.

## Operating Context
- Flow: create room (name, Town Hall, picks, timer, optional practice bot) > lobby (opponent joins, mark epics you don't own, Ready) > 30 s board preview > snake draft with per-pick timer, auto-pick, change-pool request (max 2, needs the other's consent), finish drafting early at the minimum > attack phase with 3-minute army-build timer, rosters, results (stars, %, time left) > rematch or close.
- Spectators can watch any room; an admin panel lists and deletes rooms.
- Played on phones in portrait during clan events; also on desktop by the organiser.

## Capabilities and Constraints
- Single static page, no framework, served by GitHub Pages; Firebase Firestore for live rooms.
- 112px WebP icons for every item, hero, pet and equipment (from ClashKingAssets) are the only imagery on hand.
- Defaults: TH18, 7 troops (max 2 supers), 4 spells, 1 siege, 4 epics; pool 15/6/12/4/10; 20 s timer.
- Fan-made, community tool. Must not imitate Supercell's official branding or logos.

## Brand Commitments
Name "CoC Megadraft". No other brand assets exist yet. (Inferred from the session, not interviewed.)

## Evidence on Hand
Real game data and icons in data.json and icons/. No player counts, testimonials or tournament results exist; do not invent them.

## Product Principles
- Whose turn it is must be unmistakable at a glance, on a phone, from across a room.
- The board is the product: pool, both rosters and the clock on one screen.
- Fair by construction: legality, consent for pool changes, randomness that is really random.
- Fast for friends: no accounts, a link to share, a draft done in minutes.
