export const predicateDescription: Record<string, string> = {
  INTRODUCES: '논문이 방법·모델·데이터셋을 제시한다', EXTENDS: '기존 방법 또는 모델을 확장한다', ADAPTS: '한 분야의 설계를 다른 분야에 적용한다', ADDRESSES: '문제를 해결 대상으로 삼는다', MITIGATES: '문제의 영향을 완화한다', PREREQUISITE_OF: '대상 역량을 위해 이 지식이 필요하다', RECOMMENDED_BEFORE: '먼저 배우기를 권한다', PART_OF: '구성 요소 관계다', IS_A: '더 일반적인 개념의 한 종류다', CITES: '문헌 인용 관계다', EVALUATED_ON: '벤치마크에서 평가했다', TRAINED_ON: '데이터셋으로 학습했다', IMPROVES_ON: '동일 조건에서 성능을 개선했다', COMPARED_WITH: '동일 조건에서 비교했다',
};
export const claimSentence = (c: Record<string, unknown>, name: (id: string) => string) => `${name(String(c.subject))}은(는) ${name(String(c.object))}에 대해 ${predicateDescription[String(c.predicate)] || String(c.predicate)}.`;
