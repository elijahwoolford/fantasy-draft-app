import { useCallback, useState } from "react";
import { postDraft } from "./api";
import { fireDraftConfetti } from "./confettiBurst";
import { Countdown } from "./components/Countdown";
import { Header } from "./components/Header";
import { PickListStatic, PickReveal } from "./components/PickReveal";
import { TeamInputs } from "./components/TeamInputs";

type Phase = "idle" | "loading" | "countdown" | "revealing" | "complete";

const ODDS = [37, 28, 20, 15];

export default function App() {
  const [phase, setPhase] = useState<Phase>("idle");
  const [names, setNames] = useState<string[]>(["", "", "", ""]);
  const [error, setError] = useState<string | null>(null);
  const [draftOrder, setDraftOrder] = useState<string[] | null>(null);

  const handleNameChange = useCallback((index: number, value: string) => {
    setNames((prev: string[]) => {
      const next = [...prev];
      next[index] = value;
      return next;
    });
  }, []);

  const handleDraw = useCallback(async () => {
    setError(null);
    const trimmed = names.map((n: string) => n.trim());
    if (trimmed.some((n: string) => !n)) {
      setError("Please enter all four team names.");
      return;
    }
    if (new Set(trimmed).size !== 4) {
      setError("Team names must be unique.");
      return;
    }
    setPhase("loading");
    try {
      const data = await postDraft(trimmed);
      setDraftOrder(data.draftOrder);
      setPhase("countdown");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to draw lottery.");
      setPhase("idle");
    }
  }, [names]);

  const onCountdownDone = useCallback(() => {
    setPhase("revealing");
  }, []);

  const onRevealComplete = useCallback(() => {
    setPhase("complete");
    requestAnimationFrame(() => {
      fireDraftConfetti();
    });
  }, []);

  return (
    <>
      <img className="sleeper-watermark" src="/sleeper.jpeg" alt="" aria-hidden />
      <div className="app-shell">
        <Header />

        {phase === "idle" || phase === "loading" ? (
          <>
            <TeamInputs
              names={names}
              onChange={handleNameChange}
              onSubmit={handleDraw}
              disabled={phase === "loading"}
            />
            {phase === "loading" && <p className="loading-text">Drawing lottery…</p>}
            {error && <div className="error-banner">{error}</div>}
            <p style={{ marginTop: "1rem", opacity: 0.85, fontSize: "0.9rem" }}>
              Odds are fixed by slot: Team 1 = {ODDS[0]}%, Team 2 = {ODDS[1]}%, Team 3 = {ODDS[2]}%, Team 4 ={" "}
              {ODDS[3]}% (worst record first).
            </p>
          </>
        ) : null}

        {phase === "countdown" ? <Countdown onDone={onCountdownDone} /> : null}

        {phase === "revealing" && draftOrder ? (
          <PickReveal draftOrder={draftOrder} onComplete={onRevealComplete} />
        ) : null}

        {phase === "complete" && draftOrder ? <PickListStatic draftOrder={draftOrder} /> : null}
      </div>
    </>
  );
}
