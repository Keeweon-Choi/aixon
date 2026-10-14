# F2 — Attention lineage papers: verified seed facts (checked 2026-10-15)

Method notes (apply to all four blocks):

- Full texts: arXiv HTML (LaTeXML) exists for all four papers and was downloaded unmodified from the unversioned URL `https://arxiv.org/html/<id>` (served: 1409.0473v7, 1607.06450v1, 1706.03762v7, 1810.04805v2). Evidence anchors use the versioned URL plus the HTML element id.
- Every `quote` below was machine-checked to be a substring of the raw file's text, extracted with BeautifulSoup `get_text('')`, then Unicode NFKC, then whitespace collapsed to single spaces. Quotes that contain inline links, citation markers, or small-caps (e.g. "[11]", "(Figure 2)", "BERT") do **not** match if the text is extracted with a space separator (`get_text(' ')`) instead.
- `paragraph` is the position of the LaTeXML `ltx_para` block within its (sub)section in the arXiv HTML, and `html_id` is the exact element id. A display equation can be its own `ltx_para` (e.g. Transformer §3.2.1 p3 = Eq. (1)).
- `transcription` fields are LaTeX copied from the MathML `alttext`. They are **transcribed, not verbatim text spans** (`transcribed: true`).
- Semantic Scholar graph API: HTTP 429 on the first call and on all 3 retries (8 s apart) for 1409.0473, 1706.03762 and 1810.04805, so those values are recorded as 미확인. 1607.06450 succeeded.
- DBLP (dblp.org, dblp.uni-trier.de, dblp.dagstuhl.de) returned an Anubis bot-challenge page ("Making sure you're not a bot!", HTTP 202) to the API and to WebFetch ("Access Denied"). The DBLP keys below come from the DBLP links on each arXiv abs page, or from the Semantic Scholar externalIds for Layer Norm. None were checked on dblp.org.
- OpenAlex needed no API key and returned no errors. It does have serious metadata errors in two records (Transformer, BERT preprint), described in `ids_notes`.
- Other raw sources saved in `src/`: `abs_<id>.html` (arXiv abs pages), `<slug>.openalex_doi*.json`, `<slug>.openalex_search.json`, `<slug>.s2.json` (three of these hold the 429 error body), `bahdanau2014-attention.iclr2015_accepted.html`, `vaswani2017-transformer.neurips_abstract.html`, `vaswani2017-transformer.neurips_bibtex.bib`, `vaswani2017-transformer.neurips_metadata.json`, `devlin2018-bert.acl_anthology.html`.

Candidate claims NOT fully supported / needing rewording:

1. ba2016-layernorm: "layer normalization EXTENDS batch normalization" → **partially_supported**. The paper says it *transposes* BN and is *designed to overcome the drawbacks of* BN, which fits VARIANT_OF/ADAPTS plus ADDRESSES_LIMITATION_OF better than EXTENDS.
2. vaswani2017-transformer: "EN-FR BLEU 41.8" → **partially_supported** (depends on the version). 41.8 appears in the arXiv v5–v7 abstracts and in Table 2 of v7 (Table 2 of v5/v6 was not checked). The NIPS 2017 proceedings version, the arXiv v1–v4 abstracts, and §6.1 of v7 itself all say 41.0.
3. devlin2018-bert: "BERT EXTENDS the Transformer" → **partially_supported**. The text says BERT *uses* a Transformer encoder whose "implementation is almost identical to the original". BUILDS_ON/USES fits better than EXTENDS.
4. bahdanau2014-attention: "later called additive attention". The term never appears in Bahdanau et al.; the label is evidenced only in Vaswani et al. 2017 §3.2.1 ("additive attention [2]"). The word "attention" appears in Bahdanau et al. only in §3.1 paragraph 6.

```yaml
paper: bahdanau2014-attention
title: "Neural Machine Translation by Jointly Learning to Align and Translate"
authors: ["Dzmitry Bahdanau", "Kyunghyun Cho", "Yoshua Bengio"]
earliest_public_date: 2014-09-01
latest_arxiv_version: v7
latest_arxiv_version_date: 2016-05-19
venue: "ICLR 2015 (oral presentation)"
venue_source: "https://iclr.cc/archive/www/doku.php%3Fid=iclr2015:accepted-main.html"
venue_notes: >-
  The ICLR 2015 accepted-papers page lists "Neural Machine Translation by Jointly Learning to Align and Translate,
  Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio" under "Main Conference - Oral Presentations"
  (saved as src/bahdanau2014-attention.iclr2015_accepted.html). The arXiv abs page Comments field says
  "Accepted at ICLR 2015 as oral presentation". The arXiv abs page DBLP link points to
  db/conf/iclr/iclr2015.html#BahdanauCB14. ICLR 2015 issued no publisher DOIs.
ids:
  arxiv: "1409.0473"
  doi: ""
  arxiv_doi: "10.48550/arXiv.1409.0473"
  openalex:
    - {id: "W2133564696", kind: preprint, title_as_listed: "Neural Machine Translation by Jointly Learning to Align and Translate"}
  s2: "미확인"
  s2_corpus_id: "미확인"
  dblp: "conf/iclr/BahdanauCB14"
ids_notes: >-
  OpenAlex /works/doi:10.48550/arXiv.1409.0473 returns W2133564696 (type preprint, publication_date 2014-09-01,
  cited_by_count 14130). It has 5 locations: arXiv OAI, arXiv DOI, two arXiv MAG locations (one from merged
  mag:2964308564), and an odd TIB Data Manager "Dataset" DOI 10.57702/sq75seit. Neither search= nor
  filter=title.search found a separate ICLR-proceedings work; the only other hits were unrelated 2019 papers.
  Semantic Scholar returned HTTP 429 on the first call and on 3 retries, so it is 미확인. The DBLP key comes from the
  arXiv abs page link and was not checked on dblp.org (bot challenge).
openalex_primary_topic: {id: "T10181", name: "Natural Language Processing Techniques", subfield: "Artificial Intelligence", field: "Computer Science", domain: "Physical Sciences"}
fulltext_url_used: "https://arxiv.org/html/1409.0473"
fulltext_version_served: "1409.0473v7"
raw_file: "src/bahdanau2014-attention.html"
claims:
  - candidate: "ADDRESSES the fixed-length-vector bottleneck of basic encoder–decoder NMT"
    verdict: supported
    evidence:
      - quote: "we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder–decoder architecture"
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1409.0473v7"
      - quote: "A potential issue with this encoder–decoder approach is that a neural network needs to be able to compress all the necessary information of a source sentence into a fixed-length vector."
        locator: {section: "1 Introduction", paragraph: 3, html_id: "S1.p3"}
        url: "https://arxiv.org/html/1409.0473v7#S1.p3"
      - quote: "In order to address this issue, we introduce an extension to the encoder–decoder model which learns to align and translate jointly."
        locator: {section: "1 Introduction", paragraph: 4, html_id: "S1.p4"}
        url: "https://arxiv.org/html/1409.0473v7#S1.p4"
      - quote: "We conjectured that this limitation may make the basic encoder–decoder approach to underperform with long sentences."
        locator: {section: "5.1 Quantitative Results", paragraph: 2, html_id: "S5.SS1.p2"}
        url: "https://arxiv.org/html/1409.0473v7#S5.SS1.p2"
      - quote: "RNNsearch-50, especially, shows no performance deterioration even with sentences of length 50 or more."
        locator: {section: "5.1 Quantitative Results", paragraph: 2, html_id: "S5.SS1.p2"}
        url: "https://arxiv.org/html/1409.0473v7#S5.SS1.p2"
      - quote: "In this paper, we proposed a novel architecture that addresses this issue."
        locator: {section: "7 Conclusion", paragraph: 2, html_id: "S7.p2"}
        url: "https://arxiv.org/html/1409.0473v7#S7.p2"
    note: >-
      The authors frame the bottleneck as a conjecture and then support it empirically (Fig. 2, Table 1 show
      robustness to sentence length). The full text writes "encoder–decoder" with an EN DASH (U+2013), which NFKC
      leaves unchanged. The arXiv listing abstract uses a hyphen and different wording ("...and consists of an encoder
      that encodes a source sentence..."), so quote from the full text, not the listing.
  - candidate: "INTRODUCES a soft-search / alignment mechanism, later called additive attention"
    verdict: supported
    evidence:
      - quote: "propose to extend this by allowing a model to automatically (soft-)search for parts of a source sentence that are relevant to predicting a target word, without having to form these parts as a hard segment explicitly"
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1409.0473v7"
      - quote: "Each time the proposed model generates a word in a translation, it (soft-)searches for a set of positions in a source sentence where the most relevant information is concentrated."
        locator: {section: "1 Introduction", paragraph: 4, html_id: "S1.p4"}
        url: "https://arxiv.org/html/1409.0473v7#S1.p4"
      - quote: "Instead, the alignment model directly computes a soft alignment, which allows the gradient of the cost function to be backpropagated through."
        locator: {section: "3.1 Decoder: General Description", paragraph: 4, html_id: "S3.SS1.p4"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p4"
      - quote: "Intuitively, this implements a mechanism of attention in the decoder. The decoder decides parts of the source sentence to pay attention to."
        locator: {section: "3.1 Decoder: General Description", paragraph: 6, html_id: "S3.SS1.p6"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p6"
      - quote: "By letting the decoder have an attention mechanism, we relieve the encoder from the burden of having to encode all information in the source sentence into a fixed-length vector."
        locator: {section: "3.1 Decoder: General Description", paragraph: 6, html_id: "S3.SS1.p6"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p6"
      - quote: "the other is the proposed model, to which we refer as RNNsearch."
        locator: {section: "4.2 Models", paragraph: 1, html_id: "S4.SS2.p1"}
        url: "https://arxiv.org/html/1409.0473v7#S4.SS2.p1"
      - quote: "A similar approach of aligning an output symbol with an input symbol was proposed recently by Graves (2013) in the context of handwriting synthesis."
        locator: {section: "6.1 Learning to Align", paragraph: 1, html_id: "S6.SS1.p1"}
        url: "https://arxiv.org/html/1409.0473v7#S6.SS1.p1"
      - quote: "The main difference from our approach is that, in (Graves, 2013), the modes of the weights of the annotations only move in one direction."
        locator: {section: "6.1 Learning to Align", paragraph: 2, html_id: "S6.SS1.p2"}
        url: "https://arxiv.org/html/1409.0473v7#S6.SS1.p2"
    note: >-
      The word "attention" appears in this paper only in §3.1 paragraph 6, three times ("mechanism of attention",
      "pay attention to", "attention mechanism"), and not in any caption, table or appendix. The paper's own terms are
      "(soft-)search", "alignment model", "soft alignment" and the model name "RNNsearch". The term "additive
      attention" does NOT appear here. It comes from Vaswani et al. 2017 §3.2.1: "The two most commonly used attention
      functions are additive attention [2], and dot-product (multiplicative) attention.", where bibliography [2] is this
      paper (see the vaswani2017-transformer block; that quote is checked against src/vaswani2017-transformer.html, not
      this file). A suggested rewording: "INTRODUCES a jointly trained soft alignment (attention) mechanism for NMT
      (RNNsearch); later literature calls its scoring function additive attention". Prior art the paper acknowledges:
      Graves (2013), a monotonic, location-based alignment for handwriting synthesis.
  - candidate: "The alignment model e_ij = a(s_{i-1}, h_j) is parametrized as a feedforward neural network"
    verdict: supported
    evidence:
      - quote: "is, then, computed as a weighted sum of these annotations"
        locator: {section: "3.1 Decoder: General Description", paragraph: 3, html_id: "S3.SS1.p3"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p3"
        transcription: 'c_{i}=\sum_{j=1}^{T_{x}}\alpha_{ij}h_{j}\ \ (5);\qquad \alpha_{ij}=\frac{\exp\left(e_{ij}\right)}{\sum_{k=1}^{T_{x}}\exp\left(e_{ik}\right)}\ \ (6)'
        transcribed: true
      - quote: "is an alignment model which scores how well the inputs around position"
        locator: {section: "3.1 Decoder: General Description", paragraph: 3, html_id: "S3.SS1.p3"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p3"
        transcription: 'e_{ij}=a(s_{i-1},h_{j})'
        transcribed: true
      - quote: "We parametrize the alignment model"
        locator: {section: "3.1 Decoder: General Description", paragraph: 4, html_id: "S3.SS1.p4"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p4"
      - quote: "as a feedforward neural network which is jointly trained with all the other components of the proposed system."
        locator: {section: "3.1 Decoder: General Description", paragraph: 4, html_id: "S3.SS1.p4"}
        url: "https://arxiv.org/html/1409.0473v7#S3.SS1.p4"
      - quote: "In order to reduce computation, we use a single-layer multilayer perceptron such that"
        locator: {section: "A.1.2 Alignment Model", paragraph: 1, html_id: "A1.SS1.SSS2.p1"}
        url: "https://arxiv.org/html/1409.0473v7#A1.SS1.SSS2.p1"
        transcription: 'a(s_{i-1},h_{j})=v_{a}^{\top}\tanh\left(W_{a}s_{i-1}+U_{a}h_{j}\right),\quad W_{a}\in\mathbb{R}^{n\times n},\ U_{a}\in\mathbb{R}^{n\times 2n},\ v_{a}\in\mathbb{R}^{n}'
        transcribed: true
      - quote: "we can pre-compute it in advance to minimize the computational cost."
        locator: {section: "A.1.2 Alignment Model", paragraph: 1, html_id: "A1.SS1.SSS2.p1"}
        url: "https://arxiv.org/html/1409.0473v7#A1.SS1.SSS2.p1"
    note: >-
      e_ij = a(s_{i-1}, h_j) is written inline right after Eq. (6) and has no equation number of its own. The concrete
      form v_a^T tanh(W_a s_{i-1} + U_a h_j) is in Appendix A.1.2. It appears again in A.2.2 with
      v_a ∈ R^{n'}, W_a ∈ R^{n'×n}, U_a ∈ R^{n'×2n}; A.2.3 sets n' (the number of hidden units in the alignment
      model) to 1000. This is the "feed-forward network with a single hidden layer" that Vaswani et al.
      2017 call additive attention. The pre-computable term is U_a h_j, which does not depend on i.
results:
  - benchmark: "WMT'14 English-to-French, test set news-test-2014 (3003 sentences)"
    metric: "BLEU"
    values:
      "RNNencdec-30": {"All": "13.93", "No UNK∘": "24.19"}
      "RNNsearch-30": {"All": "21.50", "No UNK∘": "31.44"}
      "RNNencdec-50": {"All": "17.82", "No UNK∘": "26.71"}
      "RNNsearch-50": {"All": "26.75", "No UNK∘": "34.16"}
      "RNNsearch-50⋆": {"All": "28.45", "No UNK∘": "36.15"}
      "Moses": {"All": "33.30", "No UNK∘": "35.63"}
    locator: {table: "Table 1", html_id: "S5.T1.fig1"}
    conditions: >-
      Caption: "BLEU scores of the trained models computed on the test set." "All" = all test sentences.
      "No UNK∘" = only sentences with no unknown word in the source or the reference; for this column the models were
      not allowed to generate [UNK]. RNNsearch-50⋆ was trained much longer, until development-set performance stopped
      improving. -30/-50 = maximum training sentence length. Moses uses an extra 418M-word monolingual corpus (§5.1).
    url: "https://arxiv.org/html/1409.0473v7#S5.T1.fig1"
```

```yaml
paper: ba2016-layernorm
title: "Layer Normalization"
authors: ["Jimmy Lei Ba", "Jamie Ryan Kiros", "Geoffrey E. Hinton"]
earliest_public_date: 2016-07-21
latest_arxiv_version: v1
venue: "arXiv preprint only (CoRR abs/1607.06450); no peer-reviewed or workshop venue found"
venue_source: "https://arxiv.org/abs/1607.06450"
venue_notes: >-
  The arXiv abs page has no Comments and no Journal-ref field. The v1 PDF (streamed and read, not saved) carries no
  venue footer, only the arXiv stamp "arXiv:1607.06450v1 [stat.ML] 21 Jul 2016". Semantic Scholar has
  venue "arXiv.org" and journal "ArXiv, abs/1607.06450". OpenAlex holds only preprint locations. Two web searches,
  including one for a NIPS 2016 Deep Learning Symposium listing, found no primary source for any workshop or symposium
  presentation. Any such attribution should be treated as 미확인, not as a venue.
ids:
  arxiv: "1607.06450"
  doi: ""
  arxiv_doi: "10.48550/arXiv.1607.06450"
  openalex:
    - {id: "W3037932933", kind: preprint, title_as_listed: "Layer Normalization"}
  s2: "97fb4e3d45bb098e27e0071448b6152217bd35a5"
  s2_corpus_id: 8236317
  dblp: "journals/corr/BaKH16"
ids_notes: >-
  Semantic Scholar (arXiv:1607.06450) returned HTTP 200 on the first retry, after one 429. It gives
  externalIds {MAG: 3037932933, ArXiv: 1607.06450, DBLP: journals/corr/BaKH16, CorpusId: 8236317},
  publicationDate 2016-07-21 and venue "arXiv.org". OpenAlex W3037932933 is type preprint with 3 arXiv locations;
  filter=title.search:"layer normalization",publication_year:2016 matches only this work. The DBLP key comes from
  S2 externalIds and was not checked on dblp.org.
openalex_primary_topic: {id: "T10320", name: "Neural Networks and Applications", subfield: "Artificial Intelligence", field: "Computer Science", domain: "Physical Sciences"}
fulltext_url_used: "https://arxiv.org/html/1607.06450"
fulltext_version_served: "1607.06450v1"
raw_file: "src/ba2016-layernorm.html"
claims:
  - candidate: "INTRODUCES layer normalization"
    verdict: supported
    evidence:
      - quote: "In this paper, we transpose batch normalization into layer normalization by computing the mean and variance used for normalization from all of the summed inputs to the neurons in a layer on a single training case."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1607.06450v1"
      - quote: "This paper introduces layer normalization, a simple normalization method to improve the training speed for various neural network models."
        locator: {section: "1 Introduction", paragraph: 3, html_id: "S1.p3"}
        url: "https://arxiv.org/html/1607.06450v1#S1.p3"
      - quote: "We, thus, compute the layer normalization statistics over all the hidden units in the same layer as follows:"
        locator: {section: "3 Layer normalization", paragraph: 2, html_id: "S3.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S3.p2"
        transcription: '\mu^{l}=\frac{1}{H}\sum_{i=1}^{H}a^{l}_{i}\qquad\sigma^{l}=\sqrt{\frac{1}{H}\sum_{i=1}^{H}\left(a^{l}_{i}-\mu^{l}\right)^{2}}\quad (3),\ H=\text{number of hidden units in a layer}'
        transcribed: true
      - quote: "In this paper, we introduced layer normalization to speed-up the training of neural networks."
        locator: {section: "7 Conclusion", paragraph: 1, html_id: "S7.p1"}
        url: "https://arxiv.org/html/1607.06450v1#S7.p1"
    note: "The RNN form is Eq. (4) in §3.1, with statistics computed separately at each time step and one shared set of gain and bias parameters."
  - candidate: "Motivation: batch normalization depends on mini-batch size and is not obviously applicable to RNNs"
    verdict: supported
    evidence:
      - quote: "However, the effect of batch normalization is dependent on the mini-batch size and it is not obvious how to apply it to recurrent neural networks."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1607.06450v1"
      - quote: "This puts constraints on the size of a mini-batch and it is hard to apply to recurrent neural networks."
        locator: {section: "2 Background", paragraph: 2, html_id: "S2.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S2.p2"
      - quote: "Furthermore, batch normalization cannot be applied to online learning tasks or to extremely large distributed models where the minibatches have to be small."
        locator: {section: "1 Introduction", paragraph: 2, html_id: "S1.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S1.p2"
      - quote: "Unlike batch normalization, layer normaliztion does not impose any constraint on the size of a mini-batch and it can be used in the pure online regime with batch size 1."
        locator: {section: "3 Layer normalization", paragraph: 2, html_id: "S3.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S3.p2"
      - quote: "It is also straightforward to apply to recurrent neural networks by computing the normalization statistics separately at each time step."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1607.06450v1"
    note: >-
      The abstract's wording is "not obvious how to apply", not "impossible". §1 p2 explains why: the summed inputs
      of an RNN vary with sequence length, so BN would need different statistics for each time step. The misspelling
      "normaliztion" is in the original text.
  - candidate: "Layer normalization EXTENDS batch normalization (builds on and modifies it)"
    verdict: partially_supported
    evidence:
      - quote: "In this paper, we transpose batch normalization into layer normalization by computing the mean and variance used for normalization from all of the summed inputs to the neurons in a layer on a single training case."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1607.06450v1"
      - quote: "Like batch normalization, we also give each neuron its own adaptive bias and gain which are applied after the normalization but before the non-linearity."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1607.06450v1"
      - quote: "Unlike batch normalization, layer normalization performs exactly the same computation at training and test times."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1607.06450v1"
      - quote: "We now consider the layer normalization method which is designed to overcome the drawbacks of batch normalization."
        locator: {section: "3 Layer normalization", paragraph: 1, html_id: "S3.p1"}
        url: "https://arxiv.org/html/1607.06450v1#S3.p1"
      - quote: "the batch normalization method rescales the summed inputs according to their variances under the distribution of the data"
        locator: {section: "2 Background", paragraph: 2, html_id: "S2.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S2.p2"
        transcription: '\bar{a}^{l}_{i}=\frac{g^{l}_{i}}{\sigma^{l}_{i}}\left(a^{l}_{i}-\mu^{l}_{i}\right)\qquad\mu^{l}_{i}=\mathbb{E}_{x\sim P(x)}\left[a^{l}_{i}\right]\qquad\sigma^{l}_{i}=\sqrt{\mathbb{E}_{x\sim P(x)}\left[\left(a^{l}_{i}-\mu^{l}_{i}\right)^{2}\right]}\quad (2)'
        transcribed: true
      - quote: "The difference between Eq. (2) and Eq. (3) is that under layer normalization, all the hidden units in a layer share the same normalization terms"
        locator: {section: "3 Layer normalization", paragraph: 2, html_id: "S3.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S3.p2"
      - quote: "but different training cases have different normalization terms."
        locator: {section: "3 Layer normalization", paragraph: 2, html_id: "S3.p2"}
        url: "https://arxiv.org/html/1607.06450v1#S3.p2"
      - quote: "The proposed layer normalization is related to batch normalization and weight normalization."
        locator: {section: "5.1 Invariance under weights and data transformations", paragraph: 1, html_id: "S5.SS1.p1"}
        url: "https://arxiv.org/html/1607.06450v1#S5.SS1.p1"
      - quote: "Batch normalization has been previously extended to recurrent neural networks [Laurent et al., 2015, Amodei et al., 2015, Cooijmans et al., 2016]."
        locator: {section: "4 Related work", paragraph: 1, html_id: "S4.p1"}
        url: "https://arxiv.org/html/1607.06450v1#S4.p1"
      - quote: "In our preliminary experiments, we observed that layer normalization offers a speedup over the baseline model without normalization, but batch normalization outperforms the other methods."
        locator: {section: "6.7 Convolutional Networks", paragraph: 1, html_id: "S6.SS7.p1"}
        url: "https://arxiv.org/html/1607.06450v1#S6.SS7.p1"
    note: >-
      "Builds on and modifies" is supported. LN keeps BN's normalize-then-gain/bias form (Eq. 2 vs Eq. 3) and changes
      which units the statistics are computed over: the hidden units of one layer for a single training case, instead
      of the data distribution or mini-batch. The verb the authors use is "transpose", and they say LN is "designed to
      overcome the drawbacks of" BN. They never call LN an extension of BN. The only "extended" in the paper (§4) is
      about OTHER work extending BN to RNNs. LN is also not a superset of BN: its invariance properties differ
      (Table 1, "Invariance properties under the normalization methods."), and BN still outperforms it on ConvNets
      (§6.7). Recommended edges: LN VARIANT_OF/ADAPTS BN, plus LN ADDRESSES_LIMITATION_OF BN (dependence on
      mini-batch size, applicability to RNNs). If EXTENDS is kept, mark it as an interpretation, not a quoted relation.
results:
  - benchmark: "MSCOCO caption retrieval and image retrieval (order-embeddings, GRU encoder)"
    metric: "R@1 / R@5 / R@10 (higher is better), Mean r (lower is better)"
    values:
      "Sym [Vendrov et al., 2016]": {"caption": {"R@1": "45.4", "R@5": "", "R@10": "88.7", "Mean r": "5.8"}, "image": {"R@1": "36.3", "R@5": "", "R@10": "85.8", "Mean r": "9.0"}}
      "OE [Vendrov et al., 2016]": {"caption": {"R@1": "46.7", "R@5": "", "R@10": "88.9", "Mean r": "5.7"}, "image": {"R@1": "37.9", "R@5": "", "R@10": "85.9", "Mean r": "8.1"}}
      "OE (ours)": {"caption": {"R@1": "46.6", "R@5": "79.3", "R@10": "89.1", "Mean r": "5.2"}, "image": {"R@1": "37.8", "R@5": "73.6", "R@10": "85.7", "Mean r": "7.9"}}
      "OE + LN": {"caption": {"R@1": "48.5", "R@5": "80.6", "R@10": "89.8", "Mean r": "5.1"}, "image": {"R@1": "38.9", "R@5": "74.3", "R@10": "86.3", "Mean r": "7.6"}}
    locator: {table: "Table 2", html_id: "S6.T2"}
    conditions: >-
      Caption: "Average results across 5 test splits for caption and image retrieval." Each split has 1000 images and
      5000 captions. An empty R@5 means the cell is blank in the table. In §6.1 p3 LN "converges to its best validation
      model in 60% of the time it takes the baseline model to do so."
    url: "https://arxiv.org/html/1607.06450v1#S6.T2"
  - benchmark: "Skip-thought vectors, downstream evaluations"
    metric: "SICK(r) and SICK(ρ) correlations, SICK(MSE) (lower is better), MR/CR/SUBJ/MPQA accuracy"
    values:
      "Original [Kiros et al., 2015]": {"SICK(r)": "0.848", "SICK(ρ)": "0.778", "SICK(MSE)": "0.287", "MR": "75.5", "CR": "79.3", "SUBJ": "92.1", "MPQA": "86.9"}
      "Ours": {"SICK(r)": "0.842", "SICK(ρ)": "0.767", "SICK(MSE)": "0.298", "MR": "77.3", "CR": "81.8", "SUBJ": "92.6", "MPQA": "87.9"}
      "Ours + LN": {"SICK(r)": "0.854", "SICK(ρ)": "0.785", "SICK(MSE)": "0.277", "MR": "79.5", "CR": "82.6", "SUBJ": "93.4", "MPQA": "89.0"}
      "Ours + LN †": {"SICK(r)": "0.858", "SICK(ρ)": "0.788", "SICK(MSE)": "0.270", "MR": "79.4", "CR": "83.1", "SUBJ": "93.7", "MPQA": "89.3"}
    locator: {table: "Table 3", html_id: "S6.T3"}
    conditions: "Caption: \"Skip-thoughts results.\" Models trained for 1M iterations, except † (trained 1 month, about 1.7M iterations)."
    url: "https://arxiv.org/html/1607.06450v1#S6.T3"
```

```yaml
paper: vaswani2017-transformer
title: "Attention Is All You Need"
title_in_proceedings: "Attention is All you Need"
authors: ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar", "Jakob Uszkoreit", "Llion Jones", "Aidan N. Gomez", "Łukasz Kaiser", "Illia Polosukhin"]
authors_note: >-
  The order is the same in the arXiv listing, the paper and the proceedings. The arXiv metadata spells "Lukasz Kaiser";
  the paper and the NeurIPS proceedings spell "Łukasz Kaiser". The paper's footnote says "Equal contribution. Listing
  order is random."
earliest_public_date: 2017-06-12
latest_arxiv_version: v7
latest_arxiv_version_date: 2023-08-02
venue: "NIPS 2017 (now NeurIPS): Advances in Neural Information Processing Systems 30, pp. 5998–6008"
venue_source: "https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html"
venue_notes: >-
  The proceedings page reads "Advances in Neural Information Processing Systems 30 (NIPS 2017)". The proceedings
  Metadata.json gives page_first 5998 and page_last 6008; the BibTeX gives booktitle "Advances in Neural Information
  Processing Systems", volume 30, publisher Curran Associates, Inc. (saved as src/vaswani2017-transformer.neurips_*).
  The arXiv v7 PDF footer reads "31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach,
  CA, USA." The arXiv Comments field only says "15 pages, 5 figures". The NIPS 2017 proceedings have no DOI. The
  conference was named NIPS in 2017; "NeurIPS 2017" is the retroactive name.
ids:
  arxiv: "1706.03762"
  doi: ""
  arxiv_doi: "10.48550/arXiv.1706.03762"
  openalex:
    - {id: "W2626778328", kind: preprint, title_as_listed: "Attention Is All You Need"}
  s2: "미확인"
  s2_corpus_id: "미확인"
  dblp: "journals/corr/VaswaniSPUJGKP17"
ids_notes: >-
  OpenAlex /works/doi:10.48550/arXiv.1706.03762 returns W2626778328. The title is correct but the metadata is
  CORRUPTED: its doi field is https://doi.org/10.65215/2q58a426 (a "posted-content" DOI whose OA URL is on
  langtaosha.org.cn), its publication_date is 2025-08-23 (publication_year 2025), and 8 of its 11 locations are
  10.65215/* posted-content DOIs. The remaining locations are the arXiv OAI record, the arXiv DOI and the merged
  mag:2963403868 (arXiv v5 PDF). Its biblio (volume 30, pages 5998–6008) comes from the NIPS proceedings, but no
  NIPS location is listed. Use the work ID, not its doi or date. No separate NeurIPS-proceedings work exists:
  filter=title.search:"attention is all you need",publication_year:2017 returns 0 results, and the search=
  results are other papers. Semantic Scholar returned HTTP 429 on the first call and on 3 retries, so it is 미확인.
  The DBLP key (CoRR) comes from the arXiv abs page link. A NIPS-proceedings DBLP key was not checked (dblp.org bot
  challenge).
openalex_primary_topic: {id: "T10181", name: "Natural Language Processing Techniques", subfield: "Artificial Intelligence", field: "Computer Science", domain: "Physical Sciences"}
fulltext_url_used: "https://arxiv.org/html/1706.03762"
fulltext_version_served: "1706.03762v7"
raw_file: "src/vaswani2017-transformer.html"
claims:
  - candidate: "INTRODUCES the Transformer"
    verdict: supported
    evidence:
      - quote: "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1706.03762v7"
      - quote: "In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output."
        locator: {section: "1 Introduction", paragraph: 4, html_id: "S1.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S1.p4"
      - quote: "In this work, we presented the Transformer, the first sequence transduction model based entirely on attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention."
        locator: {section: "7 Conclusion", paragraph: 1, html_id: "S7.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S7.p1"
    note: "The v7 HTML abstract differs slightly from the arXiv listing abstract (\"that include an encoder and a decoder\" vs \"in an encoder-decoder configuration\"). The quoted sentence is the same in both."
  - candidate: "ADDRESSES sequential computation in recurrent models"
    verdict: supported
    evidence:
      - quote: "This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples."
        locator: {section: "1 Introduction", paragraph: 2, html_id: "S1.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S1.p2"
      - quote: "The fundamental constraint of sequential computation, however, remains."
        locator: {section: "1 Introduction", paragraph: 2, html_id: "S1.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S1.p2"
      - quote: "The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs."
        locator: {section: "1 Introduction", paragraph: 4, html_id: "S1.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S1.p4"
    note: "Table 1 quantifies this: minimum sequential operations are O(1) for self-attention and O(n) for a recurrent layer."
  - candidate: "General definition of an attention function: maps a query and key-value pairs to an output; weighted sum of values; weights from a compatibility function"
    verdict: supported
    evidence:
      - quote: "An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors."
        locator: {section: "3.2 Attention", paragraph: 1, html_id: "S3.SS2.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.p1"
      - quote: "The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key."
        locator: {section: "3.2 Attention", paragraph: 1, html_id: "S3.SS2.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.p1"
    note: ""
  - candidate: "INTRODUCES Scaled Dot-Product Attention (Eq. 1)"
    verdict: supported
    evidence:
      - quote: 'We call our particular attention "Scaled Dot-Product Attention" (Figure 2).'
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 1, html_id: "S3.SS2.SSS1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p1"
      - quote: "We compute the dot products of the query with all keys, divide each by"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 1, html_id: "S3.SS2.SSS1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p1"
        transcription: '\sqrt{d_{k}}'
        transcribed: true
      - quote: "and apply a softmax function to obtain the weights on the values."
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 1, html_id: "S3.SS2.SSS1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p1"
      - quote: "We compute the matrix of outputs as:"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 2, html_id: "S3.SS2.SSS1.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p2"
        transcription: '\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^{T}}{\sqrt{d_{k}}}\right)V'
        transcription_locator: {section: "3.2.1 Scaled Dot-Product Attention", equation: 1, html_id: "S3.SS2.SSS1.p3"}
        transcribed: true
      - quote: "Dot-product attention is identical to our algorithm, except for the scaling factor of"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 4, html_id: "S3.SS2.SSS1.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p4"
        transcription: '\frac{1}{\sqrt{d_{k}}}'
        transcribed: true
      - quote: "Noam proposed scaled dot-product attention, multi-head attention and the parameter-free position representation"
        locator: {footnote: "∗ (author-contribution note, page 1)", html_id: "id1"}
        url: "https://arxiv.org/html/1706.03762v7"
    note: >-
      What is new is the 1/sqrt(d_k) scaling. The paper itself says plain dot-product (multiplicative) attention is
      "identical to our algorithm, except for the scaling factor". The author-contribution footnote credits Noam Shazeer
      with proposing scaled dot-product attention.
  - candidate: "Reason for scaling: for large d_k dot products grow large, pushing softmax into regions with extremely small gradients; scale by 1/sqrt(d_k) (footnote 4: q, k components independent, mean 0, variance 1 → q·k has mean 0, variance d_k)"
    verdict: supported
    evidence:
      - quote: "[3]. We suspect that for large values of"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 5, html_id: "S3.SS2.SSS1.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p5"
        transcription: 'd_{k}'
        transcribed: true
      - quote: "the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 5, html_id: "S3.SS2.SSS1.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p5"
      - quote: "To counteract this effect, we scale the dot products by"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 5, html_id: "S3.SS2.SSS1.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p5"
        transcription: '\frac{1}{\sqrt{d_{k}}}'
        transcribed: true
      - quote: "To illustrate why the dot products get large, assume that the components of"
        locator: {footnote: 4, html_id: "footnote1", rendered_mark_in_html: 1}
        url: "https://arxiv.org/html/1706.03762v7#footnote1"
      - quote: "are independent random variables with mean"
        locator: {footnote: 4, html_id: "footnote1", rendered_mark_in_html: 1}
        url: "https://arxiv.org/html/1706.03762v7#footnote1"
        transcription: 'q,k:\ \text{components independent, mean }0,\ \text{variance }1\ \Rightarrow\ q\cdot k=\sum_{i=1}^{d_{k}}q_{i}k_{i}\ \text{has mean }0\text{ and variance }d_{k}'
        transcribed: true
    note: >-
      The authors present this as a hypothesis ("We suspect"); the footnote is a variance argument, not an experiment.
      The arXiv v7 PDF and the NIPS 2017 PDF both print this footnote as 4; it comes after the three page-1 symbol
      notes ∗ † ‡. The arXiv HTML shows it with mark "1" (id footnote1) and renders the page-1 notes as author "thanks" notes.
      The text is the same.
  - candidate: "Additive vs dot-product attention: similar theoretical complexity; dot-product faster and more space-efficient in practice; additive outperforms unscaled dot product for larger d_k"
    verdict: supported
    evidence:
      - quote: "The two most commonly used attention functions are additive attention [2], and dot-product (multiplicative) attention."
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 4, html_id: "S3.SS2.SSS1.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p4"
      - quote: "Additive attention computes the compatibility function using a feed-forward network with a single hidden layer."
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 4, html_id: "S3.SS2.SSS1.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p4"
      - quote: "While the two are similar in theoretical complexity, dot-product attention is much faster and more space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code."
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 4, html_id: "S3.SS2.SSS1.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p4"
      - quote: "the two mechanisms perform similarly, additive attention outperforms dot product attention without scaling for larger values of"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 5, html_id: "S3.SS2.SSS1.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p5"
        transcription: 'd_{k}\ [3]'
        transcribed: true
      - quote: "[3]. We suspect that for large values of"
        locator: {section: "3.2.1 Scaled Dot-Product Attention", paragraph: 5, html_id: "S3.SS2.SSS1.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS1.p5"
      - quote: "Denny Britz, Anna Goldie, Minh-Thang Luong, and Quoc V. Le."
        locator: {section: "References", item: "[3]", html_id: "bib.bib3"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib3"
      - quote: "Massive exploration of neural machine translation architectures."
        locator: {section: "References", item: "[3]", html_id: "bib.bib3"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib3"
    note: >-
      The marker [3] comes right after the math d_k, so it cannot sit in the same verbatim span as "...for larger
      values of". That is why the separate quote "[3]. We suspect..." is included. [3] = Britz, Goldie, Luong, Le,
      "Massive exploration of neural machine translation architectures", CoRR abs/1703.03906, 2017. The empirical
      claim (additive beats unscaled dot product at large d_k) is therefore cited, not the authors' own experiment.
      [2] = Bahdanau et al. (see the encoder claim), which links bahdanau2014-attention to the term "additive attention".
  - candidate: "INTRODUCES Multi-Head Attention (MultiHead formula; base model h = 8, d_k = d_v = d_model/h = 64)"
    verdict: supported
    evidence:
      - quote: "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 2, html_id: "S3.SS2.SSS2.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p2"
      - quote: "With a single attention head, averaging inhibits this."
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 2, html_id: "S3.SS2.SSS2.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p2"
      - quote: "we found it beneficial to linearly project the queries, keys and values"
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 1, html_id: "S3.SS2.SSS2.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p1"
      - quote: "These are concatenated and once again projected, resulting in the final values, as depicted in Figure 2."
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 1, html_id: "S3.SS2.SSS2.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p1"
        transcription: '\mathrm{MultiHead}(Q,K,V)=\mathrm{Concat}(\mathrm{head_{1}},\dots,\mathrm{head_{h}})W^{O}\quad\text{where}\ \mathrm{head_{i}}=\mathrm{Attention}(QW^{Q}_{i},KW^{K}_{i},VW^{V}_{i})'
        transcription_locator: {section: "3.2.2 Multi-Head Attention", paragraph: 3, equation: "unnumbered display", html_id: "S3.SS2.SSS2.p3"}
        transcribed: true
      - quote: "Where the projections are parameter matrices"
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 4, html_id: "S3.SS2.SSS2.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p4"
        transcription: 'W^{Q}_{i}\in\mathbb{R}^{d_{\text{model}}\times d_{k}},\ W^{K}_{i}\in\mathbb{R}^{d_{\text{model}}\times d_{k}},\ W^{V}_{i}\in\mathbb{R}^{d_{\text{model}}\times d_{v}},\ W^{O}\in\mathbb{R}^{hd_{v}\times d_{\text{model}}}'
        transcribed: true
      - quote: "parallel attention layers, or heads. For each of these we use"
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 5, html_id: "S3.SS2.SSS2.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p5"
        transcription: 'h=8;\qquad d_{k}=d_{v}=d_{\text{model}}/h=64'
        transcribed: true
      - quote: "Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality."
        locator: {section: "3.2.2 Multi-Head Attention", paragraph: 5, html_id: "S3.SS2.SSS2.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS2.SSS2.p5"
    note: >-
      h = 8 and d_k = d_v = 64 are inline math in the source and are only transcribed here. Table 3's "base" row has
      the same values printed as plain table cells (h 8, d_k 64, d_v 64; d_model 512). The MultiHead display equation
      is unnumbered. The author-contribution footnote credits Noam Shazeer with multi-head attention.
  - candidate: "Encoder layer = multi-head self-attention + position-wise fully connected FFN, each with residual connection [11] followed by layer normalization [1]; identify [11], [1], [2]"
    verdict: supported
    evidence:
      - quote: "The encoder is composed of a stack of"
        locator: {section: "3.1 Encoder and Decoder Stacks — Encoder:", paragraph: 1, html_id: "S3.SS1.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS1.SSS0.Px1.p1"
        transcription: 'N=6'
        transcribed: true
      - quote: "Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position-wise fully connected feed-forward network."
        locator: {section: "3.1 Encoder and Decoder Stacks — Encoder:", paragraph: 1, html_id: "S3.SS1.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS1.SSS0.Px1.p1"
      - quote: "We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1]."
        locator: {section: "3.1 Encoder and Decoder Stacks — Encoder:", paragraph: 1, html_id: "S3.SS1.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS1.SSS0.Px1.p1"
      - quote: "That is, the output of each sub-layer is"
        locator: {section: "3.1 Encoder and Decoder Stacks — Encoder:", paragraph: 1, html_id: "S3.SS1.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS1.SSS0.Px1.p1"
        transcription: '\mathrm{LayerNorm}(x+\mathrm{Sublayer}(x))'
        transcribed: true
      - quote: "To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension"
        locator: {section: "3.1 Encoder and Decoder Stacks — Encoder:", paragraph: 1, html_id: "S3.SS1.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS1.SSS0.Px1.p1"
        transcription: 'd_{\text{model}}=512'
        transcribed: true
      - quote: "Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun."
        locator: {section: "References", item: "[11]", html_id: "bib.bib11"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib11"
      - quote: "Deep residual learning for image recognition."
        locator: {section: "References", item: "[11]", html_id: "bib.bib11"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib11"
      - quote: "In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 770–778, 2016."
        locator: {section: "References", item: "[11]", html_id: "bib.bib11"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib11"
      - quote: "Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton."
        locator: {section: "References", item: "[1]", html_id: "bib.bib1"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib1"
      - quote: "arXiv preprint arXiv:1607.06450, 2016."
        locator: {section: "References", item: "[1]", html_id: "bib.bib1"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib1"
      - quote: "Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio."
        locator: {section: "References", item: "[2]", html_id: "bib.bib2"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib2"
      - quote: "Neural machine translation by jointly learning to align and translate."
        locator: {section: "References", item: "[2]", html_id: "bib.bib2"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib2"
      - quote: "CoRR, abs/1409.0473, 2014."
        locator: {section: "References", item: "[2]", html_id: "bib.bib2"}
        url: "https://arxiv.org/html/1706.03762v7#bib.bib2"
    note: >-
      [11] = He, Zhang, Ren, Sun, "Deep residual learning for image recognition", CVPR 2016, pp. 770–778 (ResNet).
      [1] = Ba, Kiros, Hinton, "Layer normalization", arXiv:1607.06450, 2016 (= ba2016-layernorm).
      [2] = Bahdanau, Cho, Bengio, "Neural machine translation by jointly learning to align and translate",
      CoRR abs/1409.0473, 2014 (= bahdanau2014-attention). This gives citation edges Transformer → ResNet (residual
      connections), Transformer → LayerNorm, and Transformer → Bahdanau (additive attention, encoder-decoder attention,
      sequence-to-sequence models). LayerNorm is applied after the residual sum, LayerNorm(x + Sublayer(x)), the
      "post-LN" arrangement. N = 6 and d_model = 512 are inline math (transcribed).
  - candidate: "Positional encoding: needed because there is no recurrence and no convolution; sinusoidal; learned positional embeddings gave nearly identical results"
    verdict: supported
    evidence:
      - quote: "Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence."
        locator: {section: "3.5 Positional Encoding", paragraph: 1, html_id: "S3.SS5.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS5.p1"
      - quote: 'To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks.'
        locator: {section: "3.5 Positional Encoding", paragraph: 1, html_id: "S3.SS5.p1"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS5.p1"
      - quote: "In this work, we use sine and cosine functions of different frequencies:"
        locator: {section: "3.5 Positional Encoding", paragraph: 2, html_id: "S3.SS5.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS5.p2"
        transcription: 'PE_{(pos,2i)}=\sin\left(pos/10000^{2i/d_{\text{model}}}\right)\qquad PE_{(pos,2i+1)}=\cos\left(pos/10000^{2i/d_{\text{model}}}\right)'
        transcription_locator: {section: "3.5 Positional Encoding", paragraph: 3, equation: "unnumbered display", html_id: "S3.SS5.p3"}
        transcribed: true
      - quote: "That is, each dimension of the positional encoding corresponds to a sinusoid."
        locator: {section: "3.5 Positional Encoding", paragraph: 4, html_id: "S3.SS5.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS5.p4"
      - quote: "We also experimented with using learned positional embeddings [9] instead, and found that the two versions produced nearly identical results (see Table 3 row (E))."
        locator: {section: "3.5 Positional Encoding", paragraph: 5, html_id: "S3.SS5.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS5.p5"
      - quote: "We chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than the ones encountered during training."
        locator: {section: "3.5 Positional Encoding", paragraph: 5, html_id: "S3.SS5.p5"}
        url: "https://arxiv.org/html/1706.03762v7#S3.SS5.p5"
    note: >-
      Table 3 row (E), "positional embedding instead of sinusoids", gives PPL (dev) 4.92 and BLEU (dev) 25.7, against
      4.92 and 25.8 for the base row. [9] = Gehring et al., Convolutional sequence to sequence learning. The
      extrapolation benefit is stated as a possibility ("may allow") and is not tested. The positional encodings are
      added to the input embeddings, not concatenated.
  - candidate: "Result: WMT 2014 English-to-German BLEU 28.4"
    verdict: supported
    evidence:
      - quote: "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1706.03762v7"
      - quote: "The Transformer achieves better BLEU scores than previous state-of-the-art models on the English-to-German and English-to-French newstest2014 tests at a fraction of the training cost."
        locator: {table: "Table 2", part: caption, html_id: "S6.T2"}
        url: "https://arxiv.org/html/1706.03762v7#S6.T2"
    note: "Table 2 gives Transformer (big) EN-DE 28.4. The same value appears in §6.1 (as inline math), in every arXiv version's abstract, and in the NIPS 2017 proceedings version. The test set is newstest2014."
  - candidate: "Result: WMT 2014 English-to-French BLEU 41.8"
    verdict: partially_supported
    evidence:
      - quote: "On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs"
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1706.03762v7"
      - quote: "On the WMT 2014 English-to-French translation task, our big model achieves a BLEU score of"
        locator: {section: "6.1 Machine Translation", paragraph: 2, html_id: "S6.SS1.p2"}
        url: "https://arxiv.org/html/1706.03762v7#S6.SS1.p2"
        transcription: '41.0'
        transcribed: true
    note: >-
      The value depends on the version. In arXiv v7 (the raw file), the abstract and Table 2 (Transformer (big), EN-FR)
      say 41.8, but §6.1 paragraph 2 of the same version still says 41.0. The arXiv abstracts of v1–v4 (June 2017)
      say 41.0 and those of v5–v7 (from 2017-12-06) say 41.8 (checked on https://arxiv.org/abs/1706.03762v1 to v6).
      The NIPS 2017 proceedings paper says 41.0 in its abstract, Table 2 and §6.1
      (https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf, text
      checked via src/vaswani2017-transformer.neurips_metadata.json full_text). Suggested rewording: "41.8 BLEU (arXiv
      v5+ abstracts and v7 Table 2; the NIPS 2017 proceedings report 41.0)". The proceedings metadata "abstract" field
      holds an even older abstract (27.5 EN-DE and 41.1 EN-FR, "165 million parameters") that does not match the
      proceedings PDF; do not use it.
  - candidate: "Self-attention complexity per layer is O(n^2·d)"
    verdict: supported
    evidence:
      - quote: "Maximum path lengths, per-layer complexity and minimum number of sequential operations for different layer types."
        locator: {table: "Table 1", part: caption, html_id: "S4.T1"}
        url: "https://arxiv.org/html/1706.03762v7#S4.T1"
        transcription: 'Self-Attention:\ O(n^{2}\cdot d)\ |\ O(1)\ |\ O(1);\quad Recurrent:\ O(n\cdot d^{2})\ |\ O(n)\ |\ O(n);\quad Convolutional:\ O(k\cdot n\cdot d^{2})\ |\ O(1)\ |\ O(\log_{k}(n));\quad Self\text{-}Attention\ (restricted):\ O(r\cdot n\cdot d)\ |\ O(1)\ |\ O(n/r)\quad [\text{columns: Complexity per Layer | Sequential Operations | Maximum Path Length}]'
        transcribed: true
      - quote: "In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence length"
        locator: {section: "4 Why Self-Attention", paragraph: 4, html_id: "S4.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S4.p4"
      - quote: "As noted in Table 1, a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires"
        locator: {section: "4 Why Self-Attention", paragraph: 4, html_id: "S4.p4"}
        url: "https://arxiv.org/html/1706.03762v7#S4.p4"
    note: >-
      Table 1 caption: n = sequence length, d = representation dimension, k = convolution kernel size, r =
      neighbourhood size in restricted self-attention. All table cells are math, so they are transcribed. Per §4,
      self-attention is cheaper than a recurrent layer when n < d.
results:
  - benchmark: "WMT 2014 English-German and English-French (newstest2014)"
    metric: "BLEU; training cost (FLOPs)"
    values:
      "Transformer (base model)": {"BLEU EN-DE": "27.3", "BLEU EN-FR": "38.1", "Training cost (one value spanning both EN-DE/EN-FR columns)": "3.3·10^18"}
      "Transformer (big)": {"BLEU EN-DE": "28.4", "BLEU EN-FR": "41.8", "Training cost (one value spanning both EN-DE/EN-FR columns)": "2.3·10^19"}
      "GNMT + RL Ensemble [38]": {"BLEU EN-DE": "26.30", "BLEU EN-FR": "41.16", "Training cost EN-DE": "1.8·10^20", "Training cost EN-FR": "1.1·10^21"}
      "ConvS2S Ensemble [9]": {"BLEU EN-DE": "26.36", "BLEU EN-FR": "41.29", "Training cost EN-DE": "7.7·10^19", "Training cost EN-FR": "1.2·10^21"}
      "MoE [32]": {"BLEU EN-DE": "26.03", "BLEU EN-FR": "40.56", "Training cost EN-DE": "2.0·10^19", "Training cost EN-FR": "1.2·10^20"}
    locator: {table: "Table 2", html_id: "S6.T2"}
    conditions: >-
      arXiv v7 table; FLOP values are math in the HTML (transcribed). The NIPS 2017 proceedings Table 2 prints 41.0 for
      Transformer (big) EN-FR. Big model: 8 P100 GPUs, 300K steps (3.5 days); base: 100K steps (12 hours). Beam size 4,
      length penalty α = 0.6; checkpoint averaging (last 5 for base, last 20 for big).
    url: "https://arxiv.org/html/1706.03762v7#S6.T2"
  - benchmark: "WMT 2014 English-German development set (newstest2013), architecture variations"
    metric: "PPL (dev), BLEU (dev), params ×10^6"
    values:
      "base": {"N": "6", "d_model": "512", "d_ff": "2048", "h": "8", "d_k": "64", "d_v": "64", "P_drop": "0.1", "ε_ls": "0.1", "train steps": "100K", "PPL (dev)": "4.92", "BLEU (dev)": "25.8", "params ×10^6": "65"}
      "(E) positional embedding instead of sinusoids": {"PPL (dev)": "4.92", "BLEU (dev)": "25.7"}
      "big": {"N": "6", "d_model": "1024", "d_ff": "4096", "h": "16", "P_drop": "0.3", "train steps": "300K", "PPL (dev)": "4.33", "BLEU (dev)": "26.4", "params ×10^6": "213"}
    locator: {table: "Table 3", html_id: "S6.T3"}
    conditions: "Caption: \"Unlisted values are identical to those of the base model. All metrics are on the English-to-German translation development set, newstest2013.\" Perplexities are per-wordpiece. No checkpoint averaging (§6.2)."
    url: "https://arxiv.org/html/1706.03762v7#S6.T3"
  - benchmark: "English constituency parsing, WSJ Section 23"
    metric: "F1"
    values:
      "Transformer (4 layers), WSJ only, discriminative": "91.3"
      "Transformer (4 layers), semi-supervised": "92.7"
    locator: {table: "Table 4", html_id: "S6.T4"}
    conditions: "Caption: \"The Transformer generalizes well to English constituency parsing (Results are on Section 23 of WSJ)\". d_model = 1024; beam size 21, α = 0.3."
    url: "https://arxiv.org/html/1706.03762v7#S6.T4"
```

```yaml
paper: devlin2018-bert
title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
authors: ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"]
earliest_public_date: 2018-10-11
latest_arxiv_version: v2
latest_arxiv_version_date: 2019-05-24
venue: "NAACL-HLT 2019: Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 4171–4186"
venue_source: "https://aclanthology.org/N19-1423/"
venue_notes: >-
  The ACL Anthology page gives Anthology ID N19-1423, Month: June, Year: 2019, Address: Minneapolis, Minnesota,
  Venue: NAACL, Publisher: Association for Computational Linguistics, Pages: 4171–4186, DOI: 10.18653/v1/N19-1423,
  Award: Best Long Paper (saved as src/devlin2018-bert.acl_anthology.html). https://doi.org/10.18653/v1/N19-1423
  redirects (302) to https://aclanthology.org/N19-1423. The arXiv abs page has no Comments or Journal-ref field.
ids:
  arxiv: "1810.04805"
  doi: "10.18653/v1/N19-1423"
  arxiv_doi: "10.48550/arXiv.1810.04805"
  openalex:
    - {id: "W2963341956", kind: proceedings, title_as_listed: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"}
    - {id: "W2896457183", kind: preprint, title_as_listed: "AI-Assisted Pipeline for Dynamic Generation of Trustworthy Health Supplement Content at Scale"}
  s2: "미확인"
  s2_corpus_id: "미확인"
  dblp: "journals/corr/abs-1810-04805"
ids_notes: >-
  W2963341956 (main record) is a conference-paper with doi 10.18653/v1/n19-1423, source "Conference of the North
  American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)",
  biblio pages 4171–4186, publication_date 2019-01-01 (year only), cited_by_count 31891. W2896457183 is what
  /works/doi:10.48550/arXiv.1810.04805 and filter=locations.landing_page_url:http://arxiv.org/abs/1810.04805 return.
  It is the arXiv-preprint record (publication_date 2018-10-11, arXiv OAI and arXiv DOI locations, cited_by_count
  44473), but its metadata is CORRUPTED: the title is "AI-Assisted Pipeline for Dynamic Generation of Trustworthy
  Health Supplement Content at Scale", the doi is 10.4230/lipics.cosit.2022.18, the authorships are Kefallinos et
  al., and it has 20 locations including Dagstuhl/Zenodo items. Do not use its title, authors, doi or topic. No other
  OpenAlex work matches; W3033156098 is a Japanese review article about BERT, not the paper. Semantic Scholar
  returned HTTP 429 on the first call and on 3 retries, so it is 미확인. The DBLP key (CoRR) comes from the arXiv abs
  page link. The NAACL DBLP key was not checked (dblp.org bot challenge).
openalex_primary_topic: {id: "T10028", name: "Topic Modeling", subfield: "Artificial Intelligence", field: "Computer Science", domain: "Physical Sciences"}
openalex_primary_topic_note: "This is the topic of the main record W2963341956 (score 0.99). The corrupted preprint W2896457183 has T11596 \"Constraint Satisfaction and Optimization\" (subfield Computer Networks and Communications); ignore it."
fulltext_url_used: "https://arxiv.org/html/1810.04805"
fulltext_version_served: "1810.04805v2"
raw_file: "src/devlin2018-bert.html"
claims:
  - candidate: "INTRODUCES BERT"
    verdict: supported
    evidence:
      - quote: "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."
        locator: {section: Abstract}
        url: "https://arxiv.org/html/1810.04805v2"
      - quote: "In this paper, we improve the fine-tuning based approaches by proposing BERT: Bidirectional Encoder Representations from Transformers."
        locator: {section: "1 Introduction", paragraph: 4, html_id: "S1.p4"}
        url: "https://arxiv.org/html/1810.04805v2#S1.p4"
    note: ""
  - candidate: "BERT's architecture is a multi-layer bidirectional Transformer encoder based on Vaswani et al. (2017)"
    verdict: supported
    evidence:
      - quote: "BERT’s model architecture is a multi-layer bidirectional Transformer encoder based on the original implementation described in Vaswani et al. (2017) and released in the tensor2tensor library."
        locator: {section: "3 BERT — Model Architecture", paragraph: 1, html_id: "S3.SS0.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px1.p1"
      - quote: "We primarily report results on two model sizes:"
        locator: {section: "3 BERT — Model Architecture", paragraph: 2, html_id: "S3.SS0.SSS0.Px1.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px1.p2"
      - quote: "(L=12, H=768, A=12, Total Parameters=110M)"
        locator: {section: "3 BERT — Model Architecture", paragraph: 2, html_id: "S3.SS0.SSS0.Px1.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px1.p2"
      - quote: "(L=24, H=1024, A=16, Total Parameters=340M)"
        locator: {section: "3 BERT — Model Architecture", paragraph: 2, html_id: "S3.SS0.SSS0.Px1.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px1.p2"
    note: "The apostrophe in \"BERT’s\" is U+2019. The two sizes are BERT_BASE (L=12, H=768, A=12, 110M) and BERT_LARGE (L=24, H=1024, A=16, 340M); the subscripts are math in the HTML."
  - candidate: "BERT EXTENDS the Transformer (same domain, builds on its encoder)"
    verdict: partially_supported
    evidence:
      - quote: "Because the use of Transformers has become common and our implementation is almost identical to the original, we will omit an exhaustive background description of the model architecture"
        locator: {section: "3 BERT — Model Architecture", paragraph: 1, html_id: "S3.SS0.SSS0.Px1.p1"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px1.p1"
      - quote: "Critically, however, the BERT Transformer uses bidirectional self-attention, while the GPT Transformer uses constrained self-attention where every token can only attend to context to its left."
        locator: {section: "3 BERT — Model Architecture", paragraph: 3, html_id: "S3.SS0.SSS0.Px1.p3"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px1.p3"
      - quote: "We note that in the literature the bidirectional Transformer is often referred to as a “Transformer encoder” while the left-context-only version is referred to as a “Transformer decoder” since it can be used for text generation."
        locator: {footnote: 4, html_id: "footnote4"}
        url: "https://arxiv.org/html/1810.04805v2#footnote4"
      - quote: "Unlike left-to-right language model pre-training, the MLM objective enables the representation to fuse the left and the right context, which allows us to pre-train a deep bidirectional Transformer."
        locator: {section: "1 Introduction", paragraph: 4, html_id: "S1.p4"}
        url: "https://arxiv.org/html/1810.04805v2#S1.p4"
      - quote: "For a given token, its input representation is constructed by summing the corresponding token, segment, and position embeddings."
        locator: {section: "3 BERT — Input/Output Representations", paragraph: 3, html_id: "S3.SS0.SSS0.Px2.p3"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px2.p3"
      - quote: "We use a gelu activation Hendrycks and Gimpel (2016) rather than the standard relu, following OpenAI GPT."
        locator: {section: "A.2 Pre-training Procedure", paragraph: 2, html_id: "A1.SS2.p2"}
        url: "https://arxiv.org/html/1810.04805v2#A1.SS2.p2"
      - quote: "Then, we train the rest 10% of the steps of sequence of 512 to learn the positional embeddings."
        locator: {section: "A.2 Pre-training Procedure", paragraph: 4, html_id: "A1.SS2.p4"}
        url: "https://arxiv.org/html/1810.04805v2#A1.SS2.p4"
      - quote: "and OpenAI GPT are nearly identical in terms of model architecture apart from the attention masking."
        locator: {section: "4.1 GLUE", paragraph: 4, html_id: "S4.SS1.p4"}
        url: "https://arxiv.org/html/1810.04805v2#S4.SS1.p4"
    note: >-
      "Builds on its encoder" is directly supported: BERT uses a Transformer encoder stack with bidirectional
      self-attention, and the implementation is "almost identical to the original". "Modifies/extends the
      Transformer" is weak. The changes the text names are small and come from GPT or are standard: GELU instead of
      ReLU, learned position embeddings plus segment embeddings, and the [CLS]/[SEP] input format. BERT's stated
      contribution is the pre-training scheme (masked LM and NSP) and fine-tuning, not a new architecture. The same
      domain (NLP) holds: the Transformer targets sequence transduction (MT, parsing), BERT targets pre-trained
      language representations for NLU. Recommended edges: BERT USES/BUILDS_ON the Transformer (encoder), and
      INTRODUCES MLM/NSP pre-training. Keep EXTENDS only as an interpretive edge.
  - candidate: "The first token of every sequence is always a special classification token ([CLS]); its final hidden state is the aggregate sequence representation for classification"
    verdict: supported
    evidence:
      - quote: "The first token of every sequence is always a special classification token ([CLS]). The final hidden state corresponding to this token is used as the aggregate sequence representation for classification tasks."
        locator: {section: "3 BERT — Input/Output Representations", paragraph: 2, html_id: "S3.SS0.SSS0.Px2.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px2.p2"
      - quote: "the final hidden vector of the special [CLS] token as"
        locator: {section: "3 BERT — Input/Output Representations", paragraph: 2, html_id: "S3.SS0.SSS0.Px2.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS0.SSS0.Px2.p2"
        transcription: 'C\in\mathbb{R}^{H}'
        transcribed: true
      - quote: "and the [CLS] representation is fed into an output layer for classification, such as entailment or sentiment analysis."
        locator: {section: "3.2 Fine-tuning BERT", paragraph: 2, html_id: "S3.SS2.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS2.p2"
      - quote: "corresponding to the first input token ([CLS]) as the aggregate representation."
        locator: {section: "4.1 GLUE", paragraph: 2, html_id: "S4.SS1.p2"}
        url: "https://arxiv.org/html/1810.04805v2#S4.SS1.p2"
      - quote: "is used for next sentence prediction (NSP)."
        locator: {section: "3.1 Pre-training BERT — Task #2: Next Sentence Prediction (NSP)", paragraph: 1, html_id: "S3.SS1.SSS0.Px2.p1"}
        url: "https://arxiv.org/html/1810.04805v2#S3.SS1.SSS0.Px2.p1"
        transcription: 'C'
        transcribed: true
      - quote: "is not a meaningful sentence representation without fine-tuning, since it was trained with NSP."
        locator: {footnote: 6, html_id: "footnote6"}
        url: "https://arxiv.org/html/1810.04805v2#footnote6"
        transcription: 'The\ vector\ C'
        transcribed: true
    note: >-
      Footnote 6 qualifies this. C (the final [CLS] vector) is trained by NSP during pre-training and "is not a
      meaningful sentence representation without fine-tuning". It acts as the aggregate representation for
      classification only after fine-tuning. For GLUE, the only new parameters are a classification layer
      W ∈ R^{K×H} on C (§4.1).
results:
  - benchmark: "Headline results (abstract)"
    metric: "GLUE score; MultiNLI accuracy; SQuAD v1.1 Test F1; SQuAD v2.0 Test F1"
    values: {"GLUE score": "80.5% (7.7% point absolute improvement)", "MultiNLI accuracy": "86.7% (4.6% absolute improvement)", "SQuAD v1.1 Test F1": "93.2 (1.5 point absolute improvement)", "SQuAD v2.0 Test F1": "83.1 (5.1 point absolute improvement)"}
    locator: {section: Abstract}
    conditions: "Abstract quote: \"It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement)\". The GLUE 80.5 is the official leaderboard score of BERT_LARGE, compared with 72.8 for OpenAI GPT (§4.1 p4). It is not the Table 1 \"Average\" column."
    url: "https://arxiv.org/html/1810.04805v2"
  - benchmark: "GLUE test (evaluation server)"
    metric: "accuracy (F1 for QQP/MRPC, Spearman for STS-B); Average excludes WNLI"
    values:
      "BERT_BASE": {"MNLI-(m/mm)": "84.6/83.4", "QQP": "71.2", "QNLI": "90.5", "SST-2": "93.5", "CoLA": "52.1", "STS-B": "85.8", "MRPC": "88.9", "RTE": "66.4", "Average": "79.6"}
      "BERT_LARGE": {"MNLI-(m/mm)": "86.7/85.9", "QQP": "72.1", "QNLI": "92.7", "SST-2": "94.9", "CoLA": "60.5", "STS-B": "86.5", "MRPC": "89.3", "RTE": "70.1", "Average": "82.1"}
      "OpenAI GPT": {"MNLI-(m/mm)": "82.1/81.4", "QQP": "70.3", "QNLI": "87.4", "SST-2": "91.3", "CoLA": "45.4", "STS-B": "80.0", "MRPC": "82.3", "RTE": "56.0", "Average": "75.1"}
    locator: {table: "Table 1", html_id: "S3.T1"}
    conditions: "Caption: \"GLUE Test results, scored by the evaluation server\". The \"Average\" column differs from the official GLUE score because it excludes WNLI. BERT and GPT are single-model, single-task. Row labels BERT_BASE/BERT_LARGE are subscript math in the HTML."
    url: "https://arxiv.org/html/1810.04805v2#S3.T1"
  - benchmark: "SQuAD 1.1"
    metric: "EM / F1"
    values:
      "BERT_BASE (Single)": {"Dev EM": "80.8", "Dev F1": "88.5", "Test EM": "-", "Test F1": "-"}
      "BERT_LARGE (Single)": {"Dev EM": "84.1", "Dev F1": "90.9", "Test EM": "-", "Test F1": "-"}
      "BERT_LARGE (Sgl.+TriviaQA)": {"Dev EM": "84.2", "Dev F1": "91.1", "Test EM": "85.1", "Test F1": "91.8"}
      "BERT_LARGE (Ens.+TriviaQA)": {"Dev EM": "86.2", "Dev F1": "92.2", "Test EM": "87.4", "Test F1": "93.2"}
    locator: {table: "Table 2", html_id: "S4.T2"}
    conditions: "Caption: \"SQuAD 1.1 results.\" The headline Test F1 93.2 is an ensemble (7 systems) fine-tuned with extra TriviaQA data. The compared top leaderboard entry (#1 Ensemble - nlnet) has Test F1 91.7 (Dec 10th, 2018)."
    url: "https://arxiv.org/html/1810.04805v2#S4.T2"
  - benchmark: "SQuAD 2.0"
    metric: "EM / F1"
    values:
      "BERT_LARGE (Single)": {"Dev EM": "78.7", "Dev F1": "81.9", "Test EM": "80.0", "Test F1": "83.1"}
    locator: {table: "Table 3", html_id: "S4.T3"}
    conditions: "Caption: \"SQuAD 2.0 results.\" The best compared system is #1 Single - MIR-MRC (F-Net) with Test F1 78.0; entries that use BERT are excluded."
    url: "https://arxiv.org/html/1810.04805v2#S4.T3"
```
