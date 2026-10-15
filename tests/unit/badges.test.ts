import { describe, expect, it } from 'vitest';
import { reviewLabel } from '../../src/lib/badges';

describe('reviewLabel', () => {
  it('shows a human review', () => {
    expect(reviewLabel({ review: { by: 'human:choi', at: '2026-10-15', decision: 'approve' } })).toBe(
      '사람 검토: human:choi, 2026-10-15',
    );
  });

  it('shows the panel size and approval date', () => {
    expect(
      reviewLabel({
        review: {
          by: 'panel:first-release',
          method: 'cross-review',
          reviewers: ['agent:source', 'agent:claim'],
          at: '2026-10-15',
          decision: 'approve',
        },
      }),
    ).toBe('AI 교차 검증 2명, 2026-10-15');
  });

  it('shows pending for missing or unapproved reviews', () => {
    expect(reviewLabel({})).toBe('검토 대기');
    expect(reviewLabel({ review: { by: 'agent:x', decision: 'approve' } })).toBe('검토 대기');
  });
});
