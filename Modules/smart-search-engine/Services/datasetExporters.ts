import { ChatConversation, PIIRuleMatch } from '../types';

export interface PIIAuditResult {
  scrubbedConversations: ChatConversation[];
  matchesFound: PIIRuleMatch[];
  totalRedactions: number;
}

// Regex patterns for sensitive data detection
const REGEX_PATTERNS = {
  API_KEY: /(?:sk_live_|ghp_|AKIA|AIzaSy|xoxb-)[A-Za-z0-9_-]{12,}/g,
  EMAIL: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
  IP_ADDRESS: /\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/g,
  JWT_SECRET: /bearer\s+eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/gi,
  CREDIT_CARD: /\b(?:\d{4}[-\s]?){3}\d{4}\b/g
};

export function auditAndScrubPII(conversations: ChatConversation[]): PIIAuditResult {
  const matchesMap: Record<string, PIIRuleMatch> = {};
  let totalCount = 0;

  const scrubText = (text: string): string => {
    let result = text;

    // API Keys
    result = result.replace(REGEX_PATTERNS.API_KEY, (match) => {
      totalCount++;
      const key = `API_KEY_${match.slice(0, 7)}`;
      matchesMap[key] = {
        type: 'API_KEY',
        originalText: match,
        redactedText: '[REDACTED_API_KEY]',
        count: (matchesMap[key]?.count || 0) + 1
      };
      return '[REDACTED_API_KEY]';
    });

    // Emails
    result = result.replace(REGEX_PATTERNS.EMAIL, (match) => {
      totalCount++;
      const key = `EMAIL_${match}`;
      matchesMap[key] = {
        type: 'EMAIL',
        originalText: match,
        redactedText: '[REDACTED_EMAIL]',
        count: (matchesMap[key]?.count || 0) + 1
      };
      return '[REDACTED_EMAIL]';
    });

    // IP addresses (filter out 127.0.0.1 or 0.0.0.0 as safe)
    result = result.replace(REGEX_PATTERNS.IP_ADDRESS, (match) => {
      if (match === '127.0.0.1' || match === '0.0.0.0') return match;
      totalCount++;
      const key = `IP_${match}`;
      matchesMap[key] = {
        type: 'IP_ADDRESS',
        originalText: match,
        redactedText: '[REDACTED_IP]',
        count: (matchesMap[key]?.count || 0) + 1
      };
      return '[REDACTED_IP]';
    });

    return result;
  };

  const scrubbedConversations: ChatConversation[] = conversations.map(conv => ({
    ...conv,
    title: scrubText(conv.title),
    messages: conv.messages.map(msg => ({
      ...msg,
      content: scrubText(msg.content)
    }))
  }));

  return {
    scrubbedConversations,
    matchesFound: Object.values(matchesMap),
    totalRedactions: totalCount
  };
}

// Convert conversations to OpenAI / Mistral Chat Completion fine-tuning JSONL format
export function exportToOpenAIJSONL(conversations: ChatConversation[]): string {
  const lines = conversations.map(conv => {
    const formatted = {
      messages: [
        { role: 'system', content: `You are an expert AI assistant specialized in ${conv.tags.join(', ')}.` },
        ...conv.messages.map(m => ({
          role: m.role,
          content: m.content
        }))
      ]
    };
    return JSON.stringify(formatted);
  });
  return lines.join('\n');
}

// Convert conversations to Alpaca / ShareGPT instruction dataset format
export function exportToAlpacaJSON(conversations: ChatConversation[]): string {
  const records: { instruction: string; input: string; output: string; source_provider: string }[] = [];

  conversations.forEach(conv => {
    for (let i = 0; i < conv.messages.length - 1; i += 2) {
      const userMsg = conv.messages[i];
      const asstMsg = conv.messages[i + 1];
      if (userMsg && asstMsg && userMsg.role === 'user' && asstMsg.role === 'assistant') {
        records.push({
          instruction: userMsg.content,
          input: `Context: ${conv.title} (Tags: ${conv.tags.join(', ')})`,
          output: asstMsg.content,
          source_provider: conv.provider
        });
      }
    }
  });

  return JSON.stringify(records, null, 2);
}
