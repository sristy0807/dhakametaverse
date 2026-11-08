# Dhaka Metaverse

A single-file, browser-based 3D driving game set on the **real road network of central Dhaka** (OpenStreetMap). Drive a car through Dhaka-style traffic, take ride-share passengers, race bots, honk at rickshaws and play your own YouTube playlist. Built with Three.js r128, no build step and no server needed.

## Run it

Open `index.html` in a browser (it loads Three.js r128 from cdnjs). Works on desktop and on phones in portrait or landscape.

| Input | Keyboard | Touch |
|---|---|---|
| Steer | A / D | ◀ ▶ |
| Gas / brake / reverse | W / S | GAS / BRAKE·REV (reverses when stopped) |
| Nitro | Shift | NITRO |
| Handbrake | Space | – |
| Horn | H | 📢 |

## Features

- **Real map** – roads, water, rail and junctions from OSM, streamed in 120 m chunks around the car (nothing outside the view distance is built). Area and street name panel.
- **Procedural buildings** – Dhaka-style oriented blocks with estimated heights, shop signs, lamps, poles and wires, placed without overlapping roads.
- **Traffic** – rickshaws, CNG, buses, cycles and cars drive on the left along the road polylines, queue behind each other, take junction turns and collide with mass-based physics. Density follows a predicted time-of-day model (🚦 label).
- **Ride sharing** – toggle on/off; requests pop up, A* routing along the OSM graph gives a guidance arrow, minimap route and 2–6 km trips with fares. A passenger waits at the kerb, boards, rides and is dropped off.
- **Race** – ৳500 entry, 3 laps against 4 bots, prizes, results screen.
- **Day/night** from system time, lighting and street lamps.
- **Sound** – synthesized engine, crash and horn (Web Audio, no audio files). Slower vehicles ahead sometimes pull aside when you honk.
- **Music** – paste YouTube video or playlist links; embedded player that can be minimised. Playlist is kept in `localStorage`.
- **Mobile UI** – compact portrait layout, large touch controls, wider field of view on narrow screens.

## Repository layout

| Path | What it is |
|---|---|
| `index.html` | The complete game (HTML + CSS + JS + embedded map data, ~1.1 MB). This is the file to run and publish. |
| `data/dhaka.json` | Processed road/water/rail/junction/place data (also embedded in `index.html` as `<script type="application/json" id="dhaka-data">`). |
| `src/engine.js` | Source of the OSM world engine: road lookup grid, junctions, A* routing, chunk builder, buildings. |
| `src/traffic.js` | Source of the traffic system: polyline-following vehicles, queueing, collisions. |
| `tools/convert.py` | Converts a raw Overpass JSON export into `dhaka.json`. |
| `tools/patches/` | The ordered Python patch scripts used to grow `index.html` feature by feature (history; they assume older versions of the file). |
| `tests/` | Ad-hoc puppeteer screenshot/behaviour scripts used during development (they point at a local `test.html`; see below). |

## Assets

There are no image, audio or model files; everything is generated at runtime.

- **Map data:** © OpenStreetMap contributors (ODbL). Area covered: roughly lat 23.706–23.774, lon 90.366–90.434 (Dhanmondi to Motijheel). Local metric projection with origin lat 23.74, lon 90.40; x = east, z = −north. Road classes 0–7 (service … motorway) with widths 3.8–16 m.
- **Geometry:** cars, vehicles, people, buildings, signs and lamps are code-built meshes (box geometry, merged per chunk for performance).
- **Sound:** oscillators and noise buffers through the Web Audio API.
- **Libraries:** Three.js r128 (CDN). YouTube playback uses the YouTube embedded player iframe.

## Build process

The game has no bundler. `index.html` is the source of truth and is edited directly. How it was produced:

1. **Get map data.** Export OSM data for the bounding box above from Overpass (highways, water, railway, place nodes and traffic signals, with member nodes, e.g. `out body; >; out skel qt;`) and save the JSON.
2. **Convert it.**
   ```bash
   python3 tools/convert.py raw-overpass.json   # writes dhaka.json in the current directory
   ```
   This projects coordinates, simplifies ways, assigns road classes and widths, finds junction nodes (`j:[[pointIndex, junctionId]]`) and writes `{o, bb, names, roads, water, wl, rail, places, sig}`.
3. **Embed.** `tools/patches/patch8.py` splices `src/engine.js`, `src/traffic.js` and the JSON into the HTML (the JSON goes into the `dhaka-data` script tag).
4. **Add features.** Later changes (portrait UI, audio/horn/music, passengers) were applied with small exact-match patch scripts (`patch20.py`–`patch23.py`), but you can simply edit `index.html` by hand.

### Testing

```bash
npm install                      # puppeteer-core + three@0.128
# make an offline copy that uses the local Three.js
sed 's#https://[^"]*three[^"]*\.js#node_modules/three/build/three.min.js#' index.html > test.html
node --check <(sed -n '/<script>/,/<\/script>/p' index.html | sed '1d;$d')   # syntax check
node tests/run16.js p1.png p2.png   # portrait screenshots
```

The scripts in `tests/` expect Chrome at `/usr/bin/google-chrome` and `test.html` in the working directory, and were written for a headless software-rendered environment, so adjust the paths for your machine.

## Known limits / roadmap

- Only central Dhaka is covered; add more OSM tiles for other districts.
- Building heights are estimated; flyovers and traffic signals are not modelled; some one-way destinations are unreachable and skipped.
- Tested with software rendering only; real-phone performance is unverified.
- Ideas: selectable Hi-Ace/private car and inter-city trips, scripted voice or LLM companion, signals and flyovers.
