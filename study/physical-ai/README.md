# Physical AI 공부 로드맵
Self-contained Korean study notebook for the Physical AI roadmap.
Open `index.html` in a Claude Artifact-compatible browser surface.
Run `node selftest.mjs` with Node 22 to verify content and calculation logic.
`index.html` contains the whole UI, embedded JSON content, and pure lab functions.
The `content` JSON block stores metadata, overview, stages, glossary, quizzes, and labs.
Stage resources, tasks, checks, concepts, and roadmapped links are embedded per stage.
Quiz and lab values are copied from `assessments.json`; no network data is fetched.
Progress uses Claude's optional `db` capability and falls back to in-memory state.
The page is designed for publication as a single claude.ai Artifact.
