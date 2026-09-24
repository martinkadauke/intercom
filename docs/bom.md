# What to buy (bill of materials)

State: 2026-09-24. Prices are rough, gross, from German/EU shops in September 2026 and only given
where we actually saw them. "Pending" means the choice is not made yet; do not buy those blind.

Parts marked **measure** have dimensions the maker does not publish. The drawings in
[hardware/parts](../hardware/parts/) show what is known and what still has to be measured.

## Indoors: network and power

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | PoE switch port, 802.3af or better, e.g. Ubiquiti USW-Lite-8-PoE | data + power down one cable | put the switch on a UPS |
| 1 | Ubiquiti ETH-SP-G2 surge protector | protects the house network from the outdoor cable | **must be earthed by an electrician**; datasheet lists 802.3af only |
| 1 | Short patch cable | switch → surge protector | |

## Through the wall

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | Ready-made outdoor Cat6 cable, solid copper AWG24, -40 to +75 °C, e.g. goobay 55432 (10 m) | the one cable | **not** goobay 94389 (copper-clad aluminium); no crimping needed |
| 1 | Split cable gland Conta-Clip KDS-KV M25 with split sealing insert | lets the moulded plug through, then seals | hole Ø25.5 mm |

## In the box: power

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | Industrial PoE splitter, rated down to -40 °C | separates data and power | **pending:** 12 V TRENDnet TI-SG104 (-40 to +75 °C, price unknown) or 5 V Waveshare industrial splitter (Amazon.de B0D795H51H, about €34) |
| 1 | Pololu D30V30F5 step-down 12 → 5 V, 3.4 A | 5 V rail | only with the 12 V splitter; about €24–34 |
| 1 set | Lever clamps (WAGO) or a small terminal strip | 5 V and ground distribution | |
| 1 | 0.3 m patch cable | splitter → doorbell computer | |

## In the box: the three computers

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | WT32-ETH01 (ESP32 + LAN8720 + RJ45) | doorbell computer, wired | about €20; no USB: flash it once over serial |
| 1 | USB-to-serial adapter, 3.3 V logic (e.g. CP2102 or CH340G) | first flash of the WT32-ETH01 | |
| 1 | Waveshare ESP32-S3-POE-ETH | talk computer, on WiFi | about €25–32; its plug-on PoE module is only for desk tests |
| 1 | LilyGO T5-4.7-S3 **Touch** (SKU H716) | screen computer + 4.7" e-paper, 960 × 540 | about €55 at OpenELAB; several marketplace listings with a touch photo are **not** touch versions; **measure** the mounting holes |

## Audio

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | INMP441 I²S MEMS microphone module | voice at the door | 3.3 V only; the labelled side (sound hole) faces the membrane |
| 1 | Adafruit MAX98357A I²S amplifier | drives the speaker | set to 3 dB: 100 kΩ from GAIN to Vin; 10 µF + 0.1 µF at its supply |
| 1 | VISATON K 40 SQ, 8 Ω, IP65/67 front | speaker behind the grille | 40 × 40 mm, Ø35 cut-out, 11.5 mm deep, 4 × Ø3.4 on 32 × 32; about €5.50 |
| 1 | Acoustic/vent membrane, self-adhesive PTFE, e.g. B+B Thermo-Technik DAM-AD10 | keeps water out of the mic holes | sold as a pressure vent: test voice quality through it |

## Light, sensor, heater

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | SK6812 RGBW LED strip, 5 V, ~4 LEDs used | light under the roof + status colours | a real white channel helps; **measure** height |
| 1 | SN74AHCT125N + DIP-14 socket + 330 Ω | lifts the 3.3 V LED data to 5 V | cheap insurance against flaky LEDs in the cold |
| 1 | 1000 µF electrolytic capacitor | at the strip, absorbs switch-on inrush | stripe = minus |
| 1 | BME280 module (with humidity) | box temperature and humidity | many "BMP280" boards look the same: check the chip ID |
| 1 | Silicone heater pad ~5 W (12 V candidate: round Ø50 × 1.5 mm, Amazon.de B0CTTRXZCC) | keeps the e-paper above 0 °C | voltage follows the splitter decision |
| 1 | Thermal fuse 73 °C | one-shot overheat cut-off | soldering heat can blow it: crimp, or heat-sink the leg |
| 1 | Opto-coupled MOSFET module (FR120N type) | switches the heater | needs ~10 V on the gate: fine on 12 V, use a logic-level module on 5 V |
| – | Thermally conductive tape | pad onto the display's back | |

## Button line

| Qty | Part | Why | Notes |
|---|---|---|---|
| 1 | A plain (dumb) brass push button, no electronics | the doorbell | the prototype uses a Ø48.5 mm ring |
| 2 | 10 kΩ resistor | pull-up + end-of-line at the button | the end-of-line one is soldered across the button contacts |
| 1 | 1 kΩ resistor, 1 × 100 nF capacitor | series resistor and filter | on perfboard |
| – | Adhesive-lined heat shrink | seals the joint behind the button | |

## Enclosure and front

| Qty | Part | Why | Notes |
|---|---|---|---|
| – | ASA filament | box and carrier plate | UV- and heat-resistant |
| – | Translucent filament | diffuser | |
| – | PLA | front-sheet prototype | the final front is brass |
| 1 | 2 mm brass sheet, laser-cut and folded by a metal shop | the final front | from [the front-sheet STEP](../hardware/models/front-sheet-v5.step); only after the bench tests pass |
| 4 | M3 countersunk brass screws, single slot (DIN 963) + M3 threaded inserts | hold the front | |
| 1 | Pressure vent M12 × 1.5 (Bopla DAE M12 or AGRO 595.15.AS) | the sealed box breathes | vents into the grille cavity |
| – | Gasket cord Ø2.0 mm + O-ring for the button (check the CAD groove: 42 × 2 or 26 × 2) | rain seal | |
| – | Neutral-cure silicone | around the diffuser | acetic-cure silicone corrodes brass |

## Optional

| Qty | Part | Why |
|---|---|---|
| 1 | Home Assistant Voice PE (+ USB-C 5 V / 3 A supply) | a chime inside the house |

## Not needed any more (so you do not buy them by mistake)

- A power supply in the technical room, passive PoE injector sets, a separate DC cable.
- Field-installable RJ45 plugs and cable rolls: the ready-made outdoor cable replaces them.
- A switch inside the box (only if WiFi calls fail the in-box test).
