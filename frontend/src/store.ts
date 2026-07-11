import { create } from 'zustand';
import { ChronicleEntry, Settlement, chronicleSeed, settlements } from './data';

type Mode = 'Overview' | 'Throne' | 'Providence' | 'World Forge' | 'Community';

type OmenTrail = {
  parsed: string;
  plausibility: string;
  materialized: string;
  consequence: string;
};

type DominionState = {
  mode: Mode;
  selectedSettlementId: string;
  balance: number;
  settlements: Settlement[];
  chronicle: ChronicleEntry[];
  omenTrail: OmenTrail[];
  setMode: (mode: Mode) => void;
  selectSettlement: (id: string) => void;
  issueDecree: (text: string) => void;
  castAct: (text: string) => void;
  bless: () => void;
  disaster: () => void;
};

export const useDominion = create<DominionState>((set, get) => ({
  mode: 'Overview',
  selectedSettlementId: 's1',
  balance: 128,
  settlements,
  chronicle: chronicleSeed,
  omenTrail: [],
  setMode: (mode) => set({ mode }),
  selectSettlement: (id) => set({ selectedSettlementId: id }),
  issueDecree: (text) =>
    set((state) => ({
      balance: state.balance - 2,
      chronicle: [
        { id: crypto.randomUUID(), tick: state.chronicle.length + 1, kind: 'decree', actor: 'House Veyr', text },
        ...state.chronicle,
      ],
    })),
  castAct: (text) => {
    const settlement = get().settlements.find((item) => item.id === get().selectedSettlementId)!;
    const dragon = text.toLowerCase().includes('dragon');
    set((state) => ({
      balance: state.balance - 3,
      settlements: state.settlements.map((item) =>
        item.id === settlement.id
          ? { ...item, happiness: Math.max(0, item.happiness - (dragon ? 8 : -3)), food: Math.max(0, item.food - (dragon ? 10 : -8)) }
          : item,
      ),
      omenTrail: [
        {
          parsed: dragon ? 'Summon a dangerous winged predator' : 'Reveal a grounded divine intervention',
          plausibility: dragon ? 'grounded supernatural' : 'minor grounded nudge',
          materialized: dragon ? 'Entity: dragon, territorial predator, 90 day lifespan' : 'State change applied to settlement',
          consequence: dragon ? `${settlement.name} loses food and morale this tick` : `${settlement.name} gains resilience`,
        },
        ...state.omenTrail,
      ],
      chronicle: [
        { id: crypto.randomUUID(), tick: state.chronicle.length + 1, kind: 'divine_act', actor: 'providence', text },
        ...state.chronicle,
      ],
    }));
  },
  bless: () =>
    set((state) => ({
      balance: state.balance - 1,
      settlements: state.settlements.map((item) =>
        item.id === state.selectedSettlementId ? { ...item, food: item.food + 8, happiness: Math.min(100, item.happiness + 4) } : item,
      ),
      chronicle: [
        { id: crypto.randomUUID(), tick: state.chronicle.length + 1, kind: 'blessing', actor: 'providence', text: 'Fertile rain settles over the fields.' },
        ...state.chronicle,
      ],
    })),
  disaster: () =>
    set((state) => ({
      balance: state.balance - 2,
      settlements: state.settlements.map((item) =>
        item.id === state.selectedSettlementId ? { ...item, food: Math.max(0, item.food - 15), happiness: Math.max(0, item.happiness - 6) } : item,
      ),
      chronicle: [
        { id: crypto.randomUUID(), tick: state.chronicle.length + 1, kind: 'disaster', actor: 'providence', text: 'A drought bites into the granaries.' },
        ...state.chronicle,
      ],
    })),
}));
