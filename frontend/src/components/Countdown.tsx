import { useEffect, useState } from "react";

const GOOD_LUCK_MS = 2000;
const COUNTDOWN_SEC = 10;

type Props = {
  onDone: () => void;
};

export function Countdown({ onDone }: Props) {
  const [phase, setPhase] = useState<"luck" | "numbers">("luck");
  const [remaining, setRemaining] = useState(COUNTDOWN_SEC);

  useEffect(() => {
    const t = window.setTimeout(() => setPhase("numbers"), GOOD_LUCK_MS);
    return () => window.clearTimeout(t);
  }, []);

  useEffect(() => {
    if (phase !== "numbers") return;
    if (remaining === 0) {
      onDone();
      return;
    }
    const t = window.setTimeout(() => setRemaining((r) => r - 1), 1000);
    return () => window.clearTimeout(t);
  }, [phase, remaining, onDone]);

  return (
    <div className="countdown-stage" aria-live="polite">
      <div className="countdown-backdrop">
        <img src="/sleeper.jpeg" alt="" aria-hidden />
      </div>
      {phase === "luck" ? (
        <div className="good-luck">Good Luck!</div>
      ) : remaining > 0 ? (
        <div className="countdown-text">{remaining}</div>
      ) : null}
    </div>
  );
}
