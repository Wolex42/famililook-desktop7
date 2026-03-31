/**
 * CharacterMugDesigner.jsx
 * FamiliLook — Character Mug product line
 * 
 * Drop-in React component. No external dependencies beyond React.
 * Reads from useKeepsakeData hook shape or accepts props directly.
 * 
 * Props:
 *   analysisData  — { winner, winnerPct, winnerLabel, loserLabel, childName, dominantFeature }
 *   onAddToBasket — (designState) => void
 *   onClose       — () => void  (optional, if used in modal)
 * 
 * Internal state handles everything else (character choice, emotion, theme, headline).
 */

import { useState, useCallback, useMemo } from 'react';

// ─── Colour themes ────────────────────────────────────────────────────────────

const THEMES = [
  { id: 'rose',   label: 'Rose',   primary:'#C0364E', light:'#E8637A', wash:'#FDF0F2', muted:'#9B6070', faint:'#C9A0AC', dark:'#3D0F22', bg:'#FDF0F2' },
  { id: 'ocean',  label: 'Ocean',  primary:'#1D6FA4', light:'#4A9BC7', wash:'#E8F4FB', muted:'#4A7A99', faint:'#A0C4D8', dark:'#0A2E44', bg:'#E8F4FB' },
  { id: 'forest', label: 'Forest', primary:'#2A7A4B', light:'#4FA86E', wash:'#EAF5EE', muted:'#4A7A5A', faint:'#A0C8AD', dark:'#0E2E1C', bg:'#EAF5EE' },
  { id: 'plum',   label: 'Plum',   primary:'#7B4EA6', light:'#A07BC8', wash:'#F2EAF9', muted:'#7A5A99', faint:'#C4A8D8', dark:'#2E1244', bg:'#F2EAF9' },
  { id: 'amber',  label: 'Amber',  primary:'#C47D1A', light:'#E0A840', wash:'#FDF4E3', muted:'#9A6A30', faint:'#D8C090', dark:'#3D2200', bg:'#FDF4E3' },
  { id: 'slate',  label: 'Slate',  primary:'#5F5E5A', light:'#888780', wash:'#F1EFE8', muted:'#6A6A66', faint:'#B4B2A9', dark:'#2C2C2A', bg:'#F1EFE8' },
];

// ─── Emotion sets per character ───────────────────────────────────────────────

const EMOTIONS = {
  mama:   ['proud','surprised','cheeky','celebrating','loving'],
  papa:   ['proud','surprised','cheeky','celebrating','loving'],
  cub:    ['happy','sleeping','surprised','giggling','curious'],
  mini:   ['proud','cheeky','surprised','pointing','celebrating'],
  gran:   ['proud','surprised','loving','showing_off','laughing'],
  gramps: ['proud','surprised','loving','showing_off','laughing'],
};

const EMOTION_LABELS = {
  proud:'Proud', surprised:'Surprised', cheeky:'Cheeky', celebrating:'Celebrating',
  loving:'Loving', happy:'Happy', sleeping:'Sleeping', giggling:'Giggling',
  curious:'Curious', pointing:'Pointing', showing_off:'Showing off', laughing:'Laughing',
};

// ─── Headline engine ──────────────────────────────────────────────────────────

const HEADLINE_POOLS = {
  mum: {
    high:   ["MUMMY'S\nMINI ME","SORRY DAD,\nI'M ALL MUM","MUM DID\nALL THE WORK","COPY + PASTE:\nMUM EDITION","MUM'S\nGREATEST HIT","MADE BY MUM","100% MUM\nENERGY"],
    medium: ["LIKE MOTHER,\nLIKE BABY","MOSTLY MUM","STRONG\nMUM VIBES","MUM'S TWIN"],
    close:  ["THE PERFECT\nBLEND","BEST\nOF BOTH","THE GREAT\nDEBATE","TEAMWORK!"],
  },
  dad: {
    high:   ["DADDY'S\nDOUBLE","SORRY MUM,\nALL DAD","DAD'S\nCTRL+C CTRL+V","THE APPLE\nDOESN'T FALL FAR","DAD'S\nGREATEST HIT","MADE BY DAD"],
    medium: ["MOSTLY DAD","STRONG\nDAD VIBES","DAD'S TWIN","CHIP OFF\nTHE OLD BLOCK"],
    close:  ["THE PERFECT\nBLEND","BEST\nOF BOTH","THE GREAT\nDEBATE","YOU BOTH\nDID GOOD"],
  },
  blend: {
    high:   ["THE PERFECT\nBLEND","BEST\nOF BOTH","MADE WITH LOVE","TEAMWORK\nMAKES IT WORK"],
    medium: ["THE PERFECT\nBLEND","BEST OF BOTH"],
    close:  ["THE GREAT\nDEBATE","50/50?\nNOT QUITE...","THE PERFECT\nBLEND"],
  },
};

const FEATURE_LINES = {
  eyes:      { mum:"GOT MUM'S EYES",      dad:"DAD'S EYES, ALL THE WAY",        blend:"THOSE EYES ARE UNIQUE" },
  nose:      { mum:"THAT NOSE? 100% MUM", dad:"DAD'S NOSE, NO QUESTION",        blend:"THE NOSE KNOWS" },
  smile:     { mum:"MUM'S SMILE ALL THE WAY", dad:"DAD'S SMILE, THROUGH & THROUGH", blend:"BEST SMILE FROM BOTH" },
  hair:      { mum:"HAIR BY MUM",         dad:"HAIR BY DAD",                    blend:"HAIR: THE GREAT BLEND" },
  eyebrows:  { mum:"MUM'S BROWS, NO DOUBT", dad:"THOSE BROWS? ALL DAD",         blend:"BROWS: A JOINT EFFORT" },
  face_shape:{ mum:"MUM'S FACE SHAPE",    dad:"DAD'S FACE SHAPE",               blend:"PERFECTLY BLENDED FACE" },
  jawline:   { mum:"MUM'S JAWLINE",       dad:"DAD'S JAWLINE",                  blend:"THE PERFECT JAW" },
  cheeks:    { mum:"MUM'S CHEEKS",        dad:"DAD'S CHEEKS",                   blend:"CHEEKS FROM BOTH" },
};

const OCCASION_HEADERS = {
  mothers_day: "HAPPY MOTHER'S DAY",
  fathers_day: "HAPPY FATHER'S DAY",
  birthday:    "HAPPY BIRTHDAY",
  christmas:   "MERRY CHRISTMAS",
};

function getPercentageBracket(pct) {
  if (pct >= 70) return 'high';
  if (pct >= 60) return 'medium';
  return 'close';
}

function normaliseWinner(label) {
  if (!label) return 'blend';
  const l = label.toLowerCase().trim();
  const mumAliases = ['mum','mom','mummy','mommy','mama','mother','ma'];
  const dadAliases = ['dad','daddy','papa','father','pa','dada'];
  if (mumAliases.includes(l)) return 'mum';
  if (dadAliases.includes(l)) return 'dad';
  return 'blend';
}

// ─── SVG character drawing functions ─────────────────────────────────────────

function getEyes(emo) {
  const celebrating = ['celebrating','happy','giggling','loving','sleeping','showing_off','laughing'];
  if (celebrating.includes(emo)) {
    return `<path d="M78 96Q98 80 118 96" fill="none" stroke="#1A1A1A" stroke-width="7" stroke-linecap="round"/>
            <path d="M142 96Q162 80 182 96" fill="none" stroke="#1A1A1A" stroke-width="7" stroke-linecap="round"/>`;
  }
  if (emo === 'surprised') {
    return `<circle cx="98" cy="92" r="14" fill="#1A1A1A"/>
            <circle cx="162" cy="92" r="14" fill="#1A1A1A"/>
            <circle cx="104" cy="86" r="5" fill="white"/>
            <circle cx="168" cy="86" r="5" fill="white"/>`;
  }
  if (emo === 'cheeky' || emo === 'pointing') {
    return `<circle cx="100" cy="94" r="11" fill="#1A1A1A"/>
            <circle cx="105" cy="89" r="4" fill="white"/>
            <path d="M144 92Q162 80 180 92" fill="none" stroke="#1A1A1A" stroke-width="7" stroke-linecap="round"/>`;
  }
  return `<circle cx="100" cy="94" r="11" fill="#1A1A1A"/>
          <circle cx="164" cy="94" r="11" fill="#1A1A1A"/>
          <circle cx="105" cy="89" r="4" fill="white"/>
          <circle cx="169" cy="89" r="4" fill="white"/>`;
}

function getMouth(emo) {
  if (emo === 'surprised') {
    return `<ellipse cx="130" cy="130" rx="14" ry="16" fill="#1A1A1A"/>
            <ellipse cx="130" cy="131" rx="9" ry="11" fill="#7A1835"/>`;
  }
  if (['celebrating','showing_off','giggling','laughing'].includes(emo)) {
    return `<path d="M86 118Q130 154 174 118" fill="#1A1A1A" stroke="#1A1A1A" stroke-width="3"/>
            <path d="M90 120Q130 148 170 120Q155 140 130 142Q105 140 90 120Z" fill="#1A1A1A"/>
            <path d="M94 122Q130 144 166 122Q152 138 130 140Q108 138 94 122Z" fill="#7A1835"/>
            <rect x="106" y="126" width="17" height="9" rx="3" fill="white"/>
            <rect x="125" y="126" width="17" height="9" rx="3" fill="white"/>`;
  }
  if (emo === 'cheeky' || emo === 'pointing') {
    return `<path d="M90 120Q112 142 168 128" fill="none" stroke="#1A1A1A" stroke-width="6.5" stroke-linecap="round"/>
            <path d="M93 122Q115 140 165 128Q145 136 110 136Q95 134 93 122Z" fill="#1A1A1A"/>`;
  }
  if (['loving','sleeping','curious'].includes(emo)) {
    return `<path d="M96 122Q130 144 164 122" fill="none" stroke="#1A1A1A" stroke-width="5.5" stroke-linecap="round"/>
            <path d="M99 124Q130 142 161 124Q148 134 130 136Q112 134 99 124Z" fill="#1A1A1A"/>`;
  }
  // proud / happy / default
  return `<path d="M92 122Q130 150 168 122" fill="none" stroke="#1A1A1A" stroke-width="6" stroke-linecap="round"/>
          <path d="M95 124Q130 146 165 124Q155 138 130 140Q105 138 95 124Z" fill="#1A1A1A"/>
          <path d="M98 126Q130 142 162 126Q152 136 130 138Q108 136 98 126Z" fill="#7A1835"/>`;
}

function getLashes(emo) {
  const noLash = ['surprised','sleeping','giggling'];
  if (noLash.includes(emo)) return '';
  return `<line x1="76" y1="72" x2="68" y2="56" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>
          <line x1="88" y1="66" x2="84" y2="50" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>
          <line x1="100" y1="63" x2="100" y2="47" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>
          <line x1="184" y1="72" x2="192" y2="56" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>
          <line x1="172" y1="66" x2="176" y2="50" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>
          <line x1="160" y1="63" x2="160" y2="47" stroke="#3D0F22" stroke-width="4.5" stroke-linecap="round"/>`;
}

function getArms(char, emo, T) {
  if (char === 'cub') {
    return `<path d="M82 195Q60 188 52 200Q46 210 56 218Q68 224 80 212Z" fill="${T.light}" stroke="${T.dark}" stroke-width="5"/>
            <path d="M178 195Q200 188 208 200Q214 210 204 218Q192 224 180 212Z" fill="${T.light}" stroke="${T.dark}" stroke-width="5"/>`;
  }
  if (['celebrating','showing_off'].includes(emo)) {
    return `<path d="M66 152Q44 126 30 96Q18 70 32 58Q48 46 62 66Q76 86 76 116Q76 136 70 154Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <path d="M194 152Q216 126 230 96Q242 70 228 58Q212 46 198 66Q184 86 184 116Q184 136 190 154Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <ellipse cx="34" cy="60" rx="18" ry="16" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
            <ellipse cx="226" cy="60" rx="18" ry="16" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
            <path d="M14 30L17 20L20 30L30 33L20 36L17 46L14 36L4 33Z" fill="#FAC775" stroke="${T.dark}" stroke-width="2"/>
            <path d="M232 18L234 10L236 18L244 20L236 22L234 30L232 22L224 20Z" fill="${T.light}" stroke="${T.dark}" stroke-width="2"/>`;
  }
  if (emo === 'surprised') {
    return `<path d="M66 158Q36 140 22 116Q12 96 26 84Q40 72 54 88Q66 102 68 126Q70 144 68 158Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <path d="M194 158Q224 140 238 116Q248 96 234 84Q220 72 206 88Q194 102 192 126Q190 144 192 158Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <ellipse cx="26" cy="90" rx="20" ry="17" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
            <ellipse cx="234" cy="90" rx="20" ry="17" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>`;
  }
  if (['cheeky','pointing'].includes(emo)) {
    return `<path d="M68 170Q40 178 30 196Q22 212 28 224Q36 238 52 232Q66 226 70 210Q74 194 72 176Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <ellipse cx="36" cy="228" rx="18" ry="15" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
            <path d="M192 162Q218 150 242 136Q256 126 258 138Q260 150 248 158Q234 166 214 172Q200 176 192 170Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <ellipse cx="254" cy="140" rx="12" ry="10" fill="${T.primary}" stroke="${T.dark}" stroke-width="5"/>`;
  }
  if (emo === 'loving') {
    return `<path d="M66 168Q40 180 28 200Q18 218 28 230Q38 242 54 234Q68 226 70 208Q72 190 70 172Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <path d="M194 168Q220 180 232 200Q242 218 232 230Q222 242 206 234Q192 226 190 208Q188 190 190 172Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <ellipse cx="32" cy="232" rx="18" ry="15" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
            <ellipse cx="228" cy="232" rx="18" ry="15" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
            <path d="M38 70Q38 62 46 62Q54 62 54 70Q54 78 38 88Q22 78 22 70Q22 62 30 62Q38 62 38 70Z" fill="${T.light}" stroke="${T.dark}" stroke-width="3"/>
            <path d="M214 56Q214 50 220 50Q226 50 226 56Q226 62 214 70Q202 62 202 56Q202 50 208 50Q214 50 214 56Z" fill="${T.light}" stroke="${T.dark}" stroke-width="2.5"/>`;
  }
  // proud / default — arm on hip + tea
  return `<path d="M68 170Q40 178 30 196Q22 212 28 224Q36 238 52 232Q66 226 70 210Q74 194 72 176Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
          <ellipse cx="36" cy="228" rx="18" ry="15" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
          <path d="M192 168Q218 172 228 188Q236 202 230 216Q222 230 208 226Q194 220 190 206Q186 190 190 174Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
          <rect x="204" y="212" width="38" height="30" rx="7" fill="${T.wash}" stroke="${T.dark}" stroke-width="5"/>
          <rect x="208" y="216" width="30" height="7" rx="3" fill="${T.faint}" opacity="0.5"/>
          <path d="M242 217Q256 217 256 227Q256 238 242 237" fill="none" stroke="${T.dark}" stroke-width="5" stroke-linecap="round"/>
          <path d="M214 208Q210 198 214 188Q218 178 214 168" fill="none" stroke="${T.faint}" stroke-width="3.5" stroke-linecap="round"/>
          <path d="M224 206Q220 196 224 186Q228 176 224 166" fill="none" stroke="${T.faint}" stroke-width="3.5" stroke-linecap="round"/>`;
}

function getBody(char, T) {
  if (char === 'cub') {
    return `<ellipse cx="130" cy="200" rx="38" ry="50" fill="${T.wash}" stroke="${T.dark}" stroke-width="6"/>
            <ellipse cx="130" cy="230" rx="55" ry="20" fill="${T.light}" stroke="${T.dark}" stroke-width="5"/>`;
  }
  if (char === 'gran' || char === 'gramps') {
    return `<path d="M70 150Q62 220 66 260Q70 280 130 282Q190 280 194 260Q198 220 190 150Z" fill="${T.muted}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
            <line x1="130" y1="152" x2="130" y2="275" stroke="${T.wash}" stroke-width="2" opacity="0.5"/>
            <circle cx="130" cy="185" r="5" fill="${T.wash}" opacity="0.7"/>
            <circle cx="130" cy="210" r="5" fill="${T.wash}" opacity="0.7"/>
            <circle cx="130" cy="235" r="5" fill="${T.wash}" opacity="0.7"/>`;
  }
  const w = char === 'papa' ? 60 : 54;
  return `<path d="M${130-w} 150Q${122-w} 220 ${126-w} 260Q130 282 130 282Q130 282 ${134+w} 260Q${138+w} 220 ${130+w} 150Z" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
          <path d="M88 165Q88 240 130 245Q172 240 172 165Q155 155 130 153Q105 155 88 165Z" fill="${T.primary}" opacity="0.4"/>`;
}

function getEars(char, T) {
  const r = (char === 'gran' || char === 'gramps') ? 26 : 28;
  const inner = (char === 'gran' || char === 'gramps') ? 14 : 16;
  return `<circle cx="60" cy="44" r="${r}" fill="${T.primary}" stroke="${T.dark}" stroke-width="7"/>
          <circle cx="60" cy="44" r="${inner}" fill="${T.light}" stroke="${T.dark}" stroke-width="4"/>
          <circle cx="200" cy="44" r="${r}" fill="${T.primary}" stroke="${T.dark}" stroke-width="7"/>
          <circle cx="200" cy="44" r="${inner}" fill="${T.light}" stroke="${T.dark}" stroke-width="4"/>`;
}

function getHair(char, T) {
  if (char === 'papa' || char === 'gramps') {
    return `<ellipse cx="84" cy="44" rx="18" ry="10" fill="${T.faint}" stroke="${T.dark}" stroke-width="3"/>
            <ellipse cx="176" cy="44" rx="18" ry="10" fill="${T.faint}" stroke="${T.dark}" stroke-width="3"/>`;
  }
  if (char === 'gran') {
    return `<ellipse cx="130" cy="34" rx="36" ry="18" fill="${T.faint}" stroke="${T.dark}" stroke-width="4"/>
            <circle cx="130" cy="26" r="14" fill="${T.faint}" stroke="${T.dark}" stroke-width="3"/>`;
  }
  if (char === 'mini') {
    return `<path d="M98 44Q108 28 118 40Q124 28 130 38Q136 26 142 38Q152 28 162 44" fill="none" stroke="${T.dark}" stroke-width="5" stroke-linecap="round"/>`;
  }
  if (char === 'cub') {
    return `<path d="M125 30Q130 20 135 30" fill="none" stroke="${T.dark}" stroke-width="5" stroke-linecap="round"/>`;
  }
  // mama — bun
  return `<circle cx="130" cy="30" r="30" fill="${T.dark}"/>
          <circle cx="130" cy="30" r="22" fill="${T.dark}" opacity="0.6"/>
          <ellipse cx="120" cy="22" rx="10" ry="7" fill="${T.dark}" opacity="0.3"/>`;
}

function buildCharacterSVG(char, emo, T) {
  return `
    <ellipse cx="130" cy="292" rx="58" ry="8" fill="${T.light}" opacity="0.18"/>
    <rect x="90" y="252" width="30" height="36" rx="15" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
    <rect x="140" y="252" width="30" height="36" rx="15" fill="${T.primary}" stroke="${T.dark}" stroke-width="7" stroke-linejoin="round"/>
    ${getBody(char, T)}
    ${getArms(char, emo, T)}
    <rect x="108" y="132" width="44" height="24" rx="8" fill="${T.primary}" stroke="${T.dark}" stroke-width="6"/>
    <ellipse cx="130" cy="96" rx="76" ry="72" fill="${T.primary}" stroke="${T.dark}" stroke-width="8"/>
    ${getEars(char, T)}
    ${getHair(char, T)}
    ${getLashes(emo)}
    <ellipse cx="98" cy="92" rx="19" ry="18" fill="white" stroke="${T.dark}" stroke-width="5"/>
    <ellipse cx="162" cy="92" rx="19" ry="18" fill="white" stroke="${T.dark}" stroke-width="5"/>
    ${getEyes(emo)}
    <ellipse cx="130" cy="112" rx="12" ry="9" fill="${T.dark}"/>
    ${getMouth(emo)}
    <ellipse cx="74" cy="108" rx="18" ry="13" fill="${T.light}" opacity="0.32"/>
    <ellipse cx="186" cy="108" rx="18" ry="13" fill="${T.light}" opacity="0.32"/>
  `;
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function CharacterSVG({ char, emo, theme, size = '100%' }) {
  const T = THEMES.find(t => t.id === theme) || THEMES[0];
  return (
    <svg
      viewBox="0 0 260 300"
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      style={{ display: 'block' }}
      dangerouslySetInnerHTML={{ __html: buildCharacterSVG(char, emo, T) }}
    />
  );
}

function MugPreview({ char, emo, theme, winner, pct, feature, occasion, headline, childName }) {
  const T = THEMES.find(t => t.id === theme) || THEMES[0];
  const winLabel = winner === 'mum' ? 'MUM' : winner === 'dad' ? 'DAD' : 'BOTH';
  const featLine = FEATURE_LINES[feature]?.[winner] || '';
  const occLine  = occasion ? OCCASION_HEADERS[occasion] : '';
  const name     = childName?.trim().toUpperCase() || '';
  const displayHero = name && headline.includes('MINI ME')
    ? headline.replace('MINI ME', name)
    : headline;

  return (
    <div style={{
      width: '100%',
      maxWidth: 560,
      background: 'white',
      borderRadius: 10,
      overflow: 'hidden',
      aspectRatio: '2670/1110',
      display: 'flex',
      boxShadow: '0 2px 20px rgba(0,0,0,.16)',
    }}>
      {/* Character panel */}
      <div style={{ flex: '0 0 28%', background: T.bg, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', overflow: 'hidden' }}>
        <CharacterSVG char={char} emo={emo} theme={theme} />
      </div>

      {/* Photo panel */}
      <div style={{ flex: '0 0 34%', background: '#f0ebe5', borderLeft: '3px solid #ddd5cc', borderRight: '3px solid #ddd5cc', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
        {/* Corner flourishes */}
        {[['5%','4%',''],['5%','4%','scaleX(-1)'],['auto','4%','scaleY(-1)'],['auto','4%','scale(-1,-1)']].map(([top, right, transform], i) => (
          <svg key={i} style={{ position: 'absolute', width: '16%', opacity: .3,
            top: i < 2 ? '5%' : 'auto', bottom: i >= 2 ? '5%' : 'auto',
            left: (i === 0 || i === 2) ? '4%' : 'auto',
            right: (i === 1 || i === 3) ? '4%' : 'auto',
            transform: ['','scaleX(-1)','scaleY(-1)','scale(-1,-1)'][i],
          }} viewBox="0 0 40 40">
            <path d="M4 36Q4 4 36 4" fill="none" stroke="#9B6070" strokeWidth="2.5" strokeLinecap="round"/>
            <circle cx="4" cy="36" r="3" fill="#9B6070"/>
            <circle cx="36" cy="4" r="3" fill="#9B6070"/>
          </svg>
        ))}
        <div style={{ width: '72%', aspectRatio: '1', borderRadius: '50%', background: 'white', border: `3px solid ${T.faint}`, padding: '3%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ width: '100%', aspectRatio: '1', borderRadius: '50%', background: '#ddd5cc', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
            <svg viewBox="0 0 100 100" width="80%">
              <circle cx="50" cy="38" r="26" fill="#c4b0a4"/>
              <ellipse cx="50" cy="82" rx="34" ry="24" fill="#c4b0a4"/>
              <ellipse cx="42" cy="34" rx="5" ry="6" fill="#8a6a5a" opacity=".7"/>
              <ellipse cx="58" cy="34" rx="5" ry="6" fill="#8a6a5a" opacity=".7"/>
              <path d="M44 46Q50 52 56 46" fill="none" stroke="#8a6a5a" strokeWidth="2" strokeLinecap="round" opacity=".8"/>
            </svg>
          </div>
        </div>
        <div style={{ position: 'absolute', bottom: '5%', fontSize: 'clamp(4px,.7vw,6px)', color: '#a89890', fontStyle: 'italic', letterSpacing: '.04em' }}>
          Your photo here
        </div>
      </div>

      {/* Text panel */}
      <div style={{ flex: '0 0 38%', background: 'white', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '4% 6%' }}>
        {occLine && (
          <div style={{ fontFamily: "'Arial Rounded MT Bold', Arial, sans-serif", fontWeight: 800, fontSize: 'clamp(5px,1.2vw,10px)', textTransform: 'uppercase', letterSpacing: '.07em', textAlign: 'center', color: T.primary, lineHeight: 1, marginBottom: '3%' }}>
            {occLine}
          </div>
        )}
        <div style={{ fontFamily: "'Arial Black', 'Arial Bold', Impact, sans-serif", fontWeight: 900, fontSize: 'clamp(12px,4vw,36px)', textAlign: 'center', lineHeight: .92, color: T.dark, textTransform: 'uppercase', letterSpacing: '-.025em', whiteSpace: 'pre-line' }}>
          {displayHero}
        </div>
        <div style={{ width: '60%', height: 2, background: T.light, borderRadius: 2, margin: '4% auto' }}/>
        {featLine && (
          <div style={{ fontFamily: "'Arial Rounded MT Bold', Arial, sans-serif", fontWeight: 700, fontSize: 'clamp(5px,1.1vw,10px)', textTransform: 'uppercase', letterSpacing: '.04em', textAlign: 'center', color: T.muted, lineHeight: 1.2, marginBottom: '3%' }}>
            {featLine}
          </div>
        )}
        <div style={{ background: T.primary, color: 'white', borderRadius: 999, fontFamily: "'Arial Black', sans-serif", fontWeight: 900, fontSize: 'clamp(9px,2.3vw,20px)', padding: '.3em 1em', letterSpacing: '.04em', textAlign: 'center' }}>
          {Math.round(pct)}% {winLabel}
        </div>
        <div style={{ fontSize: 'clamp(4px,.8vw,7px)', color: T.faint, marginTop: 'auto', paddingTop: '3%', letterSpacing: '.07em', fontFamily: 'sans-serif', textTransform: 'uppercase' }}>
          famililook.com
        </div>
      </div>
    </div>
  );
}

// ─── Main designer component ──────────────────────────────────────────────────

export default function CharacterMugDesigner({ analysisData = {}, onAddToBasket, onClose }) {

  // Derive initial state from analysis data if provided
  const initWinner  = useMemo(() => normaliseWinner(analysisData.winnerLabel), [analysisData.winnerLabel]);
  const initPct     = useMemo(() => analysisData.winnerPct || 72, [analysisData.winnerPct]);
  const initFeature = useMemo(() => analysisData.dominantFeature || 'eyes', [analysisData.dominantFeature]);
  const initName    = useMemo(() => analysisData.childName || '', [analysisData.childName]);

  const [char,     setChar]     = useState('mama');
  const [emo,      setEmo]      = useState('proud');
  const [winner,   setWinner]   = useState(initWinner);
  const [pct,      setPct]      = useState(initPct);
  const [feature,  setFeature]  = useState(initFeature);
  const [occasion, setOccasion] = useState('');
  const [themeId,  setThemeId]  = useState('rose');
  const [hlIdx,    setHlIdx]    = useState(0);
  const [childName,setChildName]= useState(initName);

  const bracket    = getPercentageBracket(pct);
  const hlPool     = (HEADLINE_POOLS[winner] || HEADLINE_POOLS.blend)[bracket];
  const safeHlIdx  = hlIdx < hlPool.length ? hlIdx : 0;
  const headline   = hlPool[safeHlIdx];

  const handleCharChange = useCallback((c) => {
    setChar(c);
    setEmo(EMOTIONS[c][0]);
  }, []);

  const handleWinnerChange = useCallback((w) => {
    setWinner(w);
    setHlIdx(0);
  }, []);

  const handleAddToBasket = useCallback(() => {
    const design = { char, emo, winner, pct, feature, occasion, themeId, headline, childName };
    onAddToBasket?.(design);
  }, [char, emo, winner, pct, feature, occasion, themeId, headline, childName, onAddToBasket]);

  // Shared styles
  const s = {
    chip: (active) => ({
      fontSize: 11, padding: '4px 10px', borderRadius: 999,
      border: active ? '1.5px solid #3D0F22' : '0.5px solid #ccc',
      cursor: 'pointer', whiteSpace: 'nowrap',
      background: active ? '#3D0F22' : 'white',
      color: active ? 'white' : '#555',
      fontFamily: 'inherit', transition: 'all .15s',
    }),
    secTitle: {
      fontSize: 11, fontWeight: 600, color: '#888', textTransform: 'uppercase',
      letterSpacing: '.07em', marginBottom: 8,
    },
    section: {
      padding: '14px 0', borderBottom: '0.5px solid #eee',
    },
    chipRow: { display: 'flex', flexWrap: 'wrap', gap: 5 },
  };

  const T = THEMES.find(t => t.id === themeId) || THEMES[0];

  return (
    <div style={{ fontFamily: "'Helvetica Neue', Helvetica, Arial, sans-serif", background: '#fafaf9', minHeight: '100vh' }}>

      {/* Header */}
      <div style={{ background: 'white', borderBottom: '0.5px solid #eee', padding: '12px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ fontSize: 15, fontWeight: 700, color: '#3D0F22', letterSpacing: '-.01em' }}>
          Design your Character Mug
        </div>
        {onClose && (
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: 18, cursor: 'pointer', color: '#888', lineHeight: 1 }}>✕</button>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 0, minHeight: 'calc(100vh - 49px)' }}>

        {/* Canvas col */}
        <div style={{ padding: 24, display: 'flex', flexDirection: 'column', gap: 16, background: '#f5f3f0', alignItems: 'center' }}>
          <MugPreview
            char={char} emo={emo} theme={themeId}
            winner={winner} pct={pct} feature={feature}
            occasion={occasion} headline={headline} childName={childName}
          />

          {/* Headline picker pills */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5, justifyContent: 'center', maxWidth: 560 }}>
            {hlPool.map((h, i) => (
              <button key={h} style={s.chip(i === safeHlIdx)} onClick={() => setHlIdx(i)}>
                {h.replace('\n', ' ')}
              </button>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div style={{ background: 'white', borderLeft: '0.5px solid #eee', padding: '0 20px', overflowY: 'auto', maxHeight: 'calc(100vh - 49px)' }}>

          {/* Character */}
          <div style={s.section}>
            <div style={s.secTitle}>Character</div>
            <div style={s.chipRow}>
              {Object.keys(EMOTIONS).map(c => (
                <button key={c} style={s.chip(char === c)} onClick={() => handleCharChange(c)}>
                  {c === 'mama' ? 'Mama Bear' : c === 'papa' ? 'Papa Bear' : c === 'cub' ? 'Little Cub' : c === 'mini' ? 'Mini Me' : c === 'gran' ? 'Gran' : 'Gramps'}
                </button>
              ))}
            </div>
          </div>

          {/* Emotion */}
          <div style={s.section}>
            <div style={s.secTitle}>Emotion</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 4 }}>
              {EMOTIONS[char].map(e => (
                <div
                  key={e}
                  title={EMOTION_LABELS[e]}
                  onClick={() => setEmo(e)}
                  style={{
                    aspectRatio: '1', borderRadius: 8,
                    border: emo === e ? `2px solid ${T.primary}` : '1.5px solid #eee',
                    cursor: 'pointer', background: emo === e ? T.bg : '#fafafa',
                    display: 'flex', flexDirection: 'column', alignItems: 'center',
                    justifyContent: 'center', overflow: 'hidden', padding: 2, transition: 'all .15s',
                  }}
                >
                  <CharacterSVG char={char} emo={e} theme={themeId} />
                  <div style={{ fontSize: 9, color: emo === e ? T.dark : '#aaa', textAlign: 'center', paddingBottom: 2, letterSpacing: '.03em' }}>
                    {EMOTION_LABELS[e]}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Result */}
          <div style={s.section}>
            <div style={s.secTitle}>Resemblance result</div>
            <div style={{ ...s.chipRow, marginBottom: 8 }}>
              {['mum','dad','blend'].map(w => (
                <button key={w} style={s.chip(winner === w)} onClick={() => handleWinnerChange(w)}>
                  {w === 'mum' ? 'Mum' : w === 'dad' ? 'Dad' : 'Blend'}
                </button>
              ))}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              <label style={{ fontSize: 12, color: '#888', minWidth: 50 }}>Match</label>
              <input type="range" min="51" max="100" step="1" value={pct}
                onChange={e => setPct(Number(e.target.value))}
                style={{ flex: 1 }}
              />
              <span style={{ fontSize: 12, fontWeight: 600, minWidth: 34, color: '#333' }}>{pct}%</span>
            </div>
            <div style={s.chipRow}>
              {Object.keys(FEATURE_LINES).map(f => (
                <button key={f} style={s.chip(feature === f)} onClick={() => setFeature(f)}>
                  {f === 'face_shape' ? 'Face' : f.charAt(0).toUpperCase() + f.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Occasion */}
          <div style={s.section}>
            <div style={s.secTitle}>Occasion</div>
            <div style={s.chipRow}>
              {[['', 'None'], ['mothers_day', "Mother's Day"], ['fathers_day', "Father's Day"], ['birthday', 'Birthday'], ['christmas', 'Christmas']].map(([v, label]) => (
                <button key={v} style={s.chip(occasion === v)} onClick={() => setOccasion(v)}>
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Colour theme */}
          <div style={s.section}>
            <div style={s.secTitle}>Colour theme</div>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {THEMES.map(t => (
                <div
                  key={t.id}
                  title={t.label}
                  onClick={() => setThemeId(t.id)}
                  style={{
                    width: 26, height: 26, borderRadius: '50%',
                    background: t.primary, cursor: 'pointer',
                    border: themeId === t.id ? '3px solid #222' : '2px solid transparent',
                    transform: themeId === t.id ? 'scale(1.15)' : 'scale(1)',
                    transition: 'all .15s',
                  }}
                />
              ))}
            </div>
          </div>

          {/* Child name */}
          <div style={s.section}>
            <div style={s.secTitle}>Child's name</div>
            <input
              type="text"
              value={childName}
              onChange={e => setChildName(e.target.value)}
              placeholder="e.g. Olivia"
              maxLength={14}
              style={{
                width: '100%', fontSize: 13, padding: '7px 10px',
                borderRadius: 8, border: '0.5px solid #ddd',
                background: 'white', color: '#333', outline: 'none',
                fontFamily: 'inherit',
              }}
            />
            <div style={{ fontSize: 11, color: '#bbb', marginTop: 4 }}>
              Replaces "Mini Me" in the headline
            </div>
          </div>

          {/* Order */}
          <div style={{ padding: '16px 0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 10 }}>
              <div>
                <div style={{ fontSize: 22, fontWeight: 800, color: '#3D0F22', letterSpacing: '-.02em' }}>£16.99</div>
                <div style={{ fontSize: 11, color: '#aaa', marginTop: 2 }}>Free UK delivery · 3–5 days</div>
              </div>
              <div style={{ fontSize: 11, color: '#aaa', textAlign: 'right' }}>
                Dishwasher safe<br/>11oz ceramic
              </div>
            </div>
            <button
              onClick={handleAddToBasket}
              style={{
                width: '100%', padding: '12px 0', borderRadius: 8,
                background: T.primary, color: 'white', border: 'none',
                fontSize: 14, fontWeight: 700, letterSpacing: '.04em',
                cursor: 'pointer', transition: 'opacity .15s',
              }}
              onMouseOver={e => e.currentTarget.style.opacity = '.88'}
              onMouseOut={e => e.currentTarget.style.opacity = '1'}
            >
              Add to basket
            </button>
            <div style={{ fontSize: 10, color: '#bbb', textAlign: 'center', marginTop: 8 }}>
              AI-powered face analysis · For entertainment purposes
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}