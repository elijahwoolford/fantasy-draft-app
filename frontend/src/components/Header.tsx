export function Header() {
  return (
    <>
      <header className="app-header">
        <img src="/sleeper.jpeg" alt="Sleeper" width={75} height={75} />
        <div className="app-header__titles">
          <h1 className="app-title">
            <span className="app-title__line app-title__line--primary">Fantasy Football</span>
            <span className="app-title__line app-title__line--accent">Draft Lottery</span>
          </h1>
        </div>
      </header>
      <div className="divider divider--glow" aria-hidden />
    </>
  );
}
