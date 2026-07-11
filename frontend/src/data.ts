export type Settlement = {
  id: string;
  name: string;
  region: string;
  population: number;
  happiness: number;
  food: number;
  culture: number;
  tags: string[];
};

export type ChronicleEntry = {
  id: string;
  tick: number;
  kind: string;
  actor: string;
  text: string;
};

export const settlements: Settlement[] = [
  { id: 's1', name: 'Bellroot', region: 'Crown Basin', population: 420, happiness: 62, food: 130, culture: 20, tags: ['drought-prone'] },
  { id: 's2', name: 'Emberwatch', region: 'Ashen March', population: 210, happiness: 51, food: 70, culture: 15, tags: ['hardy', 'superstitious'] },
  { id: 's3', name: 'Marrow Quay', region: 'Southmere', population: 300, happiness: 66, food: 110, culture: 24, tags: ['seafaring'] },
];

export const chronicleSeed: ChronicleEntry[] = [
  { id: 'c1', tick: 0, kind: 'world_event', actor: 'nature', text: 'The Crown Basin begins under unsettled skies.' },
  { id: 'c2', tick: 0, kind: 'diplomacy', actor: 'House Veyr', text: 'Envoys report iron caravans massing in the Ashen March.' },
];
