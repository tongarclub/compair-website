/**
 * AI Hardware VRAM Calculator — Pure Functions
 *
 * Domain: AI Hardware Compatibility
 * All functions are stateless pure functions with no side effects.
 * Designed for easy unit testing with Jest / Vitest.
 *
 * Usage:
 *   import { getQuantCompatibility, scoreGPU, estimateTokPerSec } from './calculator.js';
 */

'use strict';

// ─────────────────────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────────────────────

/** VRAM overhead multiplier — models need ~10% extra breathing room */
export const VRAM_OVERHEAD = 1.10;

/** Reference bandwidth (GB/s) used to normalise token speed estimates */
export const BANDWIDTH_REFERENCE_GBS = 600;

/**
 * Compatibility status values.
 * - ok    : VRAM is sufficient with comfortable headroom
 * - warn  : VRAM is tight but runnable (may stutter on large context)
 * - split : Not enough VRAM alone, but GPU+CPU split is viable
 * - no    : Incompatible — cannot run even with offload
 */
export const STATUS = Object.freeze({
  OK: 'ok',
  WARN: 'warn',
  SPLIT: 'split',
  NO: 'no',
});

// ─────────────────────────────────────────────────────────────
// CORE CALCULATION FUNCTIONS
// ─────────────────────────────────────────────────────────────

/**
 * Determine whether a given GPU can run a model at a specific quantization level.
 *
 * @param {number} gpuVramGB       - Available GPU VRAM in GB
 * @param {number} modelVramGB     - Model VRAM requirement at this quantization (GB)
 * @param {number} systemRamGB     - System RAM available for CPU offload (GB)
 * @returns {'ok'|'warn'|'split'|'no'} Compatibility status
 *
 * @example
 * getQuantCompatibility(12, 4.1, 32) // → 'ok'   (RTX 4070 + Llama-3.1-8B Q4_K_M)
 * getQuantCompatibility(8, 14, 32)   // → 'split' (RTX 3060 Ti + Llama-2-13B Q8)
 * getQuantCompatibility(8, 40, 16)   // → 'no'    (RTX 3060 Ti + Llama-3.1-70B Q4)
 */
export function getQuantCompatibility(gpuVramGB, modelVramGB, systemRamGB) {
  if (typeof gpuVramGB !== 'number' || typeof modelVramGB !== 'number' || typeof systemRamGB !== 'number') {
    throw new TypeError('All arguments must be numbers');
  }
  if (gpuVramGB <= 0 || modelVramGB <= 0 || systemRamGB < 0) {
    throw new RangeError('VRAM and RAM values must be positive');
  }

  const ratio = gpuVramGB / modelVramGB;

  if (ratio >= VRAM_OVERHEAD)       return STATUS.OK;
  if (ratio >= 0.90)                return STATUS.WARN;
  if (ratio >= 0.55 && systemRamGB >= 24) return STATUS.SPLIT;
  return STATUS.NO;
}

/**
 * Evaluate all quantization levels for a model against available hardware.
 *
 * @param {object} model        - Model object with quantization VRAM keys
 * @param {number} gpuVramGB    - GPU VRAM in GB
 * @param {number} systemRamGB  - System RAM in GB
 * @param {Array}  quantKeys    - Array of { key, label, qualityPct }
 * @returns {Array<{ key, label, qualityPct, vramGB, status }>}
 *
 * @example
 * const quants = evaluateModelQuants(llama8b, 12, 32, QUANT_KEYS);
 */
export function evaluateModelQuants(model, gpuVramGB, systemRamGB, quantKeys) {
  if (!model || typeof model !== 'object') throw new TypeError('model must be an object');
  if (!Array.isArray(quantKeys) || quantKeys.length === 0) throw new TypeError('quantKeys must be a non-empty array');

  return quantKeys.map(q => {
    const vramGB = model.quantizations?.[q.key]?.vramGB ?? model[q.key];
    if (vramGB == null) throw new Error(`Quantization key "${q.key}" not found in model`);

    return {
      key: q.key,
      label: q.label,
      qualityPct: q.qualityPct,
      vramGB,
      status: getQuantCompatibility(gpuVramGB, vramGB, systemRamGB),
    };
  });
}

/**
 * Determine the best overall compatibility status for a model from its quant results.
 *
 * @param {Array<{ status: string }>} quantResults - Output of evaluateModelQuants
 * @returns {'ok'|'warn'|'split'|'no'} Best achievable status
 */
export function getBestCompatStatus(quantResults) {
  if (!Array.isArray(quantResults) || quantResults.length === 0) {
    throw new TypeError('quantResults must be a non-empty array');
  }

  const priority = [STATUS.OK, STATUS.WARN, STATUS.SPLIT, STATUS.NO];
  for (const s of priority) {
    if (quantResults.some(q => q.status === s)) return s;
  }
  return STATUS.NO;
}

/**
 * Estimate inference speed in tokens per second.
 *
 * Formula: baseSpeed × (actualBandwidth / referenceBandwidth)
 * Result is clamped to a minimum of 1 tok/s.
 *
 * @param {number} baseTokensPerSec  - Model's baseline tok/s at reference bandwidth
 * @param {number} actualBandwidthGBs - GPU memory bandwidth (GB/s)
 * @returns {number} Estimated tokens per second (integer)
 *
 * @example
 * estimateTokPerSec(80, 1008) // → ~134  (RTX 4090 running 7B)
 * estimateTokPerSec(80, 272)  // → ~36   (RTX 4060 running 7B)
 */
export function estimateTokPerSec(baseTokensPerSec, actualBandwidthGBs) {
  if (typeof baseTokensPerSec !== 'number' || typeof actualBandwidthGBs !== 'number') {
    throw new TypeError('Arguments must be numbers');
  }
  const raw = baseTokensPerSec * (actualBandwidthGBs / BANDWIDTH_REFERENCE_GBS);
  return Math.max(1, Math.round(raw));
}

/**
 * Compute an overall GPU suitability score (0–100) for running LLMs.
 *
 * Scoring weights:
 *   60% raw performance tier  (perfScore / 10 × 60)
 *   40% VRAM headroom         (capped at 24 GB reference, linearly scaled)
 *
 * @param {number} perfScore  - GPU performance tier 1–10
 * @param {number} vramGB     - GPU VRAM in GB
 * @returns {number} Score 0–100
 *
 * @example
 * scoreGPU(10, 24) // → 100 (RTX 4090)
 * scoreGPU(5,  8)  // → 43  (RTX 4060 Ti 8GB)
 */
export function scoreGPU(perfScore, vramGB) {
  if (typeof perfScore !== 'number' || typeof vramGB !== 'number') {
    throw new TypeError('Arguments must be numbers');
  }
  if (perfScore < 0 || perfScore > 10) throw new RangeError('perfScore must be 0–10');
  if (vramGB <= 0) throw new RangeError('vramGB must be positive');

  const perfComponent = (perfScore / 10) * 60;
  const vramComponent = Math.min(100, (vramGB / 24) * 40);
  return Math.min(100, Math.round(perfComponent + vramComponent));
}

/**
 * Determine GPU compute backend label.
 *
 * @param {{ cuda: boolean, brand: string }} gpu
 * @returns {'CUDA'|'Metal'|'ROCm'|'Vulkan'}
 */
export function getComputeBackend(gpu) {
  if (!gpu || typeof gpu !== 'object') throw new TypeError('gpu must be an object');
  if (gpu.cuda) return 'CUDA';
  if (gpu.brand === 'Apple') return 'Metal';
  if (gpu.brand === 'AMD') return 'ROCm';
  return 'Vulkan';
}

/**
 * Recommend the best quantization level for a given GPU VRAM.
 * Returns the highest-quality quant the GPU can handle with STATUS.OK.
 * Falls back to WARN, then SPLIT, then null if nothing works.
 *
 * @param {Array<{ key, label, vramGB, status }>} quantResults - from evaluateModelQuants
 * @returns {{ key, label, vramGB, status }|null} Best recommended quant or null
 *
 * @example
 * const best = recommendQuant(evaluateModelQuants(llama8b, 12, 32, QUANT_KEYS));
 * // → { key: 'q8_0', label: 'Q8.0', ... } for RTX 4070 12GB
 */
export function recommendQuant(quantResults) {
  if (!Array.isArray(quantResults)) throw new TypeError('quantResults must be an array');
  for (const preferred of [STATUS.OK, STATUS.WARN, STATUS.SPLIT]) {
    const found = quantResults.find(q => q.status === preferred);
    if (found) return found;
  }
  return null;
}
