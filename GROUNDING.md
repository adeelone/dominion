# Grounding Engine

The Grounding Engine turns free-form divine acts into structured, simulated consequences.

## Pipeline

1. Parse intent.
2. Classify plausibility against the world's magic and technology rules.
3. Materialize a real entity, phenomenon, resource, state change, or decline.
4. Simulate first-order consequences immediately.
5. Write the interpretation trail to the Omen Log.

## Worked Example

Prompt: `summon a dragon in the mountains`

High-magic world:

- Parsed intent: summon a dangerous winged predator.
- Plausibility: grounded supernatural.
- Materialized effect: entity, dragon, territorial predator, home region, strength, lifespan.
- First consequence: nearby settlement loses happiness and food on the next projection.

Low-magic historical world:

- Parsed intent: summon a dragon.
- Plausibility: reinterpreted low magic.
- Materialized effect: mountain wildfire mistaken for a dragon.
- First consequence: fear and food disruption, but no literal dragon entity.

World-breaking request:

- Prompt: `give them a spaceship`
- Classification: declined world breaking unless the world is configured for sci-fi.
- Result: no state mutation beyond the logged explanation.
