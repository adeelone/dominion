import { ChevronRight, Crown, Globe2, Hammer, Landmark, ScrollText, ShieldAlert, Sparkles } from 'lucide-react';
import { useState } from 'react';
import { useDominion } from './store';

const modes = ['Overview', 'Throne', 'Providence', 'World Forge', 'Community'] as const;

function Header() {
  const mode = useDominion((state) => state.mode);
  const setMode = useDominion((state) => state.setMode);
  const balance = useDominion((state) => state.balance);
  return (
    <header className="topbar">
      <div className="brand"><Crown size={22} /> Dominion</div>
      <nav aria-label="Mode switcher">
        {modes.map((item) => (
          <button key={item} className={item === mode ? 'active' : ''} onClick={() => setMode(item)}>{item}</button>
        ))}
      </nav>
      <div className="credits">{balance} credits</div>
    </header>
  );
}

function MapView() {
  const selected = useDominion((state) => state.selectedSettlementId);
  const select = useDominion((state) => state.selectSettlement);
  const settlements = useDominion((state) => state.settlements);
  return (
    <section className="mapPane" aria-label="World map">
      <div className="mapToolbar">
        <button><Globe2 size={16} /> Globe</button>
        <button className="active"><Landmark size={16} /> Polities</button>
        <button><ShieldAlert size={16} /> Pressure</button>
      </div>
      <svg viewBox="0 0 100 100" role="img" aria-label="Vector map of Crown Basin regions">
        <path className="region basin" d="M5 8 L45 10 L38 45 L16 40 Z" />
        <path className="region march" d="M48 8 L92 16 L72 62 L39 46 Z" />
        <path className="region coast" d="M8 48 L55 58 L32 92 L5 80 Z" />
        {settlements.map((item, index) => {
          const positions = [[26, 26], [65, 34], [27, 70]][index];
          return (
            <g key={item.id} className={selected === item.id ? 'settlement selected' : 'settlement'} onClick={() => select(item.id)} tabIndex={0}>
              <circle cx={positions[0]} cy={positions[1]} r="3.6" />
              <text x={positions[0] + 5} y={positions[1] + 1}>{item.name}</text>
            </g>
          );
        })}
      </svg>
      <div className="diffStrip">
        <span>What changed</span>
        <strong>Food, morale, armies, and omen effects update from the chronicle projection.</strong>
      </div>
    </section>
  );
}

function CommandPanel() {
  const [decree, setDecree] = useState('Raise a river guard and repair the east levee.');
  const [act, setAct] = useState('Summon a dragon in the Ashen March.');
  const issueDecree = useDominion((state) => state.issueDecree);
  const castAct = useDominion((state) => state.castAct);
  const bless = useDominion((state) => state.bless);
  const disaster = useDominion((state) => state.disaster);
  const selected = useDominion((state) => state.settlements.find((item) => item.id === state.selectedSettlementId)!);
  return (
    <aside className="commandPane">
      <section className="toolBlock">
        <h2><Crown size={18} /> Throne Decrees</h2>
        <textarea value={decree} onChange={(event) => setDecree(event.target.value)} aria-label="Throne decree" />
        <button className="primary" onClick={() => issueDecree(decree)}>Confirm decree <ChevronRight size={16} /></button>
      </section>
      <section className="toolBlock">
        <h2><Sparkles size={18} /> Providence Acts</h2>
        <div className="target">Watching {selected.name}</div>
        <textarea value={act} onChange={(event) => setAct(event.target.value)} aria-label="Free-form divine act" />
        <div className="buttonRow">
          <button onClick={bless}>Bless</button>
          <button onClick={disaster}>Drought</button>
        </div>
        <button className="primary" onClick={() => castAct(act)}>Materialize act <ChevronRight size={16} /></button>
      </section>
    </aside>
  );
}

function SettlementPanel() {
  const settlements = useDominion((state) => state.settlements);
  const selected = useDominion((state) => state.selectedSettlementId);
  const select = useDominion((state) => state.selectSettlement);
  return (
    <section className="settlementPanel">
      <h2><Hammer size={18} /> Settlements</h2>
      {settlements.map((item) => (
        <button key={item.id} className={selected === item.id ? 'settlementRow selected' : 'settlementRow'} onClick={() => select(item.id)}>
          <span>{item.name}<small>{item.region}</small></span>
          <span>{item.population} pop</span>
          <meter min="0" max="100" value={item.happiness} />
          <span>{item.food} food</span>
        </button>
      ))}
    </section>
  );
}

function OmenLog() {
  const omenTrail = useDominion((state) => state.omenTrail);
  return (
    <section className="omenLog">
      <h2><Sparkles size={18} /> Omen Log</h2>
      {(omenTrail.length ? omenTrail : [{ parsed: 'No divine act yet', plausibility: 'waiting', materialized: 'none', consequence: 'none' }]).map((item, index) => (
        <div className="omen" key={`${item.parsed}-${index}`}>
          <span>Parsed intent</span><p>{item.parsed}</p>
          <span>Plausibility</span><p>{item.plausibility}</p>
          <span>Materialized effect</span><p>{item.materialized}</p>
          <span>First consequence</span><p>{item.consequence}</p>
        </div>
      ))}
    </section>
  );
}

function Chronicle() {
  const chronicle = useDominion((state) => state.chronicle);
  return (
    <section className="chronicle">
      <h2><ScrollText size={18} /> Chronicle</h2>
      {chronicle.map((entry) => (
        <article key={entry.id}>
          <span>Day {entry.tick} / {entry.kind}</span>
          <p>{entry.text}</p>
        </article>
      ))}
    </section>
  );
}

export function App() {
  return (
    <div className="appShell">
      <Header />
      <main>
        <MapView />
        <CommandPanel />
        <SettlementPanel />
        <OmenLog />
        <Chronicle />
      </main>
    </div>
  );
}
