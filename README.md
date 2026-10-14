# AIXON

AIXON은 AI 연구 관계를 근거와 함께 탐색하는 정적 Knowledge Atlas입니다.
각 개념의 Wiki와 계산 가능한 작은 Lab을 같은 그래프에서 연결합니다.

## 시작하기

```bash
make install
make build && npx astro preview
make verify
```

`AIXON_BASE`(기본 `/`), `AIXON_SITE`(기본 `http://localhost:4321`),
`AIXON_BUILD`(`preview` 또는 `public`), `AIXON_GRAPH`(쉼표로 구분한 YAML 경로),
`AIXON_WIKI_DIR`를 설정할 수 있습니다.

콘텐츠는 `draft`에서 시작해 사람이 `review`를 승인한 뒤 `published`로 올립니다.
설계 문서는 [docs](docs/)에 있고, Wiki 계약은
[CONTENT_SCHEMA.md](docs/CONTENT_SCHEMA.md)에 있습니다.
