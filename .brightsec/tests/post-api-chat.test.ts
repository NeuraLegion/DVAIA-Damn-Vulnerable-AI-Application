import { test, before, after } from 'node:test';
import { SecRunner } from '@sectester/runner';
import { AttackParamLocation, HttpMethod } from '@sectester/scan';

const timeout = 40 * 60 * 1000;
const baseUrl = process.env.BRIGHT_TARGET_URL!;

let runner!: SecRunner;

before(async () => {
  runner = new SecRunner({
    hostname: process.env.BRIGHT_HOSTNAME!,
    projectId: process.env.BRIGHT_PROJECT_ID!
  });

  await runner.init();
});

after(() => runner.clear());

test('POST /api/chat', { signal: AbortSignal.timeout(timeout) }, async () => {
  await runner
    .createScan({
      tests: [
        'prompt_injection',
        'xss',
        'csrf',
        'sqli',
        'ssrf'
      ],
      attackParamLocations: [AttackParamLocation.BODY],
      starMetadata: {
        code_source: 'NeuraLegion/DVAIA-Damn-Vulnerable-AI-Application:master',
        databases: ['SQLite'],
        user_roles: null
      },
      poolSize: +process.env.SECTESTER_SCAN_POOL_SIZE || undefined
    })
    .setFailFast(false)
    .timeout(timeout)
    .run({
      method: HttpMethod.POST,
      url: `${baseUrl}/api/chat`,
      body: {
        prompt: 'Say short hi',
        model_id: 'openai:gpt-4o-mini',
        options: {
          temperature: 0.7,
          top_p: 0.9,
          max_tokens: 30
        }
      },
      headers: { 'Content-Type': 'application/json' }
    });
});