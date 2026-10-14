# F3 — ViT-family papers: fact verification (BiT, ViT, DeiT, Swin)

Checked 2026-10-15. Quotes are taken from the arXiv HTML full text (the `raw_file` of each block), which renders the latest arXiv version (BiT v3, ViT v2, DeiT v2, Swin v2). All quotes were machine-checked against `BeautifulSoup(html).get_text()` → NFKC → whitespace-collapsed text. Key numbers were also cross-checked in the arXiv PDFs saved next to them (src/*.v2.pdf, src/kolesnikov2019-bit.v3.pdf, src/liu2021-swin.v1.pdf).

Access problems (not resolved, recorded as 미확인): dblp.org (and its mirrors dblp.uni-trier.de / dblp.dagstuhl.de) returned HTTP 202 with an Anubis "Making sure you're not a bot!" proof-of-work page; openreview.net API returned HTTP 403 `{"name":"ChallengeRequiredError","message":"Challenge verification required",...}`; link.springer.com returned a "Client Challenge" page; Semantic Scholar returned HTTP 429 `{"message": "Too Many Requests. Please wait and try again or apply for a key for higher rate limits. ...", "code": "429"}` for 2010.11929 and 2103.14030 on the first try and on all 3 retries (7 s apart). OpenAlex worked without a key.

```yaml
paper: kolesnikov2019-bit
title: "Big Transfer (BiT): General Visual Representation Learning"
authors: ["Alexander Kolesnikov", "Lucas Beyer", "Xiaohua Zhai", "Joan Puigcerver", "Jessica Yung", "Sylvain Gelly", "Neil Houlsby"]
earliest_public_date: 2019-12-24
latest_arxiv_version: v3
venue: "ECCV 2020"
venue_source: "https://api.crossref.org/works/10.1007/978-3-030-58558-7_29"
ids:
  arxiv: "1912.11370"
  doi: "10.1007/978-3-030-58558-7_29"
  arxiv_doi: "10.48550/arXiv.1912.11370"
  openalex:
    - {id: "W3015146382", kind: proceedings, title_as_listed: "Big Transfer (BiT): General Visual Representation Learning"}
  s2: "bc51622358d8eea83248ef29402fe10640d07ba6"
  s2_corpus_id: 214728308
  dblp: "conf/eccv/KolesnikovBZPYG20"
  openreview: "N/A"
openalex_primary_topic: {id: "https://openalex.org/T11307", name: "Domain Adaptation and Few-Shot Learning", subfield: "Artificial Intelligence (https://openalex.org/subfields/1702)", field: "Computer Science (https://openalex.org/fields/17)", domain: "Physical Sciences (https://openalex.org/domains/3)"}
fulltext_url_used: "https://arxiv.org/html/1912.11370"
raw_file: "src/kolesnikov2019-bit.html"
metadata_notes:
  - "arXiv Submission history: v1 Tue, 24 Dec 2019 14:04:11 UTC; v2 Mon, 30 Mar 2020; v3 Tue, 5 May 2020. arXiv comments: 'The first three authors contributed equally. Results on ObjectNet are reported in v3'. No journal-ref on arXiv."
  - "Venue: Crossref record deposited by Springer gives type book-chapter, container-title ['Lecture Notes in Computer Science', 'Computer Vision – ECCV 2020'], pages 491-507, published-online 2020-10-29. The book record (10.1007/978-3-030-58558-7) has subtitle '16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part V'. The LNCS volume number is not in either Crossref record, so it is not confirmed here. The Springer landing page returned a bot 'Client Challenge'."
  - "OpenAlex: the arXiv DOI lookup (works/doi:10.48550/arXiv.1912.11370) resolves to the same merged work W3015146382 (type conference-paper; primary location Springer LNCS, plus arXiv locations). The title.search filter finds only this one work."
  - "Semantic Scholar externalIds: DBLP conf/eccv/KolesnikovBZPYG20, MAG 3015146382, ArXiv 1912.11370, DOI 10.1007/978-3-030-58558-7_29, CorpusId 214728308. S2 gives venue 'European Conference on Computer Vision', year 2019, publicationDate 2019-12-24, pages 491-507. The dblp key comes only from S2, because dblp.org itself was blocked by a bot challenge."
claims:
  - candidate: "BiT INTRODUCES Big Transfer (BiT)."
    verdict: supported
    evidence:
      - {quote: "We scale up pre-training, and propose a simple recipe that we call Big Transfer (BiT).", locator: {section: Abstract}, url: "https://arxiv.org/html/1912.11370"}
      - {quote: "We aim not to introduce a new component or complexity, but to provide a recipe that uses the minimal number of tricks yet attains excellent performance on many tasks.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/1912.11370#S1.p2"}
      - {quote: "Instead, we present BiT-HyperRule, a heuristic to determine all hyperparameters for fine-tuning.", locator: {section: "3.3 Hyperparameter Details", paragraph: 3}, url: "https://arxiv.org/html/1912.11370#S3.SS3.SSSx2.p1"}
    note: "The paper presents BiT as a recipe (scaled-up supervised pre-training, a few chosen components, and the BiT-HyperRule transfer heuristic). It says outright that it adds no new architectural component. Use 'introduces a recipe/model family', not 'introduces an architecture'."
  - candidate: "BiT uses the transfer-learning paradigm of pre-training on large supervised datasets and then fine-tuning on a target task."
    verdict: supported
    evidence:
      - {quote: "We revisit the paradigm of pre-training on large supervised datasets and fine-tuning the model on a target task.", locator: {section: Abstract}, url: "https://arxiv.org/html/1912.11370"}
      - {quote: "We revisit a simple paradigm: pre-train on a large supervised source dataset, and fine-tune the weights on the target task.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/1912.11370#S1.p2"}
      - {quote: "Transfer learning offers a solution: task-specific data and compute are replaced with a pre-training phase.", locator: {section: "1 Introduction", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S1.p1"}
    note: "BiT 'revisits' and scales up an existing paradigm. It does not introduce it. Use USES/REVISITS (or BUILDS_ON), not INTRODUCES."
  - candidate: "BiT's architecture is based on ResNet (ResNet-v2)."
    verdict: supported
    evidence:
      - {quote: "All of our BiT models use a vanilla ResNet-v2 architecture [16], except that we replace all Batch Normalization [21] layers with Group Normalization [60] and use Weight Standardization [43] in all convolutional layers.", locator: {section: "3.3 Hyperparameter Details", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S3.SS3.SSSx1.p1"}
    note: "The quote is under the unnumbered sub-heading 'Upstream Pre-Training' in 3.3. Reference [16] is He et al., 'Identity mappings in deep residual networks' (ECCV 2016)."
  - candidate: "BiT-L (ResNet152x4) is trained on JFT-300M."
    verdict: supported
    evidence:
      - {quote: "BiT-L is trained on the JFT-300M dataset [51, 38, 61].", locator: {section: "3.1 Data for Upstream Training", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S3.SS1.p1"}
      - {quote: "Note: the “-S/M/L” suffix refers to the pre-training datasets size and schedule, not architecture. We train BiT with several architecture sizes, the default (largest) being ResNet152x4.", locator: {section: "3.1 Data for Upstream Training", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S3.SS1.p1"}
      - {quote: "We train ResNet-152 architectures in all datasets, with every hidden layer widened by a factor of four (ResNet152x4).", locator: {section: "3.3 Hyperparameter Details", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S3.SS3.SSSx1.p1"}
    note: "Rewording needed. 'BiT-L' names the pre-training data and schedule (JFT-300M), not an architecture. ResNet152x4 is the default and largest architecture, and the paper also trains R50x1, R50x3, R101x1 and R101x3 (Section 4.1). Safer: 'BiT-L = BiT pre-trained on JFT-300M; its default/headline architecture is ResNet152x4.' ViT's Table 2 labels the BiT-L column 'BiT-L (ResNet152x4)'. JFT-300M: 'around 300 million images with 1.26 labels per image on average'."
  - candidate: "BiT-M is trained on ImageNet-21k."
    verdict: supported
    evidence:
      - {quote: "BiT-M is trained on the full ImageNet-21k dataset [10], a public dataset containing 14.2 million images and 21k classes organized by the WordNet hierarchy.", locator: {section: "3.1 Data for Upstream Training", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S3.SS1.p1"}
      - {quote: "For this, we train three BiT models on three large datasets: ILSVRC-2012 [46] which contains 1.3M images (BiT-S), ImageNet-21k [10] which contains 14M images (BiT-M), and JFT [51] which contains 300M images (BiT-L).", locator: {section: "2.1 Upstream Pre-Training", paragraph: 1}, url: "https://arxiv.org/html/1912.11370#S2.SS1.p1"}
      - {quote: "We also train BiT-M on the public ImageNet-21k dataset, and attain marked improvements over the popular ILSVRC-2012 pre-training.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/1912.11370#S1.p3"}
    note: "Section 2.1 gives 14M images and Section 3.1 gives 14.2 million images for ImageNet-21k."
  - candidate: "BiT uses Group Normalization + Weight Standardization instead of Batch Normalization."
    verdict: supported
    evidence:
      - {quote: "The second component is Group Normalization (GN) [60] and Weight Standardization (WS) [34].", locator: {section: "2.1 Upstream Pre-Training", paragraph: 2}, url: "https://arxiv.org/html/1912.11370#S2.SS1.p2"}
      - {quote: "However, we find that BN is detrimental to Big Transfer for two reasons.", locator: {section: "2.1 Upstream Pre-Training", paragraph: 2}, url: "https://arxiv.org/html/1912.11370#S2.SS1.p2"}
      - {quote: "The results in Table 5 indicate that the GN/WS combination transfers better than BN, so we use GN/WS in all BiT models.", locator: {section: "4.3 Large Batches, Group Normalization, Weight Standardization", paragraph: 4}, url: "https://arxiv.org/html/1912.11370#S4.SS3.p4"}
    note: "The WS citation number differs inside the paper ([34] in 2.1, [43] in 3.3 and 4.3), and each quote keeps its own marker. HTML caveat: in 4.3 paragraph 3 the HTML says 'see Table 5', but the PDF (v3) says 'see Table 4'. Table 4 is the upstream ResNet-50 ablation and Table 5 is VTAB transfer, so do not quote that sentence from the HTML."
results:
  - {benchmark: "ILSVRC-2012", metric: "top-1 accuracy (%)", values: {"BiT-L": "87.54 ± 0.02", "Generalist SOTA": "86.4 [57]", "Specialist SOTA": "88.4 [61]⋆"}, locator: {table: "Table 1"}, conditions: "BiT-L = pre-trained on JFT-300M (default architecture ResNet152x4); single model, single hyperparameter setting per task (BiT-HyperRule); entries are median ± standard deviation across 3 fine-tuning runs; ⋆ = concurrent work. Abstract rounds this to 87.5%.", url: "https://arxiv.org/html/1912.11370#S3.T1"}
  - {benchmark: "CIFAR-10 / CIFAR-100 / Pets / Flowers / VTAB (19 tasks)", metric: "top-1 accuracy (%)", values: {"CIFAR-10": "99.37 ± 0.06", "CIFAR-100": "93.51 ± 0.08", "Pets": "96.62 ± 0.23", "Flowers": "99.63 ± 0.03", "VTAB (19 tasks)": "76.29 ± 1.70"}, locator: {table: "Table 1"}, conditions: "BiT-L column; same conditions as above (median ± std over 3 fine-tuning runs). Generalist SOTA column: 99.0 [19], 91.7 [55], 95.9 [19], 98.8 [55], 70.5 [58]; Specialist SOTA: Pets 97.1 [38], Flowers 97.7 [38].", url: "https://arxiv.org/html/1912.11370#S3.T1"}
  - {benchmark: "ILSVRC-2012 / CIFAR-10 / CIFAR-100 / Pets / Flowers / VTAB-1k (19 tasks)", metric: "top-1 accuracy (%)", values: {"BiT-S (ILSVRC-2012)": "81.30 / 97.51 / 86.21 / 93.97 / 89.89 / 66.87", "BiT-M (ImageNet-21k)": "85.39 / 98.91 / 92.17 / 94.46 / 99.30 / 70.64", "Improvement": "+4.09 / +1.40 / +5.96 / +0.49 / +9.41 / +3.77"}, locator: {table: "Table 2"}, conditions: "Caption: 'Both models are ResNet152x4.' Improvement from ImageNet-21k pre-training over ILSVRC-2012 pre-training.", url: "https://arxiv.org/html/1912.11370#S3.T2"}
  - {benchmark: "ILSVRC-2012 (upstream)", metric: "top-1 accuracy (%)", values: {"Batch Norm. + Plain Conv": "75.6", "Batch Norm. + Weight Std.": "75.8", "Group Norm. + Plain Conv": "70.2", "Group Norm. + Weight Std.": "76.0"}, locator: {table: "Table 4"}, conditions: "ResNet-50 trained from scratch on ILSVRC-2012 with a batch size of 4096.", url: "https://arxiv.org/html/1912.11370#S4.T5"}
  - {benchmark: "VTAB-1k (19 tasks)", metric: "transfer accuracy (%)", values: {"Batch Norm. + Plain Conv": "67.72", "Batch Norm. + Weight Std.": "66.78", "Group Norm. + Plain Conv": "68.77", "Group Norm. + Weight Std.": "70.39"}, locator: {table: "Table 5"}, conditions: "The Table 4 models fine-tuned to the 19 VTAB-1k tasks. The HTML caption says 'models from Table 5'; the PDF (v3) says 'from Table 4'.", url: "https://arxiv.org/html/1912.11370#S4.T5"}
```

```yaml
paper: dosovitskiy2020-vit
title: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"
authors: ["Alexey Dosovitskiy", "Lucas Beyer", "Alexander Kolesnikov", "Dirk Weissenborn", "Xiaohua Zhai", "Thomas Unterthiner", "Mostafa Dehghani", "Matthias Minderer", "Georg Heigold", "Sylvain Gelly", "Jakob Uszkoreit", "Neil Houlsby"]
earliest_public_date: 2020-10-22
latest_arxiv_version: v2
venue: "ICLR 2021 (oral)"
venue_source: "https://iclr.cc/virtual/2021/oral/3458"
ids:
  arxiv: "2010.11929"
  doi: ""
  arxiv_doi: "10.48550/arXiv.2010.11929"
  openalex:
    - {id: "W3094502228", kind: preprint, title_as_listed: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"}
    - {id: "W3119786062", kind: proceedings, title_as_listed: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"}
  s2: "미확인"
  s2_corpus_id: "미확인"
  dblp: "미확인"
  openreview: "YicbFdNTTy"
openalex_primary_topic: {id: "https://openalex.org/T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition (https://openalex.org/subfields/1707)", field: "Computer Science (https://openalex.org/fields/17)", domain: "Physical Sciences (https://openalex.org/domains/3)"}
fulltext_url_used: "https://arxiv.org/html/2010.11929"
raw_file: "src/dosovitskiy2020-vit.html"
metadata_notes:
  - "arXiv Submission history: v1 Thu, 22 Oct 2020 17:55:59 UTC; v2 Thu, 3 Jun 2021. arXiv comments: 'ICLR camera-ready version with 2 small modifications: 1) Added a discussion of CLS vs GAP classifier in the appendix, 2) Fixed an error in exaFLOPs computation in Figure 5 and Table 6 ...'."
  - "Venue: official ICLR 2021 virtual pages https://iclr.cc/virtual/2021/oral/3458 (page title 'ICLR Oral ...') and https://iclr.cc/virtual/2021/poster/3013 (also a poster slot). Both link 'Paper' to https://openreview.net/forum?id=YicbFdNTTy. The v2 PDF header reads 'Published as a conference paper at ICLR 2021'. openreview.net itself returned a challenge page (API: HTTP 403 ChallengeRequiredError), so the OpenReview note was not read directly."
  - "No publisher DOI: neither OpenAlex ICLR work W3119786062 (doi null) nor any other source lists one."
  - "OpenAlex: W3094502228 is the main work (type preprint; arXiv DOI; 21131 citations; returned by works/doi:10.48550/arXiv.2010.11929). W3119786062 is the ICLR record (type conference-paper; source 'International Conference on Learning Representations'; publication_date 2021-05-03; location https://openreview.net/pdf?id=YicbFdNTTy; 449 citations). Both have primary topic T10036."
  - "Semantic Scholar: 미확인 (HTTP 429 on the first try and on all 3 retries). dblp: 미확인 (bot challenge)."
claims:
  - candidate: "ViT INTRODUCES the Vision Transformer."
    verdict: supported
    evidence:
      - {quote: "When pre-trained on large amounts of data and transferred to multiple mid-sized or small image recognition benchmarks (ImageNet, CIFAR-100, VTAB, etc.), Vision Transformer (ViT) attains excellent results compared to state-of-the-art convolutional networks while requiring substantially fewer computational resources to train.", locator: {section: Abstract}, url: "https://arxiv.org/html/2010.11929"}
      - {quote: "Our Vision Transformer (ViT) attains excellent results when pre-trained at sufficient scale and transferred to tasks with fewer datapoints.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://arxiv.org/html/2010.11929#S1.p5"}
    note: ""
  - candidate: "ViT ADAPTS the Transformer from NLP to vision."
    verdict: supported
    evidence:
      - {quote: "While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited.", locator: {section: Abstract}, url: "https://arxiv.org/html/2010.11929"}
      - {quote: "a pure transformer applied directly to sequences of image patches can perform very well on image classification tasks", locator: {section: Abstract}, url: "https://arxiv.org/html/2010.11929"}
      - {quote: "Inspired by the Transformer scaling successes in NLP, we experiment with applying a standard Transformer directly to images, with the fewest possible modifications.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S1.p3"}
      - {quote: "Image patches are treated the same way as tokens (words) in an NLP application.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S1.p3"}
      - {quote: "In model design we follow the original Transformer (Vaswani et al., 2017) as closely as possible.", locator: {section: "3 Method", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S3.p1"}
    note: "Locator correction: 'In model design we follow the original Transformer ...' is the opening paragraph of Section 3 'Method' (before 3.1), not Section 3.1. The next sentence is: 'An advantage of this intentionally simple setup is that scalable NLP Transformer architectures – and their efficient implementations – can be used almost out of the box.'"
  - candidate: "ViT ADDRESSES whether reliance on CNNs is necessary in vision."
    verdict: supported
    evidence:
      - {quote: "In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keeping their overall structure in place.", locator: {section: Abstract}, url: "https://arxiv.org/html/2010.11929"}
      - {quote: "We show that this reliance on CNNs is not necessary and a pure transformer applied directly to sequences of image patches can perform very well on image classification tasks.", locator: {section: Abstract}, url: "https://arxiv.org/html/2010.11929"}
    note: "The claim is scoped to image classification and depends on large-scale pre-training (Section 1, paragraphs 4-5). The paper also studies CNN+ViT hybrids (Section 3.1, 'Hybrid Architecture.'), so it does not reject CNNs altogether."
  - candidate: "ViT INTRODUCES patch embedding (image -> sequence of flattened 2D patches -> trainable linear projection -> 'patch embeddings')."
    verdict: partially_supported
    evidence:
      - {quote: "The standard Transformer receives as input a 1D sequence of token embeddings.", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p1"}
      - {quote: "To handle 2D images, we reshape the image", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p1"}
      - {quote: "into a sequence of flattened 2D patches", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p1"}
      - {quote: "dimensions with a trainable linear projection (Eq. 1). We refer to the output of this projection as the patch embeddings.", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p1"}
      - {transcription: 'we reshape the image \mathbf{x}\in\mathbb{R}^{H\times W\times C} into a sequence of flattened 2D patches \mathbf{x}_{p}\in\mathbb{R}^{N\times(P^{2}\cdot C)} ... N=HW/P^{2} ... map to D dimensions with a trainable linear projection', flag: transcribed, locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p1"}
      - {quote: "Most related to ours is the model of Cordonnier et al. (2020), which extracts patches of size", locator: {section: "2 Related Work", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S2.p3"}
      - {quote: "from the input image and applies full self-attention on top. This model is very similar to ViT, but our work goes further to demonstrate that large scale pre-training makes vanilla transformers competitive with (or even better than) state-of-the-art CNNs.", locator: {section: "2 Related Work", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S2.p3"}
    note: "Supported: ViT defines its own patch-embedding input (flattened P×P patches, trainable linear projection E, output named 'patch embeddings'). Not supported as 'first to introduce': the paper calls Cordonnier et al. (2020), which uses 2×2 patches with full self-attention, 'very similar to ViT'. Safer relations: DEFINES/USES patch embedding, or 'introduces patch embedding as ViT's input representation'. The transcription is LaTeX taken from the HTML alttext."
  - candidate: "ViT borrows the [class] token from BERT; its output state serves as the image representation."
    verdict: supported
    evidence:
      - {quote: "Similar to BERT’s [class] token, we prepend a learnable embedding to the sequence of embedded patches", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p2"}
      - {quote: "whose state at the output of the Transformer encoder", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p2"}
      - {quote: "serves as the image representation", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p2"}
      - {transcription: '(\mathbf{z}_{0}^{0}=\mathbf{x}_{\text{class}}), whose state at the output of the Transformer encoder (\mathbf{z}^{0}_{L}) serves as the image representation \mathbf{y} (Eq. 4)', flag: transcribed, locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p2"}
      - {quote: "The classification head is implemented by a MLP with one hidden layer at pre-training time and by a single linear layer at fine-tuning time.", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p2"}
    note: "The apostrophe in 'BERT’s' is U+2019 in the source. The sentence is broken by inline math, so it is quoted in three pieces plus a transcription."
  - candidate: "ViT adds learnable 1D position embeddings to the patch embeddings."
    verdict: supported
    evidence:
      - {quote: "Position embeddings are added to the patch embeddings to retain positional information. We use standard learnable 1D position embeddings, since we have not observed significant performance gains from using more advanced 2D-aware position embeddings (Appendix D.4).", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p3"}
    note: ""
  - candidate: "ViT encoder: alternating MSA and MLP blocks; LayerNorm before every block, residual connections after every block."
    verdict: supported
    evidence:
      - {quote: "The Transformer encoder (Vaswani et al., 2017) consists of alternating layers of multiheaded self-attention (MSA, see Appendix A) and MLP blocks (Eq. 2, 3).", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p4"}
      - {quote: "Layernorm (LN) is applied before every block, and residual connections after every block (Wang et al., 2019; Baevski & Auli, 2019).", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p4"}
      - {quote: "The MLP contains two layers with a GELU non-linearity.", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.SS1.p4"}
    note: "This is pre-LN placement (LN inside the residual branch, before MSA/MLP), as Eqs. (2)-(3) show."
  - candidate: "ViT model equations (1)-(4)."
    verdict: supported
    evidence:
      - {transcription: '(1) \mathbf{z}_{0}=[\mathbf{x}_{\text{class}};\,\mathbf{x}^{1}_{p}\mathbf{E};\,\mathbf{x}^{2}_{p}\mathbf{E};\cdots;\,\mathbf{x}^{N}_{p}\mathbf{E}]+\mathbf{E}_{pos},\quad \mathbf{E}\in\mathbb{R}^{(P^{2}\cdot C)\times D},\,\mathbf{E}_{pos}\in\mathbb{R}^{(N+1)\times D}', flag: transcribed, locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.EGx1"}
      - {transcription: '(2) \mathbf{z^{\prime}}_{\ell}=\operatorname{MSA}(\operatorname{LN}(\mathbf{z}_{\ell-1}))+\mathbf{z}_{\ell-1},\quad \ell=1\ldots L', flag: transcribed, locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.EGx1"}
      - {transcription: '(3) \mathbf{z}_{\ell}=\operatorname{MLP}(\operatorname{LN}(\mathbf{z^{\prime}}_{\ell}))+\mathbf{z^{\prime}}_{\ell},\quad \ell=1\ldots L', flag: transcribed, locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.EGx1"}
      - {transcription: '(4) \mathbf{y}=\operatorname{LN}(\mathbf{z}_{L}^{0})', flag: transcribed, locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S3.EGx1"}
    note: "Display equations (1)-(4) close paragraph 4 of Section 3.1 (HTML equation group id S3.EGx1). The LaTeX is copied from the HTML alttext attributes; alignment '&'/\\displaystyle removed."
  - candidate: "ViT inductive bias: much less image-specific inductive bias than CNNs; with mid-sized data (ImageNet, no strong regularization) accuracy a few points below comparable ResNets; Transformers lack translation equivariance/locality and generalize poorly with insufficient data; 'large scale training trumps inductive bias'."
    verdict: supported
    evidence:
      - {quote: "We note that Vision Transformer has much less image-specific inductive bias than CNNs.", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 5}, url: "https://arxiv.org/html/2010.11929#S3.SS1.SSS0.Px1.p1"}
      - {quote: "In CNNs, locality, two-dimensional neighborhood structure, and translation equivariance are baked into each layer throughout the whole model. In ViT, only MLP layers are local and translationally equivariant, while the self-attention layers are global.", locator: {section: "3.1 Vision Transformer (ViT)", paragraph: 5}, url: "https://arxiv.org/html/2010.11929#S3.SS1.SSS0.Px1.p1"}
      - {quote: "When trained on mid-sized datasets such as ImageNet without strong regularization, these models yield modest accuracies of a few percentage points below ResNets of comparable size.", locator: {section: "1 Introduction", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S1.p4"}
      - {quote: "Transformers lack some of the inductive biases inherent to CNNs, such as translation equivariance and locality, and therefore do not generalize well when trained on insufficient amounts of data.", locator: {section: "1 Introduction", paragraph: 4}, url: "https://arxiv.org/html/2010.11929#S1.p4"}
      - {quote: "However, the picture changes if the models are trained on larger datasets (14M-300M images). We find that large scale training trumps inductive bias.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://arxiv.org/html/2010.11929#S1.p5"}
    note: "Paragraph 5 of 3.1 is the one headed 'Inductive bias.'. Exact wording is 'lack some of the inductive biases', not 'lack the inductive biases'."
  - candidate: "ViT model variants (Table 1): ViT-Base/Large/Huge."
    verdict: supported
    evidence:
      - {quote: "We base ViT configurations on those used for BERT (Devlin et al., 2019), as summarized in Table 1.", locator: {section: "4.1 Setup", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S4.SS1.p3"}
      - {quote: "The “Base” and “Large” models are directly adopted from BERT and we add the larger “Huge” model.", locator: {section: "4.1 Setup", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S4.SS1.p3"}
    note: "Values are in results (Table 1). Notation: 'ViT-L/16 means the “Large” variant with 16×16 input patch size'. That sentence contains math in the HTML, so it is not quoted."
  - candidate: "ViT pre-training datasets: ImageNet-21k and JFT (Sun et al., 2017) — classes/images."
    verdict: supported
    evidence:
      - {quote: "its superset ImageNet-21k with 21k classes and 14M images (Deng et al., 2009), and JFT (Sun et al., 2017) with 18k classes and 303M high-resolution images.", locator: {section: "4.1 Setup", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S4.SS1.p1"}
      - {quote: "To explore model scalability, we use the ILSVRC-2012 ImageNet dataset with 1k classes and 1.3M images (we refer to it as ImageNet in what follows),", locator: {section: "4.1 Setup", paragraph: 1}, url: "https://arxiv.org/html/2010.11929#S4.SS1.p1"}
    note: "Elsewhere the paper calls JFT 'the in-house JFT-300M dataset' (Section 1). 4.1 gives 303M images and 18k classes."
  - candidate: "ViT 'attention distance' is analogous to receptive field size in CNNs (Section 4.5)."
    verdict: supported
    evidence:
      - {quote: "Specifically, we compute the average distance in image space across which information is integrated, based on the attention weights (Figure 7, right). This “attention distance” is analogous to receptive field size in CNNs.", locator: {section: "4.5 Inspecting Vision Transformer", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S4.SS5.p3"}
      - {quote: "We find that some heads attend to most of the image already in the lowest layers, showing that the ability to integrate information globally is indeed used by the model.", locator: {section: "4.5 Inspecting Vision Transformer", paragraph: 3}, url: "https://arxiv.org/html/2010.11929#S4.SS5.p3"}
    note: "The same sentence ('This “attention distance” is analogous to receptive field size in CNNs.') also appears in Appendix D.7 'Attention Distance', paragraph 1."
  - candidate: "Appendix A: multihead self-attention; D_h is typically set to D/k."
    verdict: supported
    evidence:
      - {quote: "Multihead self-attention (MSA) is an extension of SA in which we run", locator: {section: "A Multihead Self-attention", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#A1.p2"}
      - {quote: "self-attention operations, called “heads”, in parallel, and project their concatenated outputs.", locator: {section: "A Multihead Self-attention", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#A1.p2"}
      - {quote: "To keep compute and number of parameters constant when changing", locator: {section: "A Multihead Self-attention", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#A1.p2"}
      - {transcription: 'To keep compute and number of parameters constant when changing k, D_{h} (Eq. 5) is typically set to D/k.  (8) \operatorname{MSA}(\mathbf{z})=[\operatorname{SA}_{1}(z);\operatorname{SA}_{2}(z);\cdots;\operatorname{SA}_{k}(z)]\,\mathbf{U}_{msa},\quad \mathbf{U}_{msa}\in\mathbb{R}^{k\cdot D_{h}\times D}', flag: transcribed, locator: {section: "A Multihead Self-attention", paragraph: 2}, url: "https://arxiv.org/html/2010.11929#A1.p2"}
    note: "k = number of heads; D_h is from Eq. (5): [q,k,v]=zU_qkv, U_qkv ∈ R^{D×3D_h}."
results:
  - {benchmark: "model variants", metric: "Layers / Hidden size D / MLP size / Heads / Params", values: {"ViT-Base": "12 / 768 / 3072 / 12 / 86M", "ViT-Large": "24 / 1024 / 4096 / 16 / 307M", "ViT-Huge": "32 / 1280 / 5120 / 16 / 632M"}, locator: {table: "Table 1"}, conditions: "Table 1: Details of Vision Transformer model variants.", url: "https://arxiv.org/html/2010.11929#S4.T1"}
  - {benchmark: "ImageNet", metric: "top-1 accuracy (%), mean ± std", values: {"Ours-JFT (ViT-H/14)": "88.55 ± 0.04", "Ours-JFT (ViT-L/16)": "87.76 ± 0.03", "Ours-I21k (ViT-L/16)": "85.30 ± 0.02", "BiT-L (ResNet152x4)": "87.54 ± 0.02", "Noisy Student (EfficientNet-L2)": "88.4/88.5∗"}, locator: {table: "Table 2"}, conditions: "Mean and standard deviation over three fine-tuning runs (caption). Ours-JFT = pre-trained on JFT-300M, Ours-I21k = pre-trained on ImageNet-21k. For ImageNet in Table 2, fine-tuned at higher resolution, 512 for ViT-L/16 and 518 for ViT-H/14, with Polyak averaging factor 0.9999 (Section 4.1, transcribed from math). ∗ = 'Slightly improved 88.5% result reported in Touvron et al. (2020)'. The BiT-L numbers match BiT's own Table 1, which BiT describes as median ± std.", url: "https://arxiv.org/html/2010.11929#S4.T2"}
  - {benchmark: "ImageNet ReaL", metric: "top-1 accuracy (%)", values: {"Ours-JFT (ViT-H/14)": "90.72 ± 0.05", "Ours-JFT (ViT-L/16)": "90.54 ± 0.03", "Ours-I21k (ViT-L/16)": "88.62 ± 0.05", "BiT-L (ResNet152x4)": "90.54", "Noisy Student (EfficientNet-L2)": "90.55"}, locator: {table: "Table 2"}, conditions: "Same as the ImageNet row.", url: "https://arxiv.org/html/2010.11929#S4.T2"}
  - {benchmark: "CIFAR-10 / CIFAR-100", metric: "accuracy (%)", values: {"Ours-JFT (ViT-H/14)": "99.50 ± 0.06 / 94.55 ± 0.04", "Ours-JFT (ViT-L/16)": "99.42 ± 0.03 / 93.90 ± 0.05", "Ours-I21k (ViT-L/16)": "99.15 ± 0.03 / 93.25 ± 0.05", "BiT-L (ResNet152x4)": "99.37 ± 0.06 / 93.51 ± 0.08", "Noisy Student (EfficientNet-L2)": "− / −"}, locator: {table: "Table 2"}, conditions: "Mean ± std over three fine-tuning runs.", url: "https://arxiv.org/html/2010.11929#S4.T2"}
  - {benchmark: "Oxford-IIIT Pets / Oxford Flowers-102 / VTAB (19 tasks)", metric: "accuracy (%)", values: {"Ours-JFT (ViT-H/14)": "97.56 ± 0.03 / 99.68 ± 0.02 / 77.63 ± 0.23", "Ours-JFT (ViT-L/16)": "97.32 ± 0.11 / 99.74 ± 0.00 / 76.28 ± 0.46", "Ours-I21k (ViT-L/16)": "94.67 ± 0.15 / 99.61 ± 0.02 / 72.72 ± 0.21", "BiT-L (ResNet152x4)": "96.62 ± 0.23 / 99.63 ± 0.03 / 76.29 ± 1.70", "Noisy Student (EfficientNet-L2)": "− / − / −"}, locator: {table: "Table 2"}, conditions: "Mean ± std over three fine-tuning runs.", url: "https://arxiv.org/html/2010.11929#S4.T2"}
  - {benchmark: "pre-training compute", metric: "TPUv3-core-days", values: {"Ours-JFT (ViT-H/14)": "2.5k", "Ours-JFT (ViT-L/16)": "0.68k", "Ours-I21k (ViT-L/16)": "0.23k", "BiT-L (ResNet152x4)": "9.9k", "Noisy Student (EfficientNet-L2)": "12.3k"}, locator: {table: "Table 2"}, conditions: "'the number of TPU v3 cores (2 per chip) used for training multiplied by the training time in days' (Section 4.2).", url: "https://arxiv.org/html/2010.11929#S4.T2"}
```

```yaml
paper: touvron2020-deit
title: "Training data-efficient image transformers & distillation through attention"
authors: ["Hugo Touvron", "Matthieu Cord", "Matthijs Douze", "Francisco Massa", "Alexandre Sablayrolles", "Hervé Jégou"]
earliest_public_date: 2020-12-23
latest_arxiv_version: v2
venue: "ICML 2021 (PMLR 139)"
venue_source: "https://proceedings.mlr.press/v139/touvron21a.html"
ids:
  arxiv: "2012.12877"
  doi: ""
  arxiv_doi: "10.48550/arXiv.2012.12877"
  openalex:
    - {id: "W4394668313", kind: preprint, title_as_listed: "Training data-efficient image transformers & distillation through attention"}
    - {id: "W3116489684", kind: preprint, title_as_listed: "Training data-efficient image transformers & distillation through attention"}
    - {id: "W4376983091", kind: proceedings, title_as_listed: "Training data-efficient image transformers & distillation through attention"}
  s2: "ad7ddcc14984caae308c397f1a589aae75d4ab71"
  s2_corpus_id: 229363322
  dblp: "journals/corr/abs-2012-12877"
  openreview: "N/A"
openalex_primary_topic: {id: "https://openalex.org/T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition (https://openalex.org/subfields/1707)", field: "Computer Science (https://openalex.org/fields/17)", domain: "Physical Sciences (https://openalex.org/domains/3)"}
fulltext_url_used: "https://arxiv.org/html/2012.12877"
raw_file: "src/touvron2020-deit.html"
metadata_notes:
  - "arXiv Submission history: v1 Wed, 23 Dec 2020 18:42:10 UTC; v2 Fri, 15 Jan 2021. No comments or journal-ref on arXiv."
  - "Venue: the PMLR page reads 'Proceedings of the 38th International Conference on Machine Learning, PMLR 139:10347-10357, 2021.' (citation_firstpage 10347, citation_lastpage 10357, citation_publication_date 2021/07/01). The PMLR page lists no DOI. PMLR spells the last author 'Herve Jegou' without diacritics."
  - "OpenAlex has three works and none has PMLR as its source. W4394668313: type preprint, doi 10.48550/arxiv.2012.12877, returned by works/doi lookup, 151 citations; treated here as the main work. W3116489684: type preprint, MAG id, arXiv landing page, no DOI, 992 citations (most cited). W4376983091: type conference-paper, HAL record hal-03997937, raw source 'ICML, Jul 2021, visio, France'. All three have primary topic T10036. OpenAlex spells the last author 'Hervé Jeǵou' (a diacritic error)."
  - "Semantic Scholar: venue 'International Conference on Machine Learning', journal.pages 10347-10357, year 2020, publicationDate 2020-12-23; externalIds ArXiv 2012.12877, DBLP journals/corr/abs-2012-12877 (this is the CoRR record). The dblp key of the ICML record is 미확인 (dblp.org bot challenge)."
  - "ABSTRACT VERSION WARNING: the arXiv listing (abs-page metadata) abstract differs from the abstract in the paper itself. The listing says 'However, these visual transformers are pre-trained with hundreds of millions of images using an expensive infrastructure', 'we produce a competitive convolution-free transformer' and '83.1% (single-crop evaluation)'. The v2 paper (HTML and PDF) says 'These high-performing vision transformers ... using a large infrastructure', 'competitive convolution-free transformers' and '83.1% (single-crop)'. The PMLR abstract is a third, reworded version. Quotes below follow the paper text."
claims:
  - candidate: "DeiT INTRODUCES DeiT (Data-efficient image Transformers) and the distillation token."
    verdict: supported
    evidence:
      - {quote: "More importantly, we introduce a teacher-student strategy specific to transformers. It relies on a distillation token ensuring that the student learns from the teacher through attention.", locator: {section: Abstract}, url: "https://arxiv.org/html/2012.12877"}
      - {quote: "With our Data-efficient image Transformers (DeiT), we report large improvements over previous results, see Figure 1.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2012.12877#S1.p3"}
      - {quote: "We introduce a new distillation procedure based on a distillation token, which plays the same role as the class token, except that it aims at reproducing the label estimated by the teacher.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://arxiv.org/html/2012.12877#S1.I1.i2.p1"}
      - {quote: "We add a new token, the distillation token, to the initial embeddings (patches and class token).", locator: {section: "4 Distillation through attention", paragraph: 7}, url: "https://arxiv.org/html/2012.12877#S4.SS0.SSS0.Px3.p1"}
    note: "Introduction paragraph 5 is the contributions list (second bullet). Section 4 paragraph 7 is the paragraph headed 'Distillation token.' (standalone display equations are not counted as paragraphs). HTML caveat: the alembic sign that marks distilled models (DeiT⚗) is an embedded SVG <object>, so it is missing from the extracted text. Quotes avoid spans where it matters."
  - candidate: "DeiT ADDRESSES ViT's need for very large pre-training data / large infrastructure, by training on ImageNet only."
    verdict: supported
    evidence:
      - {quote: "These high-performing vision transformers are pre-trained with hundreds of millions of images using a large infrastructure, thereby limiting their adoption.", locator: {section: Abstract}, url: "https://arxiv.org/html/2012.12877"}
      - {quote: "In this work, we produce competitive convolution-free transformers by training on Imagenet only. We train them on a single computer in less than 3 days.", locator: {section: Abstract}, url: "https://arxiv.org/html/2012.12877"}
      - {quote: "Their paper presented excellent results with transformers trained with a large private labelled image dataset (JFT-300M [46], 300 millions images).", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/2012.12877#S1.p2"}
      - {quote: "The paper concluded that transformers “do not generalize well when trained on insufficient amounts of data”, and the training of these models involved extensive computing resources.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/2012.12877#S1.p2"}
      - {quote: "It uses Imagenet as the sole training set.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2012.12877#S1.p3"}
    note: "The candidate's wording 'large infrastructure' matches the paper and PMLR text. The arXiv listing abstract instead says 'an expensive infrastructure' (see metadata_notes). Independent corroboration from Swin (2103.14030, Related Work paragraph 4): 'While ViT requires large-scale training datasets (i.e., JFT-300M) to perform well, DeiT [63] introduces several training strategies that allow ViT to also be effective using the smaller ImageNet-1K dataset.'"
  - candidate: "DeiT EXTENDS ViT: same/identical architecture; adds training strategies and the distillation token."
    verdict: supported
    evidence:
      - {quote: "As mentioned earlier, our architecture design is identical to the one proposed by Dosovitskiy et al. [15] with no convolutions. Our only differences are the training strategies, and the distillation token.", locator: {section: "5.1 Transformer models", paragraph: 1}, url: "https://arxiv.org/html/2012.12877#S5.SS1.p1"}
      - {quote: "Also we do not use a MLP head for the pre-training but only a linear classifier.", locator: {section: "5.1 Transformer models", paragraph: 1}, url: "https://arxiv.org/html/2012.12877#S5.SS1.p1"}
      - {quote: "If not specified, DeiT refers to our referent model DeiT-B, which has the same architecture as ViT-B.", locator: {section: "5.1 Transformer models", paragraph: 1}, url: "https://arxiv.org/html/2012.12877#S5.SS1.p1"}
      - {quote: "We build upon the visual transformer architecture from Dosovitskiy et al. [15] and improvements included in the timm library [55].", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2012.12877#S1.p3"}
    note: "Reference [15] = Dosovitskiy et al. (ViT). Besides training recipe and distillation token, a third stated difference is a linear classifier instead of an MLP head at pre-training. DeiT-Ti and DeiT-S are new smaller variants that change the number of heads while keeping the per-head dimension d = 64 (Section 5.1, Table 1)."
  - candidate: "DeiT result: 83.1% top-1 on ImageNet with no external data (abstract); comparison to ViT-B/16 trained on ImageNet only."
    verdict: supported
    evidence:
      - {quote: "Our reference vision transformer (86M parameters) achieves top-1 accuracy of 83.1% (single-crop) on ImageNet with no external data.", locator: {section: Abstract}, url: "https://arxiv.org/html/2012.12877"}
      - {quote: "This leads us to report results competitive with convnets for both Imagenet (where we obtain up to 85.2% accuracy) and when transferring to other tasks.", locator: {section: Abstract}, url: "https://arxiv.org/html/2012.12877"}
      - {quote: "These results are a major improvement (+6.3% top-1 in a comparable setting) over previous ViT models trained on Imagenet1k only [15].", locator: {section: "5.3 Efficiency vs accuracy: a comparative study with convnets", paragraph: 3}, url: "https://arxiv.org/html/2012.12877#S5.SS3.p3"}
    note: "Exact abstract wording is '83.1% (single-crop)'. '(single-crop evaluation)' is only in the arXiv listing metadata. The abstract gives no resolution, but Table 5 shows 83.1 is DeiT-B↑384 (86M, fine-tuned at 384²). DeiT-B at 224² is 81.8, and ViT-B/16 [15] (ImageNet only, 384²) is 77.9. 85.2 is the distilled DeiT-B⚗↑384 trained for 1000 epochs. The paper does not show how '+6.3%' is computed, so do not derive it."
  - candidate: "DeiT uses a convnet teacher (RegNetY) and hard(-label) distillation."
    verdict: supported
    evidence:
      - {quote: "We have observed that using a convnet teacher gives better performance than using a transformer.", locator: {section: "5.2 Distillation", paragraph: 2}, url: "https://arxiv.org/html/2012.12877#S5.SS2.SSS0.Px1.p1"}
      - {quote: "In all of our subsequent distillation experiments the default teacher is a RegNetY-16GF [40] (84M parameters) that we trained with the same data and same data-augmentation as DeiT.", locator: {section: "5.2 Distillation", paragraph: 2}, url: "https://arxiv.org/html/2012.12877#S5.SS2.SSS0.Px1.p1"}
      - {quote: "We introduce a variant of distillation where we take the hard decision of the teacher as a true label.", locator: {section: "4 Distillation through attention", paragraph: 4}, url: "https://arxiv.org/html/2012.12877#S4.SS0.SSS0.Px2.p1"}
      - {quote: "Hard distillation significantly outperforms soft distillation for transformers, even when using only a class token", locator: {section: "5.2 Distillation", paragraph: 3}, url: "https://arxiv.org/html/2012.12877#S5.SS2.SSS0.Px2.p1"}
      - {transcription: '\mathcal{L}_{\mathrm{global}}^{\mathrm{hardDistill}}=\frac{1}{2}\mathcal{L}_{\mathrm{CE}}(\psi(Z_{s}),y)+\frac{1}{2}\mathcal{L}_{\mathrm{CE}}(\psi(Z_{s}),y_{\mathrm{t}}),\quad y_{\mathrm{t}}=\mathrm{argmax}_{c}Z_{\mathrm{t}}(c)', flag: transcribed, locator: {section: "4 Distillation through attention", paragraph: 4}, url: "https://arxiv.org/html/2012.12877#S4.SS0.SSS0.Px2.p1"}
    note: "Section 5.2 paragraph 2 is headed 'Convnets teachers.', paragraph 3 is headed 'Comparison of distillation methods.', and Section 4 paragraph 4 is headed 'Hard-label distillation.'. The teacher reaches 82.9% top-1 (inline math in the HTML, so not quoted; Table 2 and Table 5 list RegNetY-16GF at 82.9). The default teacher is RegNetY-16GF; Table 2 also tests RegNetY-4GF/8GF/12GF and a DeiT-B teacher."
results:
  - {benchmark: "ImageNet-1k (ImNet) / ImageNet Real / ImageNet V2 matched frequency", metric: "top-1 accuracy (%)", values: {"ViT-B/16 [15] (86M, 384², 85.9 im/s)": "77.9 / 83.6 / not reported", "ViT-L/16 [15] (307M, 384², 27.3 im/s)": "76.5 / 82.2 / not reported", "DeiT-Ti (5M, 224², 2536.5 im/s)": "72.2 / 80.1 / 60.4", "DeiT-S (22M, 224², 940.4 im/s)": "79.8 / 85.7 / 68.5", "DeiT-B (86M, 224², 292.3 im/s)": "81.8 / 86.7 / 71.5", "DeiT-B↑384 (86M, 384², 85.9 im/s)": "83.1 / 87.7 / 72.4", "DeiT-B⚗ (87M, 224², 290.9 im/s)": "83.4 / 88.3 / 73.2", "DeiT-B⚗ / 1000 epochs (87M, 224², 290.9 im/s)": "84.2 / 88.7 / 73.9", "DeiT-B⚗↑384 (87M, 384², 85.8 im/s)": "84.5 / 89.0 / 74.8", "DeiT-B⚗↑384 / 1000 epochs (87M, 384², 85.8 im/s)": "85.2 / 89.3 / 75.2", "RegNetY-16GF [40]⋆ teacher (84M, 224², 334.7 im/s)": "82.9 / 88.1 / 72.4"}, locator: {table: "Table 5"}, conditions: "Caption: 'for models trained with no external data'. Throughput is images/s on one 16GB V100 GPU. ⚗ = trained with DeiT's distillation, teacher RegNetY-16GF. ↑384 = fine-tuned at 384². ViT rows are as reported in [15] (ViT-B/16 V2 entry blank, '_' in the HTML). ⋆ = RegNet trained with DeiT's optimization procedure. The HTML shows hidden phantom zeros (e.g. '0085.9'); the visible PDF values are given here. Table 7 repeats the ImageNet column (ViT-B/16 77.9; DeiT-B 81.8; DeiT-B↑384 83.1; DeiT-B⚗ 83.4) but lists DeiT-B⚗↑384 as 84.4, while Tables 3 and 5 give 84.5. This internal inconsistency is in both the HTML and the PDF v2.", url: "https://arxiv.org/html/2012.12877#S5.T5"}
  - {benchmark: "DeiT variants", metric: "embedding dim / #heads / #layers / #params / training resolution / throughput (im/s)", values: {"DeiT-Ti": "192 / 3 / 12 / 5M / 224 / 2536", "DeiT-S": "384 / 6 / 12 / 22M / 224 / 940", "DeiT-B (ViT model: ViT-B)": "768 / 12 / 12 / 86M / 224 / 292"}, locator: {table: "Table 1"}, conditions: "Caption: DeiT-B 'has the same architecture as the ViT-B [15]'; dimension per head kept at 64; throughput at 224×224. Phantom zeros removed.", url: "https://arxiv.org/html/2012.12877#S5.T1"}
  - {benchmark: "ImageNet top-1 by distillation method (DeiT-B, 224 / ↑384)", metric: "top-1 accuracy (%)", values: {"DeiT– no distillation": "81.8 / 83.1", "DeiT– usual distillation (soft)": "81.8 / 83.2", "DeiT– hard distillation": "83.0 / 84.0", "DeiT⚗: class embedding": "83.0 / 84.2", "DeiT⚗: distil. embedding": "83.1 / 84.4", "DeiT⚗: class+distillation": "83.4 / 84.5"}, locator: {table: "Table 3"}, conditions: "300 epochs of pre-training. Columns 'B 224' and 'B↑384' only; Ti 224 and S 224 columns omitted here. The class+distillation row is the late fusion of both classifiers.", url: "https://arxiv.org/html/2012.12877#S5.T3"}
```

```yaml
paper: liu2021-swin
title: "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows"
authors: ["Ze Liu", "Yutong Lin", "Yue Cao", "Han Hu", "Yixuan Wei", "Zheng Zhang", "Stephen Lin", "Baining Guo"]
earliest_public_date: 2021-03-25
latest_arxiv_version: v2
venue: "ICCV 2021"
venue_source: "https://openaccess.thecvf.com/content/ICCV2021/html/Liu_Swin_Transformer_Hierarchical_Vision_Transformer_Using_Shifted_Windows_ICCV_2021_paper.html"
ids:
  arxiv: "2103.14030"
  doi: "10.1109/ICCV48922.2021.00986"
  arxiv_doi: "10.48550/arXiv.2103.14030"
  openalex:
    - {id: "W3138516171", kind: proceedings, title_as_listed: "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows"}
  s2: "미확인"
  s2_corpus_id: "미확인"
  dblp: "미확인"
  openreview: "N/A"
openalex_primary_topic: {id: "https://openalex.org/T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition (https://openalex.org/subfields/1707)", field: "Computer Science (https://openalex.org/fields/17)", domain: "Physical Sciences (https://openalex.org/domains/3)"}
fulltext_url_used: "https://arxiv.org/html/2103.14030"
raw_file: "src/liu2021-swin.html"
metadata_notes:
  - "arXiv Submission history: v1 Thu, 25 Mar 2021 17:59:31 UTC; v2 Tue, 17 Aug 2021. No comments or journal-ref on arXiv."
  - "Venue: the CVF open-access page reads 'Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2021, pp. 10012-10022' and lists the title as '... Using Shifted Windows'. Crossref (https://api.crossref.org/works/10.1109/ICCV48922.2021.00986) gives container '2021 IEEE/CVF International Conference on Computer Vision (ICCV)', publisher IEEE, pages 9992-10002, event Montreal, QC, Canada, 2021-10-10 to 2021-10-17. The CVF and IEEE page numbers differ."
  - "OpenAlex: one merged work W3138516171 (type conference-paper, IEEE DOI, plus arXiv locations), returned by both the arXiv-DOI lookup and title search. The title.search filter finds only this one work."
  - "Semantic Scholar: 미확인 (HTTP 429 on the first try and on all 3 retries). dblp: 미확인 (bot challenge)."
claims:
  - candidate: "Swin INTRODUCES the Swin Transformer and shifted-window self-attention."
    verdict: supported
    evidence:
      - {quote: "This paper presents a new vision Transformer, called Swin Transformer, that capably serves as a general-purpose backbone for computer vision.", locator: {section: Abstract}, url: "https://arxiv.org/html/2103.14030"}
      - {quote: "To address these differences, we propose a hierarchical Transformer whose representation is computed with Shifted windows.", locator: {section: Abstract}, url: "https://arxiv.org/html/2103.14030"}
      - {quote: "The shifted windowing scheme brings greater efficiency by limiting self-attention computation to non-overlapping local windows while also allowing for cross-window connection.", locator: {section: Abstract}, url: "https://arxiv.org/html/2103.14030"}
      - {quote: "A key design element of Swin Transformer is its shift of the window partition between consecutive self-attention layers, as illustrated in Figure 2.", locator: {section: "1 Introduction", paragraph: 4}, url: "https://arxiv.org/html/2103.14030#S1.p4"}
      - {quote: "To introduce cross-window connections while maintaining the efficient computation of non-overlapping windows, we propose a shifted window partitioning approach which alternates between two partitioning configurations in consecutive Swin Transformer blocks.", locator: {section: "3.2 Shifted Window based Self-Attention", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S3.SS2.SSS0.Px2.p1"}
    note: "In the source, 'Shifted windows' has bold 'S' and 'win' (\\textbf{S}hifted \\textbf{win}dows), so the bold letters spell 'Swin'. Plain get_text() yields 'Shifted windows'. A space-separated extractor would split it, so the next abstract sentence is also given. Section 3.2 paragraph 3 is headed 'Shifted window partitioning in successive blocks'."
  - candidate: "Swin ADAPTS the Transformer from language to vision."
    verdict: supported
    evidence:
      - {quote: "Challenges in adapting Transformer from language to vision arise from differences between the two domains, such as large variations in the scale of visual entities and the high resolution of pixels in images compared to words in text.", locator: {section: Abstract}, url: "https://arxiv.org/html/2103.14030"}
      - {quote: "In this paper, we seek to expand the applicability of Transformer such that it can serve as a general-purpose backbone for computer vision, as it does for NLP and as CNNs do in vision.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S1.p3"}
    note: ""
  - candidate: "Swin ADDRESSES the quadratic complexity of global self-attention w.r.t. image size; critique of ViT (single low-resolution feature maps; quadratic complexity)."
    verdict: supported
    evidence:
      - {quote: "The global computation leads to quadratic complexity with respect to the number of tokens, making it unsuitable for many vision problems requiring an immense set of tokens for dense prediction or to represent a high-resolution image.", locator: {section: "3.2 Shifted Window based Self-Attention", paragraph: 1}, url: "https://arxiv.org/html/2103.14030#S3.SS2.p1"}
      - {quote: "There exist many vision tasks such as semantic segmentation that require dense prediction at the pixel level, and this would be intractable for Transformer on high-resolution images, as the computational complexity of its self-attention is quadratic to image size.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S1.p3"}
      - {quote: "in contrast to previous Transformer based architectures [20] which produce feature maps of a single resolution and have quadratic complexity.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S1.p3"}
      - {quote: "The results of ViT on image classification are encouraging, but its architecture is unsuitable for use as a general-purpose backbone network on dense vision tasks or when the input image resolution is high, due to its low-resolution feature maps and the quadratic increase in complexity with image size.", locator: {section: "2 Related Work", paragraph: 4}, url: "https://arxiv.org/html/2103.14030#S2.SS0.SSS0.Px4.p1"}
    note: "Reference [20] in Swin = Dosovitskiy et al., 'An image is worth 16x16 words ...', ICLR 2021. Section 3.2 paragraph 1 names both 'The standard Transformer architecture [64] and its adaptation for image classification [20]' as doing global self-attention. Related Work paragraph 4 is headed 'Transformer based vision backbones'."
  - candidate: "Swin MITIGATES this: linear computational complexity with respect to image size (window-based self-attention, Eqs. (1)-(2))."
    verdict: supported
    evidence:
      - {quote: "This hierarchical architecture has the flexibility to model at various scales and has linear computational complexity with respect to image size.", locator: {section: Abstract}, url: "https://arxiv.org/html/2103.14030"}
      - {quote: "The linear computational complexity is achieved by computing self-attention locally within non-overlapping windows that partition an image (outlined in red). The number of patches in each window is fixed, and thus the complexity becomes linear to image size.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S1.p3"}
      - {quote: "For efficient modeling, we propose to compute self-attention within local windows. The windows are arranged to evenly partition the image in a non-overlapping manner.", locator: {section: "3.2 Shifted Window based Self-Attention", paragraph: 2}, url: "https://arxiv.org/html/2103.14030#S3.SS2.SSS0.Px1.p1"}
      - {transcription: '(1) \Omega(\text{MSA})=4hwC^{2}+2(hw)^{2}C,  (2) \Omega(\text{W-MSA})=4hwC^{2}+2M^{2}hwC, where the former is quadratic to patch number hw, and the latter is linear when M is fixed (set to 7 by default).', flag: transcribed, locator: {section: "3.2 Shifted Window based Self-Attention", paragraph: 2}, url: "https://arxiv.org/html/2103.14030#S3.EGx1"}
      - {quote: "while the window based self-attention is scalable.", locator: {section: "3.2 Shifted Window based Self-Attention", paragraph: 2}, url: "https://arxiv.org/html/2103.14030#S3.SS2.SSS0.Px1.p1"}
    note: "Scope: complexity is linear only for a fixed window size M (M×M patches per window, default 7) on an h×w patch map with C channels. Footnote 3 says SoftMax is omitted from the complexity count. Section 3.2 paragraph 2 is headed 'Self-attention in non-overlapped windows'. Equation LaTeX is copied from the HTML alttext."
  - candidate: "Swin IMPROVES_ON DeiT under regular ImageNet-1K training (Table 1(a))."
    verdict: supported
    evidence:
      - {quote: "Compared to the previous state-of-the-art Transformer-based architecture, i.e. DeiT [63], Swin Transformers noticeably surpass the counterpart DeiT architectures with similar complexities:", locator: {section: "4.1 Image Classification on ImageNet-1K", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S4.SS1.SSS0.Px2.p2"}
      - {quote: "+1.5% for Swin-T (81.3%) over DeiT-S (79.8%) using", locator: {section: "4.1 Image Classification on ImageNet-1K", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S4.SS1.SSS0.Px2.p2"}
      - {quote: "+1.5%/1.4% for Swin-B (83.3%/84.5%) over DeiT-B (81.8%/83.1%) using", locator: {section: "4.1 Image Classification on ImageNet-1K", paragraph: 3}, url: "https://arxiv.org/html/2103.14030#S4.SS1.SSS0.Px2.p2"}
      - {quote: "It outperforms the ViT / DeiT [20, 63] and ResNe(X)t models [30, 70] significantly with similar latency on the three tasks.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://arxiv.org/html/2103.14030#S1.p5"}
    note: "INTERNAL INCONSISTENCY in v2: the text gives Swin-B (224²) as 83.3%, but Table 1(a) gives 83.5 (checked in both the v2 HTML and the v2 PDF). In v1 both said 83.3 (224²) and 84.2 (384², text '+1.5%/1.1%'). v2 updated the table to 83.5/84.5 but updated the text only for 384². Use the Table 1(a) values. Scope: the gain is in top-1 at similar params/FLOPs. The DeiT baselines here are without distillation, and distilled DeiT-B⚗ reaches 83.4 at 224² in DeiT's own Table 5. Throughput is not improved: Swin-T 755.2 vs DeiT-S 940.4 im/s, Swin-B 278.1 vs DeiT-B 292.3 im/s. Section 4.1 paragraph 3 is under the heading 'Results with regular ImageNet-1K training'."
results:
  - {benchmark: "ImageNet-1K (regular ImageNet-1K training)", metric: "image size / #param. / FLOPs / throughput (image/s) / ImageNet top-1 acc.", values: {"DeiT-S [63]": "224² / 22M / 4.6G / 940.4 / 79.8", "DeiT-B [63] (224)": "224² / 86M / 17.5G / 292.3 / 81.8", "DeiT-B [63] (384)": "384² / 86M / 55.4G / 85.9 / 83.1", "Swin-T": "224² / 29M / 4.5G / 755.2 / 81.3", "Swin-S": "224² / 50M / 8.7G / 436.9 / 83.0", "Swin-B (224)": "224² / 88M / 15.4G / 278.1 / 83.5", "Swin-B (384)": "384² / 88M / 47.0G / 84.7 / 84.5", "ViT-B/16 [20]": "384² / 86M / 55.4G / 85.9 / 77.9", "ViT-L/16 [20]": "384² / 307M / 190.7G / 27.3 / 76.5"}, locator: {table: "Table 1"}, conditions: "Table 1(a) 'Regular ImageNet-1K trained models'. Single-crop top-1 on ImageNet-1K val (Section 4.1). Throughput measured with the GitHub repository of [68] on a V100 GPU, following [63]. Training: AdamW, 300 epochs, cosine decay, 20 warm-up epochs, batch 1024, lr 0.001, weight decay 0.05, mostly following [63] but without repeated augmentation and EMA. DeiT rows are non-distilled DeiT. v1 of the paper listed Swin-B 83.3 (224²) and 84.2 (384²).", url: "https://arxiv.org/html/2103.14030#S4.T1"}
  - {benchmark: "ImageNet-1K (ImageNet-22K pre-trained, fine-tuned on ImageNet-1K)", metric: "image size / #param. / FLOPs / throughput (image/s) / ImageNet top-1 acc.", values: {"R-101x3 [38]": "384² / 388M / 204.6G / - / 84.4", "R-152x4 [38]": "480² / 937M / 840.5G / - / 85.4", "ViT-B/16 [20]": "384² / 86M / 55.4G / 85.9 / 84.0", "ViT-L/16 [20]": "384² / 307M / 190.7G / 27.3 / 85.2", "Swin-B (224)": "224² / 88M / 15.4G / 278.1 / 85.2", "Swin-B (384)": "384² / 88M / 47.0G / 84.7 / 86.4", "Swin-L": "384² / 197M / 103.9G / 42.1 / 87.3"}, locator: {table: "Table 1"}, conditions: "Table 1(b) 'ImageNet-22K pre-trained models'. Swin-L 87.3 is the abstract's '87.3 top-1 accuracy on ImageNet-1K'. R-101x3/R-152x4 [38] are BiT models.", url: "https://arxiv.org/html/2103.14030#S4.T1"}
```
