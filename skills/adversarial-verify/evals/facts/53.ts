// Eval 53: which mutants of isWeekend the two tests kill.
type F = (day: number) => boolean;
const original: F = (day) => day === 0 || day === 6;
const tests: Array<[number, boolean]> = [
  [new Date(Date.UTC(2026, 9, 24)).getUTCDay(), true],  // Saturday 24 October 2026
  [new Date(Date.UTC(2026, 9, 21)).getUTCDay(), false], // Wednesday 21 October 2026
];
if (tests[0][0] !== 6 || tests[1][0] !== 3) throw new Error("dates");
const mutants: Record<string, F> = {
  "day === 0 -> false": (day) => false || day === 6,
  "day === 6 -> false": (day) => day === 0 || false,
  "|| -> &&": (day) => day === 0 && day === 6,
  "0 -> 1": (day) => day === 1 || day === 6,
};
const killed = (f: F) => tests.some(([d, want]) => f(d) !== want);
if (!tests.every(([d, want]) => original(d) === want)) throw new Error("original fails");
const survivors = Object.keys(mutants).filter((n) => !killed(mutants[n])).sort();
const expected = ["0 -> 1", "day === 0 -> false"];
if (JSON.stringify(survivors) !== JSON.stringify(expected)) throw new Error(JSON.stringify(survivors));
// A Sunday test kills both survivors.
const sunday = new Date(Date.UTC(2026, 9, 25)).getUTCDay();
if (sunday !== 0 || !survivors.every((n) => mutants[n](sunday) !== true)) throw new Error("sunday");
console.log("ok 53");
