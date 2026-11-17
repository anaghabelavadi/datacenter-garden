# System map data

Source and exports for [`content/project/system-map.md`](../../content/project/system-map.md) and the explorer at `content/static/system-map.htm`.

| File | What it is |
| --- | --- |
| `impact-taxonomy.tsv` | Header rows of the team's impact taxonomy sheet (input) |
| `model.py` | Single source of truth: drivers, signed links, loops, physical parts, stock-and-flow panels. Validates labels and loop polarity. |
| `model.json` | Built model (output) |
| `nodes.csv`, `links.csv` | Kumu-ready elements and connections |
| `loops.csv` | Named loops with type, path and story |
| `component_impacts.csv` | Physical part → impact mapping |

Rebuild: `cd data/system-map && python3 model.py impact-taxonomy.tsv`

Everything here is agent-drafted and unverified (see `AGENTS.md`). Add a source per link before promoting.
