import type { RecordMap } from './graph/types';

export const predicateDescription: Record<string, string> = {
  INTRODUCES: '논문이 방법·모델·데이터셋을 제시한다.',
  EXTENDS: '기존 방법 또는 모델을 확장한다.',
  ADAPTS: '한 분야의 설계를 다른 분야에 적용한다.',
  ADDRESSES: '연구 문제를 해결 대상으로 삼는다.',
  MITIGATES: '문제의 영향을 완화한다.',
  PREREQUISITE_OF: '대상 역량에 앞서 필요한 지식이다.',
  RECOMMENDED_BEFORE: '대상보다 먼저 배우기를 권한다.',
  PART_OF: '전체를 이루는 구성 요소다.',
  IS_A: '더 일반적인 개념의 한 종류다.',
  CITES: '문헌을 인용한다.',
  EVALUATED_ON: '벤치마크에서 평가했다.',
  TRAINED_ON: '데이터셋으로 학습했다.',
  IMPROVES_ON: '보고된 성능을 비교한다.',
  COMPARED_WITH: '비교 대상으로 함께 평가했다.',
};

export const predicateLabels: Record<string, string> = {
  INTRODUCES: '제시',
  EXTENDS: '확장',
  ADAPTS: '적용',
  ADDRESSES: '다루는 문제',
  MITIGATES: '완화',
  PREREQUISITE_OF: '선수 지식',
  RECOMMENDED_BEFORE: '권장 선수',
  PART_OF: '구성 요소',
  IS_A: '한 종류',
  CITES: '인용',
  EVALUATED_ON: '평가',
  TRAINED_ON: '학습',
  IMPROVES_ON: '성능 비교',
  COMPARED_WITH: '비교',
};

export function predicateName(predicate: string): string {
  return predicateLabels[predicate] || predicate;
}

const template: Record<string, (subject: string, object: string, qualifiers: RecordMap) => string> =
  {
    INTRODUCES: (subject, object) => `${subject}은(는) ${object}을(를) 제시했다`,
    EXTENDS: (subject, object) => `${subject}은(는) ${object}을(를) 확장했다`,
    ADAPTS: (subject, object) => `${subject}은(는) ${object}을(를) 적용했다`,
    ADDRESSES: (subject, object) => `${subject}은(는) ${object} 문제를 다룬다`,
    MITIGATES: (subject, object) => `${subject}은(는) ${object}을(를) 완화한다`,
    PREREQUISITE_OF: (subject, object) => `${subject}은(는) ${object}의 선수 지식이다`,
    RECOMMENDED_BEFORE: (subject, object) =>
      `${subject}은(는) ${object}보다 먼저 배우기를 권장한다`,
    PART_OF: (subject, object) => `${subject}은(는) ${object}의 일부다`,
    IS_A: (subject, object) => `${subject}은(는) ${object}의 한 종류다`,
    CITES: (subject, object) => `${subject}은(는) ${object}을(를) 인용한다`,
    EVALUATED_ON: (subject, object) => `${subject}은(는) ${object}에서 평가됐다`,
    TRAINED_ON: (subject, object) => `${subject}은(는) ${object}(으)로 학습됐다`,
    IMPROVES_ON: (subject, object, qualifiers) => {
      const benchmark = String(qualifiers.benchmark || '보고된 벤치마크');
      const metric = String(qualifiers.metric || '지표');
      return `${subject}은(는) ${benchmark}의 ${metric}에서 ${object}보다 좋은 결과를 보고했다`;
    },
    COMPARED_WITH: (subject, object) => `${subject}은(는) ${object}과(와) 비교됐다`,
  };

export function claimSentence(claim: RecordMap, name: (id: string) => string): string {
  const qualifiers = (claim.qualifiers as RecordMap | undefined) || {};
  const predicate = String(claim.predicate);
  const sentence = (
    template[predicate] ||
    ((subject, object) => `${subject}은(는) ${object}과(와) ${predicate} 관계다`)
  )(name(String(claim.subject)), name(String(claim.object)), qualifiers);
  return qualifiers.conditions ? `${sentence} (${String(qualifiers.conditions)})` : sentence;
}
