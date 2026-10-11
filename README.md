# Stovetop math

How long the pasta water really takes, what the lid is worth in minutes, and what the boiling habit costs the grid in a year. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/stovetopmath/

## The three tools

- **Boil plan** - `boilPlan(waterL, watts, startC)`: liters, watts and start temperature become minutes and kWh.
- **Lid plan** - `lidPlan(waterL, watts, startC)`: the same boil with a labeled lid effect becomes minutes saved.
- **Year plan** - `yearPlan(boilsWeek, waterL, watts, startC, tariff)`: boils a week become kWh and cost per year.

## Labeled norms (illustrative references, not rules)

- Physics: 4.186 kJ to raise a liter by one degree, at a labeled 80% ring efficiency.
- Start: 20°C tap water. Lid effect: about 25% faster with the lid on.
- Tariff: 0.15 per kWh reference; put in your own. Altitude, pot and ring decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (36 cases, 108 checks)

Regenerate the oracle expectations: `python3 oracle.py`
