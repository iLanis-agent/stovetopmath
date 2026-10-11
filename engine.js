/* Stovetop math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function article(n) { return /^(8|11|18)/.test(String(n)) ? "an" : "a"; }

  function boilKwh(waterL, startC) { return waterL * 4.186 * (100 - startC) / 3600 / 0.8; }
  function boilMin(waterL, watts, startC) { return boilKwh(waterL, startC) / (watts / 1000) * 60; }

  function boilPlan(waterL, watts, startC) {
    if (!(waterL > 0) || !(watts > 0) || !(startC >= 0)) return { error: "water, power and start temperature must be positive" };
    if (startC >= 100) return { error: "the start temperature must be below boiling" };
    return { waterL: waterL, watts: watts, startC: startC, kwh: r2(boilKwh(waterL, startC)), minutes: r1(boilMin(waterL, watts, startC)) };
  }

  function lidPlan(waterL, watts, startC) {
    if (!(waterL > 0) || !(watts > 0) || !(startC >= 0)) return { error: "water, power and start temperature must be positive" };
    if (startC >= 100) return { error: "the start temperature must be below boiling" };
    var open = boilMin(waterL, watts, startC);
    var lid = open * 0.75;
    return { waterL: waterL, watts: watts, startC: startC, openMin: r1(open), lidMin: r1(lid), savedMin: r1(open - lid) };
  }

  function yearPlan(boilsWeek, waterL, watts, startC, tariff) {
    if (!(boilsWeek > 0) || !(waterL > 0) || !(watts > 0) || !(startC >= 0) || !(tariff > 0)) return { error: "pace, water, power, temperature and tariff must be positive" };
    if (startC >= 100) return { error: "the start temperature must be below boiling" };
    var kwhYear = r2(boilKwh(waterL, startC) * boilsWeek * 52);
    var costYear = r2(kwhYear * tariff);
    return { boilsWeek: boilsWeek, waterL: waterL, watts: watts, startC: startC, tariff: tariff, kwhYear: kwhYear, costYear: costYear };
  }

  function renderBoil(r) {
    return r.waterL + " liter" + (r.waterL === 1 ? "" : "s") + " from a labeled " + r.startC + "°C on " + article(r.watts) + " " + r.watts + " W ring takes about " + r.minutes + " minutes - " + r.kwh + " kWh at a labeled 80% efficiency.";
  }

  function renderLid(r) {
    return "An open pot takes about " + r.openMin + " minutes; a labeled lid cuts that to about " + r.lidMin + " minutes - " + r.savedMin + " minutes saved every boil at a labeled 25% faster with the lid on.";
  }

  function renderYear(r) {
    return r.boilsWeek + " boils a week of " + r.waterL + " liter" + (r.waterL === 1 ? "" : "s") + " on " + article(r.watts) + " " + r.watts + " W ring uses about " + r.kwhYear + " kWh a year - about " + r.costYear + " at your labeled " + r.tariff + " per kWh tariff, at a labeled 80% efficiency.";
  }

  var api = { boilPlan: boilPlan, lidPlan: lidPlan, yearPlan: yearPlan,
              renderBoil: renderBoil, renderLid: renderLid, renderYear: renderYear };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.StovetopMath = api;
})(typeof window !== "undefined" ? window : this);
