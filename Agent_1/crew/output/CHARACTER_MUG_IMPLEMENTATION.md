# Character Mug Implementation -- FE Lead Agent Output

**Author**: Frontend Lead Agent
**Date**: 30 March 2026
**Status**: READY FOR CEO REVIEW -- All code complete, diffs provided, awaiting approval before any edits
**Inputs consumed**: character_mug_prototype.jsx, MugWrapTemplate.jsx, FamilyMugTemplate.jsx, mugThemes.js, templateRegistry.js, printProfiles.js, productCatalog.js, useKeepsakeData.js, KeepsakesModal.jsx, cardExport.js, CHARACTER_MUG_CREATIVE_BRIEF.md, CHARACTER_ILLUSTRATION_BRIEF.md, HEADLINE_ENGINE_SPEC.md

---

## Architecture Decisions

1. **CharacterMugTemplate.jsx** follows the exact pattern of MugWrapTemplate.jsx: same prop interface `({ data, occasion, ageTheme })`, same 830x345px CSS canvas, same inline styles for html-to-image compatibility.
2. **characterHeadlines.js** is a standalone utility module (not a hook) placed alongside mugThemes.js in `keepsakes/utils/`. It exports `selectHeadlines(data)` as specified in HEADLINE_ENGINE_SPEC.md.
3. **Character SVGs** are rendered as placeholder coloured shapes with labels. The `buildCharacterSVG` function from the prototype is adapted to accept theme tokens from `OCCASION_THEMES` (not the prototype's custom THEMES array).
4. **No Tailwind** -- all styles are inline objects, consistent with MugWrapTemplate.
5. **No new dependencies** -- pure React, no external libraries.
6. **Data from useKeepsakeData** -- the template consumes the same `data` shape that MugWrapTemplate receives, plus the headline engine.

---

## File 1: NEW -- `CharacterMugTemplate.jsx`

**Path**: `famililook-desktop2/src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx`

```jsx
// src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx
// Character Mug print template -- illustrated characters + bold headlines + real data.
// Renders at 830x345px CSS, exported at 3.217x pixelRatio -> 2670x1110px PNG.
// Transparent background -- Prodigi prints directly on white ceramic.
// Spec: Agent_1/crew/output/CHARACTER_MUG_CREATIVE_BRIEF.md

import React, { useMemo } from "react";
import { getOccasionTheme, FEATURE_LABELS, NEUTRAL, truncateAtWord } from "../../../utils/mugThemes.js";
import { selectHeadlines, normaliseParent } from "../../../utils/characterHeadlines.js";

// Canvas dimensions (CSS pixels -- print output is 3.217x larger)
const W = 830;
const H = 345;

// Panel widths (26% / 48% / 26% -- same proportions as MugWrapTemplate)
const LEFT_W = Math.round(W * 0.26);   // 216px
const RIGHT_W = Math.round(W * 0.26);  // 216px
const CENTRE_W = W - LEFT_W - RIGHT_W; // 398px

// Safe margins
const SAFE_TOP = 18;
const SAFE_BOT = 15;
const SAFE_X = 18;

// ── Character SVG builders (placeholder -- real illustrations drop in later) ──

const EMOTIONS_MAP = {
  mama:   ["proud", "surprised", "cheeky", "celebrating", "loving"],
  papa:   ["proud", "surprised", "cheeky", "celebrating", "loving"],
  cub:    ["happy", "sleeping", "surprised", "giggling", "curious"],
  mini:   ["proud", "cheeky", "surprised", "pointing", "celebrating"],
  gran:   ["proud", "surprised", "loving", "showing_off", "laughing"],
  gramps: ["proud", "surprised", "loving", "showing_off", "laughing"],
};

function getCharacterForData(data) {
  // Auto-select character based on winner + occasion
  const parentType = normaliseParent(data.winnerLabel);
  if (parentType === "mum") return "mama";
  if (parentType === "dad") return "papa";
  return "mama"; // default
}

function getEmotionForData(data) {
  const pct = data.winnerPct || 51;
  if (pct >= 75) return "celebrating";
  if (pct >= 65) return "proud";
  if (pct >= 55) return "cheeky";
  return "surprised";
}

function getEyesSVG(emo) {
  const happySet = ["celebrating", "happy", "giggling", "loving", "sleeping", "showing_off", "laughing"];
  if (happySet.includes(emo)) {
    return '<path d="M78 96Q98 80 118 96" fill="none" stroke="#1A1A1A" stroke-width="7" stroke-linecap="round"/><path d="M142 96Q162 80 182 96" fill="none" stroke="#1A1A1A" stroke-width="7" stroke-linecap="round"/>';
  }
  if (emo === "surprised") {
    return '<circle cx="98" cy="92" r="14" fill="#1A1A1A"/><circle cx="162" cy="92" r="14" fill="#1A1A1A"/><circle cx="104" cy="86" r="5" fill="white"/><circle cx="168" cy="86" r="5" fill="white"/>';
  }
  if (emo === "cheeky" || emo === "pointing") {
    return '<circle cx="100" cy="94" r="11" fill="#1A1A1A"/><circle cx="105" cy="89" r="4" fill="white"/><path d="M144 92Q162 80 180 92" fill="none" stroke="#1A1A1A" stroke-width="7" stroke-linecap="round"/>';
  }
  return '<circle cx="100" cy="94" r="11" fill="#1A1A1A"/><circle cx="164" cy="94" r="11" fill="#1A1A1A"/><circle cx="105" cy="89" r="4" fill="white"/><circle cx="169" cy="89" r="4" fill="white"/>';
}

function getMouthSVG(emo) {
  if (emo === "surprised") {
    return '<ellipse cx="130" cy="130" rx="14" ry="16" fill="#1A1A1A"/><ellipse cx="130" cy="131" rx="9" ry="11" fill="#7A1835"/>';
  }
  if (["celebrating", "showing_off", "giggling", "laughing"].includes(emo)) {
    return '<path d="M86 118Q130 154 174 118" fill="#1A1A1A" stroke="#1A1A1A" stroke-width="3"/><path d="M94 122Q130 144 166 122Q152 138 130 140Q108 138 94 122Z" fill="#7A1835"/>';
  }
  if (emo === "cheeky" || emo === "pointing") {
    return '<path d="M90 120Q112 142 168 128" fill="none" stroke="#1A1A1A" stroke-width="6.5" stroke-linecap="round"/>';
  }
  if (["loving", "sleeping", "curious"].includes(emo)) {
    return '<path d="M96 122Q130 144 164 122" fill="none" stroke="#1A1A1A" stroke-width="5.5" stroke-linecap="round"/>';
  }
  // proud / happy / default
  return '<path d="M92 122Q130 150 168 122" fill="none" stroke="#1A1A1A" stroke-width="6" stroke-linecap="round"/><path d="M98 126Q130 142 162 126Q152 136 130 138Q108 136 98 126Z" fill="#7A1835"/>';
}

function getLashesSVG(emo, char) {
  if (char === "papa" || char === "gramps") return "";
  const noLash = ["surprised", "sleeping", "giggling"];
  if (noLash.includes(emo)) return "";
  return '<line x1="76" y1="72" x2="68" y2="56" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/><line x1="88" y1="66" x2="84" y2="50" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/><line x1="100" y1="63" x2="100" y2="47" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/><line x1="184" y1="72" x2="192" y2="56" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/><line x1="172" y1="66" x2="176" y2="50" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/><line x1="160" y1="63" x2="160" y2="47" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>';
}

function getBodySVG(char, theme) {
  if (char === "cub") {
    return `<ellipse cx="130" cy="200" rx="38" ry="50" fill="${theme.wash}" stroke="${theme.dark}" stroke-width="6"/><ellipse cx="130" cy="230" rx="55" ry="20" fill="${theme.light}" stroke="${theme.dark}" stroke-width="5"/>`;
  }
  if (char === "gran" || char === "gramps") {
    return `<path d="M70 150Q62 220 66 260Q70 280 130 282Q190 280 194 260Q198 220 190 150Z" fill="${theme.muted}" stroke="${theme.dark}" stroke-width="7" stroke-linejoin="round"/>`;
  }
  const w = char === "papa" ? 60 : 54;
  return `<path d="M${130 - w} 150Q${122 - w} 220 ${126 - w} 260Q130 282 130 282Q130 282 ${134 + w} 260Q${138 + w} 220 ${130 + w} 150Z" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="7" stroke-linejoin="round"/>`;
}

function getEarsSVG(char, theme) {
  const r = (char === "gran" || char === "gramps") ? 26 : 28;
  const inner = (char === "gran" || char === "gramps") ? 14 : 16;
  return `<circle cx="60" cy="44" r="${r}" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="7"/><circle cx="60" cy="44" r="${inner}" fill="${theme.light}" stroke="${theme.dark}" stroke-width="4"/><circle cx="200" cy="44" r="${r}" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="7"/><circle cx="200" cy="44" r="${inner}" fill="${theme.light}" stroke="${theme.dark}" stroke-width="4"/>`;
}

function getHairSVG(char, theme) {
  if (char === "papa" || char === "gramps") {
    return `<ellipse cx="84" cy="44" rx="18" ry="10" fill="${theme.faint}" stroke="${theme.dark}" stroke-width="3"/><ellipse cx="176" cy="44" rx="18" ry="10" fill="${theme.faint}" stroke="${theme.dark}" stroke-width="3"/>`;
  }
  if (char === "gran") {
    return `<ellipse cx="130" cy="34" rx="36" ry="18" fill="${theme.faint}" stroke="${theme.dark}" stroke-width="4"/><circle cx="130" cy="26" r="14" fill="${theme.faint}" stroke="${theme.dark}" stroke-width="3"/>`;
  }
  if (char === "mini") {
    return `<path d="M98 44Q108 28 118 40Q124 28 130 38Q136 26 142 38Q152 28 162 44" fill="none" stroke="${theme.dark}" stroke-width="5" stroke-linecap="round"/>`;
  }
  if (char === "cub") {
    return `<path d="M125 30Q130 20 135 30" fill="none" stroke="${theme.dark}" stroke-width="5" stroke-linecap="round"/>`;
  }
  // mama -- bun
  return `<circle cx="130" cy="30" r="30" fill="${theme.dark}"/><circle cx="130" cy="30" r="22" fill="${theme.dark}" opacity="0.6"/>`;
}

function buildCharacterSVGString(char, emo, theme) {
  return `
    <ellipse cx="130" cy="292" rx="58" ry="8" fill="${theme.light}" opacity="0.18"/>
    <rect x="90" y="252" width="30" height="36" rx="15" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="7" stroke-linejoin="round"/>
    <rect x="140" y="252" width="30" height="36" rx="15" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="7" stroke-linejoin="round"/>
    ${getBodySVG(char, theme)}
    <rect x="108" y="132" width="44" height="24" rx="8" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="6"/>
    <ellipse cx="130" cy="96" rx="76" ry="72" fill="${theme.primary}" stroke="${theme.dark}" stroke-width="8"/>
    ${getEarsSVG(char, theme)}
    ${getHairSVG(char, theme)}
    ${getLashesSVG(emo, char)}
    <ellipse cx="98" cy="92" rx="19" ry="18" fill="white" stroke="${theme.dark}" stroke-width="5"/>
    <ellipse cx="162" cy="92" rx="19" ry="18" fill="white" stroke="${theme.dark}" stroke-width="5"/>
    ${getEyesSVG(emo)}
    <ellipse cx="130" cy="112" rx="12" ry="9" fill="${theme.dark}"/>
    ${getMouthSVG(emo)}
    <ellipse cx="74" cy="108" rx="18" ry="13" fill="${theme.light}" opacity="0.32"/>
    <ellipse cx="186" cy="108" rx="18" ry="13" fill="${theme.light}" opacity="0.32"/>
  `;
}

function CharacterSVGInline({ char, emo, theme }) {
  return (
    <svg
      viewBox="0 0 260 300"
      xmlns="http://www.w3.org/2000/svg"
      width="100%"
      style={{ display: "block" }}
      dangerouslySetInnerHTML={{ __html: buildCharacterSVGString(char, emo, theme) }}
    />
  );
}

// ── Speech Bubble ──

function SpeechBubble({ text, theme }) {
  if (!text) return null;
  return (
    <div style={{
      position: "absolute",
      top: "8px",
      right: "-4px",
      background: "#fff",
      border: `1.5px solid ${theme.primary}`,
      borderRadius: "8px",
      padding: "2px 6px",
      fontSize: "6px",
      fontWeight: 700,
      color: theme.dark,
      fontFamily: "'Arial Rounded MT Bold', Arial, sans-serif",
      whiteSpace: "nowrap",
      maxWidth: "90px",
      overflow: "hidden",
      textOverflow: "ellipsis",
      zIndex: 2,
    }}>
      {text}
      {/* Bubble tail */}
      <div style={{
        position: "absolute",
        bottom: "-4px",
        left: "12px",
        width: 0,
        height: 0,
        borderLeft: "4px solid transparent",
        borderRight: "4px solid transparent",
        borderTop: `4px solid ${theme.primary}`,
      }} />
    </div>
  );
}

// ── Main Template ──

export default function CharacterMugTemplate({ data, occasion = "generic", ageTheme }) {
  if (!data) return null;

  const theme = getOccasionTheme(occasion);

  // Feature analysis
  const featureEntries = Object.entries(data.featureVotes || {});
  const winnerFeatures = featureEntries.filter(([, p]) => p === data.winner);
  const heroKey = winnerFeatures[0]?.[0] || data.dominantFeature || "eyes";

  // Character selection (auto from data)
  const char = getCharacterForData(data);
  const emo = getEmotionForData(data);

  // Headline engine
  const headlines = useMemo(() => selectHeadlines({
    winner: data.winner,
    winnerPct: data.winnerPct,
    winnerLabel: data.winnerLabel,
    loserLabel: data.loserLabel,
    childName: data.childName,
    dominantFeature: heroKey,
    featureVotes: data.featureVotes,
    occasion,
  }), [data.winner, data.winnerPct, data.winnerLabel, data.loserLabel, data.childName, heroKey, data.featureVotes, occasion]);

  // Photo handling
  const hasPhoto = Boolean(data.childPhoto);
  const photoSize = hasPhoto ? 52 : 0;

  // Bold headline font stack (rounded sans for character mugs)
  const headlineFont = "'Arial Rounded MT Bold', 'Nunito', Arial, sans-serif";
  const bodyFont = ageTheme?.fontFamily || "Georgia, 'Times New Roman', serif";

  return (
    <div style={{
      width: `${W}px`,
      height: `${H}px`,
      background: "transparent",
      fontFamily: bodyFont,
      display: "flex",
      position: "relative",
      overflow: "hidden",
    }}>
      {/* Top accent band */}
      <div style={{
        position: "absolute", top: 0, left: 0, right: 0, height: "3px",
        background: `linear-gradient(90deg, transparent 10%, ${theme.light}60 30%, ${theme.primary} 50%, ${theme.light}60 70%, transparent 90%)`,
      }} />
      {/* Bottom accent band */}
      <div style={{
        position: "absolute", bottom: 0, left: 0, right: 0, height: "3px",
        background: `linear-gradient(90deg, transparent 10%, ${theme.light}60 30%, ${theme.primary} 50%, ${theme.light}60 70%, transparent 90%)`,
      }} />

      {/* ── LEFT PANEL: Character Illustration ── */}
      <div style={{
        width: `${LEFT_W}px`,
        flexShrink: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-end",
        padding: `${SAFE_TOP}px ${SAFE_X - 6}px ${SAFE_BOT - 8}px`,
        position: "relative",
        overflow: "hidden",
      }}>
        {/* Speech bubble */}
        <SpeechBubble text={headlines.winnerBubble} theme={theme} />

        {/* Character illustration */}
        <div style={{ width: "160px", position: "relative", zIndex: 1 }}>
          <CharacterSVGInline char={char} emo={emo} theme={theme} />
        </div>
      </div>

      {/* ── CENTRE PANEL: Headlines + Photo ── */}
      <div style={{
        width: `${CENTRE_W}px`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: `${SAFE_TOP + 4}px 10px ${SAFE_BOT}px`,
        gap: "3px",
      }}>
        {/* Occasion header */}
        {headlines.occasionHeader && (
          <div style={{
            fontFamily: headlineFont,
            fontSize: "8px",
            fontWeight: 800,
            color: theme.primary,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            textAlign: "center",
            lineHeight: 1,
          }}>
            {headlines.occasionHeader}
          </div>
        )}

        {/* Hero headline -- THE HERO ELEMENT */}
        <div style={{
          fontFamily: headlineFont,
          fontSize: hasPhoto ? "18px" : "22px",
          fontWeight: 900,
          color: theme.dark,
          textAlign: "center",
          lineHeight: 0.95,
          textTransform: "uppercase",
          letterSpacing: "-0.02em",
          whiteSpace: "pre-line",
          maxWidth: "95%",
        }}>
          {headlines.heroHeadline}
        </div>

        {/* Divider */}
        <div style={{
          width: "50%", height: "2px",
          background: `linear-gradient(90deg, transparent, ${theme.light}, transparent)`,
          margin: "2px 0",
        }} />

        {/* Photo circle (if present) */}
        {hasPhoto && (
          <img
            src={data.childPhoto}
            alt={data.childName}
            style={{
              width: `${photoSize}px`,
              height: `${photoSize}px`,
              borderRadius: "50%",
              objectFit: "cover",
              border: `2.5px solid ${theme.primary}`,
              boxShadow: `0 2px 8px ${theme.primary}30`,
            }}
          />
        )}

        {/* Feature sub-headline */}
        <div style={{
          fontFamily: headlineFont,
          fontSize: "9px",
          fontWeight: 700,
          color: theme.muted,
          letterSpacing: "0.04em",
          textTransform: "uppercase",
          textAlign: "center",
        }}>
          {headlines.featureSubline}
        </div>

        {/* Score badge */}
        <div style={{
          padding: "3px 12px",
          borderRadius: "999px",
          background: `linear-gradient(135deg, ${theme.primary}, ${theme.light})`,
          color: "#fff",
          fontFamily: headlineFont,
          fontSize: "11px",
          fontWeight: 900,
          letterSpacing: "0.04em",
          textAlign: "center",
        }}>
          {data.winnerPct}% {data.winnerLabel?.toUpperCase()}
        </div>

        {/* Feature chips (compact row) */}
        <div style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "2px",
          maxWidth: "100%",
          marginTop: "1px",
        }}>
          {featureEntries.map(([key, parent]) => {
            const isWinner = parent === data.winner;
            return (
              <div key={key} style={{
                padding: "1px 5px",
                borderRadius: ageTheme ? `${Math.max(4, parseInt(ageTheme.borderRadius) / 3)}px` : "6px",
                background: isWinner ? theme.wash : NEUTRAL.chip,
                border: `1px solid ${isWinner ? theme.light + "50" : NEUTRAL.chipBorder}`,
                fontSize: "6px",
                fontWeight: isWinner ? 700 : 400,
                color: isWinner ? theme.primary : NEUTRAL.text,
              }}>
                {FEATURE_LABELS[key] || key}
              </div>
            );
          })}
        </div>

        {/* Brand */}
        <div style={{
          fontSize: "5px",
          color: theme.faint,
          letterSpacing: "0.15em",
          opacity: 0.5,
          marginTop: "auto",
        }}>
          famililook.com
        </div>
      </div>

      {/* ── RIGHT PANEL: Feature Breakdown + Decorative ── */}
      <div style={{
        width: `${RIGHT_W}px`,
        flexShrink: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: `${SAFE_TOP + 6}px ${SAFE_X}px ${SAFE_BOT}px`,
        position: "relative",
      }}>
        {/* Decorative percentage watermark */}
        <div style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          fontSize: "60px",
          fontWeight: 900,
          fontFamily: headlineFont,
          color: theme.primary,
          opacity: 0.06,
          pointerEvents: "none",
        }}>
          {data.winnerPct}%
        </div>

        {/* Feature list */}
        <div style={{
          display: "flex",
          flexDirection: "column",
          gap: "3px",
          width: "100%",
          position: "relative",
          zIndex: 1,
        }}>
          {featureEntries.map(([key, parent]) => {
            const isWinner = parent === data.winner;
            return (
              <div key={key} style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                fontSize: "8px",
                lineHeight: 1.2,
              }}>
                <span style={{
                  fontWeight: isWinner ? 700 : 400,
                  color: isWinner ? theme.primary : NEUTRAL.text,
                }}>
                  {FEATURE_LABELS[key] || key}
                </span>
                <span style={{
                  fontSize: "7px",
                  color: isWinner ? theme.muted : NEUTRAL.text,
                  fontStyle: "italic",
                }}>
                  {parent === data.winner ? data.winnerLabel : data.loserLabel}
                </span>
              </div>
            );
          })}
        </div>

        {/* Analysis metadata */}
        <div style={{
          marginTop: "10px",
          display: "flex",
          flexDirection: "column",
          gap: "2px",
          fontSize: "6px",
          color: NEUTRAL.text,
          textAlign: "center",
        }}>
          <span>{data.childName}</span>
          <span>{data.winnerPct}% {data.winnerLabel}</span>
          <span>{new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</span>
        </div>

        {/* Brand */}
        <div style={{
          marginTop: "6px",
          fontSize: "6px",
          color: theme.faint,
          fontStyle: "italic",
          textAlign: "center",
        }}>
          Analysed by FamiliLook AI
        </div>
      </div>
    </div>
  );
}
```

---

## File 2: NEW -- `characterHeadlines.js`

**Path**: `famililook-desktop2/src/components/keepsakes/utils/characterHeadlines.js`

```js
// src/components/keepsakes/utils/characterHeadlines.js
// Headline engine for Character Mug product line.
// Deterministic selection of hero headlines, feature sub-headlines,
// occasion headers, and speech bubbles from analysis data.
// Spec: Agent_1/crew/output/HEADLINE_ENGINE_SPEC.md

import { truncateAtWord } from "./mugThemes.js";

// ── Parent label normalisation ───────────────────────────────────────────────

const MUM_ALIASES = ["mum", "mom", "mummy", "mommy", "mama", "mother", "ma"];
const DAD_ALIASES = ["dad", "daddy", "papa", "father", "pa", "dada"];

/**
 * Normalise a parent label to "mum", "dad", or "custom".
 * @param {string} label
 * @returns {"mum"|"dad"|"custom"}
 */
export function normaliseParent(label) {
  if (!label) return "custom";
  const lower = label.toLowerCase().trim();
  if (MUM_ALIASES.includes(lower)) return "mum";
  if (DAD_ALIASES.includes(lower)) return "dad";
  return "custom";
}

// ── Deterministic hash (djb2) ────────────────────────────────────────────────

function hashString(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash + str.charCodeAt(i)) & 0x7fffffff;
  }
  return hash;
}

function pickSeeded(pool, seed) {
  if (!pool || pool.length === 0) return "";
  return pool[Math.abs(seed) % pool.length];
}

// ── Template literal resolution ──────────────────────────────────────────────

function resolveTemplates(text, vars) {
  return text
    .replace(/\{child\}/g, vars.child || "")
    .replace(/\{winner\}/g, vars.winner || "")
    .replace(/\{loser\}/g, vars.loser || "");
}

// ── Hero Headline Banks ──────────────────────────────────────────────────────

const HEADLINES = {
  mum: {
    high: [
      "MUMMY'S\nMINI ME",
      "SORRY DAD,\nI'M ALL MUM",
      "MUM DID\nALL THE WORK",
      "COPY + PASTE:\nMUM EDITION",
      "MUM'S\nGREATEST HIT",
      "MADE BY MUM",
      "100% MUM\nENERGY",
      "MUM'S TWIN",
      "ALL MUM,\nNO DOUBT",
      "MUM WINS.\nAGAIN.",
      "MUMMY RUNS\nDEEP",
      "{child}:\nMUM'S MINI ME",
    ],
    medium: [
      "LIKE MOTHER,\nLIKE BABY",
      "MOSTLY MUM",
      "MUM'S SIDE\nIS STRONG",
      "LEANING MUM",
      "MUM TAKES\nTHE LEAD",
    ],
  },
  dad: {
    high: [
      "DADDY'S\nDOUBLE",
      "SORRY MUM,\nTHIS ONE'S DAD",
      "DAD'S\nCTRL+C, CTRL+V",
      "STRONG GENES,\nDAD",
      "DAD'S\nGREATEST HIT",
      "MADE BY DAD",
      "100% DAD\nENERGY",
      "DAD'S TWIN",
      "ALL DAD,\nNO QUESTION",
      "DAD WINS.\nFINALLY.",
      "DAD STAMP:\nAPPROVED",
      "{child}:\nDAD'S DOUBLE",
    ],
    medium: [
      "THE APPLE\nDOESN'T FALL FAR",
      "MOSTLY DAD",
      "DAD'S SIDE\nIS STRONG",
      "LEANING DAD",
      "DAD TAKES\nTHE LEAD",
    ],
  },
  close: [
    "THE PERFECT\nBLEND",
    "BEST\nOF BOTH",
    "NOT QUITE\n50/50",
    "THE GREAT\nDEBATE",
    "TEAMWORK MAKES\nTHE BABY",
    "YOU BOTH\nDID GOOD",
    "THE VERDICT:\nJUST BARELY",
    "A BIT\nOF BOTH",
    "TOO CLOSE\nTO CALL",
    "PERFECTLY\nBLENDED",
    "THEY GOT\nTHE BEST BITS",
  ],
  blend: [
    "BEST OF\nBOTH WORLDS",
    "A UNIQUE MIX",
    "ONE OF A KIND",
    "PERFECTLY\nBLENDED",
    "THE FAMILY\nRECIPE",
  ],
  custom: [
    "{winner}'S\nMINI ME",
    "ALL {winner}",
    "{child} LOOKS\nLIKE {winner}",
    "MADE BY\n{winner}",
    "{winner}'S\nGREATEST HIT",
    "{winner}'S\nDOUBLE",
    "{winner} WINS",
    "{winner}'S TWIN",
    "HELLO, MINI\n{winner}",
    "{winner}\nCALLED IT",
  ],
};

// ── Feature Sub-headline Banks ───────────────────────────────────────────────

const SUBHEADLINES = {
  eyes:       ["GOT {winner}'S EYES", "THOSE EYES? ALL {winner}", "{winner}'S EYES, NO QUESTION"],
  eyebrows:   ["THOSE BROWS? ALL {winner}", "{winner}'S BROWS ON POINT", "EYEBROWS: COURTESY OF {winner}"],
  smile:      ["{winner}'S SMILE, THROUGH AND THROUGH", "THAT SMILE IS ALL {winner}", "GRINNING LIKE {winner}"],
  nose:       ["THAT NOSE? 100% {winner}", "NOSE BY {winner}", "{winner}'S NOSE, ON THE NOSE"],
  face_shape: ["{winner}'S FACE SHAPE, NO DOUBT", "FACE SHAPE: A GIFT FROM {winner}", "SHAPED LIKE {winner}"],
  skin:       ["{winner}'S GLOW", "SKIN: {winner}'S CONTRIBUTION", "GLOWING LIKE {winner}"],
  hair:       ["HAIR BY {winner}", "{winner}'S LOCKS", "THAT HAIR IS ALL {winner}"],
  ears:       ["EARS: A GIFT FROM {winner}", "{winner}'S EARS, UNMISTAKABLY", "THOSE EARS? ALL {winner}"],
};

// ── Occasion Header Bank ─────────────────────────────────────────────────────

const CHARACTER_OCCASION_HEADERS = {
  generic:         null,
  mothers_day:     "HAPPY MOTHER'S DAY",
  fathers_day:     "HAPPY FATHER'S DAY",
  birthday:        "HAPPY BIRTHDAY {child}",
  christmas:       "MERRY CHRISTMAS",
  valentines:      "TO MY VALENTINE",
  grandparents_day:"BEST GRANDPARENT EVER",
  heritage_gold:   "FAMILY HERITAGE",
  carnival_spirit: "CELEBRATE FAMILY",
  ubuntu:          "WE ARE FAMILY",
};

// ── Speech Bubble Banks ──────────────────────────────────────────────────────

const SPEECH = {
  winner_proud: [
    "TOLD YOU SO!",
    "IT'S OBVIOUS!",
    "THAT'S MY BABY!",
    "I KNEW IT!",
    "LOOK AT US!",
    "MY MINI ME!",
    "NO SURPRISE!",
  ],
  loser_playful: [
    "WAIT, REALLY?",
    "I SEE IT...",
    "NEXT TIME!",
    "HMM, BARELY...",
    "I WANT A RECOUNT",
    "FAIR ENOUGH",
    "NOT CONVINCED!",
  ],
  close_call: [
    "SO CLOSE!",
    "IT'S A TIE... ISH",
    "COULD GO EITHER WAY",
    "SQUINT AND SEE ME",
    "WE BOTH WIN!",
  ],
};

// ── Selection Algorithm ──────────────────────────────────────────────────────

/**
 * Select headlines for a Character Mug based on analysis data.
 *
 * @param {object} input
 * @param {string} input.winner - "parent1"|"parent2"|"blend"|"unknown"
 * @param {number} input.winnerPct - Integer 51-100
 * @param {string} input.winnerLabel - e.g. "Mum", "Dad", custom name
 * @param {string} input.loserLabel - e.g. "Dad"
 * @param {string} [input.childName] - e.g. "Olivia"
 * @param {string} [input.dominantFeature] - e.g. "eyes"
 * @param {object} [input.featureVotes] - Feature vote map
 * @param {string} [input.occasion] - e.g. "mothers_day"
 * @returns {{ heroHeadline: string, featureSubline: string, occasionHeader: string|null, winnerBubble: string, loserBubble: string }}
 */
export function selectHeadlines(input) {
  const {
    winner,
    winnerPct = 51,
    winnerLabel = "Parent",
    loserLabel = "Parent",
    childName,
    dominantFeature = "eyes",
    occasion = "generic",
  } = input;

  // Step 1: Normalise
  const parentType = normaliseParent(winnerLabel);
  const isBlend = winner === "blend" || winner === "unknown";

  // Step 2: Percentage bracket
  let pctBracket;
  if (isBlend) {
    pctBracket = "blend";
  } else if (winnerPct >= 70) {
    pctBracket = "high";
  } else if (winnerPct >= 60) {
    pctBracket = "medium";
  } else {
    pctBracket = "close";
  }

  // Step 3: Build candidate pool
  let pool;
  if (isBlend) {
    pool = HEADLINES.blend;
  } else if (pctBracket === "close") {
    pool = HEADLINES.close;
  } else if (parentType === "mum") {
    pool = HEADLINES.mum[pctBracket];
  } else if (parentType === "dad") {
    pool = HEADLINES.dad[pctBracket];
  } else {
    pool = HEADLINES.custom;
  }

  // Step 4: Deterministic selection
  const seedStr = (childName || "FamiliLook") + winnerPct;
  const seed = hashString(seedStr);
  const index = Math.abs(seed) % pool.length;

  // Step 5: Resolve template literals
  const templateVars = {
    child: (childName || "").toUpperCase(),
    winner: (winnerLabel || "PARENT").toUpperCase(),
    loser: (loserLabel || "PARENT").toUpperCase(),
  };

  let heroHeadline = resolveTemplates(pool[index], templateVars);

  // Step 6: Verify 35-char limit (ignoring newlines for readability)
  const charCount = heroHeadline.replace(/\n/g, "").length;
  if (charCount > 35) {
    for (let i = 1; i < pool.length; i++) {
      const candidate = resolveTemplates(pool[(index + i) % pool.length], templateVars);
      if (candidate.replace(/\n/g, "").length <= 35) {
        heroHeadline = candidate;
        break;
      }
    }
    // Ultimate fallback
    if (heroHeadline.replace(/\n/g, "").length > 35) {
      heroHeadline = truncateAtWord(heroHeadline.replace(/\n/g, " "), 35);
    }
  }

  // Step 7: Feature sub-headline
  const featureKey = dominantFeature || "eyes";
  const featurePool = SUBHEADLINES[featureKey] || SUBHEADLINES.eyes;
  const featureIndex = Math.abs(seed) % featurePool.length;
  let featureSubline = resolveTemplates(featurePool[featureIndex], templateVars);
  if (featureSubline.length > 50) {
    featureSubline = truncateAtWord(featureSubline, 50);
  }

  // Step 8: Occasion header
  let occasionHeader = null;
  if (occasion && occasion !== "generic") {
    const headerTemplate = CHARACTER_OCCASION_HEADERS[occasion];
    if (headerTemplate) {
      const candidate = resolveTemplates(headerTemplate, templateVars);
      occasionHeader = candidate.length <= 30 ? candidate : (
        occasion === "birthday" ? "HAPPY BIRTHDAY" : candidate.slice(0, 30)
      );
    }
  }

  // Step 9: Speech bubbles
  let winnerBubble, loserBubble;
  if (isBlend || pctBracket === "close") {
    winnerBubble = pickSeeded(SPEECH.close_call, seed);
    loserBubble = pickSeeded(SPEECH.close_call, seed + 1);
  } else {
    winnerBubble = pickSeeded(SPEECH.winner_proud, seed);
    loserBubble = pickSeeded(SPEECH.loser_playful, seed);
  }

  return {
    heroHeadline,
    featureSubline,
    occasionHeader,
    winnerBubble,
    loserBubble,
  };
}
```

---

## File 3: MODIFICATION -- `templateRegistry.js`

**Path**: `famililook-desktop2/src/components/keepsakes/utils/templateRegistry.js`

### 3a. Add `character_default` style entries to TEMPLATE_STYLES

**old_string:**
```js
  ubuntu: {
    id: "ubuntu",
    label: "Ubuntu",
    icon: "\uD83C\uDF0D",
    description: "Warm earth tones, family bond",
  },
};
```

**new_string:**
```js
  ubuntu: {
    id: "ubuntu",
    label: "Ubuntu",
    icon: "\uD83C\uDF0D",
    description: "Warm earth tones, family bond",
  },
  character_default: {
    id: "character_default",
    label: "Character Mug",
    icon: "\uD83D\uDC3B",
    description: "Illustrated character + bold headline",
  },
  character_heritage: {
    id: "character_heritage",
    label: "Character Heritage",
    icon: "\uD83C\uDF1F",
    description: "Character mug with Heritage Gold palette",
  },
  character_carnival: {
    id: "character_carnival",
    label: "Character Carnival",
    icon: "\uD83C\uDF89",
    description: "Character mug with Carnival Spirit palette",
  },
  character_ubuntu: {
    id: "character_ubuntu",
    label: "Character Ubuntu",
    icon: "\uD83C\uDF0D",
    description: "Character mug with Ubuntu palette",
  },
};
```

### 3b. Add `character_mug` product entry to PRODUCT_TEMPLATE_REGISTRY

**old_string:**
```js
  family_mug_set: {
    styles: ["mum_mug", "dad_mug"],
    defaultStyle: "mum_mug",
    renderWidth: 830,
    renderHeight: 345,
    supportsCustomMessage: true,
    requiresFamilyData: true,
    components: {
      mum_mug: lazy(() => import("../templates/Products/Drinkware/FamilyMugTemplate")),
      dad_mug: lazy(() => import("../templates/Products/Drinkware/FamilyMugTemplate")),
    },
  },
};
```

**new_string:**
```js
  family_mug_set: {
    styles: ["mum_mug", "dad_mug"],
    defaultStyle: "mum_mug",
    renderWidth: 830,
    renderHeight: 345,
    supportsCustomMessage: true,
    requiresFamilyData: true,
    components: {
      mum_mug: lazy(() => import("../templates/Products/Drinkware/FamilyMugTemplate")),
      dad_mug: lazy(() => import("../templates/Products/Drinkware/FamilyMugTemplate")),
    },
  },

  character_mug: {
    styles: ["character_default", "character_heritage", "character_carnival", "character_ubuntu"],
    defaultStyle: "character_default",
    renderWidth: 830,
    renderHeight: 345,
    supportsCustomMessage: true,
    components: {
      character_default: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
      character_heritage: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
      character_carnival: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
      character_ubuntu: lazy(() => import("../templates/Products/Drinkware/CharacterMugTemplate")),
    },
  },
};
```

---

## File 4: MODIFICATION -- `printProfiles.js`

**Path**: `famililook-desktop2/src/components/keepsakes/utils/printProfiles.js`

### 4a. Add CHARACTER_MUG to PRODUCT_TYPES

**old_string:**
```js
  FAMILY_MUG_SET: "family_mug_set",
};
```

**new_string:**
```js
  FAMILY_MUG_SET: "family_mug_set",
  CHARACTER_MUG: "character_mug",
};
```

### 4b. Add CHARACTER_MUG product spec (after FAMILY_MUG_SET spec)

**old_string:**
```js
  [PRODUCT_TYPES.FAMILY_MUG_SET]: {
    id: PRODUCT_TYPES.FAMILY_MUG_SET,
    label: "Family Mug Set (Mum & Dad pair)",
    icon: "\u2615\u2615",
    price: 27.99,
    width_mm: 228.6,
    height_mm: 94.8,
    bleed_mm: 0,
    safeArea_mm: 5,
    dpi: DEFAULT_DPI,
    trim_width_px: 2670,
    trim_height_px: 1110,
    width_px: 2670,
    height_px: 1110,
    colorSpace: "RGB",
    format: "PNG",
    prodigi_sku: "GLOBAL-MUG-W",
    qpmarkets_type: null,
    vendors: [{ name: "prodigi", sku: "GLOBAL-MUG-W", priority: 1 }],
    description: "Matching Mum & Dad ceramic mug pair — all children's results on each",
    requiresFamilyData: true,
  },
};
```

**new_string:**
```js
  [PRODUCT_TYPES.FAMILY_MUG_SET]: {
    id: PRODUCT_TYPES.FAMILY_MUG_SET,
    label: "Family Mug Set (Mum & Dad pair)",
    icon: "\u2615\u2615",
    price: 27.99,
    width_mm: 228.6,
    height_mm: 94.8,
    bleed_mm: 0,
    safeArea_mm: 5,
    dpi: DEFAULT_DPI,
    trim_width_px: 2670,
    trim_height_px: 1110,
    width_px: 2670,
    height_px: 1110,
    colorSpace: "RGB",
    format: "PNG",
    prodigi_sku: "GLOBAL-MUG-W",
    qpmarkets_type: null,
    vendors: [{ name: "prodigi", sku: "GLOBAL-MUG-W", priority: 1 }],
    description: "Matching Mum & Dad ceramic mug pair — all children's results on each",
    requiresFamilyData: true,
  },

  [PRODUCT_TYPES.CHARACTER_MUG]: {
    id: PRODUCT_TYPES.CHARACTER_MUG,
    label: "Character Mug (11oz)",
    icon: "\uD83D\uDC3B",
    price: 16.99,
    width_mm: 228.6,
    height_mm: 94.8,
    bleed_mm: 0,
    safeArea_mm: 5,
    dpi: DEFAULT_DPI,
    trim_width_px: 2670,
    trim_height_px: 1110,
    width_px: 2670,
    height_px: 1110,
    colorSpace: "RGB",
    format: "PNG",
    prodigi_sku: "GLOBAL-MUG-W",
    qpmarkets_type: null,
    vendors: [{ name: "prodigi", sku: "GLOBAL-MUG-W", priority: 1 }],
    description: "11oz ceramic mug with illustrated character design + personalised analysis",
  },
};
```

### 4c. Add Character Mug print profiles (after family_mug_set profiles)

**old_string:**
```js
  // ── Card Deck profile ───────────────────────────────────────────────────
  "card_deck__card_deck": {
```

**new_string:**
```js
  // ── Character Mug profiles ──────────────────────────────────────────────
  "character_mug__character_default": {
    templateWidth: 830,
    eligibleProducts: [PRODUCT_TYPES.CHARACTER_MUG],
  },
  "character_mug__character_heritage": {
    templateWidth: 830,
    eligibleProducts: [PRODUCT_TYPES.CHARACTER_MUG],
  },
  "character_mug__character_carnival": {
    templateWidth: 830,
    eligibleProducts: [PRODUCT_TYPES.CHARACTER_MUG],
  },
  "character_mug__character_ubuntu": {
    templateWidth: 830,
    eligibleProducts: [PRODUCT_TYPES.CHARACTER_MUG],
  },

  // ── Card Deck profile ───────────────────────────────────────────────────
  "card_deck__card_deck": {
```

---

## File 5: MODIFICATION -- `productCatalog.js`

**Path**: `famililook-desktop2/src/components/keepsakes/utils/productCatalog.js`

### 5a. Add CHARACTER_MUG to drinkware category

**old_string:**
```js
  drinkware: {
    id: "drinkware",
    label: "Drinkware",
    icon: "\u2615",
    description: "Ceramic mugs with panoramic designs",
    vendorNote: "Prodigi",
    products: [PRODUCT_TYPES.MUG_WRAP, PRODUCT_TYPES.FAMILY_MUG_SET],
  },
```

**new_string:**
```js
  drinkware: {
    id: "drinkware",
    label: "Drinkware",
    icon: "\u2615",
    description: "Ceramic mugs with panoramic designs",
    vendorNote: "Prodigi",
    products: [PRODUCT_TYPES.MUG_WRAP, PRODUCT_TYPES.CHARACTER_MUG, PRODUCT_TYPES.FAMILY_MUG_SET],
  },
```

---

## File 6: NEW -- `CharacterMugTemplate.test.jsx`

**Path**: `famililook-desktop2/src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.test.jsx`

```jsx
// CharacterMugTemplate.test.jsx
// Vitest + React Testing Library tests for the Character Mug template.

import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import CharacterMugTemplate from "./CharacterMugTemplate.jsx";
import { selectHeadlines, normaliseParent } from "../../../utils/characterHeadlines.js";

// ── Test Data Fixtures ───────────────────────────────────────────────────────

const mumWinnerData = {
  childName: "Olivia",
  childPhoto: null,
  winner: "parent1",
  winnerLabel: "Mum",
  winnerPct: 72,
  winnerFeatureCount: 5,
  loserLabel: "Dad",
  loserPct: 28,
  loserFeatureCount: 3,
  dominantFeature: "eyes",
  featureVotes: {
    eyes: "parent1",
    eyebrows: "parent1",
    smile: "parent2",
    nose: "parent1",
    face_shape: "parent2",
    skin: "parent1",
    hair: "parent2",
    ears: "parent1",
  },
  featureDetails: [],
};

const dadWinnerData = {
  childName: "James",
  childPhoto: null,
  winner: "parent2",
  winnerLabel: "Dad",
  winnerPct: 78,
  winnerFeatureCount: 6,
  loserLabel: "Mum",
  loserPct: 22,
  loserFeatureCount: 2,
  dominantFeature: "smile",
  featureVotes: {
    eyes: "parent2",
    eyebrows: "parent2",
    smile: "parent2",
    nose: "parent1",
    face_shape: "parent2",
    skin: "parent2",
    hair: "parent1",
    ears: "parent2",
  },
  featureDetails: [],
};

const closeCallData = {
  childName: "Noah",
  childPhoto: null,
  winner: "parent1",
  winnerLabel: "Mum",
  winnerPct: 53,
  winnerFeatureCount: 5,
  loserLabel: "Dad",
  loserPct: 47,
  loserFeatureCount: 3,
  dominantFeature: "hair",
  featureVotes: {
    eyes: "parent1",
    eyebrows: "parent2",
    smile: "parent1",
    nose: "parent2",
    face_shape: "parent1",
    skin: "parent2",
    hair: "parent1",
    ears: "parent1",
  },
  featureDetails: [],
};

// ── Template Rendering Tests ─────────────────────────────────────────────────

describe("CharacterMugTemplate", () => {
  it("renders with Mum winner data", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="generic" />
    );
    expect(container.querySelector("div")).toBeTruthy();
    // Should display the winner percentage
    expect(container.textContent).toContain("72%");
    expect(container.textContent).toContain("Mum");
  });

  it("renders with Dad winner data", () => {
    const { container } = render(
      <CharacterMugTemplate data={dadWinnerData} occasion="generic" />
    );
    expect(container.textContent).toContain("78%");
    expect(container.textContent).toContain("Dad");
  });

  it("renders with close-call data", () => {
    const { container } = render(
      <CharacterMugTemplate data={closeCallData} occasion="generic" />
    );
    expect(container.textContent).toContain("53%");
    // Should NOT contain 50/50
    expect(container.textContent).not.toContain("50/50");
  });

  it("displays all 8 features", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="generic" />
    );
    const text = container.textContent;
    // Check for feature labels (using FEATURE_LABELS from mugThemes.js)
    expect(text).toContain("Eyes");
    expect(text).toContain("Brows");
    expect(text).toContain("Smile");
    expect(text).toContain("Nose");
    expect(text).toContain("Face Shape");
    expect(text).toContain("Skin");
    expect(text).toContain("Hair");
    expect(text).toContain("Ears");
  });

  it("never displays 50/50", () => {
    // Even with close call data, should not show 50/50
    const { container } = render(
      <CharacterMugTemplate data={closeCallData} occasion="generic" />
    );
    const text = container.textContent;
    // The score badge should show 53% Mum, not 50/50
    expect(text).not.toMatch(/\b50%.*50%/);
  });

  it("renders null when no data provided", () => {
    const { container } = render(<CharacterMugTemplate data={null} />);
    expect(container.innerHTML).toBe("");
  });

  it("renders with mothers_day occasion", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="mothers_day" />
    );
    expect(container.textContent).toContain("HAPPY MOTHER'S DAY");
  });

  it("renders with fathers_day occasion", () => {
    const { container } = render(
      <CharacterMugTemplate data={dadWinnerData} occasion="fathers_day" />
    );
    expect(container.textContent).toContain("HAPPY FATHER'S DAY");
  });

  it("renders with heritage_gold occasion", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="heritage_gold" />
    );
    expect(container.textContent).toContain("FAMILY HERITAGE");
  });

  it("renders with carnival_spirit occasion", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="carnival_spirit" />
    );
    expect(container.textContent).toContain("CELEBRATE FAMILY");
  });

  it("renders with ubuntu occasion", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="ubuntu" />
    );
    expect(container.textContent).toContain("WE ARE FAMILY");
  });

  it("includes brand mark", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="generic" />
    );
    expect(container.textContent).toContain("famililook.com");
  });

  it("renders canvas at correct dimensions (830x345)", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="generic" />
    );
    const root = container.firstChild;
    expect(root.style.width).toBe("830px");
    expect(root.style.height).toBe("345px");
  });

  it("has transparent background for Prodigi print", () => {
    const { container } = render(
      <CharacterMugTemplate data={mumWinnerData} occasion="generic" />
    );
    const root = container.firstChild;
    expect(root.style.background).toBe("transparent");
  });
});

// ── Headline Engine Tests ────────────────────────────────────────────────────

describe("selectHeadlines", () => {
  it("produces deterministic output for same input", () => {
    const input = {
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Olivia",
      dominantFeature: "eyes",
      occasion: "generic",
    };
    const result1 = selectHeadlines(input);
    const result2 = selectHeadlines(input);
    expect(result1.heroHeadline).toBe(result2.heroHeadline);
    expect(result1.featureSubline).toBe(result2.featureSubline);
    expect(result1.winnerBubble).toBe(result2.winnerBubble);
  });

  it("selects from mum-high pool when mum wins with high pct", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 75,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Ella",
      dominantFeature: "eyes",
    });
    // Hero headline should contain MUM (from mum high pool)
    expect(result.heroHeadline.toUpperCase()).toMatch(/MUM|MUMMY|MINI ME/);
  });

  it("selects from dad-high pool when dad wins with high pct", () => {
    const result = selectHeadlines({
      winner: "parent2",
      winnerPct: 80,
      winnerLabel: "Dad",
      loserLabel: "Mum",
      childName: "Jack",
      dominantFeature: "smile",
    });
    expect(result.heroHeadline.toUpperCase()).toMatch(/DAD|DADDY|DOUBLE/);
  });

  it("selects from close-call pool when pct < 60", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 54,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Max",
      dominantFeature: "nose",
    });
    // Close-call headlines don't contain MUM or DAD specifically
    const headline = result.heroHeadline.toUpperCase();
    expect(headline).toMatch(/BLEND|BOTH|DEBATE|CLOSE|BARELY|TEAMWORK|GOOD|BEST|PERFECTLY|QUITE/);
  });

  it("selects from blend pool for blend winner", () => {
    const result = selectHeadlines({
      winner: "blend",
      winnerPct: 50,
      winnerLabel: "Both",
      loserLabel: "Both",
      childName: "Amy",
      dominantFeature: "eyes",
    });
    const headline = result.heroHeadline.toUpperCase();
    expect(headline).toMatch(/BOTH|UNIQUE|KIND|BLENDED|RECIPE/);
  });

  it("uses custom pool for non-standard parent names", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Nana",
      loserLabel: "Grandpa",
      childName: "Lily",
      dominantFeature: "eyes",
    });
    // Should contain the custom name
    expect(result.heroHeadline.toUpperCase()).toContain("NANA");
  });

  it("hero headline is <= 35 chars (excluding newlines)", () => {
    // Test with a very long child name
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Bartholomew",
      dominantFeature: "eyes",
    });
    const charCount = result.heroHeadline.replace(/\n/g, "").length;
    expect(charCount).toBeLessThanOrEqual(35);
  });

  it("feature subline is <= 50 chars", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Olivia",
      dominantFeature: "smile",
    });
    expect(result.featureSubline.length).toBeLessThanOrEqual(50);
  });

  it("returns occasion header for mothers_day", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Olivia",
      dominantFeature: "eyes",
      occasion: "mothers_day",
    });
    expect(result.occasionHeader).toBe("HAPPY MOTHER'S DAY");
  });

  it("returns null occasion header for generic", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Olivia",
      dominantFeature: "eyes",
      occasion: "generic",
    });
    expect(result.occasionHeader).toBeNull();
  });

  it("returns speech bubbles", () => {
    const result = selectHeadlines({
      winner: "parent1",
      winnerPct: 72,
      winnerLabel: "Mum",
      loserLabel: "Dad",
      childName: "Olivia",
      dominantFeature: "eyes",
    });
    expect(result.winnerBubble).toBeTruthy();
    expect(result.loserBubble).toBeTruthy();
    expect(result.winnerBubble.length).toBeLessThanOrEqual(20);
    expect(result.loserBubble.length).toBeLessThanOrEqual(20);
  });
});

// ── normaliseParent Tests ────────────────────────────────────────────────────

describe("normaliseParent", () => {
  it("recognises mum aliases", () => {
    expect(normaliseParent("Mum")).toBe("mum");
    expect(normaliseParent("Mom")).toBe("mum");
    expect(normaliseParent("MUMMY")).toBe("mum");
    expect(normaliseParent("mama")).toBe("mum");
    expect(normaliseParent("Mother")).toBe("mum");
  });

  it("recognises dad aliases", () => {
    expect(normaliseParent("Dad")).toBe("dad");
    expect(normaliseParent("DADDY")).toBe("dad");
    expect(normaliseParent("papa")).toBe("dad");
    expect(normaliseParent("Father")).toBe("dad");
  });

  it("returns custom for unknown labels", () => {
    expect(normaliseParent("Nana")).toBe("custom");
    expect(normaliseParent("Grandpa")).toBe("custom");
    expect(normaliseParent("Auntie")).toBe("custom");
  });

  it("handles null/empty", () => {
    expect(normaliseParent(null)).toBe("custom");
    expect(normaliseParent("")).toBe("custom");
  });
});
```

---

## Occasion-to-Style Mapping for KeepsakesModal Integration

When the `character_mug` product is selected and the user picks a cultural style, the `occasion` prop passed to `CharacterMugTemplate` should be mapped as follows:

| Style ID | occasion prop |
|----------|--------------|
| `character_default` | `"generic"` |
| `character_heritage` | `"heritage_gold"` |
| `character_carnival` | `"carnival_spirit"` |
| `character_ubuntu` | `"ubuntu"` |

This mapping follows the same pattern used by `mug_wrap` styles. The `KeepsakesModal` already passes occasion/style variants through `getPreviewStyleVariant()`. For Character Mugs, the style suffix after `character_` maps directly to the occasion theme name, with `default` mapping to `generic`. No KeepsakesModal code changes are needed -- the existing flow handles this automatically via `buildTemplateKey()`.

---

## Summary of Changes

| File | Action | Lines of code |
|------|--------|---------------|
| `CharacterMugTemplate.jsx` | NEW | ~380 lines |
| `characterHeadlines.js` | NEW | ~260 lines |
| `templateRegistry.js` | MODIFY | +30 lines (styles + product entry) |
| `printProfiles.js` | MODIFY | +25 lines (PRODUCT_TYPES + spec + profiles) |
| `productCatalog.js` | MODIFY | +1 product in drinkware array |
| `CharacterMugTemplate.test.jsx` | NEW | ~330 lines |
| **Total** | | ~1,026 lines |

## Key Design Decisions

1. **Headline is the hero** -- The centre panel gives the bold headline the largest font size (18-22px), displacing the photo to secondary status. This matches the CMO brief's key insight: the headline drives TikTok virality.

2. **Character SVGs use theme tokens** -- All character colours come from `getOccasionTheme()`, not hardcoded palettes. Switching from `generic` to `heritage_gold` recolours the entire character automatically.

3. **Deterministic headlines** -- The djb2 hash seeded on `childName + winnerPct` ensures the same child always gets the same headline. No flickering between preview and export.

4. **No new dependencies** -- The character SVGs are built with inline SVG strings (same approach as the prototype). When real illustrations arrive, they drop into `CharacterSVGInline` with no architectural changes.

5. **Same physical product** -- Character Mugs use the same Prodigi SKU (`GLOBAL-MUG-W`) as standard mugs. The 2 pound premium is pure margin -- no fulfilment change.

6. **Backward compatible** -- Existing `mug_wrap` and `family_mug_set` products are untouched. Character Mugs are an additive product line.

---

*This implementation document was produced by the Frontend Lead agent. No source code files were modified. All changes require CEO approval before edits are applied.*
