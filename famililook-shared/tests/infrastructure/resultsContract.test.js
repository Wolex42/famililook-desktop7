import { describe, it, expect } from 'vitest';
import {
  getWinner,
  extractFeatureVotes,
  countFeatures,
  getPercentages,
  apply5050Rule,
  buildResultsSummary,
  validateResults,
  CANONICAL_FEATURES,
  FEATURE_LABELS,
  MIN_PERCENTAGE_GAP,
  NUDGE_WINNER_PCT,
  NUDGE_LOSER_PCT,
} from '../../src/infrastructure/resultsContract';
import resultsContract from '../../src/infrastructure/resultsContract';

// ─── Test fixtures ──────────────────────────────────────────────

const FULL_PARENT1_VOTES = {
  eyes: 'parent1', eyebrows: 'parent1', smile: 'parent1', nose: 'parent1',
  face_shape: 'parent1', skin: 'parent1', hair: 'parent1', ears: 'parent1',
};

const FULL_PARENT2_VOTES = {
  eyes: 'parent2', eyebrows: 'parent2', smile: 'parent2', nose: 'parent2',
  face_shape: 'parent2', skin: 'parent2', hair: 'parent2', ears: 'parent2',
};

const SPLIT_5_3_PARENT1 = {
  eyes: 'parent1', eyebrows: 'parent1', smile: 'parent1', nose: 'parent1',
  face_shape: 'parent1', skin: 'parent2', hair: 'parent2', ears: 'parent2',
};

const SPLIT_4_4_TIED = {
  eyes: 'parent1', eyebrows: 'parent1', smile: 'parent1', nose: 'parent1',
  face_shape: 'parent2', skin: 'parent2', hair: 'parent2', ears: 'parent2',
};

const SPLIT_4_2_2UNKNOWN = {
  eyes: 'parent1', eyebrows: 'parent1', smile: 'parent1', nose: 'parent1',
  face_shape: 'parent2', skin: 'parent2', hair: 'unknown', ears: 'unknown',
};

// ─── getWinner ──────────────────────────────────────────────────

describe('resultsContract.getWinner', () => {
  it('returns parent1 when inheritance.winner is "parent1"', () => {
    expect(getWinner({ inheritance: { winner: 'parent1' } })).toBe('parent1');
  });

  it('returns parent2 when child.winner is "parent2"', () => {
    expect(getWinner({ winner: 'parent2' })).toBe('parent2');
  });

  it('normalizes parent_a → parent1, parent_b → parent2', () => {
    expect(getWinner({ winner: 'parent_a' })).toBe('parent1');
    expect(getWinner({ winner: 'parent_b' })).toBe('parent2');
  });

  it('normalizes mum → parent1, dad → parent2', () => {
    expect(getWinner({ inheritance: { winner: 'mum' } })).toBe('parent1');
    expect(getWinner({ winner: 'dad' })).toBe('parent2');
  });

  it('returns null for null/undefined/empty input', () => {
    expect(getWinner(null)).toBeNull();
    expect(getWinner(undefined)).toBeNull();
    expect(getWinner({})).toBeNull();
  });

  // THE BUG FIX: inheritance.winner takes priority over child.winner
  // This resolves the MobileResultsSection vs useFamilyKeepsakeData disagreement
  it('inheritance.winner takes priority over child.winner (field order bug fix)', () => {
    const result = { inheritance: { winner: 'parent1' }, winner: 'parent2' };
    expect(getWinner(result)).toBe('parent1');
  });

  it('falls back to verdict.primary_parent', () => {
    expect(getWinner({ verdict: { primary_parent: 'parent1' } })).toBe('parent1');
  });

  it('falls back to verdict.primaryParent', () => {
    expect(getWinner({ verdict: { primaryParent: 'parent2' } })).toBe('parent2');
  });

  it('returns null for blend/unknown winner', () => {
    expect(getWinner({ winner: 'blend' })).toBeNull();
    expect(getWinner({ winner: 'unknown' })).toBeNull();
  });
});

// ─── extractFeatureVotes ────────────────────────────────────────

describe('resultsContract.extractFeatureVotes', () => {
  it('extracts from feature_votes (primary path)', () => {
    const result = { feature_votes: SPLIT_5_3_PARENT1 };
    const votes = extractFeatureVotes(result);
    expect(votes.eyes).toBe('parent1');
    expect(votes.skin).toBe('parent2');
    expect(Object.keys(votes)).toHaveLength(8);
  });

  // THE BUG FIX: inheritance.feature_votes path must be checked
  // AnalysisSection was missing this — showed empty features
  it('extracts from inheritance.feature_votes (fallback path)', () => {
    const result = { inheritance: { feature_votes: SPLIT_5_3_PARENT1 } };
    const votes = extractFeatureVotes(result);
    expect(votes.eyes).toBe('parent1');
    expect(votes.skin).toBe('parent2');
  });

  it('extracts from features.feature_votes (middle path)', () => {
    const result = { features: { feature_votes: SPLIT_5_3_PARENT1 } };
    const votes = extractFeatureVotes(result);
    expect(votes.eyes).toBe('parent1');
  });

  it('fills missing features as unknown', () => {
    const result = { feature_votes: { eyes: 'parent1' } };
    const votes = extractFeatureVotes(result);
    expect(votes.eyes).toBe('parent1');
    expect(votes.eyebrows).toBe('unknown');
    expect(votes.ears).toBe('unknown');
    expect(Object.keys(votes)).toHaveLength(8);
  });

  it('returns all unknown for null input', () => {
    const votes = extractFeatureVotes(null);
    expect(Object.values(votes).every(v => v === 'unknown')).toBe(true);
    expect(Object.keys(votes)).toHaveLength(8);
  });

  it('normalizes parent_a/parent_b/mum/dad in votes', () => {
    const result = { feature_votes: { eyes: 'mum', eyebrows: 'dad', smile: 'parent_a', nose: 'parent_b', face_shape: 'parent1', skin: 'parent2', hair: 'unknown', ears: null } };
    const votes = extractFeatureVotes(result);
    expect(votes.eyes).toBe('parent1');
    expect(votes.eyebrows).toBe('parent2');
    expect(votes.smile).toBe('parent1');
    expect(votes.nose).toBe('parent2');
    expect(votes.face_shape).toBe('parent1');
    expect(votes.skin).toBe('parent2');
    expect(votes.hair).toBe('unknown');
    expect(votes.ears).toBe('unknown');
  });
});

// ─── countFeatures ──────────────────────────────────────────────

describe('resultsContract.countFeatures', () => {
  it('counts 5-3 split correctly', () => {
    const counts = countFeatures(SPLIT_5_3_PARENT1);
    expect(counts).toEqual({ parent1Count: 5, parent2Count: 3, unknownCount: 0, invariantHolds: true });
  });

  it('counts with unknowns', () => {
    const counts = countFeatures(SPLIT_4_2_2UNKNOWN);
    expect(counts).toEqual({ parent1Count: 4, parent2Count: 2, unknownCount: 2, invariantHolds: true });
  });

  it('returns all unknown for null input', () => {
    const counts = countFeatures(null);
    expect(counts).toEqual({ parent1Count: 0, parent2Count: 0, unknownCount: 8, invariantHolds: true });
  });

  it('counts 4-4 tie correctly', () => {
    const counts = countFeatures(SPLIT_4_4_TIED);
    expect(counts).toEqual({ parent1Count: 4, parent2Count: 4, unknownCount: 0, invariantHolds: true });
  });
});

// ─── getPercentages ─────────────────────────────────────────────

describe('resultsContract.getPercentages', () => {
  it('calculates from backend scores', () => {
    const result = { parent_scores: { parent1: 0.62, parent2: 0.38 } };
    const pct = getPercentages(result, 'parent1');
    expect(pct.parent1Pct).toBe(62);
    expect(pct.parent2Pct).toBe(38);
    expect(pct.nudged).toBe(false);
    expect(pct.parent1Pct + pct.parent2Pct).toBe(100);
  });

  it('falls back to feature counts when no parent_scores', () => {
    const result = { feature_votes: { ...SPLIT_5_3_PARENT1 } }; // 5 parent1, 3 parent2
    const pct = getPercentages(result, 'parent1');
    // 5/8 = 0.625 → round = 63, other = 37
    expect(pct.parent1Pct).toBe(63);
    expect(pct.parent2Pct).toBe(37);
    expect(pct.parent1Pct + pct.parent2Pct).toBe(100);
  });

  // THE BUG FIX: rounding consistency
  // MobileResultsSection didn't round, useKeepsakeData did — different numbers
  // Contract always rounds. This test locks the canonical behavior.
  it('always returns integers that sum to 100 (rounding bug fix)', () => {
    const result = { parent_scores: { parent1: 0.625, parent2: 0.375 } };
    const pct = getPercentages(result, 'parent1');
    expect(Number.isInteger(pct.parent1Pct)).toBe(true);
    expect(Number.isInteger(pct.parent2Pct)).toBe(true);
    expect(pct.parent1Pct + pct.parent2Pct).toBe(100);
    expect(pct.parent1Pct).toBe(63); // round(0.625/1.0 * 100) = 63
    expect(pct.parent2Pct).toBe(37); // 100 - 63 = 37
  });

  it('applies 50/50 nudge for equal scores', () => {
    const result = { parent_scores: { parent1: 0.5, parent2: 0.5 } };
    const pct = getPercentages(result, 'parent1');
    expect(pct.parent1Pct).toBe(51);
    expect(pct.parent2Pct).toBe(49);
    expect(pct.nudged).toBe(true);
  });

  it('returns nudged 50/50 for null input', () => {
    const pct = getPercentages(null, null);
    expect(pct.parent1Pct + pct.parent2Pct).toBe(100);
    expect(pct.nudged).toBe(true);
  });
});

// ─── apply5050Rule ──────────────────────────────────────────────

describe('resultsContract.apply5050Rule', () => {
  it('nudges 50/50 to 51/49 for parent1 winner', () => {
    const result = apply5050Rule(50, 50, 'parent1');
    expect(result).toEqual({ parent1Pct: 51, parent2Pct: 49, nudged: true });
  });

  it('nudges 50/50 to 49/51 for parent2 winner', () => {
    const result = apply5050Rule(50, 50, 'parent2');
    expect(result).toEqual({ parent1Pct: 49, parent2Pct: 51, nudged: true });
  });

  it('flips percentages when winner disagrees with scores', () => {
    // parent1 is winner but parent2 has 55%
    const result = apply5050Rule(45, 55, 'parent1');
    expect(result.parent1Pct).toBeGreaterThanOrEqual(51);
    expect(result.parent2Pct).toBeLessThanOrEqual(49);
    expect(result.nudged).toBe(true);
    expect(result.parent1Pct + result.parent2Pct).toBe(100);
  });

  it('does NOT nudge when gap >= 2 and winner matches', () => {
    const result = apply5050Rule(60, 40, 'parent1');
    expect(result).toEqual({ parent1Pct: 60, parent2Pct: 40, nudged: false });
  });

  it('nudges 49/51 gap (< 2) to match winner', () => {
    const result = apply5050Rule(49, 51, 'parent1');
    expect(result).toEqual({ parent1Pct: 51, parent2Pct: 49, nudged: true });
  });

  it('uses parent1 as tiebreak when winner is null', () => {
    const result = apply5050Rule(50, 50, null);
    expect(result).toEqual({ parent1Pct: 51, parent2Pct: 49, nudged: true });
  });
});

// ─── buildResultsSummary ────────────────────────────────────────

describe('resultsContract.buildResultsSummary', () => {
  it('builds complete summary for normal result', () => {
    const childResult = {
      inheritance: { winner: 'parent1', winner_reason: '5 of 8 features match' },
      feature_votes: SPLIT_5_3_PARENT1,
      parent_scores: { parent1: 0.65, parent2: 0.35 },
    };
    const summary = buildResultsSummary(childResult);

    expect(summary.winner).toBe('parent1');
    expect(summary.winnerReason).toBe('5 of 8 features match');
    expect(summary.percentages.parent1Pct).toBe(65);
    expect(summary.percentages.parent2Pct).toBe(35);
    expect(summary.percentages.parent1Pct + summary.percentages.parent2Pct).toBe(100);
    expect(summary.featureCounts.parent1Count).toBe(5);
    expect(summary.featureCounts.parent2Count).toBe(3);
    expect(summary.featureCounts.invariantHolds).toBe(true);
    expect(summary.winnerPct).toBe(65);
    expect(summary.loserPct).toBe(35);
    expect(Object.keys(summary.featureVotes)).toHaveLength(8);
  });

  it('returns null for null input', () => {
    expect(buildResultsSummary(null)).toBeNull();
    expect(buildResultsSummary(undefined)).toBeNull();
  });

  it('handles parent2 winner correctly', () => {
    const childResult = {
      winner: 'parent2',
      feature_votes: FULL_PARENT2_VOTES,
      parent_scores: { parent1: 0.3, parent2: 0.7 },
    };
    const summary = buildResultsSummary(childResult);
    expect(summary.winner).toBe('parent2');
    expect(summary.winnerPct).toBe(70);
    expect(summary.loserPct).toBe(30);
  });

  it('handles all features tied with backend winner', () => {
    const childResult = {
      inheritance: { winner: 'parent1' },
      feature_votes: SPLIT_4_4_TIED,
      parent_scores: { parent1: 0.5, parent2: 0.5 },
    };
    const summary = buildResultsSummary(childResult);
    expect(summary.winner).toBe('parent1');
    expect(summary.percentages.nudged).toBe(true);
    expect(summary.percentages.parent1Pct).toBe(51);
    expect(summary.percentages.parent2Pct).toBe(49);
  });
});

// ─── validateResults ────────────────────────────────────────────

describe('resultsContract.validateResults', () => {
  it('validates a correct full result', () => {
    const result = {
      inheritance: { winner: 'parent1' },
      feature_votes: SPLIT_5_3_PARENT1,
      parent_scores: { parent1: 0.65, parent2: 0.35 },
    };
    const { valid, errors } = validateResults(result);
    expect(valid).toBe(true);
    expect(errors).toHaveLength(0);
  });

  it('flags missing features', () => {
    const result = {
      feature_votes: { eyes: 'parent1', nose: 'parent2', smile: 'parent1', hair: 'parent2', ears: 'parent1' },
    };
    const { valid, errors } = validateResults(result);
    expect(valid).toBe(false);
    expect(errors.some(e => e.includes('Expected 8 features'))).toBe(true);
  });

  it('flags winner contradicting feature majority', () => {
    const result = {
      winner: 'parent1',
      feature_votes: FULL_PARENT2_VOTES, // all 8 are parent2 but winner says parent1
    };
    const { valid, errors } = validateResults(result);
    expect(valid).toBe(false);
    expect(errors.some(e => e.includes('fewer features'))).toBe(true);
  });

  it('flags null input', () => {
    const { valid, errors } = validateResults(null);
    expect(valid).toBe(false);
    expect(errors).toHaveLength(1);
  });

  it('flags out-of-range parent_scores', () => {
    const result = {
      feature_votes: SPLIT_5_3_PARENT1,
      parent_scores: { parent1: 1.5, parent2: -0.2 },
    };
    const { valid, errors } = validateResults(result);
    expect(valid).toBe(false);
    expect(errors.some(e => e.includes('out of range'))).toBe(true);
  });
});

// ─── Constants & default export ─────────────────────────────────

describe('resultsContract — constants and exports', () => {
  it('CANONICAL_FEATURES has exactly 8 entries', () => {
    expect(CANONICAL_FEATURES).toHaveLength(8);
  });

  it('CANONICAL_FEATURES is frozen', () => {
    expect(Object.isFrozen(CANONICAL_FEATURES)).toBe(true);
  });

  it('FEATURE_LABELS has label for every canonical feature', () => {
    for (const f of CANONICAL_FEATURES) {
      expect(FEATURE_LABELS[f]).toBeDefined();
      expect(typeof FEATURE_LABELS[f]).toBe('string');
    }
  });

  it('default export is frozen and contains all functions', () => {
    expect(Object.isFrozen(resultsContract)).toBe(true);
    expect(typeof resultsContract.getWinner).toBe('function');
    expect(typeof resultsContract.extractFeatureVotes).toBe('function');
    expect(typeof resultsContract.countFeatures).toBe('function');
    expect(typeof resultsContract.getPercentages).toBe('function');
    expect(typeof resultsContract.apply5050Rule).toBe('function');
    expect(typeof resultsContract.buildResultsSummary).toBe('function');
    expect(typeof resultsContract.validateResults).toBe('function');
  });

  it('MIN_PERCENTAGE_GAP is 2', () => {
    expect(MIN_PERCENTAGE_GAP).toBe(2);
  });

  it('NUDGE values are 51/49', () => {
    expect(NUDGE_WINNER_PCT).toBe(51);
    expect(NUDGE_LOSER_PCT).toBe(49);
  });
});
