# D. 데이터 소스 평가: 식별자 매핑과 인용 수집 (AIXON)

- 작성 기준일: 2026-10-15 (KST). 실측 API 호출 시각: 2026-10-14 16:00–16:45 UTC (= 2026-10-15 01:00–01:45 KST).
- 조건: 계정과 API 키를 쓰지 않았고 `mailto`/`email` 파라미터도 쓰지 않았다. User-Agent는 `research-script`로 개인정보가 없다. 호출 간격은 최소 1.2초, arXiv는 최소 3.5초였다. 429를 받으면 6초 이상 기다린 뒤 최대 3회 재시도했다.
- 표기 규칙: 본문의 `[태그]`는 §7 출처 목록을 가리키며, 목록의 모든 URL에 "확인 2026-10-15"를 붙였다. **추론**은 관측에서 끌어낸 해석이고, **확인되지 않음**은 확인을 시도했으나 실패한 항목이다. **관측**은 이번 실측 결과다.
- 호출 수 고지: 데이터 소스 API 요청이 총 109건으로, 지침(~60건)을 넘었다. 대부분은 OpenAlex의 끊긴 참조(dangling reference)를 검증하는 데 들었다(약 30건, 대부분 1 credit짜리 list 호출). Semantic Scholar 429 재시도도 14건이다. 내역은 §6에 있다.

---

## 0. 핵심 결론 (TL;DR)

1. **인용 엣지 정확도 (seed 14편, 정답 46쌍 기준)**
   - **Semantic Scholar(S2)**: 재현율 45/46(97.8%), 정밀도 45/49(91.8%). 오탐 4건은 참고문헌을 엉뚱한 논문으로 연결한 결과다(BatchNorm→ResNet/VGG/AlexNet, BiT→AlexNet).
   - **OpenAlex**: 오탐 0건, 재현율 38–39/46(83–85%).
   - **S2 ∪ OpenAlex**: 46/46을 모두 찾지만 오탐 4건이 섞인다.
   - 정답은 arXiv HTML(LaTeXML) 참고문헌으로 만들었다(§4). AIXON처럼 증거 기반으로 엣지를 저장한다면 "두 소스의 합집합 + 원문 참고문헌으로 검증" 구조가 맞다.
2. **OpenAlex는 같은 논문이 여러 work로 쪼개져 있고, 일부 메타데이터가 오염돼 있다** (관측).
   - ResNet, ViT, BatchNorm, Deng2009, AlexNet, VGG, BERT는 각각 work가 2개, DeiT는 3개다.
   - Transformer work의 대표 `doi`와 `publication_date`(2025-08-23)는 제3자가 Crossref에 재등록한 사본 8건(prefix 10.65215)으로 바뀌어 있다.
   - BERT의 arXiv DOI를 가진 work는 제목과 DOI가 다른 Dagstuhl 논문이다.
   - 따라서 OpenAlex의 `display_name`·`doi`·`publication_date`를 정답으로 쓰면 안 되고, AIXON 논문 1편에 OpenAlex work N개를 매핑해야 한다.
   - arXiv DOI로 찾은 work 하나만 쓰면 seed 사이 인용 엣지가 23/46(50%)만 잡힌다(§4.5).
3. **OpenAlex에서 병합된 ID는 404를 돌려준다** (관측, W2964308564).
   - 공식 문서 두 곳이 서로 다르다. Get Singleton 페이지는 301 리다이렉트라고 쓰고 [OA-single], Sync 페이지는 리다이렉트 없이 404라고 쓴다 [OA-sync].
   - seed 23개 work의 `referenced_works` 고유 ID 537개 중 128개(24%)는 `corpus=all`로도 조회되지 않는다. 예를 들어 Swin은 136개 중 60개다.
   - 이 중 MAG 시대 ID 21개는 `/locations?filter=native_id:` 또는 `/locations/mag:{id}`로 살아남은 work를 찾을 수 있었다.
4. **OpenAlex는 키 없이도 쓸 수 있다.**
   - 키 없는 일일 예산은 $0.10, 즉 1,000 credits다(관측 헤더 `x-ratelimit-limit: 1000`). 단건 조회는 무료, list는 1 credit, search는 10 credits다.
   - 무료 키를 받으면 일일 $1이 되고 cursor paging을 쓸 수 있다 [OA-auth][OA-costs].
   - `from_updated_date` 같은 동기화 필터는 유료 플랜 전용이다 [OA-sync].
   - Concepts는 폐기(동결)됐다. Topics는 4 domains → 26 fields → 252 subfields → 4,516 topics 구조이며, 2026년 10월에 분류기가 바뀌었다(Qwen3-8B 미세조정) [OA-topics].
   - AI 논문에는 너무 거칠다. ViT의 primary topic은 "Advanced Neural Network Applications"였다(관측).
5. **S2는 큐레이션 규모에 가장 적합하지만, 키 없는 공용 풀이 혼잡하다** (27건 중 14건이 429).
   - `POST /paper/batch` 한 번에 ID 500개를 처리하므로 14편의 메타데이터와 참고문헌을 1회 호출로 받았다.
   - preprint와 출판본을 한 paperId로 병합하고, `externalIds`에 ArXiv/DOI/DBLP/MAG/ACL/CorpusId를 준다.
   - 출판사가 참고문헌을 막은 논문이 있다(AlexNet/ACM: "elided by the publisher").
6. **arXiv**
   - 메타데이터는 CC0다 [AX-tou]. API는 3초당 1회, 연결 1개로 제한된다 [AX-tou].
   - HTML 백필로 2014–2021년 seed 12편 모두 HTML 참고문헌이 있었다(관측). 참고문헌 정답 소스로 쓸 수 있다.
   - OAI-PMH의 `arXiv` 포맷 `<created>`는 최신 버전 날짜다(관측). v1 날짜로 쓰면 안 된다.
7. **Crossref는 NeurIPS/ICLR/ICML/arXiv 전용 ML 논문에서 거의 쓸모가 없다** (DOI 없음). IEEE/ACM/Springer/ACL 판에는 유효하다. 공개 풀 한도는 단건 5 rps, 목록 1 rps다 [CR-blog][CR-forum]. "Attention Is All You Need"로 검색하면 상위 5건이 모두 재등록 사본(10.65215)이다(관측).
8. **DBLP API와 OpenReview API는 오늘 스크립트로 접근할 수 없다** (관측).
   - DBLP: dblp.org, uni-trier, dagstuhl 세 호스트 모두 Anubis 챌린지(HTTP 202)를 돌려준다.
   - OpenReview: 403 `ChallengeRequiredError`.
   - 대안: DBLP XML 덤프(1.11 GB, CC0)는 바로 내려받을 수 있다 [DBLP-cc0][DBLP-dump].
9. **Papers with Code와 Hugging Face Papers**
   - Papers with Code는 HF Trending Papers로 302 리다이렉트된다. 아카이브는 HF 데이터셋 `pwc-archive/*`에 CC BY-SA 4.0으로 남아 있다 [PWC-repo][PWC-hf].
   - HF Papers의 `GET /api/papers/{arxiv_id}`는 키 없이 동작한다. 익명 IP 한도는 5분당 500 요청이다. 인용은 주지 않지만 모델·데이터셋 연결을 준다 [HF-openapi][HF-rate].
10. **DataCite와 Unpaywall**
    - DataCite의 arXiv DOI는 `10.48550/arXiv.{id}`이고 논문당 1개다(버전 무관). 버전별 날짜와 `rightsList`(라이선스)가 있지만 출판본과 연결하는 `relatedIdentifiers`는 비어 있다(관측).
    - Unpaywall은 email 파라미터가 필수이고 DataCite DOI(arXiv)를 다루지 않는다 [OA-unpaywall]. AIXON에는 OpenAlex의 `best_oa_location`이 대체재다.

---

## 1. 비교표

### 1A. 접근 조건, 한도, 라이선스

| 소스 | 키 필요? | 무료 한도 / 레이트리밋 (공식, 2026-10-15) | 메타데이터 라이선스 | 캐싱·재배포·상업 이용 | AIXON 규모 운영비 |
|---|---|---|---|---|---|
| **OpenAlex** | 기본 조회는 키 없이 가능. 무료 키는 예산 10배, cursor paging 사용 가능 [OA-auth]. 2026-02-24 블로그는 "you'll need an API key for all requests"라고 공지했다 [OA-blog-pricing]. | 키 없음: 10 rps, $0.10/일. 무료 키: 30 rps, $1/일. 연간 플랜: 50 rps. singleton 무료, list $0.10/1k, search $1/1k. OR 최대 100, `per_page` 최대 100 [OA-auth][OA-costs] | CC0 [OA-pricing][OA-sync] | 모두 허용 (CC0) | 1,000편 DOI 매핑은 OR 필터 10회(10 credits). 제목 검색은 편당 10 credits라 키 없이 하루 100건 |
| **arXiv** | 불필요 | 레거시 API·OAI-PMH·RSS: "no more than one request every three seconds", 단일 연결 [AX-tou] | 서술 메타데이터 CC0 1.0 [AX-tou] | 메타데이터는 자유. 본문은 논문별 라이선스이며 대부분 non-exclusive라 재배포 불가 [AX-tou][AX-license] | 무료. S3 벌크는 requester-pays [AX-s3] |
| **Semantic Scholar** | 대부분 불필요. Datasets 다운로드는 키 필수(관측: 401) | 키 없음: "1000 requests per second shared among all unauthenticated users", 혼잡 시 추가 제한. 키: 1 RPS부터 [S2-product]. 관측 429율 52% | API License Agreement + 데이터별 라이선스("such as CC BY-NC or ODC-BY"). S2ORC는 ODC-By 1.0 [S2-license][S2ORC] | 귀속 표기 의무. "repackage, sell, … distribute, or sublicense the API" 금지. 캐싱 조항은 명시돼 있지 않음 (확인되지 않음) | 1,000편은 batch 2회. 단, 429 백오프 필요 |
| **Crossref** | 불필요. Plus는 유료 키 | 공개 풀: 단건 5 rps(동시 1), 목록 1 rps(동시 1). polite(mailto): 단건 10/3, 목록 3/3 (2025-12-01 공지, 2026-07-21 타입별 적용) [CR-blog][CR-forum] | "almost none of the metadata is subject to copyright, … any purpose". 일부 초록은 저작권 대상 [CR-rest] | 자유. 초록만 주의 | 무료. Metadata Plus는 유료 [CR-plus] |
| **DBLP** | 불필요 | 공식 FAQ는 Anubis 때문에 열람하지 못함 (확인되지 않음). 관측: search API가 HTTP 202 챌린지 반환 | CC0 1.0 (2019-11-24부터, 덤프와 web API 포함) [DBLP-cc0] | 상업 포함 자유 | XML 덤프 1.11 GB gz (관측) |
| **OpenReview** | 관측: 게스트 요청 403 `ChallengeRequiredError`. 로그인하면 우회되는지는 확인되지 않음 | 응답 헤더 `ratelimit-policy: 180;w=60` (관측) | 메타데이터 CC0 1.0, 코멘트·리뷰 CC BY 4.0, 논문은 `license` 필드 [OR-terms] | 메타데이터 자유. 리뷰는 출처 표기 필요 | 현재 스크립트 수집 불가 |
| **Papers with Code** | 서비스 종료(HF로 302, 관측) | 해당 없음 | 아카이브 CC BY-SA 4.0 [PWC-repo][PWC-hf] | 재배포 시 Share-alike 의무 | 정적 parquet 1회 다운로드 |
| **HF Papers** | 불필요 | 익명 IP: API 5분당 500, Pages 100 (2025-09 표, "subject to change") [HF-rate] | 확인되지 않음 | 확인되지 않음 | 무료 |
| **Unpaywall** (호출 안 함) | `email` 파라미터 필수 [OA-unpaywall] | "Please limit use to 100,000 calls per day" [UPW] (JS 페이지, 검색 인덱스 문구) | 확인되지 않음 (추론: OpenAlex와 같은 DB) | — | email 금지 규칙 때문에 사용 부적합 |
| **DataCite** | 불필요 | 미식별: 5분당 500, 식별(UA나 mailto에 email): 1,000, 인증: 3,000, 모두 IP당 [DC-rate] | CC0 waiver [DC-policy] | 자유 | 무료 |

### 1B. 데이터, 식별자, 인용, 버전 처리

| 소스 | 제공 데이터 | 주요 엔드포인트 | 인용 커버리지 (이번 실측) | 식별자·중복 처리 | 변경·버전 처리 |
|---|---|---|---|---|---|
| **OpenAlex** | works, authors, sources, institutions, topics, keywords, funders, locations. 코어 works 3.2억+ [OA-corpus] | `/works/{W\|doi:}`, `/works?filter=&search=&select=`, `/locations`, `/topics` | `referenced_works` 정밀도 100%, 재현율 83–85%. 끊긴 ID 24%. ML 논문 `cited_by_count`가 S2 대비 크게 낮음 (Transformer 24,356 vs 196,727) | `ids{openalex,doi,mag,pmid,pmcid}` (arXiv 키 없음). location마다 DOI와 `merge_key{doi,arxiv,pmid,title_author}`. 같은 논문이 여러 work로 나뉘는 경우 많음 | 병합 ID는 404, 리다이렉트 없음. `deleted_ids.csv.gz`. location id로 병합 경로 추적. 분기별 무료 스냅샷 |
| **arXiv** | 메타데이터, 버전, 라이선스, PDF/소스, HTML | `export.arxiv.org/api/query`, `oaipmh.arxiv.org/oai`, `arxiv.org/html/{id}` | 구조화된 인용 없음. HTML `ltx_bibitem`이 원문 참고문헌 | arXiv ID(+vN), DOI `10.48550/arXiv.{id}` | API와 OAI는 최신 버전만 반환. `arXivRaw`에 이력. 버전별 라이선스 |
| **S2** | papers, authors, venues, citations(contexts/intents/isInfluential), embeddings, TLDR. 2.14억 편 [S2-product] | `/graph/v1/paper/{id}`, `POST /paper/batch`, `/references`, `/citations`, `/search/match`, Datasets | 재현율 97.8%, 정밀도 91.8%. 출판사가 참고문헌을 막은 경우 있음 | `paperId`(sha), `corpusId`, `externalIds{ArXiv,DOI,DBLP,MAG,ACL,PubMed,…}`. preprint와 출판본을 병합 | 릴리스와 diff(Incremental Updates). 병합 시 paperId가 유지되는지는 확인되지 않음 |
| **Crossref** | 회원사가 등록한 DOI 메타데이터, references(등록 시), funder, license | `/works/{doi}`, `/works?query.bibliographic=`, `/prefixes/{p}` | 출판사가 등록한 참고문헌만 있음. `is-referenced-by-count`는 DOI 간 인용만 셈 | DOI. `relation`(has-preprint 등)은 선택 사항 (ResNet은 비어 있음) | `indexed`, `created`, Crossmark 업데이트 |
| **DBLP** | CS 서지 정보, 저자 식별, venue | search API(차단됨), XML 덤프 | 자체 인용 데이터 없음 (추론) | dblp key. CoRR판과 학회판이 별도 key | 일간·월간 덤프 [DBLP-cc0] |
| **OpenReview** | 제출본, 리뷰, 결정 | `api2.openreview.net/notes` | 없음 | forum id (예: ViT ICLR = `YicbFdNTTy`) | Edits 이력 |
| **PwC 아카이브** | paper–code 링크, methods, tasks, SOTA 표 | HF parquet | 없음 | arXiv ID, PwC slug | 동결됨 (lastModified 2026-08-17) |
| **HF Papers** | 제목, 저자, 초록, upvotes, AI 키워드, 연결된 모델·데이터셋·Space | `/api/papers/{id}`, `/api/papers/search`, `/api/daily_papers` | 없음 | arXiv ID | 해당 없음 |
| **Unpaywall** | DOI 기준 OA 위치 | `api.unpaywall.org/v2/{DOI}?email=` | 없음 | Crossref DOI만 | OpenAlex DB 위에서 동작 |
| **DataCite** | DataCite DOI 메타데이터 (arXiv, Zenodo) | `api.datacite.org/dois/{doi}` | arXiv DOI는 `referenceCount` 0 | DOI. `identifiers`에 arXiv ID | 버전별 Submitted/Updated 날짜, `version` |

---

## 2. 소스별 상세

### 2.1 OpenAlex

**제공 데이터와 규모**
- works(코어 3.2억+, expansion 1.9억; `corpus=all`로 둘 다 조회), authors, sources, institutions, topics, keywords, publishers, funders, awards, locations [OA-corpus].
- 2026년 9월 스냅샷 기준 약 6.26억 레코드다 [OA-snapshot].

**주요 엔드포인트**
- `GET /works/{id}`: `W…`, `doi:…`, `pmid:…`을 받는다 [OA-single].
- `GET /works?filter=…&search=…&select=…&per-page=…`
- `GET /locations`, `/locations/{namespaced id}`: `doi:…`, `pmh:oai:arXiv.org:…`, `mag:…` [OA-locs]
- `/topics`, `/subfields`, `/fields`, `/domains`, `/rate-limit`
- 예전 `.search` 필터(`title.search` 등)는 폐기됐고 `search` 파라미터를 쓴다 [OA-topics].

**핵심 필드 (works)**
- 식별: `id`, `doi`(대표 DOI 1개), `ids{openalex, doi, mag, pmid, pmcid}`
- 서지: `display_name`, `publication_date`, `publication_year`, `type`
- 위치: `primary_location`, `locations[]`(`id`, `doi`, `source`, `version`, `license`, `landing_page_url`, `pdf_url`, `raw_type`), `best_oa_location`
- 인용: `referenced_works`, `referenced_works_count`, `cited_by_count`
- 주제: `primary_topic`, `topics[]`(score), `keywords`, `concepts`(폐기)
- 기타: `fwci`, `is_xpac`, `created_date`, `updated_date` [OA-works][OA-locs]
- `/locations` 행에는 추가로 `work_id`, `native_id`, `native_id_namespace`, `provenance`, `merge_key{doi, arxiv, pmid, title_author}`, `ingested_at`이 있다 [OA-locs].

**접근 조건, 요금, 레이트리밋 (2025–2026 변경)**
- 2026-02-24 블로그 "New Features and Usage-Based Pricing"에서 사용량 기반 과금을 도입했다. 요청에 키가 필요하고, 키 없이는 "a few calls … for demo purposes"만 된다고 했다 [OA-blog-pricing].
- 현재 문서는 "you can make basic queries with no key at all"이라고 쓴다. 무료 키는 예산을 10배로 늘리고 cursor paging에 필수다 [OA-auth].
- 일일 예산: 무료 키 $1, 키 없음 $0.10 [OA-costs][OA-pricing].
- 관측 헤더: `x-ratelimit-limit: 1000`, `x-ratelimit-limit-usd: 0.1`, `x-ratelimit-credits-used`, `x-ratelimit-reset`(UTC 자정까지 남은 초).
- 관측 비용: singleton 0 credit, list 1, search 10. `/locations/{id}` 단건 조회는 1 credit이 부과됐다(관측).
- 키 없는 잔여 예산이 내 사용량보다 빨리 줄었다. IP 단위로 예산을 공유하는 것으로 보인다(**추론**).
- 연산별 비용: singleton 무료, list/filter $0.10/1k, search $1/1k, rerank +$1/1k, semantic search $1/1k, PDF content $10/1k [OA-costs].
- 초당 한도: 키 없음 10, 무료 키·선불 30, 연간 플랜 50. semantic search는 1 rps. 불리언 연산자가 5개를 넘는 검색은 1/5/25 rps [OA-auth].
- 쿼리 한도: OR 값 최대 100, `per_page` 최대 100, `sample` 최대 10,000, 기본 paging 최대 10,000건 [OA-auth].
- 유료 플랜: Member $5,000/년($20/일), Member+ $10,000/년($100/일, 일간 스냅샷, 동기화 필터), Partner $20,000/년부터 [OA-pricing].

**라이선스**
- CC0이며 "no 'personal use only' carve-out"이다 [OA-pricing]. 캐싱, 재배포, 상업 이용 모두 가능하다.

**스냅샷과 증분 동기화**
- `s3://openalex`(`--no-sign-request`, AWS 계정 불필요)에 JSONL(약 745 GB)과 Parquet(약 770 GB)로 제공된다. `updated_date`로 파티션돼 있다 [OA-snapshot].
- 무료 공개 스냅샷은 1·4·7·10월 둘째 수요일에 분기별로 나온다(2026 Q4 = 2026-10-14). 일간 스냅샷은 유료다 [OA-sync].
- works 삭제 로그 `deleted_ids.csv.gz`는 2026-09-23 릴리스부터 공개 버킷에 있다. Walden 이전의 `merged_ids/`는 2025년 Walden 전환으로 동결됐다 [OA-sync].
- API의 동기화 필터 `from_created_date`와 `from_updated_date`는 유료 플랜 전용이다 [OA-sync].
- Walden(엔진 재작성)은 2025-11-03 게시물에서 가동이 공지됐다 [OA-blog-walden].

**Concepts와 Topics**
- Concepts는 폐기됐다. MAG에서 온 약 6.5만 개, 6단계 체계이며 동결됐다. 새 works에는 태깅되지 않지만 works의 `concepts` 필드는 여전히 반환된다 [OA-concepts][OA-deprec].
  - 관측: ViT에는 concepts 11개가 붙어 있었다. 예를 들어 'Image (mathematics)'(level 2)처럼 정밀도가 낮다.
- Topics 계층은 4 domains → 26 fields → 252 subfields → 4,516 topics다 [OA-topics].
  - 관측: API `meta.count`가 4516 / 252 / 26 / 4로 일치했다.
  - 토픽 목록은 인용 클러스터로 만들었다(CWTS와 협업). 이름은 LLM이 생성했고 ASJC에 매핑했다 [OA-topics].
- 2026년 10월부터 토픽 부여 방식이 바뀌었다 [OA-topics].
  - 분류기는 "fine-tuned Qwen3-8B … trained on 2 million works whose topics were chosen by Claude Opus 5.5"다.
  - 제목, 초록, source 이름을 읽고 인용은 쓰지 않는다. work마다 최대 3개 topic과 `primary_topic`을 부여하며, 약 10%는 토픽이 없다.
  - 이전 분류기 v1은 2027-01-13까지 `/text/topics?version=1`로 쓸 수 있다.
  - 이번 변경은 `updated_date`를 바꾸지 않았다. 스냅샷 사용자는 2026-10-14 스냅샷으로 전체를 다시 적재해야 한다.
- 관측: ViT의 primary topic은 T10036 "Advanced Neural Network Applications"(score 0.982), subfield는 "Computer Vision and Pattern Recognition"이다. AIXON의 개념 그래프로 쓰기에는 거칠다.

**병합된 work 처리**
- 문서끼리 충돌한다.
  - Get Singleton: "requesting the old ID returns a `301` redirect" (예시는 author) [OA-single]
  - Sync: "a deleted or merged-away ID returns **404**. There is no redirect" [OA-sync]
- 관측 1: W2964308564(Bahdanau의 MAG 중복 ID, `mag:2964308564` location이 W2133564696에 붙어 있음)를 조회하면 **404 HTML**이 온다.
- 관측 2: `/locations/mag:2964308564`는 `work_id` W2133564696을 돌려준다. `mag:2963069010`은 W1869752048("Grammar as a foreign language")로 이어진다. `mag:1799366690`은 404다.
- 공식 입장: 병합 ID와 살아남은 work를 잇는 매핑은 현재 없다. 병합 경로는 location id 이동으로 추적하고, 같은 DOI를 가진 살아 있는 work가 둘이면 `updated_date`가 최신인 쪽이 살아남는다 [OA-sync].

**arXiv preprint와 학회·저널판의 관계**
- 문서상으로는 한 work의 여러 location으로 합친다. NumPy 예시에서 arXiv DOI와 저널 DOI가 같은 work에 있다 [OA-dois].
  - work의 대표 `doi`는 Crossref(출판본이 preprint보다 우선) > DataCite(arXiv, Zenodo) > 기타 순으로 고른다.
  - `doi` 필터는 모든 location의 DOI와 매칭된다 [OA-dois].
  - 매칭 방식: 공유 PID(DOI/PMID/arXiv)는 동일하다는 증거로 보고, 없으면 제목과 저자로 fuzzy 매칭한다 [OA-works].
- **실측은 혼재**다(§3.6). Swin과 BiT는 병합됐고, ResNet·ViT·DeiT·BatchNorm·Deng2009·AlexNet·VGG·BERT는 분리돼 있다.

**메타데이터 품질 (관측)**
- **Transformer W2626778328**
  - `doi` = `10.65215/2q58a426`, `publication_date` = 2025-08-23, `type` = preprint.
  - location 11개 중 8개가 Crossref member 54718 "Shenzhen Medical Academy of Research and Translation"의 posted-content 재등록본이다.
  - "Crossref 우선" 규칙 때문에 arXiv DOI를 밀어냈다(**추론**).
- **BERT W2896457183**
  - arXiv location은 갖고 있지만 `display_name`은 "AI-Assisted Pipeline for Dynamic Generation of Trustworthy Health Supp…"이고 `doi`는 `10.4230/lipics.cosit.2022.18`이다.
  - Dagstuhl과 Zenodo 레코드 다수가 잘못 합쳐졌다. `cited_by_count`가 44,473으로, BERT 인용이 NAACL work(31,891)와 나뉘어 있다.
- **BatchNorm**: W2949117887이 MAG의 arXiv PDF와 TIB 데이터셋 DOI(`10.57702/o9raffed`)를 묶은 중복 work다. 발행일은 2024-01-01, 피인용은 14,220이다.
- **AlexNet**: 대표 work W2163605009에 NeurIPS 2012의 MAG location이 CACM 2017 work로 흡수돼 있어 연도가 2017이다. 또 다른 중복 W3147600416은 CiNii 출처이며 source가 "Medical Entomology and Zoology"로 잘못 붙어 있다.
- **ResNet CVPR work**: location에 LA Referencia의 석사논문이 섞여 있다.

**인용 커버리지**
- `referenced_works`는 원 레코드(Crossref, PubMed 등)와 OA PDF에서 참고문헌을 추출한 뒤 DOI 우선으로 매칭해 만든다. OpenAlex에 없는 문헌은 버린다 [OA-cites].
- 관측: seed 엣지 재현율 83–85%다. 끊긴 ID 비율이 높고(§4.6), ML 논문 피인용 수가 크게 낮다(LayerNorm 440 vs S2 13,311).

**운영 비용 (AIXON)**
- DOI 단건 조회는 무료다. OR 필터 1회(100 DOI)에 1 credit이 든다.
- 중복 탐지용 제목 검색은 10 credits라 키 없이는 하루 약 100건이 한계다.
- 스냅샷(약 750 GB)은 필요 없다.

### 2.2 arXiv (API, OAI-PMH, 벌크, HTML, DOI)

**데이터**
- 메타데이터: 제목, 저자, 초록, 분류, comments, 저자가 입력한 `journal_ref`와 `doi`, 버전, 라이선스
- 본문: PDF와 소스, HTML

**엔드포인트**
- API: `https://export.arxiv.org/api/query?id_list=…`(Atom)
- OAI-PMH: base URL `https://oaipmh.arxiv.org/oai`. 포맷은 `oai_dc`, `arXiv`(최신판 + license), `arXivRaw`(버전 이력) [AX-oai]
- RSS
- 벌크: Kaggle 데이터셋, S3 requester-pays [AX-bulk][AX-s3]
- HTML: `arxiv.org/html/{id}`
- ar5iv

**접근과 레이트리밋**
- 키가 필요 없다.
- 레거시 API(OAI-PMH, RSS, arXiv API)는 "no more than one request every three seconds, … single connection at a time"이며, 사용자가 통제하는 모든 기계를 합산한다 [AX-tou].
- 수집용으로는 export.arxiv.org를 쓰라고 권한다 [AX-bulk].

**라이선스**
- 서술 메타데이터는 CC0 1.0이다 [AX-tou]. "Metadata … may be reused in non-commercial and commercial systems" [AX-oai].
- 본문은 논문별 라이선스다. 선택지는 CC BY 4.0, CC BY-SA 4.0, CC BY-NC-SA 4.0, CC BY-NC-ND 4.0, arXiv perpetual non-exclusive 1.0, CC0이며, 버전마다 다를 수 있다 [AX-license].
- 허락 없이 본문을 서버에 저장해 서비스하는 것은 금지다. "A citation graph using bibliographic references from e-prints"는 권장 용도로 명시돼 있다 [AX-tou].
- 관측 (OAI `license`): 1706.03762는 nonexclusive-distrib/1.0, 2103.14030은 CC BY 4.0이다.

**버전 처리**
- API는 최신 버전을 준다. 관측: 1706.03762v7(updated 2023-08-02), 1810.04805v2, 2010.11929v2, 1512.03385v1.
- OAI-PMH는 최신 버전만 노출하고 datestamp는 제출일이 아니다 [AX-oai].
- 관측: OAI `arXiv` 포맷의 `<created>`가 1706.03762에서 2023-08-02(v7 날짜)였다. v1 날짜(2017-06-12)는 API의 `<published>`나 `arXivRaw`에서 가져와야 한다.

**HTML (LaTeXML) 커버리지**
- 공식: "We are gradually backfilling HTML for arXiv's corpus of over 2 million papers over time. Not every paper can be successfully converted" [AX-html].
- 관측: 1512.03385(2015)의 native HTML이 실제 문서(`ltx_bibitem` 50개)였다. seed 12편(2014–2021) 모두 `arxiv.org/html/{id}`에서 참고문헌이 추출됐다.
- ar5iv: "Sources upto the end of September 2026. Not a live preview service. For articles with multiple revisions, only a single version is made available." [AR5IV]

**arXiv DOI (DataCite)**
- prefix는 10.48550이고 형식은 `10.48550/arXiv.{id}`다. 등록은 2022-01-01에 시작됐고 "As of Feb 2022, all arXiv articles now have DOIs" [AX-doi].
- 관측: ViT DOI는 2022-02-24, ResNet DOI는 2022-03-06에 등록됐다(백필).

**벌크 규모**
- S3 전체는 2025년 4월 기준 약 9.2 TB, PDF는 2023년 3월 기준 약 2.7 TB다 [AX-s3].

**품질 메모**
- arXiv ID, 버전, 날짜, 분류는 권위 있는 원천이다.
- 학회 정보는 자유 텍스트 comment에만 있다. 관측: ViT의 comment는 "ICLR camera-ready". 4편 모두 `journal_ref`와 `doi`가 비어 있었다.

### 2.3 Semantic Scholar Academic Graph API와 Datasets API

**데이터**
- papers, authors, venues, citations(context, intent, influential 포함), SPECTER2 임베딩, TLDR, 추천, snippet 검색
- 규모: "214 Million Papers, 2.49 Billion Citations, 79 Million Authors" [S2-product]

**엔드포인트**
- `GET /graph/v1/paper/{id}`: ID 형식은 `<sha>`, `CorpusId:`, `DOI:`, `ARXIV:`, `MAG:`, `ACL:`, `PMID:`, `PMCID:`, `URL:`(arxiv.org, aclweb.org, acm.org, biorxiv.org, semanticscholar.org) [S2-swagger]
- `POST /paper/batch`: "500 paper ids at a time", 최대 10 MB, 최대 9999 citations [S2-swagger]
- `/paper/{id}/references`, `/citations`(offset/limit), `/paper/search`, `/search/bulk`, `/search/match`, `/snippet/search`, author 엔드포인트 [S2-swagger]

**핵심 필드**
- 식별: `paperId`, `corpusId`, `externalIds`("limited to: ArXiv, MAG, ACL, PubMed, Medline, PubMedCentral, DBLP, and DOI" + CorpusId)
- 서지: `title`, `abstract`("due to legal reasons, this may be missing"), `venue`, `publicationVenue{id,name,type,alternate_names,url}`, `year`, `publicationDate`, `publicationTypes`, `journal`
- 지표: `referenceCount`, `citationCount`, `influentialCitationCount`
- 기타: `openAccessPdf{url,status,license,disclaimer}`, `fieldsOfStudy`, `s2FieldsOfStudy`, `tldr`, `embedding`, `textAvailability`
- 인용 엣지: `contexts`, `intents`, `contextsWithIntent`, `isInfluential`, `citedPaper`/`citingPaper` [S2-swagger]

**접근과 레이트리밋**
- 키 없음: "1000 requests per second shared among all unauthenticated users. Requests may also be further throttled during periods of heavy use."
- 키 있음: "The introductory rate limit for an API key is 1 RPS on all endpoints." 키는 email로 발급된다 [S2-product].
- 관측: 27건 중 14건이 429였다. 메시지: "Too Many Requests. Please wait and try again or apply for a key for higher rate limits."

**약관 (API License Agreement, 2023-05-17 최종 갱신)** [S2-license]
- 라이선스 범위: "to access and display" S2 Data에 대한 제한적이고 비독점적인 라이선스다.
- 데이터 라이선스: S2 Data는 각 데이터에 붙은 라이선스("such as CC BY-NC or ODC-BY")를 따르고, 제3자 콘텐츠는 별도 라이선스를 따른다.
- 귀속: "Semantic Scholar" 표기가 의무이고, 논문을 쓰면 Open Data Platform 논문을 인용해야 한다.
- 금지 사항: "repackage, sell, rent, lease, lend, distribute, or sublicense the API", 레이트리밋 우회.
- 캐싱과 저장: 명시 조항이 없다(**확인되지 않음**). 개인 로컬 캐시는 명시적으로 금지되지 않았지만, 데이터를 재배포하려면 데이터별 라이선스(CC BY-NC가 붙으면 비상업)에 따라야 한다(**추론**).

**Datasets API**
- 관측: 최신 release_id는 2026-10-06이다. 데이터셋은 abstracts, authors, citations, embeddings-specter_v1/v2, paper-ids, papers, publication-venues, s2orc, s2orc_v2, tldrs다.
- 관측: 다운로드(`/dataset/papers`)는 401 "A valid API key is required"였다.
- 라이선스는 "See the README files for each dataset"라서 키 없이는 열람할 수 없다(**확인되지 않음**). 스펙에 "Incremental Updates"(diff) 태그가 있다 [S2-datasets].
- S2ORC는 "released … under the ODC-By 1.0" [S2ORC]이다.

**품질 메모 (관측)**
- preprint와 출판본을 병합한다. ResNet은 arXiv와 CVPR DOI가 같은 paperId다.
- `year`는 가장 이른 날짜를 쓴다(ResNet 2015, ViT 2020). 반면 `venue`는 CVPR(2016), ICLR(2021)이라 서로 맞지 않는다.
- `publicationDate`가 null인 경우: BERT, Swin.
- 학회 논문에도 `publicationTypes`에 'JournalArticle'이 들어간다.
- DBLP key가 CoRR key(`journals/corr/…`)인 경우: VGG, Transformer, BERT, LayerNorm, Bahdanau, Santurkar, DeiT.
- DeiT의 `citationCount`가 정확히 9999였다. 상한값일 가능성을 의심했지만 단건 재조회가 429로 실패했다(**확인되지 않음**).
- BatchNorm은 `referenceCount` 54인데 원문 참고문헌은 24개다. 미해결 참고문헌에 "Batch Normalization Presentation"이 있어 다른 문서의 참고문헌이 섞인 것으로 보인다(**추론**).

**인용 커버리지**
- 이번 seed에서 가장 좋았다.
- 출판사 차단 사례(관측): AlexNet의 `/references`가 `data: []`를 반환했고, disclaimer는 "Notice: The following paper fields have been elided by the publisher: {'references'}"였다.
- Deng2009도 `referenceCount` 27인데 반환된 참고문헌이 0건이었다. 같은 차단으로 보인다(**추론**).
- intent는 드물다. ViT 참고문헌 65개 중 54개에 contexts가 있었지만 intent는 background 8, methodology 14뿐이고 나머지는 빈 배열이었다. `isInfluential=true`는 7개였다(관측). 가능한 intent 목록은 FAQ에 있지만 직접 확인하지 않았다.

### 2.4 Crossref REST API

**데이터**
- 회원사가 등록한 DOI 메타데이터: title, author(+ORCID), container-title, published/issued/created/indexed 날짜, type, `reference`(등록한 경우), `is-referenced-by-count`, license, funder, `relation`, 일부 초록(JATS) [CR-rest]

**엔드포인트**
- `/works/{doi}`, `/works?query.bibliographic=&filter=&rows=&select=&cursor=`, `/prefixes/{prefix}`, `/members/{id}`, `/journals/{issn}/works`, `/works/{doi}/agency`

**풀과 한도**
- 2025-11-05 블로그: 2025-12-01부터 다음 한도를 적용한다 [CR-blog].
  - 공개 풀: Single record 5 rps(동시 1), List 1 rps(동시 1)
  - polite 풀: Single 10 rps(동시 3), List 3 rps(동시 3)
  - mailto 파라미터를 주면 polite 풀로 간다.
- 2026-07-21 포럼 공지: "From today, 21 July 2026" 요청 타입별 한도를 적용한다. 단건 한도는 그대로이고, email 단위로 제한하며, `x-rate-limit-type` 헤더를 새로 추가했다. 동시 연결 한도는 언급하지 않았다 [CR-forum].
- 관측 헤더: 단건은 `x-rate-limit-limit: 5`, `x-rate-limit-interval: 1s`, `x-api-pool: public-single`. 목록 검색은 `x-rate-limit-limit: 1`, `x-api-pool: public-array`.
- Metadata Plus는 유료다. 스냅샷, "priority service/rate limits", SLA(99.5% 가동률), 키 발급을 제공한다 [CR-plus]. 연 1회 공개 데이터 파일도 있다 [CR-tips].

**라이선스**
- "almost none of the metadata is subject to copyright, and you may use it for any purpose. Some abstracts contained in the metadata may be subject to copyright by publishers or authors." [CR-rest]

**품질과 커버리지 (관측)**
- ResNet `10.1109/cvpr.2016.90`
  - proceedings-article, 2016-06, pp. 770–778, reference-count 49, is-referenced-by-count 177,699
  - 초록 없음. `relation`이 비어 있어 arXiv판과 연결되지 않는다.
- AlexNet `10.1145/3065386`
  - journal-article, CACM 60(6), 2017-05-24, reference-count 32(그중 DOI 있음 17)
  - 피인용 32,969(S2는 131,928), 초록 있음, license는 ACM 정책 URL
  - "Deng J. 2009" 참고문헌 항목은 저자와 연도만 있다.
- Transformer
  - NeurIPS DOI가 없다. `query.bibliographic` 상위 5건이 모두 `10.65215/*` posted-content였다(member 54718, posted 2025-08-23 또는 2025-11-13, 원문 URL langtaosha.org.cn).
  - Crossref에도 재등록·스팸 DOI가 있으므로 제목 검색 결과를 그대로 믿으면 안 된다.

### 2.5 DBLP

**데이터**
- CS 서지 레코드: key(예: `conf/cvpr/HeZRS16`), venue, year, pages, ee 링크, 저자 페이지(동명이인 구분)
- CoRR(arXiv)판과 학회판은 서로 다른 key다(S2 `externalIds`로 관측).

**엔드포인트**
- `/search/publ/api?q=&format=json&h=`(author/venue 검색도 있음), 레코드 export, XML 덤프 `https://dblp.org/xml/dblp.xml.gz`

**접근 (관측, 2026-10-14 UTC)**
- dblp.org, dblp.uni-trier.de, dblp.dagstuhl.de의 search API와 FAQ 페이지가 모두 **HTTP 202 + Anubis PoW 챌린지 HTML**("Making sure you're not a bot!")을 돌려줬다.
- XML 덤프는 HEAD 기준 200, `content-length` 1,111,064,343, `last-modified` 2026-10-13 22:07 GMT였다.
- 공식 레이트리밋 FAQ는 열람하지 못했다(**확인되지 않음**). 검색엔진 요약에 따르면 429와 Retry-After를 쓴다고 하지만 원문으로 확인하지 못했다.

**라이선스**
- "all of dblp's data will be released under the CC0 1.0 … This affects all metadata releases, in particular the daily and monthly data dumps and data retrieved from the web APIs."(2019-11-24). 상업 이용도 허용된다 [DBLP-cc0].

**AIXON에서의 가치**
- DOI가 없는 NeurIPS, ICLR, ICML 학회판의 venue, 연도, 쪽수를 얻는 표준 소스다. 지금은 API가 막혀 있으니 덤프를 로컬에 색인하는 방식이 현실적이다(**추론**).

### 2.6 OpenReview API

**데이터와 엔드포인트**
- 제출본(notes), 리뷰, 메타리뷰, 결정, venue 설정
- API v2 엔티티: Note, Invitation, Edge, Group, Edit, Profile. 현재 venue와 대부분의 과거 venue가 v2로 옮겼고, 오래된 venue는 v1이다 [OR-docs].
- Python 클라이언트에 `get_all_notes()`가 있다 [OR-docs].

**접근 (관측)**
- `https://api2.openreview.net/notes?id=YicbFdNTTy`와 v1 모두 **403**을 돌려줬다: `{"name":"ChallengeRequiredError","message":"Challenge verification required …"}`.
- 응답 헤더: `ratelimit-policy: 180;w=60`, `x-ratelimit-limit: 180`
- 로그인 토큰으로 우회되는지는 계정을 쓰지 않아 **확인되지 않음**이다. 공개 문서에서도 이 오류를 찾지 못했다.

**약관 (2024-09-24)** [OR-terms]
- Metadata: CC0 1.0("To the extent that the Submitter or OpenReview has a copyright interest in metadata")
- Comment(리뷰, 메타리뷰, 토론 포함)와 Configuration Record: CC BY 4.0
- Article: `license` 필드를 따른다.

**ID**
- forum id. ViT의 ICLR 2021 forum id `YicbFdNTTy`는 OpenAlex ICLR work의 landing page `openreview.net/pdf?id=YicbFdNTTy`에서 확인했다(관측).

### 2.7 Papers with Code

**상태 (관측)**
- `https://paperswithcode.com/`와 `/api/v1/papers/?arxiv_id=…` 모두 **302 → https://huggingface.co/papers/trending**이다.
- 공식 종료 공지는 **확인되지 않음**이다. 2차 보도는 2025년 7월 하순 종료와 HF "Trending Papers" 대체를 전한다 [PWC-news, 비공식].

**아카이브**
- GitHub README가 HF 데이터셋 `pwc-archive/{papers-with-abstracts, links-between-paper-and-code, evaluation-tables, methods, datasets}`로 연결한다. 라이선스는 "All data is licenced under CC-BY-SA" [PWC-repo]다.
- README의 "data is regenerated daily" 문구는 갱신되지 않은 문장으로 보인다(**추론**).
- HF API(관측): `papers-with-abstracts`는 2025-08-18 생성, lastModified 2026-08-17, `cc-by-sa-4.0`, parquet 4개다 [PWC-hf].

**가치**
- methods 분류, tasks, datasets, paper–code 링크, SOTA 표를 AIXON의 Method와 Concept 시드로 쓸 수 있다.
- 파생 DB를 재배포하면 share-alike 의무가 따른다.

### 2.8 Hugging Face Papers

**엔드포인트 (공식 OpenAPI)** [HF-openapi]
- `GET /api/papers/{paperId}`("Get a paper"), `GET /api/papers/search`, `GET /api/papers`, `GET /api/daily_papers`, `POST /api/papers/index`, 댓글 엔드포인트

**관측**
- `GET /api/papers/2010.11929`가 인증 없이 200을 돌려줬다.
- 응답 키: `id`, `authors`, `publishedAt`, `title`, `summary`, `upvotes`, `discussionId`, `ai_summary`, `ai_keywords`, `ai_summary_model`, `linkedModels`, `numTotalModels`, `linkedDatasets`, `numTotalDatasets`, `linkedSpaces`, `numTotalSpaces`
- ViT의 `publishedAt`은 2020-10-22T17:55:59Z(arXiv v1과 같음), upvotes는 24였다.

**한도와 약관**
- 익명 IP 한도: API 500, Resolvers 3,000, Pages 100, 모두 5분 고정 창이다("Anonymous and Free users are subject to change") [HF-rate].
- 데이터 약관은 **확인되지 않음**이다.

**가치**
- 인용 데이터는 없다.
- 논문과 HF 모델·데이터셋을 잇는 링크를 주므로 AIXON의 "모델" 엔티티 연결에 유용하다.

### 2.9 Unpaywall (문서만 확인, 호출 안 함)

- 2025년 말부터 OpenAlex DB 위에서 동작한다. "When you look at OpenAlex, you are looking at Unpaywall's data in a different format" [OA-unpaywall].
- REST 형식은 `api.unpaywall.org/v2/{DOI}?email=…`이다. **Crossref DOI만** 다루고 DataCite DOI(arXiv)는 다루지 않는다 [OA-unpaywall].
- 한도: "Please limit use to 100,000 calls per day" [UPW]. 공식 페이지가 JS로 렌더링돼 직접 추출하지 못했고, 검색 인덱스에 잡힌 공식 문구다.
- 라이선스는 **확인되지 않음**이다.
- 결론: email 필수 조건이 AIXON의 개인정보 금지 규칙과 충돌하고, arXiv 미포함이라 가치도 낮다. OpenAlex의 `best_oa_location`이나 `open_access`로 대체한다.

### 2.10 DataCite (arXiv DOI 10.48550)

**엔드포인트와 필드**
- `https://api.datacite.org/dois/{doi}`
- 필드: `attributes.doi`, `titles`, `creators`, `publisher`("arXiv"), `publicationYear`, `types.resourceTypeGeneral`("Preprint"), `dates[]`(버전별 Submitted/Updated, `dateInformation` "v1"/"v2"; Available; Issued), `version`, `rightsList`, `relatedIdentifiers`, `identifiers`(arXiv), `subjects`(arXiv 분류 + FOS), `created`/`registered`/`updated`, `citationCount`/`referenceCount`

**한도와 라이선스**
- 한도: 미식별 IP는 5분당 500, 식별(UA나 mailto에 email)은 1,000, 인증은 3,000이다(페이지 갱신 2026-08-07). 관측: 레이트리밋 헤더가 없었다 [DC-rate].
- 라이선스: "DataCite e.V. has waived all copyright … The DataCite Data File includes all DOIs and deposited metadata", CC0 1.0 [DC-policy].

**관측**
- ViT: registered 2022-02-24, `version` "2", `rightsList` = arXiv non-exclusive, `relatedIdentifiers` = [](ICLR판과 연결 없음), `citationCount` 16, `referenceCount` 0
- ResNet: `version` "1", updated 2025-05-27

**가치**
- arXiv DOI가 실제로 존재하는지 독립적으로 검증할 수 있다. 버전별 날짜와 라이선스는 arXiv OAI(arXivRaw)로도 얻을 수 있다.

---

## 3. Task B: 식별자 실험 결과

### 3.1 방법
- OpenAlex
  - `/works/doi:10.48550/arXiv.2010.11929` 단건 조회
  - 18개 DOI OR 필터(`filter=doi:…|…`, `select=…,locations`)
  - seed 14편 제목 `search`(`per-page=10`)
  - 중복 work 단건 조회
- S2: `GET /paper/arXiv:2010.11929`, `POST /paper/batch`(seed 14편 + 출판 DOI 4개), `/paper/search`(AlexNet)
- Crossref: `/works/{doi}` 2건, `/prefixes/10.65215`, `/works/10.65215/2q58a426`, `query.bibliographic`
- DataCite 2건, arXiv API 1건, OAI-PMH 2건, HF Papers 1건

### 3.2 ViT (arXiv 2010.11929, ICLR 2021)

| 소스 | 결과 |
|---|---|
| arXiv API | 2010.11929**v2**. published 2020-10-22T17:55:59Z, updated 2021-06-03. comment는 "…ICLR camera-ready…", `journal_ref`와 `doi`는 없음 |
| DataCite | `10.48550/arxiv.2010.11929`, registered 2022-02-24, `version` 2, 버전별 Submitted/Updated 날짜, rights는 arXiv non-exclusive, `relatedIdentifiers` [] |
| OpenAlex | ① **W3094502228**: preprint, 2020-10-22, DOI는 arXiv, `ids.mag` 3094502228, 피인용 21,131, 참고문헌 52, location은 arXiv OAI와 arXiv DOI 2개뿐(ICLR 없음). ② **W3119786062**: conference-paper, "International Conference on Learning Representations", 2021-05-03, DOI 없음, 피인용 449, 참고문헌 49, MAG에서 유래, landing은 `openreview.net/pdf?id=YicbFdNTTy`. **분리됨** |
| S2 | paperId `268d347e8a55b5eb82fb5e7d2f800e33c75ab18a`, CorpusId 225039882. `externalIds`: ArXiv 2010.11929, DBLP `conf/iclr/DosovitskiyB0WZ21`, MAG 3094502228(DOI 없음). venue ICLR, year **2020**, publicationDate 2020-10-22, citationCount 71,547, referenceCount 65 |
| Crossref | 학회 DOI가 없어 조회하지 않음. OpenAlex와 S2 어디에도 출판 DOI가 없다 |
| HF Papers | id 2010.11929, publishedAt 2020-10-22T17:55:59Z, upvotes 24 |
| 불일치 | 연도: arXiv 2020, 학회 2021. S2는 venue를 ICLR로 쓰면서 year는 2020이다. OpenAlex는 preprint와 학회판을 분리했다. 피인용 수가 3.3배 차이 난다(S2 71,547 vs OpenAlex 21,131+449) |

### 3.3 ResNet (arXiv 1512.03385, CVPR 2016 DOI 10.1109/CVPR.2016.90)

| 소스 | 결과 |
|---|---|
| arXiv API | v1만 있음, 2015-12-10T19:51:55Z, comment "Tech report" |
| DataCite | `10.48550/arxiv.1512.03385`, registered 2022-03-06, `version` 1 |
| Crossref | `10.1109/cvpr.2016.90`, proceedings-article, IEEE(member 263), published 2016-06, pp. 770–778, reference-count 49, is-referenced-by-count 177,699, `relation` {} |
| OpenAlex | ① **W2194775991**: conference-paper 2016-06-01, CVPR DOI, 피인용 **221,134**, 참고문헌 80, location에 IEEE와 LA Referencia 석사논문(오병합). ② **W2949650786**: preprint 2015-12-10, arXiv DOI, 피인용 4,188, 참고문헌 50, location에 arXiv와 Zenodo DOI 2개. **분리됨**. arXiv DOI로 조회하면 피인용이 적은 쪽(②)이 나온다 |
| S2 | paperId `2c03df8b48bf3fa39054345bafabfeff15bfd11d`, CorpusId 206594692. arXiv ID와 CVPR DOI 둘 다 같은 paperId로 해석된다. `externalIds`: DBLP `conf/cvpr/HeZRS16`, MAG 2949650786, ArXiv, DOI. venue CVPR, year **2015**, publicationDate 2015-12-10, citationCount 241,890, referenceCount 54 |
| 불일치 | S2 연도는 2015인데 CVPR은 2016이다. S2의 MAG ID는 OpenAlex의 **arXiv work**(②)와 같고 인용이 몰린 CVPR work(①)와는 다르다. 참고문헌 수: Crossref 49, arXiv HTML 50, S2 54, OpenAlex ① 80(병합으로 부풀었다고 봄, **추론**) |

### 3.4 AlexNet (NeurIPS 2012, arXiv 없음; CACM 2017 DOI 10.1145/3065386)

| 소스 | 결과 |
|---|---|
| Crossref | `10.1145/3065386`, journal-article, CACM 60(6) 84–90, 2017-05-24, reference-count 32, is-referenced-by-count 32,969, 초록 있음, license는 ACM 정책 URL |
| OpenAlex | ① **W2163605009**: article, **2017-05-24**, CACM DOI, 피인용 106,345, 참고문헌 27. location에 CACM, CiteSeerX 2개, `mag:2163605009`("neural information processing systems")가 있어 NeurIPS 2012판이 CACM work에 흡수됐다. ② **W3147600416**: 2012, DOI 없음, source "Medical Entomology and Zoology"(CiNii, 오귀속), 피인용 754 |
| S2 | paperId `abd1c342495432171beb7ca8fd9551ef13cbd0ff`, CorpusId 195908774. NeurIPS와 CACM을 한 레코드로 병합했다. `externalIds`: DBLP `conf/nips/KrizhevskySH12`, MAG 2997031122, DOI 10.1145/3065386. venue는 "Communications of the ACM"인데 year는 **2012**, publicationDate 2012-12-03. citationCount 131,928, referenceCount 94이지만 references는 출판사 차단. 제목 검색 상위 5건에 중복 없음 |
| 불일치 | 연도: OpenAlex 2017, S2 2012. S2는 venue(CACM)와 year(2012)가 섞여 있다. S2 MAG 2997031122는 OpenAlex에 work로도 MAG location으로도 없다. 참고문헌 수: S2 94, Crossref 32, OpenAlex 27 |

### 3.5 Transformer (arXiv 1706.03762, NeurIPS 2017)

| 소스 | 결과 |
|---|---|
| arXiv API / OAI | 최신 **v7**(updated 2023-08-02), published 2017-06-12T17:57:34Z. license nonexclusive-distrib/1.0. OAI `<created>`는 2023-08-02 |
| Crossref | NeurIPS DOI가 없다. `query.bibliographic` 상위 5건이 모두 `10.65215/*`. `/prefixes/10.65215`는 member 54718 "Shenzhen Medical Academy of Research and Translation"이다. `10.65215/2q58a426`은 posted-content/preprint, posted 2025-08-23, created 2025-11-12, `relation.is-version-of` 10.65215/r5bs2d54, 저자는 Vaswani 외 8명, 원문 URL은 langtaosha.org.cn |
| OpenAlex | **W2626778328** 하나. type **preprint**, `publication_date` **2025-08-23**, `doi` **10.65215/2q58a426**, 피인용 24,356, 참고문헌 28. location 11개: 10.65215 DOI 8개, arXiv OAI, arXiv DOI, `mag:2963403868`(NeurIPS MAG 레코드가 흡수됨) |
| S2 | paperId `204e3073870fae3d05bcbc2f6a8e263d9b72e776`, CorpusId 13756489. `externalIds`: MAG 2626778328, DBLP `journals/corr/VaswaniSPUJGKP17`(CoRR key), ArXiv(DOI 없음). venue NeurIPS, year 2017, publicationDate 2017-06-12, citationCount 196,727, referenceCount 41 |
| 불일치 | OpenAlex의 대표 DOI, 날짜, 유형이 재등록 사본으로 오염됐다. 피인용이 8배 차이 난다. S2의 DBLP key는 학회판(`conf/nips/…`)이 아니다. 참고문헌 수: arXiv HTML 40, S2 41, OpenAlex 28 |

### 3.6 seed 14편의 OpenAlex work 현황 (중복과 병합)

| Seed | OpenAlex works (유형 · 날짜 · DOI · 피인용) | 판정 |
|---|---|---|
| Deng2009 | W2108598243 (CVPR, 2009-06-01, `10.1109/cvpr.2009.5206848`, 60,802) + W4239072543 (DOI 변형 `10.1109/cvprw.2009.5206848`, 2,714, 참고문헌 0) | 중복 |
| AlexNet | W2163605009 (CACM+NeurIPS, 2017) + W3147600416 (CiNii, 754) | 중복, 연도 오류 |
| VGG | W1686810756 (arXiv, 71,416) + W3209259379 (2015, "(No Title)", 29) | 중복, ICLR판 없음 |
| Bahdanau | W2133564696 (arXiv, 14,130). location에 TIB 데이터셋 DOI `10.57702/sq75seit`와 MAG 2개 | 병합 소멸 ID W2964308564는 404 |
| BatchNorm | W1836465849 (arXiv, 23,054) + W2949117887 (MAG + TIB DOI `10.57702/o9raffed`, 2024-01-01, 14,220) | 중복, 인용 분산 |
| ResNet | W2194775991 (CVPR, 221,134) + W2949650786 (arXiv, 4,188) | 미병합 |
| LayerNorm | W3037932933 (arXiv, **440**) | 피인용 과소 (S2 13,311) |
| Transformer | W2626778328 (DOI·날짜 오염) | 오병합 |
| Santurkar | W2898211994 (arXiv, **219**) | NeurIPS판 없음, 피인용 과소 (S2 1,774) |
| BERT | W2963341956 (NAACL `10.18653/v1/n19-1423`, 31,891) + W2896457183 (arXiv DOI를 갖지만 제목·DOI는 Dagstuhl 논문, 44,473) | 심각한 오병합 |
| BiT | W3015146382 (ECCV `10.1007/978-3-030-58558-7_29` + arXiv, 960) | 병합됨 |
| ViT | W3094502228 (arXiv) + W3119786062 (ICLR, MAG) | 미병합 |
| DeiT | W3116489684 (arXiv OAI location, 992, 참고문헌 61) + W4394668313 (arXiv DOI location만, 151, 참고문헌 0) + W4376983091 (HAL, 20, 참고문헌 0) | 같은 arXiv ID인데 work 3개 |
| Swin | W3138516171 (ICCV `10.1109/iccv48922.2021.00986` + arXiv, 33,170) | 병합됨 |

- DOI 18개로 OR 조회하면 work 16개가 나온다. BiT와 Swin은 DOI 2개가 work 1개로 합쳐졌다. ResNet과 BERT는 DOI 2개가 work 2개다.
- 문서가 설명하는 "공유 PID는 증거" 원칙과 달리, DeiT는 같은 arXiv ID(OAI location과 DataCite DOI location)가 서로 다른 work에 있다(관측).

### 3.7 S2 `externalIds.MAG`와 OpenAlex work 대응 (관측)

| 결과 | 해당 seed |
|---|---|
| `W{MAG}`가 그대로 존재 (6) | Deng2009, BatchNorm, LayerNorm, Transformer, BiT, ViT |
| 존재하지만 부차 중복 work (1) | ResNet: 2949650786은 arXiv work |
| 병합 소멸, `/locations`로만 해석됨 (1) | Bahdanau: 2964308564 → W2133564696 |
| work로도 MAG location으로도 없음 (4) | AlexNet 2997031122, VGG 2949429431, Santurkar 2806970737, BERT 2951055169 |
| MAG 없음 (2) | DeiT, Swin |

결론: S2의 MAG ID를 OpenAlex 연결 키로 단독 사용하면 안 된다.

---

## 4. Task C: seed 14편의 인용 행렬

### 4.1 방법
- **(a) S2**: `POST /graph/v1/paper/batch?fields=paperId,references.paperId,references.externalIds,references.title,…` 1회 호출로 14편을 받았다. ViT는 `/references?limit=1000`로도 받아 건수가 65건으로 같음을 확인했다(항목별 대조는 하지 않음). 참고문헌을 seed의 paperId로 매칭했다.
- **(b) OpenAlex**: seed마다 찾은 **모든** work(23개)의 `referenced_works`를 가져와, 피인용 측도 seed의 모든 work ID로 매칭했다. "+alias"는 병합으로 사라진 ID를 `/locations?filter=native_id:`로 해석한 결과다.
- **정답 (GT)**: arXiv HTML(`arxiv.org/html/{id}`, 최신판) `ltx_bibitem`에서 seed 제목 패턴을 매칭했다(인용한 쪽 12편). AlexNet→Deng2009는 arXiv판이 없어 Crossref의 CACM판 참고문헌 "Deng J., 2009"(제목·DOI 없음)로 판정했다(**추론, 강함**). BatchNorm과 BiT의 부재 판정은 저자명으로 다시 확인했다.

### 4.2 seed ID 매핑

| 약어 | Seed | S2 paperId (앞 8자) / CorpusId | OpenAlex work(s) |
|---|---|---|---|
| Dn | Deng 2009 ImageNet | d2c733e3 / 57246310 | W2108598243, W4239072543 |
| Ax | Krizhevsky 2012 AlexNet | abd1c342 / 195908774 | W2163605009, W3147600416 |
| VG | Simonyan 2014 VGG | eb42cf88 / 14124313 | W1686810756, W3209259379 |
| Bh | Bahdanau 2014 | fa72afa9 / 11212020 | W2133564696 (+ 소멸 W2964308564) |
| BN | Ioffe 2015 BatchNorm | 995c5f5e / 5808102 | W1836465849, W2949117887 |
| RN | He 2015 ResNet | 2c03df8b / 206594692 | W2194775991, W2949650786 |
| LN | Ba 2016 LayerNorm | 97fb4e3d / 8236317 | W3037932933 |
| Tf | Vaswani 2017 | 204e3073 / 13756489 | W2626778328 (+ 소멸 W2963403868) |
| Sa | Santurkar 2018 | 94be567c / 53104146 | W2898211994 |
| BE | Devlin 2018 BERT | df2b0e26 / 52967399 | W2963341956, W2896457183 |
| Bi | Kolesnikov 2019 BiT | bc516223 / 214728308 | W3015146382 |
| Vi | Dosovitskiy 2020 ViT | 268d347e / 225039882 | W3094502228, W3119786062 |
| De | Touvron 2020 DeiT | ad7ddcc1 / 229363322 | W3116489684, W4394668313, W4376983091 |
| Sw | Liu 2021 Swin | c8b25fab / 232352874 | W3138516171 |

### 4.3 행렬 (행 = 인용하는 논문 → 열 = 인용된 논문)

범례:

| 기호 | 의미 |
|---|---|
| ● | 정답 인용이고 S2와 OpenAlex 모두 검출 |
| S | 정답 인용인데 S2만 검출 (OpenAlex 누락) |
| S(a) | S2는 검출. OpenAlex는 병합 소멸 ID를 alias로 해석해야만 검출 |
| O | 정답 인용인데 OpenAlex만 검출 (S2는 참고문헌 차단) |
| s✗ | S2 오탐 (정답에 없음) |
| 빈칸 | 인용 없음 (세 소스 모두 일치) |
| · | 시간상 불가능 (인용된 논문이 더 늦음) |
| — | 자기 자신 |

| 인용↓ \ 피인용→ | Dn | Ax | VG | Bh | BN | RN | LN | Tf | Sa | BE | Bi | Vi | De | Sw |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Dn** (2009) | — | · | · | · | · | · | · | · | · | · | · | · | · | · |
| **Ax** (2012) | O | — | · | · | · | · | · | · | · | · | · | · | · | · |
| **VG** (2014-09) | ● | S | — |  | · | · | · | · | · | · | · | · | · | · |
| **Bh** (2014-09) |  |  | · | — | · | · | · | · | · | · | · | · | · | · |
| **BN** (2015-02) |  | s✗ | s✗ |  | — | s✗ | · | · | · | · | · | · | · | · |
| **RN** (2015-12) |  | ● | ● |  | ● | — | · | · | · | · | · | · | · | · |
| **LN** (2016-07) |  | ● | S |  | ● |  | — | · | · | · | · | · | · | · |
| **Tf** (2017-06) |  |  |  | S(a) |  | ● | S | — | · | · | · | · | · | · |
| **Sa** (2018-05) |  | ● | S |  | ● | ● | ● |  | — | · | · | · | · | · |
| **BE** (2018-10) | ● |  |  |  |  |  |  | ● |  | — | · | · | · | · |
| **Bi** (2019-12) | ● | s✗ | ● |  | ● | ● |  |  |  |  | — | · | · | · |
| **Vi** (2020-10) | ● | ● |  |  | ● | ● |  | ● |  | ● | ● | — | · | · |
| **De** (2020-12) | ● | ● | S |  |  | ● | S | ● |  | ● |  | ● | — | · |
| **Sw** (2021-03) | ● | ● | ● |  |  | ● |  | ● |  |  | ● | ● | S | — |

### 4.4 소스별로 찾은 쌍 (인용 → 피인용)

**S2 (49쌍)**
- VGG → AlexNet, Deng2009
- BatchNorm → ResNet✗, VGG✗, AlexNet✗
- ResNet → BatchNorm, VGG, AlexNet
- Santurkar → LayerNorm, ResNet, BatchNorm, VGG, AlexNet
- LayerNorm → BatchNorm, VGG, AlexNet
- Transformer → LayerNorm, ResNet, Bahdanau
- BERT → Transformer, Deng2009
- BiT → ResNet, BatchNorm, VGG, AlexNet✗, Deng2009
- ViT → BiT, Transformer, ResNet, BatchNorm, AlexNet, Deng2009, BERT
- DeiT → ViT, Transformer, LayerNorm, ResNet, VGG, AlexNet, Deng2009, BERT
- Swin → DeiT, ViT, BiT, Transformer, ResNet, VGG, AlexNet, Deng2009
- Deng2009와 AlexNet은 S2가 참고문헌을 0건 반환했다. Bahdanau는 seed 인용이 없다.

**OpenAlex (38쌍, alias 해석 시 39쌍)**
- AlexNet → Deng2009
- VGG → Deng2009
- ResNet → VGG, BatchNorm, AlexNet (arXiv work만 보면 BatchNorm, AlexNet)
- Santurkar → BatchNorm, AlexNet, ResNet, LayerNorm
- LayerNorm → AlexNet, BatchNorm (중복 work W2949117887 경유)
- Transformer → ResNet (+ Bahdanau, alias를 해석할 때만)
- BERT → Deng2009, Transformer (두 work 모두)
- BiT → VGG, BatchNorm, Deng2009, ResNet
- ViT → Deng2009, AlexNet, ResNet, Transformer, BatchNorm (W2949117887 경유), BERT, BiT (두 work 모두 동일)
- DeiT → Deng2009, AlexNet, ResNet, Transformer, BERT, ViT (W3116489684만. 나머지 DeiT work 2개는 참고문헌 0)
- Swin → VGG, Deng2009, AlexNet, ResNet, Transformer, BiT, ViT
- Bahdanau, BatchNorm, Deng2009는 seed 인용이 없다.

**두 소스가 엇갈린 쌍 (12쌍)**

| 쌍 | 검출 소스 | 정답 판정 | 원인 |
|---|---|---|---|
| VGG→AlexNet, LayerNorm→VGG, Santurkar→VGG, Transformer→LayerNorm, DeiT→VGG, DeiT→LayerNorm, Swin→DeiT | S2만 | 정답 (arXiv HTML로 확인) | OpenAlex 누락 |
| Transformer→Bahdanau | S2만 | 정답 | OpenAlex는 병합 소멸 ID W2964308564를 가리킴 |
| BatchNorm→ResNet, BatchNorm→VGG, BatchNorm→AlexNet, BiT→AlexNet | S2만 | 오탐. BatchNorm 원문 참고문헌 24개에 세 논문이 없다. ResNet은 BatchNorm보다 나중이다 | 아래 4.6 참고 |
| AlexNet→Deng2009 | OpenAlex만 | 정답 (추론, 강함) | S2 참고문헌 차단 |

### 4.5 정확도 요약 (정답 46쌍 기준)

| 방식 | 검출 | TP | FP | FN | 정밀도 | 재현율 |
|---|---|---|---|---|---|---|
| S2 batch references | 49 | 45 | 4 | 1 | 91.8% | 97.8% |
| OpenAlex (seed별 모든 중복 work 매핑) | 38 | 38 | 0 | 8 | 100% | 82.6% |
| OpenAlex (+ MAG alias 해석) | 39 | 39 | 0 | 7 | 100% | 84.8% |
| OpenAlex (**arXiv DOI로 찾은 work 1개만** 사용, 계산값) | 23 | 23 | 0 | 23 | 100% | 50.0% |
| S2 ∩ OpenAlex | 37 | 37 | 0 | 9 | 100% | 80.4% |
| S2 ∪ OpenAlex | 50 | 46 | 4 | 0 | 92.0% | 100% |

### 4.6 원인 분석

**참고문헌 수 비교**

| Seed | arXiv HTML bibitem (최신판) | S2 referenceCount (미해결) | OpenAlex `referenced_works_count` (work별) | 그중 끊긴 ID |
|---|---|---|---|---|
| Deng2009 | 해당 없음 | 27 (반환 0) | 33 / 0 | 7 |
| AlexNet | 해당 없음 | 94 (반환 0, 출판사 차단) | 27 / 0 | 1 |
| VGG | 34 | 43 (4) | 30 / 0 | 4 |
| Bahdanau | 29 | 33 (4) | 22 | 2 |
| BatchNorm | 24 | **54** (15) | 23 / 16 | 1 / 1 |
| ResNet | 50 | 54 (1) | 80 (CVPR) / 50 (arXiv) | 24 / 6 |
| LayerNorm | 32 | 33 (1) | 22 | 2 |
| Transformer | 40 | 41 (2) | 28 | 6 (+ alias 1) |
| Santurkar | 31 | 33 (1) | 30 | 3 |
| BERT | 56 | 63 (4) | 52 / 55 | 6 / 6 |
| BiT | 67 | 76 (1) | 79 | 16 |
| ViT | 58 | 65 (7) | 52 / 49 | 5 / 5 |
| DeiT | 62 | 66 (3) | 61 / 0 / 0 | 4 |
| Swin | 85 | 86 (2) | **136** | **60** |

**OpenAlex가 놓친 이유**
- 끊긴 ID가 많다. seed 23개 work의 참고문헌 고유 ID 537개 중 128개가 `corpus=all`로도 조회되지 않았다. 단건 조회는 404다.
- 그중 21개만 `/locations?filter=native_id:` MAG location으로 살아남은 work를 찾았고 나머지 107개는 찾지 못했다(관측).
- Swin→DeiT 누락은 DeiT가 work 3개로 쪼개진 것과 Swin의 끊긴 ID 60개가 겹친 결과로 보인다(**추론**).
- 피인용 측이 쪼개져 있다. ViT→BatchNorm은 W2949117887을 가리키고, 6개 논문의 ResNet 인용은 모두 CVPR work를 가리킨다. 그래서 seed에 work 하나만 매핑하면 엣지의 절반을 잃는다(4.5의 50%).
- Swin(136개 대 실제 85개)과 ResNet CVPR(80개 대 50개)은 참고문헌 수가 실제보다 많다. 병합된 location들의 참고문헌을 합친 결과로 보인다(**추론**).

**S2가 오탐한 이유**
- BatchNorm 원문 참고문헌은 "He et al. (2015) … Delving Deep into Rectifiers …"(PReLU)다. S2는 이를 ResNet으로 연결했다(**추론**).
- S2의 BatchNorm 참고문헌 목록(54개, 미해결에 "Batch Normalization Presentation" 포함)에는 원문에 없는 VGG와 AlexNet이 있다. 다른 문서의 목록이 섞였다고 본다(**추론**).
- BiT 원문은 "Krizhevsky, A.: Learning multiple layers of features from tiny images (2009)"(CIFAR 기술 보고서)를 인용한다. S2는 이를 AlexNet으로 연결했다(**추론**).

**S2가 놓친 이유**
- 출판사가 참고문헌을 막았다. AlexNet은 ACM이 "elided by the publisher"이고, Deng2009도 같은 이유로 보인다(**추론**).

**버전 차이**
- 정답은 arXiv 최신판 기준이다. S2와 OpenAlex는 다른 판(학회판 등)의 참고문헌을 썼을 수 있다. 이번 seed에서 판 차이로 판정이 바뀐 사례는 관측되지 않았다.

---

## 5. Implications for identifier mapping and ingestion design (AIXON 설계 시사점)

### 5.1 정체성 모델
- AIXON 내부 `paper_id` 1개에 외부 식별자 N개를 1:N으로 붙인다.
- 테이블 예: `paper_identifier(paper_id, scheme, value, source, role, first_seen, last_verified, status)`
  - `scheme`: `arxiv`(버전 없음), `arxiv_version`, `doi`, `s2_paper`, `s2_corpus`, `openalex_work`, `mag`, `dblp`, `acl`, `openreview_forum`
  - `role`: `preprint`, `published`, `duplicate`, `merged_away`, `misattributed`
  - `status`: `active`, `404`, `suspect`
- **OpenAlex work는 반드시 N개를 허용**한다(ResNet 2, DeiT 3). work마다 `role`을 기록한다. 예: BERT W2896457183은 `misattributed`이고 인용 엣지에만 사용한다.
- **필드별 원천 우선순위** (제안, 필드마다 `source`와 `license`를 저장):

  | 필드 | 우선 원천 |
  |---|---|
  | 제목, 저자, 초록, v1 날짜, 버전, 분류, 라이선스 | arXiv (메타데이터 CC0) |
  | venue, 연도, 쪽수 | DBLP 학회 레코드 (CC0) > Crossref (DOI가 있는 venue) > OpenReview (ICLR 등) > S2 `publicationVenue` |
  | 출판 DOI | Crossref에서 검증한 출판사 DOI. Crossref 제목과 1저자가 일치할 때만 채택 |
  | arXiv DOI | `10.48550/arXiv.{id}`를 계산하고, 필요하면 DataCite로 존재 확인 |

- **OpenAlex의 `display_name`·`doi`·`publication_date`·`type`은 정답으로 쓰지 않는다.** 다음 경우 `suspect`로 표시한다.
  - 정규화한 제목이 arXiv 제목과 다를 때 (BERT 사례)
  - DOI prefix가 예상한 등록기관이나 출판사와 다를 때 (10.65215, 10.57702, 10.4230 사례)
  - `publication_year`가 arXiv v1 연도보다 2년 이상 늦을 때 (Transformer 2025, BatchNorm 2024 사례)

### 5.2 해석(resolution) 파이프라인 (정확도 우선, 큐레이터 확인 포함)
1. **입력**: arXiv ID, DOI, 제목 중 하나.
2. **arXiv API `id_list`**: 버전, v1 `<published>`, comment, 라이선스를 가져온다. OAI의 `<created>`는 v1 날짜로 쓰지 않는다.
3. **S2 `POST /paper/batch`** (`ARXIV:`/`DOI:`, 500개 단위): paperId, CorpusId, `externalIds`(DOI/DBLP/MAG/ACL), venue를 가져온다. S2 year와 venue 연도가 다르면 기록한다.
4. **OpenAlex**
   - `filter=doi:<arXiv DOI>|<출판 DOI>|…`: 100개당 1 credit
   - `search=<제목>`: 10 credits
   - 결과에서 제목과 1저자가 맞는 work를 **모두** 수집하고, `locations[].id`(`pmh:oai:arXiv.org:{id}`, `doi:…`, `mag:…`)도 저장한다.
5. **DBLP**: API가 막혀 있으므로 `dblp.xml.gz`(1.1 GB)를 월 1회 받아 로컬에 색인한다. CoRR key와 학회 key를 모두 저장한다(S2는 하나만 준다).
6. **Crossref**: 출판사 DOI만 조회해 venue, 날짜, 쪽수, 등록된 참고문헌을 가져온다. 제목 검색 결과는 재등록·스팸 DOI 때문에 신뢰하지 않는다.
7. **충돌이 있으면** 사람 검토 큐로 보낸다. 커버리지보다 정확도가 우선이다.
- S2의 MAG ID를 OpenAlex 키로 쓸 때는 `W{MAG}`를 먼저 조회하고, 404면 `/locations?filter=native_id:{MAG}`를 조회한다. 그래도 없으면 쓰지 않는다(§3.7, 4/12가 없음).

### 5.3 인용 엣지 수집 (큐레이션된 논문 사이)
- **두 소스를 모두 받는다.**
  - S2: batch `references.paperId,references.externalIds,references.title`. 근거가 필요한 엣지는 `/references?fields=contexts,intents,isInfluential`로 보강한다.
  - OpenAlex: 인용하는 논문의 **모든** work에서 `referenced_works`를 가져와, 큐레이션된 논문의 **모든** work ID와 해석된 alias로 매칭한다.
- **엣지 상태**: `verified`(원문 참고문헌으로 확인), `s2_only`, `oa_only`, `refuted`. 표시와 분석 기본값은 `verified`다.
- **원문 검증**
  - arXiv HTML `ltx_bibitem`을 받아(3초 간격) 해당 항목 텍스트를 **증거 스니펫**으로 저장한다.
  - HTML이 없으면 ar5iv를 쓴다(단일 버전만 제공). 그것도 없으면 Crossref 참고문헌이나 수동 확인으로 넘어간다.
- **알려진 실패 유형에 규칙을 둔다.**
  - S2: 같은 1저자와 연도의 다른 논문으로 잘못 연결된다(He 2015, Krizhevsky). 인용 대상이 인용하는 논문보다 늦으면 자동으로 `refuted`(BatchNorm→ResNet).
  - OpenAlex: 끊긴 ID와 쪼개진 work 때문에 누락이 생긴다.
  - S2: 출판사 차단으로 참고문헌이 0건일 수 있다(ACM, IEEE 일부).
- S2의 `contexts`, `intents`, `isInfluential`은 선택적 근거 속성으로만 쓴다. intent는 대부분 비어 있다.

### 5.4 토픽과 분야
- OpenAlex **Concepts는 쓰지 않는다**(동결).
- OpenAlex **Topics는 보조 facet으로만** 쓰고, `topic_id`, `score`, `observed_at`, 분류기 버전을 함께 저장한다. 2026년 10월 분류기 교체는 `updated_date`를 바꾸지 않았으므로 큐레이션 대상의 topics를 주기적으로 전부 다시 받는다.
- AI 세부 개념(Method/Concept)은 AIXON이 직접 큐레이션한다. 시드로는 arXiv 분류(저자가 선택한 값), S2 `s2FieldsOfStudy`(거친 분류), PwC methods 아카이브(CC BY-SA, 출처 표기, share-alike 주의)를 쓴다.

### 5.5 증분 업데이트 (수십에서 수천 편 규모)
- **ID 단위 폴링이면 충분하다.**

  | 소스 | 방법 | 주기 |
  |---|---|---|
  | S2 | batch 500개/회 | 주 1회 |
  | OpenAlex | singleton(무료) 또는 OR 필터(100개당 1 credit) | 월 1회 |
  | arXiv | `id_list`로 새 버전 감지. 필요하면 OAI-PMH 증분(set=cs, 마지막 datestamp부터) | — |
  | DBLP | 덤프 | 월 1회 |

- OpenAlex의 유료 동기화 필터(`from_updated_date`)와 스냅샷(750 GB)은 필요 없다.
- **OpenAlex 404**(병합·삭제)는 리다이렉트가 없다. DOI 필터나 제목으로 다시 해석하고 이전 ID는 `merged_away`로 남긴다. 무료 공개 버킷의 `deleted_ids.csv.gz`(약 160 MB, 누적)를 대조용으로 쓸 수 있다.
- 원본 JSON 스냅샷을 `fetched_at`, 소스, 엔드포인트와 함께 보관한다(재현성과 증거). 선택한 필드의 해시로 상류 변경을 감지한다.

### 5.6 키 없는 레이트리밋 정책

| 소스 | 정책 |
|---|---|
| arXiv | 3초에 1회, 연결 1개 |
| Crossref (공개 풀) | 단건 5 rps, 목록 1 rps |
| OpenAlex | 초당 10 이하, 하루 1,000 credits (search는 10 credits). 키 없는 예산은 IP 단위로 공유되는 것으로 보임 (추론) |
| S2 | 1 rps 이하 + 지수 백오프 (관측 429율 약 50%) |
| DataCite, HF | 5분당 500 |
| OpenReview | 게스트 차단. forum id는 OpenAlex landing URL이나 수동으로 확보 |
| DBLP | 덤프 사용 |

- 사용자 결정 사항: OpenAlex 무료 키($1/일, cursor)와 S2 키(1 RPS 보장)는 계정이나 email이 필요해 현재 규칙 밖이다. 도입하면 운영 안정성이 크게 오른다(**추론**).

### 5.7 라이선스와 출처 표기
- 로컬 개인 사용 기준으로 OpenAlex, arXiv 메타데이터, DBLP, DataCite, OpenReview 메타데이터는 CC0이고, Crossref 메타데이터도 사실상 자유다.
- 초록은 arXiv(CC0)를 우선한다. Crossref 초록은 저작권 대상일 수 있고, S2 초록은 "legal reasons"로 빠질 수 있다.
- arXiv PDF와 소스는 라이선스가 허용할 때만 저장·서비스하고, 기본은 arXiv로 링크한다 [AX-tou].
- UI와 문서에 "Semantic Scholar" 출처를 표기한다 [S2-license]. OpenReview 리뷰를 인용하면 CC BY 4.0 출처를 표기한다. PwC 파생 데이터를 재배포하면 CC BY-SA를 따른다.

---

## 6. API 호출과 실패 기록 (2026-10-14 16:00–16:45 UTC)

| 소스 | 요청 수 | 결과와 특이사항 |
|---|---|---|
| OpenAlex | 59 | 모두 응답. 의도한 404 검증 4건(W2964308564, W2963069010, W1799366690, `/locations/mag:1799366690`). 키 없는 잔여 예산 1000 → 358 credits (다른 프로세스와 공유된 것으로 추정) |
| Semantic Scholar | 27 | 성공 12, **429 14회**, 401 1회(Datasets 다운로드 "A valid API key is required"). DeiT 단건 재조회는 4번 시도 모두 429로 실패 |
| Crossref | 6 | 모두 200 (`x-api-pool: public-single` / `public-array`) |
| DataCite | 2 | 모두 200 |
| arXiv API / OAI-PMH | 1 / 2 | 모두 200 |
| DBLP | 4 | search API 3회 모두 **HTTP 202 Anubis 챌린지**. XML 덤프 HEAD 200 |
| OpenReview | 3 | 모두 **403 `ChallengeRequiredError`** |
| Hugging Face | 3 | papers API, dataset API, openapi.json 모두 200 |
| Papers with Code | 2 | 302 → HF trending |
| **합계 (데이터 API)** | **109** | 지침 ~60건 초과. 주된 이유는 OpenAlex 끊긴 참조 검증(약 30건)과 S2 429 재시도(14건) |
| 검증용 웹 페이지 (arXiv HTML, ar5iv) | 21 | 3.5초 이상 간격, 모두 200 |

---

## 7. 출처 (모두 확인 2026-10-15)

**OpenAlex**
- [OA-auth] https://help.openalex.org/api/authentication/ (확인 2026-10-15)
- [OA-pricing] https://help.openalex.org/access/pricing/ (확인 2026-10-15)
- [OA-costs] https://help.openalex.org/access/example-costs/ (확인 2026-10-15)
- [OA-snapshot] https://help.openalex.org/access/snapshot/ (확인 2026-10-15)
- [OA-sync] https://help.openalex.org/access/sync/ (확인 2026-10-15)
- [OA-topics] https://help.openalex.org/data/topics/ (확인 2026-10-15)
- [OA-concepts] https://help.openalex.org/data/concepts/ (확인 2026-10-15)
- [OA-deprec] https://help.openalex.org/api/deprecations/ (확인 2026-10-15)
- [OA-single] https://help.openalex.org/api/get-single-entities/ (확인 2026-10-15)
- [OA-dois] https://help.openalex.org/data/works/dois/ (확인 2026-10-15)
- [OA-cites] https://help.openalex.org/data/works/citations/ (확인 2026-10-15)
- [OA-locs] https://help.openalex.org/data/locations/ (확인 2026-10-15)
- [OA-works] https://help.openalex.org/data/works/ (확인 2026-10-15)
- [OA-corpus] https://help.openalex.org/data/works/corpus/ (확인 2026-10-15)
- [OA-unpaywall] https://help.openalex.org/access/unpaywall/ (확인 2026-10-15)
- [OA-blog-pricing] https://blog.openalex.org/openalex-api-new-features-and-usage-based-pricing/ (2026-02-24 게시, 확인 2026-10-15)
- [OA-blog-walden] https://blog.openalex.org/openalex-rewrite-walden-launch/ (2025-11-03 게시, 확인 2026-10-15)
- 색인: https://help.openalex.org/llms.txt (확인 2026-10-15). developers.openalex.org는 help.openalex.org로 리다이렉트된다.
- [OA-API] 실측: https://api.openalex.org/works/doi:10.48550/arXiv.2010.11929 , https://api.openalex.org/works?filter=doi:… , https://api.openalex.org/works?search=… , https://api.openalex.org/locations/mag:2964308564 , https://api.openalex.org/topics?per-page=1 (확인 2026-10-15)

**arXiv**
- [AX-tou] https://info.arxiv.org/help/api/tou.html (확인 2026-10-15)
- [AX-bulk] https://info.arxiv.org/help/bulk_data.html (확인 2026-10-15)
- [AX-s3] https://info.arxiv.org/help/bulk_data_s3.html (확인 2026-10-15)
- [AX-oai] https://info.arxiv.org/help/oa/index.html (확인 2026-10-15)
- [AX-license] https://info.arxiv.org/help/license/index.html (확인 2026-10-15)
- [AX-html] https://info.arxiv.org/about/accessible_HTML.html (확인 2026-10-15)
- [AX-doi] https://blog.arxiv.org/2022/02/17/new-arxiv-articles-are-now-automatically-assigned-dois/ (확인 2026-10-15)
- [AR5IV] https://ar5iv.labs.arxiv.org/ , https://ar5iv.arxiv.org/ (확인 2026-10-15)
- [AX-API] 실측: https://export.arxiv.org/api/query?id_list=2010.11929,1512.03385,1706.03762,1810.04805 , https://oaipmh.arxiv.org/oai?verb=GetRecord&identifier=oai:arXiv.org:1706.03762&metadataPrefix=arXiv , https://arxiv.org/html/{1409.1556, 1409.0473, 1502.03167, 1512.03385, 1607.06450, 1706.03762, 1805.11604, 1810.04805, 1912.11370, 2010.11929, 2012.12877, 2103.14030} (확인 2026-10-15)

**Semantic Scholar**
- [S2-product] https://www.semanticscholar.org/product/api (확인 2026-10-15)
- [S2-license] https://www.semanticscholar.org/product/api/license (확인 2026-10-15)
- [S2-swagger] https://api.semanticscholar.org/graph/v1/swagger.json (문서 UI: https://api.semanticscholar.org/api-docs/graph) (확인 2026-10-15)
- [S2-datasets] https://api.semanticscholar.org/datasets/v1/release/latest , https://api.semanticscholar.org/datasets/v1/swagger.json (확인 2026-10-15)
- [S2ORC] https://github.com/allenai/s2orc (README) (확인 2026-10-15)
- [S2-paper] https://arxiv.org/html/2301.10140v2 (The Semantic Scholar Open Data Platform. 데이터셋 라이선스 명시는 없음) (확인 2026-10-15)
- 실측: https://api.semanticscholar.org/graph/v1/paper/arXiv:2010.11929?fields=… , https://api.semanticscholar.org/graph/v1/paper/batch , https://api.semanticscholar.org/graph/v1/paper/ARXIV:2010.11929/references?fields=contexts,intents,isInfluential,… , https://api.semanticscholar.org/graph/v1/paper/abd1c342495432171beb7ca8fd9551ef13cbd0ff/references (확인 2026-10-15)

**Crossref**
- [CR-rest] https://www.crossref.org/documentation/retrieve-metadata/rest-api/ (확인 2026-10-15)
- [CR-tips] https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/ (확인 2026-10-15)
- [CR-blog] https://www.crossref.org/blog/announcing-changes-to-rest-api-rate-limits/ (2025-11-05 게시, 확인 2026-10-15)
- [CR-forum] https://community.crossref.org/t/refining-rest-api-limits-for-improved-stability-and-reliability/16137 (2026-07-21 게시, 확인 2026-10-15)
- [CR-plus] https://www.crossref.org/services/metadata-retrieval/metadata-plus/ (확인 2026-10-15)
- 실측: https://api.crossref.org/works/10.1109/CVPR.2016.90 , https://api.crossref.org/works/10.1145/3065386 , https://api.crossref.org/prefixes/10.65215 , https://api.crossref.org/works/10.65215/2q58a426 , https://api.crossref.org/works?query.bibliographic=Attention+Is+All+You+Need+Vaswani (확인 2026-10-15)

**DBLP**
- [DBLP-cc0] https://www.dagstuhl.de/en/dblp/news/2019/license-change-to-cc0 (확인 2026-10-15)
- [DBLP-faq] https://dblp.org/faq/How+to+use+the+dblp+search+API.html , https://dblp1.uni-trier.de/faq/1474706.html (Anubis 때문에 열람 실패, 확인 2026-10-15)
- [DBLP-dump] https://dblp.org/xml/dblp.xml.gz (HEAD) (확인 2026-10-15)
- 실측: https://dblp.org/search/publ/api?q=…&format=json , https://dblp.uni-trier.de/search/publ/api?… , https://dblp.dagstuhl.de/search/publ/api?… (확인 2026-10-15)

**OpenReview**
- [OR-docs] https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-get-all-notes-for-submissions-reviews-rebuttals-etc (확인 2026-10-15)
- [OR-terms] https://openreview.net/legal/terms (2024-09-24 최종 갱신, 확인 2026-10-15)
- 실측: https://api2.openreview.net/notes?id=YicbFdNTTy , https://api.openreview.net/notes?id=YicbFdNTTy (확인 2026-10-15)

**Papers with Code**
- [PWC-repo] https://github.com/paperswithcode/paperswithcode-data (README) (확인 2026-10-15)
- [PWC-hf] https://huggingface.co/datasets/pwc-archive/papers-with-abstracts , https://huggingface.co/api/datasets/pwc-archive/papers-with-abstracts (확인 2026-10-15)
- [PWC-news] https://hyper.ai/en/news/42900 (2차 보도, 비공식, 확인 2026-10-15)
- 실측: https://paperswithcode.com/ (302) (확인 2026-10-15)

**Hugging Face**
- [HF-openapi] https://huggingface.co/.well-known/openapi.json (확인 2026-10-15)
- [HF-rate] https://huggingface.co/docs/hub/rate-limits (확인 2026-10-15)
- 실측: https://huggingface.co/api/papers/2010.11929 (확인 2026-10-15)

**Unpaywall**
- [UPW] https://unpaywall.org/products/api (JS 렌더링 페이지, 문구는 검색 인덱스에서 인용) (확인 2026-10-15), [OA-unpaywall] 참조

**DataCite**
- [DC-rate] https://support.datacite.org/docs/rate-limit (2026-08-07 갱신, 확인 2026-10-15)
- [DC-policy] https://support.datacite.org/docs/datacite-data-file-use-policy (확인 2026-10-15)
- 실측: https://api.datacite.org/dois/10.48550/arXiv.2010.11929 , https://api.datacite.org/dois/10.48550/arXiv.1512.03385 (확인 2026-10-15)
