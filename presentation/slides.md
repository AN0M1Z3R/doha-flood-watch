---
theme: default
title: Doha Flood Watch, Team Stark
info: |
  Arab Youth Space Hackathon 2026 · 813 Challenge · Proof of Concept
  Team Stark · Qatar · Theme: Climate-induced Disasters
fonts:
  sans: IBM Plex Sans
  serif: Source Serif 4
  weights: '400,500,600,700'
  provider: google
colorSchema: light
aspectRatio: 16/9
canvasWidth: 980
transition: fade
drawings:
  enabled: false
class: dark
exportFilename: doha-flood-watch-team-stark
---

<img src="/cover_bg.jpg" class="absolute inset-0 w-full h-full object-cover" alt="" />
<div class="cover-scrim"></div>
<div class="accent-bar"></div>

<div class="relative h-full flex flex-col justify-between py-2">
  <p class="eyebrow !text-[#7FA8FF]">Arab Youth Space Hackathon 2026 · 813 Challenge · Proof of Concept</p>
  <div>
    <h1 class="!text-6xl !mb-4">Doha Flood Watch</h1>
    <p class="!text-xl !leading-snug max-w-[34rem] !text-[#DCE5EE]">Mapping where heavy rain hit Doha, using free Sentinel-1 radar images</p>
  </div>
  <div class="flex gap-12">
    <div><p class="eyebrow !text-[#7FA8FF] !mb-0">Team</p><p class="!text-lg !font-semibold !text-[#F6F4EF] !m-0">Stark</p></div>
    <div><p class="eyebrow !text-[#7FA8FF] !mb-0">Country</p><p class="!text-lg !font-semibold !text-[#F6F4EF] !m-0">Qatar</p></div>
    <div><p class="eyebrow !text-[#7FA8FF] !mb-0">Theme</p><p class="!text-lg !font-semibold !text-[#F6F4EF] !m-0">Climate-induced Disasters</p></div>
  </div>
  <p class="!text-base !text-[#DCE5EE] !m-0">Ali AlHenzab (team leader) · Abdulla AlMuhaza · Hamad Abusheraida · Fahad AlMuraikhi</p>
</div>

<!--
Introduce the team and the idea in one line. We use radar satellites, which see through storm clouds, to map where heavy rain hit Doha hardest, and turn that into a ranked list of neighbourhoods for drainage and emergency teams.
The background image is our own output: blue = ground saturated by the 20 October 2018 storm.
-->

---

<p class="eyebrow">The story</p>

# What happened after the 2018 storm

<div class="grid grid-cols-4 gap-4 mt-10">
  <div v-click class="card">
    <div class="flex items-center gap-3"><div class="step-dot">1</div><carbon-rain-drop class="icon" /></div>
    <h3 class="mt-3">20 Oct 2018</h3>
    <p>Doha gets roughly a year's rain in one day. Roads, underpasses and buildings flood.</p>
  </div>
  <div v-click class="card">
    <div class="flex items-center gap-3"><div class="step-dot">2</div><carbon-cloud class="icon" /></div>
    <h3 class="mt-3">22 Oct</h3>
    <p>Optical satellite passes over, but scattered clouds and shadows hide the ground.</p>
  </div>
  <div v-click class="card">
    <div class="flex items-center gap-3"><div class="step-dot">3</div><carbon-satellite-radar class="icon" /></div>
    <h3 class="mt-3">27 Oct</h3>
    <p>Sentinel-1 radar passes over: it sees through cloud, day or night.</p>
  </div>
  <div v-click class="card !border-[#1F5FD6] !border-2">
    <div class="flex items-center gap-3"><div class="step-dot !bg-[#8A1538]">4</div><carbon-map class="icon !text-[#8A1538]" /></div>
    <h3 class="mt-3">~1 minute later</h3>
    <p>Our notebook turns the images into a map of the city and a ranked list of neighbourhoods.</p>
  </div>
</div>

<p class="mt-12 !text-xl">Radar sees through the cloud that blocked the optical satellite, and the data is free.</p>

<div class="footer"><span>Doha Flood Watch · Team Stark, Qatar</span><span>2</span></div>

<!--
Click through the four steps. Main point: storms bring cloud, so you need radar.
-->

---

<p class="eyebrow">The problem</p>

# Why heavy rain floods Doha

<div class="grid grid-cols-3 gap-4 mt-10">
  <div class="card">
    <p class="big">~75 mm</p>
    <p>That's Qatar's average rain for a whole year, so drainage was built for light rain.</p>
  </div>
  <div class="card">
    <p class="big">1 day</p>
    <p>On 20 Oct 2018 Doha received roughly a year's rainfall. Roads, underpasses and buildings flooded.</p>
  </div>
  <div class="card">
    <p class="big">Flat</p>
    <p>The city is paved and the desert ground is hard, so water collects in streets and low ground.</p>
  </div>
</div>

<div class="mt-12 flex items-start gap-3">
  <carbon-user-multiple class="icon mt-1" />
  <p class="!m-0">It affects residents, commuters, schools and businesses, and the agencies that have to find flooded areas and pump them out.</p>
</div>

<div class="footer"><span>Doha Flood Watch · Team Stark, Qatar</span><span>3</span></div>

<!--
Qatar's flood risk is not river or wadi flooding: the country is flat and mostly sealed, so heavy rain pools. Team: add local details you remember from that day.
-->

---

<p class="eyebrow">Business use case</p>

# Which areas get crews first?

<div class="grid grid-cols-2 gap-4 mt-5">
  <div class="card flex gap-4">
    <carbon-tool-kit class="icon shrink-0 mt-1" />
    <div><h3>Ashghal (Public Works Authority)</h3><p><b>Decides:</b> where to send pumps; which drainage to upgrade.<br><b>Today:</b> hotline calls and field patrols.</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-building class="icon shrink-0 mt-1" />
    <div><h3>Ministry of Municipality</h3><p><b>Decides:</b> where new development sits on flood-prone ground.<br><b>Today:</b> historic complaints, no citywide map.</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-warning-alt class="icon shrink-0 mt-1" />
    <div><h3>Civil Defence / Ministry of Interior</h3><p><b>Decides:</b> where to respond after a storm.<br><b>Today:</b> reports and social media, slow to assemble.</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-security class="icon shrink-0 mt-1" />
    <div><h3>Insurers in Qatar</h3><p><b>Decides:</b> which claims to triage; flood risk per location.<br><b>Today:</b> claim-by-claim inspection.</p></div>
  </div>
</div>

<p class="mt-5">We give them a map of the whole city after each satellite pass, even through cloud, as an image, a web map and tables they can open in GIS or Excel.</p>

<div class="footer"><span>Doha Flood Watch · Team Stark, Qatar</span><span>4</span></div>

<!--
The core user is the agency that runs drainage and pumping. Over several storms, the same map becomes a hotspot atlas for drainage investment.
-->

---

<p class="eyebrow">Data</p>

# Data we used

| Dataset | Dates | Role |
|---|---|---|
| Sentinel-1 radar (RTC, VV) | 3, 15 and 27 Oct 2018 | Dry baseline, before and after the storm |
| Sentinel-2 optical (L2A) | 12 and 22 Oct 2018 | True-colour map; proof that optical fails |
| ESA WorldCover 10 m | 2021 map | Land cover for exposure, sea mask |

<div class="grid grid-cols-2 gap-4 mt-5">
  <div class="card flex gap-4">
    <carbon-location class="icon shrink-0 mt-1" />
    <div><h3>Area of interest</h3><p>Central Doha, Al Rayyan and northern Al Wakrah: about 22 × 22 km at 20 m resolution.</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-chart-3d class="icon shrink-0 mt-1" />
    <div><h3>Hyperspectral</h3><p>We had no clear scene after the storm, so it isn't used here. We plan to add 813 or EnMAP data in incubation.</p></div>
  </div>
</div>

<div class="footer"><span>All via Microsoft Planetary Computer, no account needed · Copernicus Sentinel data · WorldCover CC BY 4.0</span><span>5</span></div>

<!--
All three radar images come from the same satellite, orbit and time of day, so the comparison is fair. Be upfront that hyperspectral is a next step.
-->

---
class: dark
---

<p class="eyebrow">Why radar</p>

# Why we switched to radar

<div class="flex gap-6 items-center mt-2">
  <img src="/why_radar.png" class="figure w-[600px]" alt="Sentinel-2 image of Doha two days after the storm with scattered clouds; red patches show where an optical water index wrongly flags cloud shadows as flood water" />
  <div class="flex flex-col gap-4">
    <p class="!m-0">The "2.2% cloud" image two days after the storm is full of small clouds over Doha.</p>
    <p class="!m-0">An optical water index flags <b class="text-[#F6F4EF]">15 km² of "flood"</b>, mostly cloud shadows.</p>
    <p class="!m-0 !text-[#F6F4EF] !text-lg"><b>Sentinel-1 radar sees through cloud, day and night.</b></p>
  </div>
</div>

<div class="footer"><span>Reproduce: python src/make_why_radar_figure.py</span><span>6</span></div>

<!--
We tried optical first. The cloud mask missed small clouds and their shadows, which look like water to the index, so we moved the whole project to radar.
-->

---

<p class="eyebrow">Approach</p>

# How it works

<div class="flex items-stretch gap-2 mt-10">
  <div class="card flex-1"><carbon-download class="icon" /><h3 class="mt-2">1 · Load</h3><p>Sentinel-1 before, after and dry-week images, clipped to Doha at 20 m</p></div>
  <carbon-arrow-right class="self-center text-[#8A1538] shrink-0" />
  <div class="card flex-1"><carbon-filter class="icon" /><h3 class="mt-2">2 · Clean</h3><p>Median speckle filter; remove sea plus a 300 m shoreline buffer</p></div>
  <carbon-arrow-right class="self-center text-[#8A1538] shrink-0" />
  <div class="card flex-1"><carbon-rain-drop class="icon" /><h3 class="mt-2">3 · Detect</h3><p>Backscatter up &gt; 3 dB = saturated ground; down + dark = standing water</p></div>
  <carbon-arrow-right class="self-center text-[#8A1538] shrink-0" />
  <div class="card flex-1"><carbon-checkmark-outline class="icon" /><h3 class="mt-2">4 · Validate</h3><p>Same detector on a dry week gives the false-alarm rate; thresholds 2 to 5 dB</p></div>
  <carbon-arrow-right class="self-center text-[#8A1538] shrink-0" />
  <div class="card flex-1"><carbon-list-numbered class="icon" /><h3 class="mt-2">5 · Rank</h3><p>km² by land cover; 1 km cells ranked by % of land saturated</p></div>
</div>

<p class="mt-12">The notebook saves a map image, an interactive web map and CSV tables. It runs in about a minute on a laptop, with no API keys.</p>

<div class="footer"><span>Code: src/floodmap.py · notebooks/01_doha_flood_mapping.ipynb</span><span>7</span></div>

<!--
Physics in one sentence: water raises the soil's dielectric constant, so wet ground reflects more radar energy, while smooth standing water mirrors it away and looks dark.
-->

---

<p class="eyebrow">How radar sees rain</p>

# What the radar shows

<img src="/radar_before_after.png" class="figure w-full mt-1" alt="Three panels of a 6 km area of western Doha: radar backscatter before the storm, after the storm, and the change map where blue shows ground that became wetter" />

<p class="mt-3 !text-sm">6 × 6 km of western Doha. Water raises the soil's dielectric constant, so saturated ground reflects more radar energy back to the satellite: <b class="text-[#1F5FD6]">blue = wetter after the storm</b>.</p>

<div class="footer"><span>Sentinel-1A, same orbit and time of day for both images</span><span>8</span></div>

<!--
Walk the judges left to right: before, after, and the difference. The blue patches are the storm's footprint a week later.
-->

---

<p class="eyebrow">Result</p>

# Where the 20 Oct 2018 storm hit Doha

<div class="flex gap-5 items-center mt-1">
  <img src="/doha_flood_impact_map.png" class="figure w-[640px] shrink-0" alt="Two-panel map of Doha: left, blue patches of rain-saturated ground over a true-colour image; right, a 1 km grid coloured by the share of land saturated with the top five cells numbered" />
  <div class="flex flex-col gap-4 flex-1 min-w-0">
    <p class="!m-0"><b class="text-[#1F5FD6]">Blue:</b> ground that became saturated (radar +3 dB)</p>
    <p class="!m-0"><b>Grid:</b> % of each 1 km cell's land saturated; darker = worse</p>
    <p class="!m-0"><b>1 to 5:</b> top priority cells for inspection</p>
    <a href="https://an0m1z3r.github.io/doha-flood-watch/results/doha_flood_impact_map.html" class="card !py-3 flex items-center gap-3 !no-underline !border-solid !border-[#1F5FD6] w-full">
      <carbon-launch class="icon shrink-0" />
      <span class="text-sm text-[#0F2233]"><b>Live interactive map</b><br><span class="text-xs text-[#3D4B5C]">an0m1z3r.github.io/doha-flood-watch</span></span>
    </a>
  </div>
</div>

<div class="footer"><span>Live: an0m1z3r.github.io/doha-flood-watch/results/doha_flood_impact_map.html</span><span>9</span></div>

<!--
Point to the inland western and southern neighbourhoods. If you have time, open the interactive HTML map live.
-->

---

<p class="eyebrow">Priority list</p>

# The five 1 km cells to inspect first

<img src="/top5_zoom.png" class="figure w-full mt-4" alt="Five zoomed satellite views, one per top-priority 1 km cell, with saturated ground in blue and the cell outlined in yellow; ranks 1 to 5 with the share of land saturated and coordinates" />

<div class="grid grid-cols-3 gap-4 mt-5">
  <div class="card"><h3>Yellow box</h3><p>The ranked 1 km cell</p></div>
  <div class="card"><h3>Blue</h3><p>Ground saturated by the storm</p></div>
  <div class="card"><h3>Full list</h3><p>Top 15 with coordinates in results/top15_priority_cells.csv</p></div>
</div>

<div class="footer"><span>Doha Flood Watch · Team Stark, Qatar</span><span>10</span></div>

<!--
Team: name the district under each cell from the coordinates; local knowledge makes this land. Cells 1 and 5 sit at the edge of our study area, so they include open ground near the coast.
-->

---

<p class="eyebrow">Key numbers</p>

# Main results

<div class="grid grid-cols-2 gap-5 mt-10">
  <div v-click class="card"><p class="big">57.5 km²</p><p>rain-saturated ground, 15.9% of the land analysed</p></div>
  <div v-click class="card"><p class="big">12.6×</p><p>signal vs false alarms on a dry week (57.5 vs 4.5 km²)</p></div>
  <div v-click class="card"><p class="big">42.2 km²</p><p>of built-up Doha saturated, 17.9% of all built-up land</p></div>
  <div v-click class="card"><p class="big">Top 15</p><p>1 km cells ranked for inspection; the worst had 57.5% of its land saturated</p></div>
</div>

<div class="footer"><span>Area analysed: 361 km² of land in Doha, Al Rayyan and northern Al Wakrah</span><span>11</span></div>

<!--
Say 57.5 square kilometres first, then the 12.6 times figure, which is why the number can be trusted.
-->

---

<p class="eyebrow">Validation and limitations</p>

# Checking the result

<div class="flex gap-6 mt-1">
  <img src="/threshold_chart.png" class="figure w-[500px] self-start" alt="Bar chart: area flagged as wet for the storm versus a dry week at thresholds from 2 to 5 dB; signal-to-noise between 7.3 and 13 times, 12.6 times at the 3 dB threshold used" />
  <div class="flex-1">
    <h3 class="mb-2">Limitations</h3>
    <ul class="!text-sm !leading-snug">
      <li>The first radar pass came 7 days after the storm, so we can only map saturated ground</li>
      <li>Standing water at day 7 (0.08 km²) is not above noise (0.06 km²), so we don't claim it</li>
      <li>Dense streets: building echoes can hide water</li>
      <li>Land cover from 2021, event in 2018</li>
      <li>Not yet checked against Ashghal hotspot records</li>
    </ul>
  </div>
</div>

<div class="footer"><span>No official flood map exists for this event, so the dry-week control is our ground reference</span><span>12</span></div>

<!--
The signal stays 7 to 13 times above the noise at every threshold, so it isn't down to the threshold we picked. The main limit is the 12-day revisit in 2018, which the incubation plan deals with.
-->

---
class: maroon
---

<p class="eyebrow">Impact and business model</p>

# What it changes, and who pays

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="card">
    <div class="flex items-center gap-3"><carbon-earth class="text-2xl text-[#F2C6D2]" /><h3>Impact</h3></div>
    <ul class="mt-2">
      <li>Crews and pumps go to the worst areas first</li>
      <li>Repeat-flooding hotspots guide drainage investment</li>
      <li>SDG 11 (resilient cities) and SDG 13 (climate action)</li>
      <li>Supports Qatar National Vision 2030 environmental goals</li>
    </ul>
  </div>
  <div class="card">
    <div class="flex items-center gap-3"><carbon-currency class="text-2xl text-[#F2C6D2]" /><h3>Business model</h3></div>
    <ul class="mt-2">
      <li>Annual subscription for government agencies: automatic report after every heavy-rain event</li>
      <li>Per-event reports and a flood-risk score per location for insurers</li>
      <li>Data costs almost nothing, since Copernicus data is free</li>
    </ul>
  </div>
</div>

<div class="footer"><span>Doha Flood Watch · Team Stark, Qatar</span><span>13</span></div>

<!--
Say clearly who pays and what for. Team: add a price point if you have one, for example a yearly licence of [QAR __] per agency. Do not invent market figures.
-->

---

<p class="eyebrow">Team</p>

# Our team

<div class="grid grid-cols-2 gap-5 mt-8">
  <div class="card flex gap-4">
    <carbon-user-avatar class="icon shrink-0 mt-1 !text-[#8A1538]" />
    <div><h3>Ali AlHenzab</h3><p class="!text-[#8A1538] !font-semibold !mt-1">Team lead & business</p><p>Business model, stakeholder contact, pitch</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-satellite-radar class="icon shrink-0 mt-1" />
    <div><h3>Hamad Abusheraida</h3><p class="!text-[#1F5FD6] !font-semibold !mt-1">Satellite data analyst</p><p>Sentinel-1 radar processing, flood detection, validation</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-code class="icon shrink-0 mt-1" />
    <div><h3>Abdulla AlMuhaza</h3><p class="!text-[#1F5FD6] !font-semibold !mt-1">Software & data engineer</p><p>Notebook, code, repository, interactive map</p></div>
  </div>
  <div class="card flex gap-4">
    <carbon-user-multiple class="icon shrink-0 mt-1" />
    <div><h3>Fahad AlMuraikhi</h3><p class="!text-[#1F5FD6] !font-semibold !mt-1">Impact & user research</p><p>Qatar flood context, user interviews, SDG and Vision 2030 alignment</p></div>
  </div>
</div>

<p class="mt-8">Between us we cover the satellite analysis, the software, the users and the business side.</p>

<div class="footer"><span>Doha Flood Watch · Team Stark, Qatar</span><span>14</span></div>

<!--
Each member introduces themselves in one sentence, with their background. Judges score team strength on skills that match what the solution needs.
-->

---
class: dark
---

<p class="eyebrow">Next steps</p>

# What we would do in incubation

<div class="grid grid-cols-2 gap-x-8 gap-y-6 mt-6">
  <div class="flex gap-4"><carbon-time class="text-3xl text-[#7FA8FF] shrink-0" /><div><h3>Faster revisits</h3><p class="!mt-1">Sentinel-1A, 1C and commercial radar together: images within 1 to 3 days, early enough to see standing water</p></div></div>
  <div class="flex gap-4"><carbon-map class="text-3xl text-[#7FA8FF] shrink-0" /><div><h3>Hotspot atlas</h3><p class="!mt-1">Every major Qatar rain event since 2015: cells that flood every time</p></div></div>
  <div class="flex gap-4"><carbon-chart-3d class="text-3xl text-[#7FA8FF] shrink-0" /><div><h3>Hyperspectral</h3><p class="!mt-1">813 / EnMAP spectra to separate wet soil, water and dark urban surfaces</p></div></div>
  <div class="flex gap-4"><carbon-cloud-upload class="text-3xl text-[#7FA8FF] shrink-0" /><div><h3>Deploy on GIQ</h3><p class="!mt-1">Triggered by Qatar Meteorology Department heavy-rain alerts; map delivered hours after the next pass</p></div></div>
</div>

<p class="mt-10 !text-2xl !text-[#F6F4EF] font-serif !mb-1">Thank you · Team Stark, Qatar</p>
<p class="!text-base !m-0">Ali AlHenzab · Abdulla AlMuhaza · Hamad Abusheraida · Fahad AlMuraikhi</p>

<div class="footer"><span>Doha Flood Watch</span><span>15</span></div>

<!--
Close with the ask: incubation support for faster radar data, validation with Ashghal, and deployment on the GIQ platform.
-->
