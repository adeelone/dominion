import { renderToString } from 'react-dom/server';
import { expect, test } from 'vitest';
import { App } from './App';

test('renders the core Dominion app shell', () => {
  const html = renderToString(<App />);
  expect(html).toContain('Dominion');
  expect(html).toContain('Throne Decrees');
  expect(html).toContain('Providence Acts');
  expect(html).toContain('Omen Log');
});
