import type { RecordMap } from './graph/types';

const statusLabels: Record<string, string> = {
  proposed: '후보(미검증)',
  disputed: '논쟁 중',
  rejected: '기각됨',
  deprecated: '폐기됨',
};
const confidenceLabels: Record<string, string> = {
  high: '높음',
  medium: '보통',
  low: '낮음',
};

export function claimStatusLabel(status: unknown): string {
  return statusLabels[String(status)] || String(status || '상태 미지정');
}

export function confidenceLabel(confidence: unknown): string {
  return confidenceLabels[String(confidence)] || String(confidence || '미지정');
}

export function hasMachineCitation(claim: RecordMap): boolean {
  return ['verified', 'disputed'].includes(String(claim.status)) && Boolean(claim.verification);
}

export function humanReviewLabel(claim: RecordMap): string {
  const review = claim.review as RecordMap | undefined;
  if (
    review?.decision === 'approve' &&
    typeof review.by === 'string' &&
    review.by.startsWith('human:')
  ) {
    return `승인: ${review.by}, ${review.at || '날짜 미지정'}`;
  }
  return '검토 대기';
}

export const entityTypeLabels: Record<string, string> = {
  ResearchField: '연구 분야',
  ResearchProblem: '연구 문제',
  Concept: '개념',
  Method: '방법',
  Model: '모델',
  Paper: '논문',
  Dataset: '데이터셋',
  Metric: '평가 지표',
  Benchmark: '벤치마크',
  LearningObjective: '학습 목표',
  LearningResource: '학습 자료',
  AssessmentItem: '평가 문항',
  LabExperiment: '실험실',
};

export const dimensionLabels: Record<string, string> = {
  recognize: '알아봄',
  explain: '설명',
  derive: '유도',
  implement: '구현',
  analyze: '분석',
};

/** Entity status for display: a normal ("active") entity gets no badge (ADR-022 wording for the rest). */
export function nodeStatusLabel(status: unknown): string {
  return !status || status === 'active'
    ? ''
    : status === 'merged'
      ? '병합됨'
      : claimStatusLabel(status);
}

/** Claim (edge) status: `verified` only means the cited quote was found in the source (ADR-022). */
export function edgeStatusLabel(status: unknown): string {
  return status === 'verified' ? '인용 확인' : claimStatusLabel(status);
}

export function typeLabel(type: string): string {
  return type === 'More' ? '더보기' : entityTypeLabels[type] || type;
}
