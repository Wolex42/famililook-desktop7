import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  report,
  getActive,
  getAll,
  dismiss,
  clear,
  subscribe,
  getStats,
  _reset,
} from "../../src/infrastructure/AppErrorBus";

// ── Setup ────────────────────────────────────────────────────────

beforeEach(() => {
  _reset();
  vi.restoreAllMocks();
});

// ── Helpers ──────────────────────────────────────────────────────

function makeReport(overrides = {}) {
  return {
    message: "Test error",
    context: "TestModule.testFn",
    severity: "medium",
    ...overrides,
  };
}

// ── Tests ────────────────────────────────────────────────────────

describe("AppErrorBus", () => {
  // 1. report() stores error
  it("report() stores error with correct fields", () => {
    const r = makeReport({ message: "Something broke", severity: "high" });
    const id = report(r);

    const active = getActive();
    expect(active).toHaveLength(1);
    expect(active[0].id).toBe(id);
    expect(active[0].report.message).toBe("Something broke");
    expect(active[0].report.severity).toBe("high");
    expect(active[0].report.context).toBe("TestModule.testFn");
    expect(active[0].dismissed).toBe(false);
    expect(active[0].timestamp).toBeGreaterThan(0);
    expect(active[0].count).toBe(1);
  });

  // 2. report() assigns unique ID
  it("report() assigns unique IDs to sequential reports", () => {
    const id1 = report(makeReport({ message: "Error A" }));
    const id2 = report(makeReport({ message: "Error B" }));

    expect(id1).not.toBe(id2);
    expect(typeof id1).toBe("string");
    expect(typeof id2).toBe("string");
  });

  // 3. report() notifies subscribers
  it("report() notifies subscribers with active errors", () => {
    const callback = vi.fn();
    subscribe(callback);

    report(makeReport());

    expect(callback).toHaveBeenCalledTimes(1);
    const receivedErrors = callback.mock.calls[0][0];
    expect(receivedErrors).toHaveLength(1);
    expect(receivedErrors[0].report.message).toBe("Test error");
  });

  // 4. Deduplication within 5s window
  it("deduplicates identical errors within 5s window", () => {
    report(makeReport({ message: "Dup", context: "Ctx", code: "DUP_CODE" }));
    report(makeReport({ message: "Dup", context: "Ctx", code: "DUP_CODE" }));

    const active = getActive();
    expect(active).toHaveLength(1);
    expect(active[0].count).toBe(2);
  });

  // 5. Deduplication expiry after 5s
  it("does not deduplicate after 5s window expires", () => {
    vi.useFakeTimers();

    report(makeReport({ message: "Dup", context: "Ctx" }));
    vi.advanceTimersByTime(5001);
    report(makeReport({ message: "Dup", context: "Ctx" }));

    const active = getActive();
    expect(active).toHaveLength(2);

    vi.useRealTimers();
  });

  // 6. dismiss() marks dismissed
  it("dismiss() marks error as dismissed", () => {
    const id = report(makeReport());

    dismiss(id);

    expect(getActive()).toHaveLength(0);
    const all = getAll();
    expect(all).toHaveLength(1);
    expect(all[0].dismissed).toBe(true);
  });

  // 7. clear() dismisses all
  it("clear() dismisses all errors", () => {
    report(makeReport({ message: "A" }));
    report(makeReport({ message: "B" }));
    report(makeReport({ message: "C" }));

    expect(getActive()).toHaveLength(3);

    clear();

    expect(getActive()).toHaveLength(0);
    expect(getAll()).toHaveLength(3); // still in history
  });

  // 8. MAX_ACTIVE cap (20)
  it("caps active errors at 20, pruning oldest", () => {
    for (let i = 0; i < 25; i++) {
      report(makeReport({ message: `Error ${i}` }));
    }

    const active = getActive();
    expect(active).toHaveLength(20);
    // Newest should be first (reversed)
    expect(active[0].report.message).toBe("Error 24");
  });

  // 9. MAX_HISTORY cap (50)
  it("caps history at 50 entries", () => {
    for (let i = 0; i < 55; i++) {
      report(makeReport({ message: `Error ${i}` }));
    }

    const all = getAll();
    expect(all).toHaveLength(50);
  });

  // 10. Unsubscribe works
  it("unsubscribe stops callback from firing", () => {
    const callback = vi.fn();
    const unsub = subscribe(callback);

    report(makeReport({ message: "Before unsub" }));
    expect(callback).toHaveBeenCalledTimes(1);

    unsub();
    report(makeReport({ message: "After unsub" }));
    expect(callback).toHaveBeenCalledTimes(1); // not called again
  });

  // 11. Multiple subscribers
  it("notifies multiple subscribers and handles partial unsubscribe", () => {
    const cb1 = vi.fn();
    const cb2 = vi.fn();

    const unsub1 = subscribe(cb1);
    subscribe(cb2);

    report(makeReport({ message: "First" }));
    expect(cb1).toHaveBeenCalledTimes(1);
    expect(cb2).toHaveBeenCalledTimes(1);

    unsub1();
    report(makeReport({ message: "Second" }));
    expect(cb1).toHaveBeenCalledTimes(1); // no longer called
    expect(cb2).toHaveBeenCalledTimes(2); // still called
  });

  // 12. getStats() counts
  it("getStats() returns correct counts by severity", () => {
    report(makeReport({ message: "A", severity: "low" }));
    report(makeReport({ message: "B", severity: "medium" }));
    report(makeReport({ message: "C", severity: "high" }));
    report(makeReport({ message: "D", severity: "high" }));
    report(makeReport({ message: "E", severity: "critical" }));

    const stats = getStats();
    expect(stats.total).toBe(5);
    expect(stats.active).toBe(5);
    expect(stats.bySeverity.low).toBe(1);
    expect(stats.bySeverity.medium).toBe(1);
    expect(stats.bySeverity.high).toBe(2);
    expect(stats.bySeverity.critical).toBe(1);
  });
});
