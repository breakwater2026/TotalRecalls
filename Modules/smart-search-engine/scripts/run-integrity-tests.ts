import { INITIAL_CONVERSATIONS } from '../constants.ts';
import { runAllTests } from '../Services/testRunner.ts';
import { buildVectorIndex } from '../Services/ragEngine.ts';

async function main(): Promise<void> {
  const chunks = buildVectorIndex(INITIAL_CONVERSATIONS, 384);
  console.log(`Running ${INITIAL_CONVERSATIONS.length} conversations and ${chunks.length} indexed chunks through the integrity suite.`);

  const { results, summary } = await runAllTests(INITIAL_CONVERSATIONS, chunks);

  for (const result of results) {
    const marker = result.status === 'passed' ? 'PASS' : 'FAIL';
    const duration = `${result.durationMs} ms`;
    console.log(`[${marker}] ${result.id} — ${result.title} (${duration})`);
    if (result.details) console.log(`       ${result.details}`);
    if (result.error) console.error(`       ${result.error}`);
  }

  console.log('');
  console.log(`Integrity suite: ${summary.passed}/${summary.total} passed, ${summary.failed} failed in ${summary.overallDurationMs} ms.`);
  console.log(`Executed: ${summary.executedAt}`);
  console.log(`SHA-256: ${summary.integrityHash}`);

  if (summary.failed > 0) process.exitCode = 1;
}

main().catch(error => {
  console.error('Unable to execute the integrity suite:', error);
  process.exitCode = 1;
});
