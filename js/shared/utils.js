/**
 * Shared Utilities
 *
 * Pure helper functions shared across both AI and Solar domains.
 * Stateless, side-effect-free — safe to import anywhere.
 */

'use strict';

// ─────────────────────────────────────────────────────────────
// JSON-LD / Schema.org Injection
// ─────────────────────────────────────────────────────────────

/**
 * Inject a JSON-LD script tag into <head> for AEO/SEO.
 * Replaces any existing tag with the same id to avoid duplicates.
 *
 * @param {object} schemaObject  - Schema.org object to inject
 * @param {string} tagId         - Unique ID for the script tag (default: 'jsonld-main')
 *
 * @example
 * injectJsonLd({ "@context": "https://schema.org", "@type": "FAQPage", ... });
 */
export function injectJsonLd(schemaObject, tagId = 'jsonld-main') {
  if (typeof document === 'undefined') return; // SSR / Node guard
  let el = document.getElementById(tagId);
  if (!el) {
    el = document.createElement('script');
    el.id = tagId;
    el.type = 'application/ld+json';
    document.head.appendChild(el);
  }
  el.textContent = JSON.stringify(schemaObject, null, 2);
}

/**
 * Build a Schema.org FAQPage object from question/answer pairs.
 *
 * @param {Array<{ question: string, answer: string }>} faqs
 * @returns {object} FAQPage JSON-LD object
 *
 * @example
 * buildFaqSchema([{ question: 'RTX 4060 รัน 7B ได้ไหม?', answer: 'ได้ ด้วย Q4_K_M' }])
 */
export function buildFaqSchema(faqs) {
  if (!Array.isArray(faqs) || faqs.length === 0) throw new TypeError('faqs must be a non-empty array');

  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(({ question, answer }) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: { '@type': 'Answer', text: answer },
    })),
  };
}

/**
 * Build a Schema.org HowTo object (useful for calculator pages).
 *
 * @param {object} params
 * @param {string}   params.name         - HowTo title
 * @param {string}   params.description  - Brief description
 * @param {Array<{ name: string, text: string }>} params.steps
 * @returns {object} HowTo JSON-LD object
 */
export function buildHowToSchema({ name, description, steps }) {
  if (!name || !steps?.length) throw new TypeError('name and steps are required');

  return {
    '@context': 'https://schema.org',
    '@type': 'HowTo',
    name,
    description,
    step: steps.map((s, i) => ({
      '@type': 'HowToStep',
      position: i + 1,
      name: s.name,
      text: s.text,
    })),
  };
}

// ─────────────────────────────────────────────────────────────
// DATA FETCHING
// ─────────────────────────────────────────────────────────────

/**
 * Fetch a JSON file from the /data directory and parse it.
 * Throws with a descriptive error on network or parse failure.
 *
 * @param {string} relativePath  - Path relative to site root, e.g. '/data/ai-models/gpus.json'
 * @returns {Promise<object>} Parsed JSON object
 *
 * @example
 * const gpuData = await fetchData('/data/ai-models/gpus.json');
 */
export async function fetchData(relativePath) {
  if (typeof relativePath !== 'string' || relativePath.trim() === '') {
    throw new TypeError('relativePath must be a non-empty string');
  }
  const res = await fetch(relativePath);
  if (!res.ok) throw new Error(`Failed to load ${relativePath}: HTTP ${res.status}`);
  try {
    return await res.json();
  } catch {
    throw new Error(`Failed to parse JSON from ${relativePath}`);
  }
}

// ─────────────────────────────────────────────────────────────
// FORMATTING HELPERS
// ─────────────────────────────────────────────────────────────

/**
 * Format a number as Thai Baht with comma thousands separator.
 *
 * @param {number} amount  - Amount in THB
 * @param {boolean} short  - If true, abbreviate thousands as 'K' (e.g. 180K)
 * @returns {string}
 *
 * @example
 * formatTHB(180000)        // → '฿180,000'
 * formatTHB(180000, true)  // → '฿180K'
 */
export function formatTHB(amount, short = false) {
  if (typeof amount !== 'number') throw new TypeError('amount must be a number');
  if (short && Math.abs(amount) >= 1000) {
    return `฿${Math.round(amount / 1000)}K`;
  }
  return `฿${amount.toLocaleString('th-TH')}`;
}

/**
 * Format a number of kWh with appropriate precision.
 *
 * @param {number} kwh
 * @returns {string}  e.g. '6,570 kWh'
 */
export function formatKWh(kwh) {
  if (typeof kwh !== 'number') throw new TypeError('kwh must be a number');
  return `${kwh.toLocaleString('th-TH', { maximumFractionDigits: 1 })} kWh`;
}

/**
 * Clamp a number between min and max.
 *
 * @param {number} value
 * @param {number} min
 * @param {number} max
 * @returns {number}
 */
export function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}
