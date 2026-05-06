const ODDS_LABELS = [37, 28, 20, 15] as const;

type Props = {
  names: string[];
  onChange: (index: number, value: string) => void;
  onSubmit: () => void;
  disabled: boolean;
};

export function TeamInputs({ names, onChange, onSubmit, disabled }: Props) {
  return (
    <div className="team-grid">
      {ODDS_LABELS.map((pct, i) => (
        <div className="team-row" key={i}>
          <label htmlFor={`team-${i}`}>
            Team {i + 1}
            <span className="odds-badge">{pct}%</span>
          </label>
          <input
            id={`team-${i}`}
            type="text"
            autoComplete="off"
            placeholder={`Team ${i + 1} name`}
            value={names[i] ?? ""}
            onChange={(e) => onChange(i, e.target.value)}
            disabled={disabled}
          />
        </div>
      ))}
      <button type="button" className="draw-btn" onClick={onSubmit} disabled={disabled}>
        Draw Lottery
      </button>
    </div>
  );
}
