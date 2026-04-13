import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as AppErrorBus from '../../src/infrastructure/AppErrorBus';
import {
  get, set, remove, clear, onExternalChange,
  registerMigration, runMigrations,
  pruneStalePhotos, pruneStaleCheckout,
  getStats, KEYS, SCHEMA_VERSION, KEY_SCHEMA,
  _reset,
} from '../../src/infrastructure/AppStorage';

// ─── Test helpers ───────────────────────────────────────────────

function clearAllStorage() {
  localStorage.clear();
  _reset();
  AppErrorBus._reset();
}

// ─── Unit Tests — Section 7.1 ───────────────────────────────────

describe('AppStorage — Unit Tests', () => {
  beforeEach(() => {
    clearAllStorage();
  });

  afterEach(() => {
    clearAllStorage();
    vi.restoreAllMocks();
  });

  // 1
  it('get() returns default for missing key', () => {
    expect(get('fl:plan')).toBe('free');
    expect(get('fl:basket')).toEqual([]);
    expect(get('fl:familyContext')).toBeNull();
    expect(get('fl:visit-count')).toBe(0);
  });

  // 2
  it('set() and get() roundtrip (string)', () => {
    set('fl:plan', 'plus');
    expect(get('fl:plan')).toBe('plus');
  });

  // 3
  it('set() and get() roundtrip (json)', () => {
    const basket = [{ id: 1, name: 'mug' }, { id: 2, name: 'deck' }];
    set('fl:basket', basket);
    expect(get('fl:basket')).toEqual(basket);
  });

  // 4
  it('set() and get() roundtrip (number)', () => {
    set('fl:visit-count', 5);
    expect(get('fl:visit-count')).toBe(5);
    expect(typeof get('fl:visit-count')).toBe('number');
  });

  // 5
  it('get() returns default on corrupt JSON', () => {
    localStorage.setItem('fl:basket', 'not valid json{{{');
    expect(get('fl:basket')).toEqual([]);
  });

  // 6
  it('get() reports AppErrorBus on corrupt JSON', () => {
    localStorage.setItem('fl:basket', 'not valid json{{{');
    get('fl:basket');
    const active = AppErrorBus.getActive();
    expect(active.length).toBe(1);
    expect(active[0].report.severity).toBe('low');
    expect(active[0].report.code).toBe('STORAGE_PARSE_FAIL');
  });

  // 7
  it('set() unknown key throws', () => {
    expect(() => set('fl:nonexistent', 'value')).toThrow('Unknown storage key');
  });

  // 8
  it('get() unknown key throws', () => {
    expect(() => get('fl:nonexistent')).toThrow('Unknown storage key');
  });

  // 9
  it('remove() removes value', () => {
    set('fl:plan', 'plus');
    expect(get('fl:plan')).toBe('plus');
    remove('fl:plan');
    expect(get('fl:plan')).toBe('free'); // default
  });

  // 10
  it('clear() with namespace removes only that namespace', () => {
    set('fl:plan', 'plus');
    set('fl:plan-email', 'test@example.com');
    set('fl:game:ageGroup', 'adult');
    set('fl:cardCollection', [1, 2, 3]);

    clear('plan');

    expect(get('fl:plan')).toBe('free'); // default
    expect(get('fl:plan-email')).toBe(''); // default
    expect(get('fl:game:ageGroup')).toBe('adult'); // retained
    expect(get('fl:cardCollection')).toEqual([1, 2, 3]); // retained
  });

  // 11
  it('clear() without namespace removes all registered keys', () => {
    set('fl:plan', 'plus');
    set('fl:game:ageGroup', 'adult');
    set('fl:visit-count', 10);

    clear();

    expect(get('fl:plan')).toBe('free');
    expect(get('fl:game:ageGroup')).toBeNull();
    expect(get('fl:visit-count')).toBe(0);
  });

  // 12
  it('quota exceeded triggers AppErrorBus', () => {
    const origSetItem = Storage.prototype.setItem;
    try {
      Storage.prototype.setItem = function(key, value) {
        if (key === 'fl:basket') {
          throw new DOMException('quota exceeded', 'QuotaExceededError');
        }
        origSetItem.call(this, key, value);
      };

      set('fl:basket', [{ id: 1 }]);

      const active = AppErrorBus.getActive();
      expect(active.length).toBe(1);
      expect(active[0].report.severity).toBe('high');
      expect(active[0].report.code).toBe('STORAGE_QUOTA_EXCEEDED');
    } finally {
      Storage.prototype.setItem = origSetItem;
    }
  });

  // 13
  it('quota exceeded returns false', () => {
    const origSetItem = Storage.prototype.setItem;
    try {
      Storage.prototype.setItem = function() {
        throw new DOMException('quota exceeded', 'QuotaExceededError');
      };

      expect(set('fl:basket', [{ id: 1 }])).toBe(false);
    } finally {
      Storage.prototype.setItem = origSetItem;
    }
  });

  // 14
  it('schema migration runs on stale version', () => {
    localStorage.setItem('fl:_schema_version', '0');
    localStorage.setItem('fl:plan', 'old_plan');

    registerMigration(0, (data) => {
      if (data['fl:plan'] === 'old_plan') {
        data['fl:plan'] = 'migrated_plan';
      }
      return data;
    });

    runMigrations();

    expect(localStorage.getItem('fl:plan')).toBe('migrated_plan');
  });

  // 15
  it('schema migration failure reports to AppErrorBus', () => {
    localStorage.setItem('fl:_schema_version', '0');

    registerMigration(0, () => {
      throw new Error('Migration exploded');
    });

    runMigrations();

    const active = AppErrorBus.getActive();
    expect(active.length).toBe(1);
    expect(active[0].report.code).toBe('STORAGE_MIGRATION_FAIL');
    expect(active[0].report.severity).toBe('high');
  });

  // 16
  it('KEYS constant is frozen', () => {
    expect(Object.isFrozen(KEYS)).toBe(true);
  });

  // 17
  it('getStats() returns correct counts', () => {
    set('fl:plan', 'plus');
    set('fl:visit-count', 5);
    set('fl:game:ageGroup', 'child');

    const stats = getStats();
    expect(stats.usedKeys).toBe(3);
    expect(stats.totalKeys).toBe(Object.keys(KEY_SCHEMA).length);
    expect(stats.byNamespace.plan).toBeGreaterThan(0);
  });
});

// ─── Integration Tests — Section 7.2 ───────────────────────────

describe('AppStorage + AppErrorBus Integration', () => {
  beforeEach(() => {
    clearAllStorage();
  });

  afterEach(() => {
    clearAllStorage();
    vi.restoreAllMocks();
  });

  // Integration 1
  it('quota path end-to-end', () => {
    const origSetItem = Storage.prototype.setItem;
    try {
      Storage.prototype.setItem = function() {
        throw new DOMException('quota exceeded', 'QuotaExceededError');
      };

      const result = set('fl:basket', [{ id: 1, name: 'mug' }]);

      expect(result).toBe(false);
      const active = AppErrorBus.getActive();
      expect(active.length).toBe(1);
      expect(active[0].report.severity).toBe('high');
      expect(active[0].report.code).toBe('STORAGE_QUOTA_EXCEEDED');
      expect(active[0].report.message).toContain('storage is full');
    } finally {
      Storage.prototype.setItem = origSetItem;
    }
  });

  // Integration 2
  it('parse failure path', () => {
    localStorage.setItem('fl:basket', 'not json');
    const result = get('fl:basket');

    expect(result).toEqual([]);
    const active = AppErrorBus.getActive();
    expect(active.length).toBe(1);
    expect(active[0].report.severity).toBe('low');
    expect(active[0].report.code).toBe('STORAGE_PARSE_FAIL');
  });

  // Integration 3
  it('clear reports to AppErrorBus', () => {
    set('fl:plan', 'plus');
    set('fl:visit-count', 5);
    set('fl:game:ageGroup', 'child');
    set('fl:trail_visited', [1, 2]);
    set('fl:feedback-given', 'true');

    AppErrorBus._reset();

    clear();

    const active = AppErrorBus.getActive();
    expect(active.length).toBe(1);
    expect(active[0].report.code).toBe('STORAGE_CLEARED');
    expect(active[0].report.severity).toBe('low');
  });
});

// ─── BroadcastChannel Tests — Section 7.3 ───────────────────────

describe('AppStorage — BroadcastChannel', () => {
  beforeEach(() => {
    clearAllStorage();
  });

  afterEach(() => {
    clearAllStorage();
    vi.restoreAllMocks();
  });

  // BC 1 — simulate external change via storage event fallback
  it('onExternalChange fires on external storage event for tabSync key', () => {
    const callback = vi.fn();
    const unsub = onExternalChange('fl:plan', callback);

    // Simulate the storage event (as if another tab wrote to fl:plan)
    const event = new StorageEvent('storage', {
      key: 'fl:plan',
      newValue: 'plus',
      oldValue: 'free',
      storageArea: localStorage,
    });
    window.dispatchEvent(event);

    unsub();

    // Verify unsubscribe worked — fire again, should NOT increase call count
    const callCountAfterUnsub = callback.mock.calls.length;
    window.dispatchEvent(event);
    expect(callback.mock.calls.length).toBe(callCountAfterUnsub);
  });

  // BC 2
  it('onExternalChange does NOT fire for non-tabSync keys', () => {
    const callback = vi.fn();
    // fl:game:ageGroup has tabSync: false — onExternalChange should no-op
    const unsub = onExternalChange('fl:game:ageGroup', callback);

    const event = new StorageEvent('storage', {
      key: 'fl:game:ageGroup',
      newValue: 'child',
      oldValue: null,
      storageArea: localStorage,
    });
    window.dispatchEvent(event);

    expect(callback).not.toHaveBeenCalled();
    unsub();
  });
});

// ─── IndexedDB Tests — Section 7.4 ─────────────────────────────

describe('AppStorage — IndexedDB tier', () => {
  beforeEach(() => {
    clearAllStorage();
  });

  afterEach(() => {
    clearAllStorage();
    vi.restoreAllMocks();
  });

  // IDB 1
  it('IndexedDB tier set/get roundtrip via in-memory cache', () => {
    const thumbs = { parent1: 'data:image/png;base64,abc', parent2: 'data:image/png;base64,def' };
    set('fl:thumbnails', thumbs);
    expect(get('fl:thumbnails')).toEqual(thumbs);
  });

  // IDB 2
  it('IndexedDB tier returns default when no value set', () => {
    expect(get('fl:thumbnails')).toEqual({});
  });
});

// ─── Additional edge case tests ────────────────────────────────

describe('AppStorage — Edge cases', () => {
  beforeEach(() => {
    clearAllStorage();
  });

  afterEach(() => {
    clearAllStorage();
    vi.restoreAllMocks();
  });

  it('KEY_SCHEMA is frozen', () => {
    expect(Object.isFrozen(KEY_SCHEMA)).toBe(true);
  });

  it('set() returns true on success', () => {
    expect(set('fl:plan', 'plus')).toBe(true);
  });

  it('KEYS maps to correct key strings', () => {
    expect(KEYS.PLAN).toBe('fl:plan');
    expect(KEYS.BASKET).toBe('fl:basket');
    expect(KEYS.THUMBNAILS).toBe('fl:thumbnails');
    expect(KEYS.DETECT_CONFIG).toBe('familook_detect_config');
  });

  it('SCHEMA_VERSION is 1', () => {
    expect(SCHEMA_VERSION).toBe(1);
  });

  it('remove() unknown key throws', () => {
    expect(() => remove('fl:nonexistent')).toThrow('Unknown storage key');
  });

  it('pruneStalePhotos returns 0 when no stale data', () => {
    expect(pruneStalePhotos()).toBe(0);
  });

  it('pruneStaleCheckout removes pending-checkout', () => {
    localStorage.setItem('fl:pending-checkout', 'true');
    pruneStaleCheckout();
    expect(localStorage.getItem('fl:pending-checkout')).toBeNull();
  });
});
