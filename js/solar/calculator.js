/**
 * Solar Cell ROI & Sizing Calculator — Pure Functions
 *
 * Domain: Solar Cell ROI & System Sizing
 * All functions are stateless pure functions with no side effects.
 * Designed for easy unit testing with Jest / Vitest.
 *
 * Units used throughout:
 *   Energy  : kWh (kilowatt-hours)
 *   Power   : kW  (kilowatts), W (watts)
 *   Money   : THB (Thai Baht)
 *   Area    : m²
 *
 * Usage:
 *   import { calcAnnualEnergy, calcROI, calcSystemSize } from './calculator.js';
 */

'use strict';

// ─────────────────────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────────────────────

/** Thailand average peak sun hours per day (national average) */
export const DEFAULT_PEAK_SUN_HOURS = 4.5;

/** Thailand average grid electricity rate (THB / kWh) */
export const DEFAULT_ELECTRICITY_RATE_THB = 4.20;

/** System losses: wiring, soiling, inverter, temperature, etc. */
export const DEFAULT_SYSTEM_LOSS_FACTOR = 0.20;

/** Annual panel degradation rate after year 1 (fraction, e.g. 0.005 = 0.5% / yr) */
export const DEFAULT_DEGRADATION_ANNUAL = 0.005;

// ─────────────────────────────────────────────────────────────
// ENERGY PRODUCTION
// ─────────────────────────────────────────────────────────────

/**
 * Calculate estimated daily energy output of a solar system.
 *
 * Formula: E_daily = systemKW × peakSunHours × (1 - lossFactor)
 *
 * @param {number} systemKW       - Total installed capacity (kW)
 * @param {number} peakSunHours   - Daily peak sun hours (default: 4.5 for Thailand)
 * @param {number} lossFactor     - System loss fraction 0–1 (default: 0.20)
 * @returns {number} Daily energy in kWh
 *
 * @example
 * calcDailyEnergy(5)        // → 18.0  (5kW system, Thailand average)
 * calcDailyEnergy(10, 5.0)  // → 40.0  (10kW, sunny location)
 */
export function calcDailyEnergy(
  systemKW,
  peakSunHours = DEFAULT_PEAK_SUN_HOURS,
  lossFactor = DEFAULT_SYSTEM_LOSS_FACTOR
) {
  if (typeof systemKW !== 'number' || systemKW <= 0) throw new RangeError('systemKW must be a positive number');
  if (typeof peakSunHours !== 'number' || peakSunHours <= 0) throw new RangeError('peakSunHours must be a positive number');
  if (typeof lossFactor !== 'number' || lossFactor < 0 || lossFactor >= 1) throw new RangeError('lossFactor must be between 0 and 1');

  return systemKW * peakSunHours * (1 - lossFactor);
}

/**
 * Calculate annual energy output for a given year accounting for degradation.
 *
 * @param {number} systemKW          - Installed capacity (kW)
 * @param {number} year              - Year number (1-based: 1 = first year)
 * @param {number} peakSunHours      - Daily peak sun hours
 * @param {number} lossFactor        - System loss fraction
 * @param {number} degradationYear1  - First-year degradation fraction (e.g. 0.02)
 * @param {number} degradationAnnual - Annual degradation fraction after year 1
 * @returns {number} Annual energy in kWh
 *
 * @example
 * calcAnnualEnergy(5, 1)   // → ~6570  kWh  (year 1)
 * calcAnnualEnergy(5, 10)  // → ~6320  kWh  (year 10, degraded)
 */
export function calcAnnualEnergy(
  systemKW,
  year = 1,
  peakSunHours = DEFAULT_PEAK_SUN_HOURS,
  lossFactor = DEFAULT_SYSTEM_LOSS_FACTOR,
  degradationYear1 = 0.02,
  degradationAnnual = DEFAULT_DEGRADATION_ANNUAL
) {
  if (!Number.isInteger(year) || year < 1) throw new RangeError('year must be a positive integer');

  const baseDaily = calcDailyEnergy(systemKW, peakSunHours, lossFactor);

  let degradationFactor;
  if (year === 1) {
    degradationFactor = 1 - degradationYear1;
  } else {
    degradationFactor = (1 - degradationYear1) * Math.pow(1 - degradationAnnual, year - 1);
  }

  return Math.round(baseDaily * 365 * degradationFactor * 100) / 100;
}

// ─────────────────────────────────────────────────────────────
// SYSTEM SIZING
// ─────────────────────────────────────────────────────────────

/**
 * Calculate recommended system size (kW) to meet a daily energy demand.
 *
 * @param {number} dailyDemandKWh  - Target daily consumption (kWh)
 * @param {number} peakSunHours    - Daily peak sun hours
 * @param {number} lossFactor      - System loss fraction
 * @returns {number} Recommended system size in kW (rounded to 1 decimal)
 *
 * @example
 * calcSystemSize(18)   // → 5.0 kW  (18 kWh/day, Thailand average)
 * calcSystemSize(36)   // → 10.0 kW
 */
export function calcSystemSize(
  dailyDemandKWh,
  peakSunHours = DEFAULT_PEAK_SUN_HOURS,
  lossFactor = DEFAULT_SYSTEM_LOSS_FACTOR
) {
  if (typeof dailyDemandKWh !== 'number' || dailyDemandKWh <= 0) throw new RangeError('dailyDemandKWh must be positive');

  const raw = dailyDemandKWh / (peakSunHours * (1 - lossFactor));
  return Math.round(raw * 10) / 10;
}

/**
 * Calculate the number of panels needed for a system capacity.
 *
 * @param {number} systemKW     - System capacity (kW)
 * @param {number} panelWattage - Single panel rated wattage (W)
 * @returns {number} Number of panels (rounded up)
 *
 * @example
 * calcPanelCount(5, 550)  // → 10 panels
 * calcPanelCount(5, 400)  // → 13 panels
 */
export function calcPanelCount(systemKW, panelWattage) {
  if (typeof systemKW !== 'number' || systemKW <= 0) throw new RangeError('systemKW must be positive');
  if (typeof panelWattage !== 'number' || panelWattage <= 0) throw new RangeError('panelWattage must be positive');

  return Math.ceil((systemKW * 1000) / panelWattage);
}

/**
 * Estimate total roof area required for a panel array.
 *
 * @param {number} panelCount         - Number of panels
 * @param {number} panelAreaM2        - Area of a single panel (m²)
 * @param {number} spacingFactor      - Multiplier for row spacing (default 1.2)
 * @returns {number} Required roof area in m²
 *
 * @example
 * calcRoofArea(10, 2.58)   // → 30.96 m²  (10 × 550W Jinko + 20% spacing)
 */
export function calcRoofArea(panelCount, panelAreaM2, spacingFactor = 1.2) {
  if (typeof panelCount !== 'number' || panelCount <= 0) throw new RangeError('panelCount must be positive');
  if (typeof panelAreaM2 !== 'number' || panelAreaM2 <= 0) throw new RangeError('panelAreaM2 must be positive');

  return Math.round(panelCount * panelAreaM2 * spacingFactor * 100) / 100;
}

// ─────────────────────────────────────────────────────────────
// FINANCIAL / ROI
// ─────────────────────────────────────────────────────────────

/**
 * Calculate annual savings on electricity bill.
 *
 * @param {number} annualEnergyKWh   - Annual energy production (kWh)
 * @param {number} electricityRate   - Grid rate (THB / kWh)
 * @param {number} selfConsumptionPct - Fraction consumed on-site (0–1), rest is exported
 * @param {number} feedInTariffTHB   - Feed-in tariff for exported energy (THB / kWh)
 * @returns {number} Annual savings in THB
 *
 * @example
 * calcAnnualSavings(6570, 4.20, 0.80, 2.20)  // → ~23,300 THB/year
 */
export function calcAnnualSavings(
  annualEnergyKWh,
  electricityRate = DEFAULT_ELECTRICITY_RATE_THB,
  selfConsumptionPct = 0.80,
  feedInTariffTHB = 2.20
) {
  if (typeof annualEnergyKWh !== 'number' || annualEnergyKWh <= 0) throw new RangeError('annualEnergyKWh must be positive');
  if (selfConsumptionPct < 0 || selfConsumptionPct > 1) throw new RangeError('selfConsumptionPct must be 0–1');

  const selfConsumptionKWh = annualEnergyKWh * selfConsumptionPct;
  const exportedKWh = annualEnergyKWh * (1 - selfConsumptionPct);

  const savedOnBill = selfConsumptionKWh * electricityRate;
  const exportRevenue = exportedKWh * feedInTariffTHB;

  return Math.round((savedOnBill + exportRevenue) * 100) / 100;
}

/**
 * Calculate full ROI analysis over the system lifetime.
 *
 * @param {object} params
 * @param {number} params.systemKW              - System capacity (kW)
 * @param {number} params.totalCostTHB          - All-in installation cost (THB)
 * @param {number} params.electricityRate        - Grid rate (THB / kWh)
 * @param {number} params.selfConsumptionPct     - On-site consumption fraction
 * @param {number} params.feedInTariffTHB        - Export tariff (THB / kWh)
 * @param {number} params.peakSunHours           - Daily peak sun hours
 * @param {number} params.lossFactor             - System loss fraction
 * @param {number} params.degradationYear1       - First-year degradation fraction
 * @param {number} params.degradationAnnual      - Annual degradation after year 1
 * @param {number} params.systemLifetimeYears    - Analysis period in years
 * @returns {object} ROI analysis result
 *
 * @example
 * const roi = calcROI({ systemKW: 5, totalCostTHB: 180000, electricityRate: 4.20, ... });
 * roi.paybackYears   // → ~7.8
 * roi.lifetimeSavings // → ~180,000 THB
 * roi.irr            // → ~10%
 */
export function calcROI({
  systemKW,
  totalCostTHB,
  electricityRate = DEFAULT_ELECTRICITY_RATE_THB,
  selfConsumptionPct = 0.80,
  feedInTariffTHB = 2.20,
  peakSunHours = DEFAULT_PEAK_SUN_HOURS,
  lossFactor = DEFAULT_SYSTEM_LOSS_FACTOR,
  degradationYear1 = 0.02,
  degradationAnnual = DEFAULT_DEGRADATION_ANNUAL,
  systemLifetimeYears = 25,
}) {
  if (typeof totalCostTHB !== 'number' || totalCostTHB <= 0) throw new RangeError('totalCostTHB must be positive');

  let cumulativeSavings = 0;
  let paybackYears = null;
  const yearlyBreakdown = [];

  for (let y = 1; y <= systemLifetimeYears; y++) {
    const energy = calcAnnualEnergy(systemKW, y, peakSunHours, lossFactor, degradationYear1, degradationAnnual);
    const savings = calcAnnualSavings(energy, electricityRate, selfConsumptionPct, feedInTariffTHB);
    cumulativeSavings += savings;

    if (paybackYears === null && cumulativeSavings >= totalCostTHB) {
      const prevCumulative = cumulativeSavings - savings;
      const remaining = totalCostTHB - prevCumulative;
      paybackYears = Math.round((y - 1 + remaining / savings) * 10) / 10;
    }

    yearlyBreakdown.push({
      year: y,
      energyKWh: energy,
      savingsTHB: savings,
      cumulativeSavingsTHB: Math.round(cumulativeSavings * 100) / 100,
    });
  }

  const netProfit = cumulativeSavings - totalCostTHB;
  const roi25yr = Math.round((netProfit / totalCostTHB) * 100 * 10) / 10;

  return {
    paybackYears: paybackYears ?? '>25',
    lifetimeSavingsTHB: Math.round(cumulativeSavings * 100) / 100,
    netProfitTHB: Math.round(netProfit * 100) / 100,
    roiPct: roi25yr,
    yearlyBreakdown,
  };
}

// ─────────────────────────────────────────────────────────────
// UTILITY HELPERS
// ─────────────────────────────────────────────────────────────

/**
 * Convert panel physical dimensions to area in m².
 *
 * @param {number} lengthMM  - Panel length in mm
 * @param {number} widthMM   - Panel width in mm
 * @returns {number} Panel area in m² (rounded to 4 decimal places)
 *
 * @example
 * panelDimsToAreaM2(2278, 1134)  // → 2.5832 m²  (Jinko 550W)
 */
export function panelDimsToAreaM2(lengthMM, widthMM) {
  if (typeof lengthMM !== 'number' || typeof widthMM !== 'number') throw new TypeError('Dimensions must be numbers');
  if (lengthMM <= 0 || widthMM <= 0) throw new RangeError('Dimensions must be positive');

  return Math.round((lengthMM / 1000) * (widthMM / 1000) * 10000) / 10000;
}

/**
 * Calculate CO₂ savings in kg/year from solar generation.
 *
 * Thailand grid emission factor: 0.5213 kg CO₂ / kWh (EGAT 2023)
 *
 * @param {number} annualEnergyKWh  - Solar energy produced annually (kWh)
 * @param {number} emissionFactor   - Grid emission factor (kg CO₂ / kWh)
 * @returns {number} CO₂ savings in kg/year
 *
 * @example
 * calcCO2Savings(6570)  // → 3425 kg/year ≈ 3.4 tonnes
 */
export function calcCO2Savings(annualEnergyKWh, emissionFactor = 0.5213) {
  if (typeof annualEnergyKWh !== 'number' || annualEnergyKWh <= 0) throw new RangeError('annualEnergyKWh must be positive');

  return Math.round(annualEnergyKWh * emissionFactor);
}
