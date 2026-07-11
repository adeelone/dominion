import { expect, test } from '@playwright/test';

test('core Throne and Providence flow updates the interface', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Dominion')).toBeVisible();
  await page.getByRole('button', { name: /Confirm decree/ }).click();
  await expect(page.locator('.chronicle').getByText(/Raise a river guard/)).toBeVisible();
  await page.getByRole('button', { name: /Materialize act/ }).click();
  await expect(page.locator('.omenLog').getByText(/territorial predator/)).toBeVisible();
});
