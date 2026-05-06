import confetti from "canvas-confetti";

const colors = ["#5eead4", "#2dd4bf", "#fcd34d", "#e2e8f0", "#38bdf8"];

/** Celebration burst after the full draft order is revealed. */
export function fireDraftConfetti(): void {
  const base = { colors, ticks: 520, gravity: 1.05, scalar: 1.05 };

  confetti({
    ...base,
    particleCount: 130,
    spread: 88,
    startVelocity: 32,
    origin: { x: 0.5, y: 0.62 },
  });

  window.setTimeout(() => {
    confetti({
      ...base,
      particleCount: 55,
      angle: 60,
      spread: 52,
      origin: { x: 0.08, y: 0.68 },
      startVelocity: 38,
    });
    confetti({
      ...base,
      particleCount: 55,
      angle: 120,
      spread: 52,
      origin: { x: 0.92, y: 0.68 },
      startVelocity: 38,
    });
  }, 280);
}
