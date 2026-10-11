#!/usr/bin/env python3
"""Oracle mirror of engine.js for Stovetop math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def article(n):
    s = str(int(n)) if isinstance(n, float) and n == int(n) else str(n)
    return "an" if s.startswith(("8", "11", "18")) else "a"

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def boilKwh(waterL, startC): return waterL * 4.186 * (100 - startC) / 3600 / 0.8
def boilMin(waterL, watts, startC): return boilKwh(waterL, startC) / (watts / 1000) * 60

def boilPlan(waterL, watts, startC):
    if not (waterL > 0) or not (watts > 0) or not (startC >= 0):
        return {"error": "water, power and start temperature must be positive"}
    if startC >= 100:
        return {"error": "the start temperature must be below boiling"}
    return {"waterL": jsnum(float(waterL)), "watts": jsnum(float(watts)), "startC": jsnum(float(startC)),
            "kwh": jsnum(r2(boilKwh(waterL, startC))), "minutes": jsnum(r1(boilMin(waterL, watts, startC)))}

def lidPlan(waterL, watts, startC):
    if not (waterL > 0) or not (watts > 0) or not (startC >= 0):
        return {"error": "water, power and start temperature must be positive"}
    if startC >= 100:
        return {"error": "the start temperature must be below boiling"}
    open_m = boilMin(waterL, watts, startC)
    lid = open_m * 0.75
    return {"waterL": jsnum(float(waterL)), "watts": jsnum(float(watts)), "startC": jsnum(float(startC)),
            "openMin": jsnum(r1(open_m)), "lidMin": jsnum(r1(lid)), "savedMin": jsnum(r1(open_m - lid))}

def yearPlan(boilsWeek, waterL, watts, startC, tariff):
    if not (boilsWeek > 0) or not (waterL > 0) or not (watts > 0) or not (startC >= 0) or not (tariff > 0):
        return {"error": "pace, water, power, temperature and tariff must be positive"}
    if startC >= 100:
        return {"error": "the start temperature must be below boiling"}
    kwhYear = r2(boilKwh(waterL, startC) * boilsWeek * 52)
    costYear = r2(kwhYear * tariff)
    return {"boilsWeek": jsnum(float(boilsWeek)), "waterL": jsnum(float(waterL)), "watts": jsnum(float(watts)),
            "startC": jsnum(float(startC)), "tariff": jsnum(float(tariff)),
            "kwhYear": jsnum(kwhYear), "costYear": jsnum(costYear)}

def renderBoil(r):
    return (fmt(r["waterL"]) + " liter" + ("" if r["waterL"] == 1 else "s") + " from a labeled " + fmt(r["startC"]) + "°C on " + article(r["watts"]) + " " + fmt(r["watts"]) +
            " W ring takes about " + fmt(r["minutes"]) + " minutes - " + fmt(r["kwh"]) + " kWh at a labeled 80% efficiency.")

def renderLid(r):
    return ("An open pot takes about " + fmt(r["openMin"]) + " minutes; a labeled lid cuts that to about " + fmt(r["lidMin"]) +
            " minutes - " + fmt(r["savedMin"]) + " minutes saved every boil at a labeled 25% faster with the lid on.")

def renderYear(r):
    return (fmt(r["boilsWeek"]) + " boils a week of " + fmt(r["waterL"]) + " liter" + ("" if r["waterL"] == 1 else "s") + " on " + article(r["watts"]) + " " + fmt(r["watts"]) +
            " W ring uses about " + fmt(r["kwhYear"]) + " kWh a year - about " + fmt(r["costYear"]) + " at your labeled " +
            fmt(r["tariff"]) + " per kWh tariff, at a labeled 80% efficiency.")

CASES = []
CASES.append({"fn": "boilPlan", "args": [1.5, 2000, 20]})
CASES.append({"fn": "boilPlan", "args": [1, 1500, 15]})
CASES.append({"fn": "boilPlan", "args": [2, 1800, 10]})
CASES.append({"fn": "boilPlan", "args": [0.5, 2200, 25]})
CASES.append({"fn": "boilPlan", "args": [3, 1200, 20]})
CASES.append({"fn": "boilPlan", "args": [0.8, 2500, 5]})
CASES.append({"fn": "boilPlan", "args": [0, 2000, 20]})
CASES.append({"fn": "boilPlan", "args": [1.5, 0, 20]})
CASES.append({"fn": "boilPlan", "args": [1.5, 2000, 100]})
CASES.append({"fn": "boilPlan", "args": [1.5, 2000, 110]})
CASES.append({"fn": "boilPlan", "args": [2.5, 800, 18]})
CASES.append({"fn": "boilPlan", "args": [1.2, 3000, 22]})
CASES.append({"fn": "lidPlan", "args": [1.5, 2000, 20]})
CASES.append({"fn": "lidPlan", "args": [1, 1500, 15]})
CASES.append({"fn": "lidPlan", "args": [2, 1800, 10]})
CASES.append({"fn": "lidPlan", "args": [0.5, 2200, 25]})
CASES.append({"fn": "lidPlan", "args": [3, 1200, 20]})
CASES.append({"fn": "lidPlan", "args": [2.5, 800, 18]})
CASES.append({"fn": "lidPlan", "args": [0, 2000, 20]})
CASES.append({"fn": "lidPlan", "args": [1.5, 0, 20]})
CASES.append({"fn": "lidPlan", "args": [1.5, 2000, 100]})
CASES.append({"fn": "lidPlan", "args": [1.2, 3000, 22]})
CASES.append({"fn": "lidPlan", "args": [0.8, 2500, 5]})
CASES.append({"fn": "lidPlan", "args": [1.5, 2000, 105]})
CASES.append({"fn": "yearPlan", "args": [5, 1.5, 2000, 20, 0.15]})
CASES.append({"fn": "yearPlan", "args": [3, 1, 1500, 15, 0.25]})
CASES.append({"fn": "yearPlan", "args": [7, 2, 1800, 10, 0.12]})
CASES.append({"fn": "yearPlan", "args": [10, 0.5, 2200, 25, 0.4]})
CASES.append({"fn": "yearPlan", "args": [2, 3, 1200, 20, 0.55]})
CASES.append({"fn": "yearPlan", "args": [4, 2.5, 800, 18, 0.22]})
CASES.append({"fn": "yearPlan", "args": [0, 1.5, 2000, 20, 0.15]})
CASES.append({"fn": "yearPlan", "args": [5, 0, 2000, 20, 0.15]})
CASES.append({"fn": "yearPlan", "args": [5, 1.5, 2000, 100, 0.15]})
CASES.append({"fn": "yearPlan", "args": [5, 1.5, 2000, 20, 0]})
CASES.append({"fn": "yearPlan", "args": [6, 1.2, 3000, 22, 0.3]})
CASES.append({"fn": "yearPlan", "args": [1, 0.8, 2500, 5, 0.65]})

out = []
for c in CASES:
    fn = {"boilPlan": boilPlan, "lidPlan": lidPlan, "yearPlan": yearPlan}[c["fn"]]
    r = fn(*c["args"])
    is_err = "error" in r
    if is_err:
        render = r["error"]
    else:
        render = {"boilPlan": renderBoil, "lidPlan": renderLid, "yearPlan": renderYear}[c["fn"]](r)
    out.append({"fn": c["fn"], "args": c["args"], "result": r, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(out), "cases")
