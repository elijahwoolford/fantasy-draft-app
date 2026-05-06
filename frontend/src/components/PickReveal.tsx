import { useEffect, useState } from "react";

const REVEAL_MS = 3000;

/** Final draft board (no timers). Top = #1 pick through #4 at bottom. */
export function PickListStatic({ draftOrder }: { draftOrder: string[] }) {
  return (
    <div className="pick-list">
      {draftOrder.map((team, i) => {
        const pickNum = i + 1;
        return (
          <div className="pick-container" key={`${pickNum}-${team}`}>
            <div className="pick-bubble">
              <span className="pick-bubble__meta">
                <span className="pick-bubble__num">#{pickNum}</span>
                <span className="pick-bubble__word">Pick</span>
              </span>
              <span className="pick-bubble__name">{team}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

type Props = {
  /** API order: index 0 = #1 overall pick */
  draftOrder: string[];
  onComplete: () => void;
};

export function PickReveal({ draftOrder, onComplete }: Props) {
  const [shown, setShown] = useState<number>(0);
  const n = draftOrder.length;

  useEffect(() => {
    if (shown >= n) {
      onComplete();
      return;
    }
    const t = window.setTimeout(() => setShown((s) => s + 1), REVEAL_MS);
    return () => window.clearTimeout(t);
  }, [shown, n, onComplete]);

  /** Reveal order: #4 first, …, #1 last. DOM order [4,3,2,1] + column-reverse → visual #1 top … #4 bottom. */
  const bubbles: { pickNum: number; team: string }[] = [];
  for (let k = 0; k < shown; k++) {
    const pickIndex = n - 1 - k;
    bubbles.push({
      pickNum: pickIndex + 1,
      team: draftOrder[pickIndex],
    });
  }

  return (
    <div className="pick-list pick-list--reveal-stack">
      {bubbles.map(({ pickNum, team }) => (
        <div className="pick-container" key={`${pickNum}-${team}`}>
          <div className="pick-bubble">
            <span className="pick-bubble__meta">
              <span className="pick-bubble__num">#{pickNum}</span>
              <span className="pick-bubble__word">Pick</span>
            </span>
            <span className="pick-bubble__name">{team}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
