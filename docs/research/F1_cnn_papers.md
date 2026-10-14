# F1 — CNN-era seed papers: metadata, raw full texts, claim verification

Verified 2026-10-15. Raw files live in `src/` (paths below are relative to this file's directory).
Quotes were machine-checked against the raw file text: pypdf `extract_text()` (PDF) or BeautifulSoup `get_text()` (arXiv HTML), then Unicode NFKC + whitespace collapse.
Paragraph numbers for arXiv-HTML papers follow the LaTeXML paragraph ids (`S<sec>.p<n>`); for PDFs they are counted by hand.
Extra keys beyond the requested schema: `metadata_notes` (top level) and `ids.cacm_2017_doi` (AlexNet only).
Other raw sources in `src/` (prefixed `<slug>.`): OpenAlex / Crossref / S2 JSON responses, proceedings landing pages (NeurIPS, PMLR, CVF, nips.cc 2012), and the arXiv PDFs used to cross-check the HTML quotes (`simonyan2014-vgg.arxiv-v6.pdf`, `ioffe2015-batchnorm.arxiv-v3.pdf`, `santurkar2018-bn-optimization.arxiv-v5.pdf`, `he2015-resnet.arxiv-v1.pdf`). Every HTML quote matches the PDF as well (alphanumeric comparison). The only misses were two ResNet quotes that a table/page break splits in the PDF; both halves of each are present.
Not reachable: DBLP (dblp.org returns an anti-bot challenge page), IEEE Xplore (HTTP 202, empty body), and Semantic Scholar for some calls (HTTP 429; marked 미확인).

```yaml
paper: deng2009-imagenet
title: "ImageNet: A Large-Scale Hierarchical Image Database"
authors: ["Jia Deng", "Wei Dong", "Richard Socher", "Li-Jia Li", "Kai Li", "Li Fei-Fei"]
earliest_public_date: 2009-06-20
latest_arxiv_version: "n/a (not on arXiv)"
venue: "CVPR 2009"
venue_source: "https://api.crossref.org/works/10.1109/CVPR.2009.5206848"
ids:
  arxiv: ""
  doi: "10.1109/CVPR.2009.5206848"
  arxiv_doi: ""
  openalex:
    - {id: "W2108598243", kind: proceedings, title_as_listed: "ImageNet: A large-scale hierarchical image database"}
    - {id: "W4239072543", kind: proceedings, title_as_listed: "ImageNet: A large-scale hierarchical image database"}
  s2: "d2c733e34d48784a37d717fe43d9e93277a8c53e"
  s2_corpus_id: 57246310
  dblp: "conf/cvpr/DengDSLL009"
openalex_primary_topic: {id: "T10824", name: "Image Retrieval and Classification Techniques", subfield: "Computer Vision and Pattern Recognition [subfields/1707]", field: "Computer Science [fields/17]", domain: "Physical Sciences [domains/3]"}
fulltext_url_used: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"
raw_file: "src/deng2009-imagenet.pdf"
metadata_notes:
  - "Not on arXiv. earliest_public_date = CVPR 2009 start date (Crossref event start 2009-06-20; S2 publicationDate 2009-06-20). The image-net.org PDF has CreationDate 2009-04-01, but when it was first posted is unknown."
  - "Crossref: container '2009 IEEE Conference on Computer Vision and Pattern Recognition', pp. 248-255, IEEE. Crossref's event name reads '... Workshops (CVPR Workshops)', which looks like an IEEE metadata quirk. IEEE Xplore page not fetchable (HTTP 202, empty body)."
  - "Raw file is the authors' copy on image-net.org (8 pp.), not the IEEE Xplore PDF."
  - "OpenAlex W4239072543 is a duplicate created from DOI 10.1109/CVPRW.2009.5206848, which the doi.org handle API shows is an HS_ALIAS of 10.1109/CVPR.2009.5206848. Main work = W2108598243. OpenAlex lists the first author there as 'Jia Hao Deng', a disambiguation artifact (the paper prints 'Jia Deng')."
  - "OpenAlex W2056568601 ('ImageNet: Constructing a large-scale image database', Journal of Vision, 2010) is a different work, not a version of this paper."
  - "S2 (DOI lookup): externalIds MAG 2108598243, DBLP conf/cvpr/DengDSLL009, DOI 10.1109/CVPR.2009.5206848, CorpusId 57246310; venue '2009 IEEE Conference on Computer Vision and Pattern Recognition'; publicationDate 2009-06-20."
  - "The DBLP key comes from S2 externalIds. dblp.org returned a bot-check page, so the key was not checked on DBLP itself."
claims:
  - candidate: "Deng et al. (2009) INTRODUCES the dataset ImageNet."
    verdict: supported
    evidence:
      - {quote: "We introduce here a new database called “ImageNet”", locator: {section: Abstract}, url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
      - {quote: "In this paper, we introduce a new image database called “ImageNet”, a large-scale ontology of images.", locator: {section: "1 Introduction", paragraph: 1}, url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
    note: "The abstract sentence continues ', a large-scale ontology of images built upon the backbone of the WordNet structure', but a line-end hyphen ('large-'/'scale') breaks the span in the extracted text, so the Section 1 sentence is quoted for that part."
  - candidate: "Scale stated in the abstract: 12 subtrees, 5247 synsets, 3.2 million images."
    verdict: supported
    evidence:
      - {quote: "This paper offers a detailed analysis of ImageNet in its current state: 12 subtrees with 5247 synsets and 3.2 million images in total.", locator: {section: Abstract}, url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
      - {quote: "ImageNet aims to populate the majority of the 80,000 synsets of WordNet", locator: {section: Abstract}, url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
      - {quote: "This will result in tens of millions of annotated images", locator: {section: Abstract}, url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
      - {quote: "These subtrees contain 5247 synsets and 3.2 million images.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
    note: "Keep the reported state apart from the goal. Reported state: 12 subtrees, 5247 synsets, 3.2M images. Goal: the majority of WordNet's ~80,000 synsets with an average of 500-1000 images each (a line-end hyphen splits '500-1000' in the extracted text), i.e. 'tens of millions'; Sec. 2 says 'in the order of 50 million'. The often-quoted '15M images / 22K categories' describes later ImageNet releases (e.g. as cited by Krizhevsky et al. 2012), not this paper."
results:
  - {benchmark: "ImageNet (state at time of paper)", metric: "dataset size", values: {subtrees: 12, synsets: 5247, images: "3.2 million"}, locator: {section: Abstract}, conditions: "12 subtrees (mammal, bird, fish, reptile, amphibian, vehicle, furniture, musical instrument, geological formation, tool, flower, fruit), per Sec. 1", url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
  - {benchmark: "ImageNet selected subtrees", metric: "# Synsets / Avg. synset size / Total # image", values: {Mammal: "1170 / 737 / 862K", Vehicle: "520 / 610 / 317K", GeoForm: "176 / 436 / 77K", Furniture: "197 / 797 / 157K", Bird: "872 / 809 / 705K", MusicInstr: "164 / 672 / 110K"}, locator: {figure: "Figure 2", part: "embedded table 'Summary of selected subtrees'"}, conditions: "as printed in the Figure 2 table", url: "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf"}
```

```yaml
paper: krizhevsky2012-alexnet
title: "ImageNet Classification with Deep Convolutional Neural Networks"
authors: ["Alex Krizhevsky", "Ilya Sutskever", "Geoffrey E. Hinton"]
earliest_public_date: 2012-12-03
latest_arxiv_version: "n/a (not on arXiv)"
venue: "NIPS 2012 (Advances in Neural Information Processing Systems 25; the conference is now NeurIPS)"
venue_source: "https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html"
ids:
  arxiv: ""
  doi: ""
  cacm_2017_doi: "10.1145/3065386"
  arxiv_doi: ""
  openalex:
    - {id: "W2163605009", kind: journal, title_as_listed: "ImageNet classification with deep convolutional neural networks"}
    - {id: "W3147600416", kind: journal, title_as_listed: "ImageNet classification with deep convolutional neural networks"}
  s2: "abd1c342495432171beb7ca8fd9551ef13cbd0ff"
  s2_corpus_id: 195908774
  dblp: "conf/nips/KrizhevskySH12"
openalex_primary_topic: {id: "T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition [subfields/1707]", field: "Computer Science [fields/17]", domain: "Physical Sciences [domains/3]"}
fulltext_url_used: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"
raw_file: "src/krizhevsky2012-alexnet.pdf"
metadata_notes:
  - "Not on arXiv. earliest_public_date = NIPS 2012 opening day (nips.cc/Conferences/2012: 'Mon Dec 3rd through Sat the 8th', Lake Tahoe). When the proceedings first went online was not verified."
  - "The NIPS 2012 version has no DOI. PDF metadata: Advances in Neural Information Processing Systems 25, pp. 1097-1105, eds. F. Pereira, C.J.C. Burges, L. Bottou, K.Q. Weinberger, Curran Associates."
  - "The abstract on the papers.nips.cc page is NOT the abstract printed in the PDF. The page says 1.3 million images, 39.7%/18.9%, 500,000 neurons and 'two globally connected layers'; the PDF says 1.2 million, 37.5%/17.0%, 650,000 neurons, three fully-connected layers, dropout, and ILSVRC-2012 15.3%. Every quote below comes from the PDF."
  - "A CACM version exists (Crossref): DOI 10.1145/3065386, Communications of the ACM 60(6):84-90, published 2017-05-24."
  - "OpenAlex merges the two versions: W2163605009 carries the CACM DOI and date 2017-05-24 plus a location for the NIPS PDF (books.nips.cc/papers/files/nips25/NIPS2012_0534.pdf). Neither search nor the title.search filter turned up a separate NIPS-2012 work. W3147600416 is a CiNii-derived stub (no DOI, author 'Krizhevsky' only, source wrongly set to 'Medical Entomology and Zoology'), not a real journal version."
  - "S2 also merges them: paperId abd1c342... has externalIds DBLP conf/nips/KrizhevskySH12 + DOI 10.1145/3065386 (+ MAG 2997031122, CorpusId 195908774), venue 'Communications of the ACM', year 2012, publicationDate 2012-12-03. The S2 title search got HTTP 429 on the first try and all 3 retries, so whether S2 holds other duplicates is 미확인."
  - "The DBLP key is from S2 externalIds (dblp.org bot-check, not checked directly). The paper never uses the name 'AlexNet'."
claims:
  - candidate: "Krizhevsky et al. (2012) INTRODUCES the AlexNet CNN."
    verdict: supported
    evidence:
      - {quote: "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest", locator: {section: Abstract}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "The neural network, which has 60 million parameters and 650,000 neurons, consists of five convolutional layers, some of which are followed by max-pooling layers, and three fully-connected layers with a final 1000-way softmax.", locator: {section: Abstract}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Below, we describe some of the novel or unusual features of our network’s architecture.", locator: {section: "3 The Architecture", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "'AlexNet' is a community name; the paper only says 'our network'/'CNN'. Map the KG node 'AlexNet' to this paper's 8-layer CNN (5 conv + 3 fully-connected)."
  - candidate: "AlexNet was trained on the ILSVRC subsets of ImageNet (ILSVRC-2010 and ILSVRC-2012)."
    verdict: supported
    evidence:
      - {quote: "we trained one of the largest convolutional neural networks to date on the subsets of ImageNet used in the ILSVRC-2010 and ILSVRC-2012 competitions [2] and achieved by far the best results ever reported on these datasets.", locator: {section: "1 Introduction", paragraph: 4}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "ILSVRC uses a subset of ImageNet with roughly 1000 images in each of 1000 categories.", locator: {section: "2 The Dataset", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "ILSVRC-2010 is the only version of ILSVRC for which the test set labels are available, so this is the version on which we performed most of our experiments.", locator: {section: "2 The Dataset", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Since we also entered our model in the ILSVRC-2012 competition, in Section 6 we report our results on this version of the dataset as well, for which test set labels are unavailable.", locator: {section: "2 The Dataset", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "and ImageNet [6], which consists of over 15 million labeled high-resolution images in over 22,000 categories.", locator: {section: "1 Introduction", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "Years: ILSVRC-2010 (most experiments; test labels available) and ILSVRC-2012 (competition entry). Ref [6] = Deng et al., 'ImageNet: A Large-Scale Hierarchical Image Database', CVPR09, so this supports a USES edge to deng2009-imagenet. Caveat: some ILSVRC-2012 models ('1 CNN*', '7 CNNs*') were pre-trained on the whole ImageNet Fall 2011 release (15M images, 22K categories), and Sec. 6 also reports results on ImageNet Fall 2009 (10,184 categories, 8.9M images)."
  - candidate: "ILSVRC-2012: winning top-5 test error 15.3% vs 26.2% for the second-best entry."
    verdict: supported
    evidence:
      - {quote: "We also entered a variant of this model in the ILSVRC-2012 competition and achieved a winning top-5 test error rate of 15.3%, compared to 26.2% achieved by the second-best entry.", locator: {section: Abstract}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Models with an asterisk* were “pre-trained” to classify the entire ImageNet 2011 Fall release.", locator: {table: "Table 2", part: caption}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "15.3% is the '7 CNNs*' ensemble in Table 2: five CNNs plus two pre-trained on Fall 2011, so it used extra training data. That is why VGG's Table 7 (without outside data) lists Krizhevsky et al. at 16.4% (5 nets). A single CNN scores 18.2% top-5 (val). The second-best 26.2% is 'SIFT + FVs [7]'."
  - candidate: "ILSVRC-2010 test: top-1 37.5% and top-5 17.0%."
    verdict: supported
    evidence:
      - {quote: "On the test data, we achieved top-1 and top-5 error rates of 37.5% and 17.0% which is considerably better than the previous state-of-the-art.", locator: {section: Abstract}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "error rates without averaging predictions over ten patches as described in Section 4.1 are 39.0% and 18.3%.", locator: {footnote: 5}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "37.5/17.0 average predictions over 10 patches at test time (4 corners + center, plus their horizontal reflections); with a single view the numbers are 39.0/18.3."
  - candidate: "AlexNet USES the ReLU nonlinearity (Sec. 3.1), following Nair and Hinton."
    verdict: supported
    evidence:
      - {quote: "Following Nair and Hinton [20], we refer to neurons with this nonlinearity as Rectified Linear Units (ReLUs).", locator: {section: "3.1 ReLU Nonlinearity", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "with ReLUs train several times faster than their equivalents with tanh units.", locator: {section: "3.1 ReLU Nonlinearity", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "A four-layer convolutional neural network with ReLUs (solid line) reaches a 25% training error rate on CIFAR-10 six times faster than an equivalent network with tanh neurons (dashed line).", locator: {figure: "Figure 1", part: caption}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "We are not the first to consider alternatives to", locator: {section: "3.1 ReLU Nonlinearity", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "transcription (flagged): 'f(x) = \\max(0, x)'. Ref [20] = V. Nair and G. E. Hinton, 'Rectified linear units improve restricted boltzmann machines', ICML 2010. The paper adopts ReLUs and does not claim to have introduced them, so model the edge as USES, not INTRODUCES."
  - candidate: "AlexNet trains on multiple GPUs (Sec. 3.2)."
    verdict: supported
    evidence:
      - {quote: "Therefore we spread the net across two GPUs.", locator: {section: "3.2 Training on Multiple GPUs", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "This scheme reduces our top-1 and top-5 error rates by 1.7% and 1.2%, respectively, as compared with a net with half as many kernels in each convolutional layer trained on one GPU.", locator: {section: "3.2 Training on Multiple GPUs", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Our network takes between five and six days to train on two GTX 580 3GB GPUs.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "Exactly two GPUs (GTX 580, 3GB), using model parallelism: half the kernels on each GPU, with communication only in certain layers."
  - candidate: "AlexNet uses local response normalization (Sec. 3.3)."
    verdict: supported
    evidence:
      - {quote: "However, we still find that the following local normalization scheme aids generalization.", locator: {section: "3.3 Local Response Normalization", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "This scheme bears some resemblance to the local contrast normalization scheme of Jarrett et al. [11], but ours would be more correctly termed “brightness normalization”, since we do not subtract the mean activity.", locator: {section: "3.3 Local Response Normalization", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Response normalization reduces our top-1 and top-5 error rates by 1.4% and 1.2%, respectively.", locator: {section: "3.3 Local Response Normalization", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "transcription (flagged): 'b^{i}_{x,y} = a^{i}_{x,y} / \\left(k + \\alpha \\sum_{j=\\max(0,i-n/2)}^{\\min(N-1,i+n/2)} (a^{j}_{x,y})^{2}\\right)^{\\beta}', with k=2, n=5, alpha=10^{-4}, beta=0.75. This is the paper's own scheme, related to Jarrett et al. [11]. VGG later reports that LRN does not help (Simonyan & Zisserman, Sec. 2.1/4.1)."
  - candidate: "AlexNet uses overlapping pooling (Sec. 3.4)."
    verdict: supported
    evidence:
      - {quote: "Traditionally, the neighborhoods summarized by adjacent pooling units do not overlap (e.g., [17, 11, 4]).", locator: {section: "3.4 Overlapping Pooling", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "This scheme reduces the top-1 and top-5 error rates by 0.4% and 0.3%, respectively, as compared with the non-overlapping scheme", locator: {section: "3.4 Overlapping Pooling", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "We generally observe during training that models with overlapping pooling find it slightly more difficult to overfit.", locator: {section: "3.4 Overlapping Pooling", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "transcription (flagged): overlapping pooling when 's < z'; used throughout with 's = 2, z = 3', compared against non-overlapping 's = 2, z = 2'."
  - candidate: "AlexNet uses data augmentation (Sec. 4.1)."
    verdict: supported
    evidence:
      - {quote: "The easiest and most common method to reduce overfitting on image data is to artificially enlarge the dataset using label-preserving transformations (e.g., [25, 4, 5]).", locator: {section: "4.1 Data Augmentation", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Without this scheme, our network suffers from substantial overfitting, which would have forced us to use much smaller networks.", locator: {section: "4.1 Data Augmentation", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "The second form of data augmentation consists of altering the intensities of the RGB channels in training images.", locator: {section: "4.1 Data Augmentation", paragraph: 3}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "This scheme reduces the top-1 error rate by over 1%.", locator: {section: "4.1 Data Augmentation", paragraph: 3}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "Two forms: (1) random 224x224 crops plus horizontal reflections of the 256x256 images (paragraph 2; its first sentence is broken by a line-end hyphen in 'reflec-tions', so it is not quoted); (2) PCA-based RGB intensity jitter. The paper presents augmentation as a way to reduce overfitting rather than as a new technique (it cites [25, 4, 5])."
  - candidate: "AlexNet USES dropout (Sec. 4.2), citing its source."
    verdict: supported
    evidence:
      - {quote: "The recently-introduced technique, called “dropout” [10], consists of setting to zero the output of each hidden neuron with probability 0.5.", locator: {section: "4.2 Dropout", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "We use dropout in the first two fully-connected layers of Figure 2.", locator: {section: "4.2 Dropout", paragraph: 2}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "To reduce overfitting in the fully-connected layers we employed a recently-developed regularization method called “dropout” that proved to be very effective.", locator: {section: Abstract}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "Ref [10] = G.E. Hinton, N. Srivastava, A. Krizhevsky, I. Sutskever, R.R. Salakhutdinov, 'Improving neural networks by preventing co-adaptation of feature detectors', arXiv:1207.0580, 2012. Dropout comes from [10], which shares co-authors with this paper, so the edge is USES rather than INTRODUCES. At test time all neurons are used with outputs multiplied by 0.5."
  - candidate: "AlexNet ADDRESSES overfitting (Sec. 4 'Reducing Overfitting')."
    verdict: supported
    evidence:
      - {quote: "Our neural network architecture has 60 million parameters.", locator: {section: "4 Reducing Overfitting", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "this turns out to be insufficient to learn so many parameters without considerable overfitting.", locator: {section: "4 Reducing Overfitting", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "Below, we describe the two primary ways in which we combat overfitting.", locator: {section: "4 Reducing Overfitting", paragraph: 1}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
      - {quote: "The size of our network made overfitting a significant problem, even with 1.2 million labeled training examples, so we used several effective techniques for preventing overfitting, which are described in Section 4.", locator: {section: "1 Introduction", paragraph: 4}, url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
    note: "The section's first sentence is just 'Our neural network architecture has 60 million parameters.'; the problem itself is stated in the next sentence. The two methods are data augmentation (4.1) and dropout (4.2)."
results:
  - {benchmark: "ILSVRC-2010", metric: "top-1 / top-5 error (test)", values: {"Sparse coding [2]": "47.1% / 28.2%", "SIFT + FVs [24]": "45.7% / 25.7%", "CNN": "37.5% / 17.0%"}, locator: {table: "Table 1"}, conditions: "test set; CNN = single network with 10-patch test-time averaging (single view: 39.0% / 18.3%, footnote 5); the first two rows are the best results by others", url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
  - {benchmark: "ILSVRC-2012", metric: "Top-1 (val) / Top-5 (val) / Top-5 (test)", values: {"SIFT + FVs [7]": "— / — / 26.2%", "1 CNN": "40.7% / 18.2% / —", "5 CNNs": "38.1% / 16.4% / 16.4%", "1 CNN*": "39.0% / 16.6% / —", "7 CNNs*": "36.7% / 15.4% / 15.3%"}, locator: {table: "Table 2"}, conditions: "* = pre-trained on the entire ImageNet Fall 2011 release (15M images, 22K categories), then fine-tuned; 1 CNN* has an extra sixth conv layer; 7 CNNs* = the five CNNs + two pre-trained CNNs; SIFT + FVs [7] = second-best contest entry", url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
  - {benchmark: "ImageNet Fall 2009 (10,184 categories, 8.9M images)", metric: "top-1 / top-5 error", values: {"this paper": "67.4% / 40.9%", "best published [19]": "78.1% / 60.9%"}, locator: {section: "6 Results", paragraph: 3}, conditions: "half the images for training, half for testing (own split); net with an additional sixth conv layer", url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
  - {benchmark: "ILSVRC (ablations reported in text)", metric: "reduction in top-1 / top-5 error", values: {"two-GPU vs one-GPU half-kernel net (3.2)": "1.7% / 1.2%", "local response normalization (3.3)": "1.4% / 1.2%", "overlapping vs non-overlapping pooling (3.4)": "0.4% / 0.3%", "PCA colour augmentation (4.1)": "top-1 by over 1%"}, locator: {section: "3.2-3.4, 4.1"}, conditions: "dataset split not stated per ablation; numbers as printed", url: "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf"}
```

```yaml
paper: simonyan2014-vgg
title: "Very Deep Convolutional Networks for Large-Scale Image Recognition"
authors: ["Karen Simonyan", "Andrew Zisserman"]
earliest_public_date: 2014-09-04
latest_arxiv_version: v6
venue: "ICLR 2015"
venue_source: "https://arxiv.org/html/1409.1556"
ids:
  arxiv: "1409.1556"
  doi: ""
  arxiv_doi: "10.48550/arXiv.1409.1556"
  openalex:
    - {id: "W1686810756", kind: preprint, title_as_listed: "Very Deep Convolutional Networks for Large-Scale Image Recognition"}
    - {id: "W3209259379", kind: journal, title_as_listed: "Very deep convolutional networks for large-scale image recognition"}
  s2: "eb42cf88027de515750f230b23b1a057dc782108"
  s2_corpus_id: 14124313
  dblp: "conf/iclr/SimonyanZ14a"
openalex_primary_topic: {id: "T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition [subfields/1707]", field: "Computer Science [fields/17]", domain: "Physical Sciences [domains/3]"}
fulltext_url_used: "https://arxiv.org/html/1409.1556"
raw_file: "src/simonyan2014-vgg.html"
metadata_notes:
  - "arXiv history: v1 2014-09-04, v2 2014-09-15, v3 2014-11-18, v4 2014-12-19, v5 2014-12-23, v6 2015-04-10. The HTML is v6."
  - "Venue ICLR 2015 is confirmed three ways: Appendix C of the full text ('v6 Camera-ready ICLR-2015 conference paper.'), the v6 PDF header ('Published as a conference paper at ICLR 2015', https://arxiv.org/pdf/1409.1556v6), and the arXiv abs page's DBLP link conf/iclr/SimonyanZ14a. ICLR 2015 assigned no DOI."
  - "S2 externalIds: MAG 2949429431, ArXiv 1409.1556, DBLP journals/corr/SimonyanZ14a (the CoRR record), CorpusId 14124313; venue 'International Conference on Learning Representations', year 2014, publicationDate 2014-09-04."
  - "OpenAlex has no ICLR proceedings work. W3209259379 is a CiNii stub (no DOI, author 'Simonyan', source '(No Title)'). Main work = W1686810756 (preprint)."
  - "The abs-page abstract prints '16-19' with a hyphen; the HTML full text prints '16–19' with an en dash. The quote below uses the HTML form."
claims:
  - candidate: "Simonyan & Zisserman INTRODUCES the VGG ConvNet configurations."
    verdict: supported
    evidence:
      - {quote: "Our main contribution is a thorough evaluation of networks of increasing depth using an architecture with very small", locator: {section: Abstract}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "convolution filters, which shows that a significant improvement on the prior-art configurations can be achieved by pushing the depth to 16–19 weight layers.", locator: {section: Abstract}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "The ConvNet configurations, evaluated in this paper, are outlined in Table 1, one per column.", locator: {section: "2.2 Configurations", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "In the following we will refer to the nets by their names (A–E).", locator: {section: "2.2 Configurations", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "Our method is denoted as “VGG”.", locator: {table: "Table 7", part: caption}, url: "https://arxiv.org/html/1409.1556"}
    note: "transcription (flagged): the gap between the two abstract quotes is '($3\\times 3$)'. The paper names its configurations A–E (D = 16, E = 19 weight layers); 'VGG' is the team/method name. 'VGG-16'/'VGG-19' are later labels, used e.g. by He et al. 2016. The abstract calls the contribution 'a thorough evaluation' of depth, but the configurations themselves are new."
  - candidate: "VGG ADDRESSES the effect of ConvNet depth on accuracy."
    verdict: supported
    evidence:
      - {quote: "In this work we investigate the effect of the convolutional network depth on its accuracy in the large-scale image recognition setting.", locator: {section: Abstract}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "In this paper, we address another important aspect of ConvNet architecture design – its depth.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "Second, we observe that the classification error decreases with the increased ConvNet depth: from 11 layers in A to 19 layers in E.", locator: {section: "4.1 Single Scale Evaluation", paragraph: 3}, url: "https://arxiv.org/html/1409.1556"}
    note: "Same paragraph: the error saturates at 19 layers on this dataset."
  - candidate: "VGG uses small 3×3 filters throughout; a stack of 3×3 conv layers has a larger effective receptive field (Sec. 2.3)."
    verdict: supported
    evidence:
      - {quote: "(which is the smallest size to capture the notion of left/right, up/down, center)", locator: {section: "2.1 Architecture", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "conv. layers (without spatial pooling in between) has an effective receptive field of", locator: {section: "2.3 Discussion", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "First, we incorporate three non-linear rectification layers instead of a single one, which makes the decision function more discriminative.", locator: {section: "2.3 Discussion", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "which confirms that a deep net with small filters outperforms a shallow net with larger filters.", locator: {section: "4.1 Single Scale Evaluation", paragraph: 3}, url: "https://arxiv.org/html/1409.1556"}
    note: "transcription (flagged), Sec. 2.3: 'It is easy to see that a stack of two $3\\times 3$ conv. layers (without spatial pooling in between) has an effective receptive field of $5\\times 5$; three such layers have a $7\\times 7$ effective receptive field.' Parameters: '$3\\left(3^{2}C^{2}\\right)=27C^{2}$' weights vs '$7^{2}C^{2}=49C^{2}$', i.e. '$81\\%$' more. Sec. 2.1: stride 1, padding 1 for 3×3 layers. One configuration (C) also uses 1×1 convolutions."
  - candidate: "VGG's design principles were INSPIRED_BY Krizhevsky et al. (2012) (and Ciresan et al. 2011)."
    verdict: supported
    evidence:
      - {quote: "all our ConvNet layer configurations are designed using the same principles, inspired by Ciresan et al. (2011); Krizhevsky et al. (2012).", locator: {section: "2 ConvNet Configurations", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "The ConvNet training procedure generally follows Krizhevsky et al. (2012) (except for sampling the input crops from multi-scale training images, as explained later).", locator: {section: "3.1 Training", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "All hidden layers are equipped with the rectification (ReLU (Krizhevsky et al., 2012)) non-linearity.", locator: {section: "2.1 Architecture", paragraph: 3}, url: "https://arxiv.org/html/1409.1556"}
    note: "This is the paper's own wording for the relation: 'inspired by' two works, Ciresan et al. 2011 and Krizhevsky et al. 2012. The training procedure 'generally follows' Krizhevsky et al. 2012."
  - candidate: "VGG EXTENDS AlexNet (builds on and modifies its design)."
    verdict: partially_supported
    evidence:
      - {quote: "a number of attempts have been made to improve the original architecture of Krizhevsky et al. (2012) in a bid to achieve better accuracy.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "Our ConvNet configurations are quite different from the ones used in the top-performing entries of the ILSVRC-2012 (Krizhevsky et al., 2012) and ILSVRC-2013 competitions (Zeiler & Fergus, 2013; Sermanet et al., 2014).", locator: {section: "2.3 Discussion", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "We note that none of our networks (except for one) contain Local Response Normalisation (LRN) normalisation (Krizhevsky et al., 2012)", locator: {section: "2.1 Architecture", paragraph: 3}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "Notably, we did not depart from the classical ConvNet architecture of LeCun et al. (1989), but improved it by substantially increasing the depth.", locator: {section: "4.5 Comparison with the State of the Art", paragraph: 2}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "state-of-the-art performance on the ImageNet challenge dataset can be achieved using a conventional ConvNet architecture (LeCun et al., 1989; Krizhevsky et al., 2012) with substantially increased depth.", locator: {section: "5 Conclusion", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
    note: "The paper never says it extends AlexNet. What it does say: (a) design principles are 'inspired by' Ciresan 2011 and Krizhevsky 2012; (b) training follows Krizhevsky; it reuses ReLU, drops LRN (Sec. 4.1: LRN does not help), and replaces AlexNet's large first-layer filters (11×11, stride 4) with 3×3, stride 1 throughout; (c) it calls its configurations 'quite different' from Krizhevsky et al.'s; (d) it describes itself as the classical ConvNet of LeCun et al. (1989), or a 'conventional ConvNet architecture (LeCun et al., 1989; Krizhevsky et al., 2012)', with more depth. Recommended edges: VGG INSPIRED_BY AlexNet (+ Ciresan 2011) and VGG IMPROVES_ON AlexNet (Table 7). If EXTENDS is kept, its target should be the conventional ConvNet lineage (LeCun 1989; Krizhevsky 2012), not AlexNet alone."
  - candidate: "ILSVRC-2014: VGG placed 2nd in classification and 1st in localisation."
    verdict: supported
    evidence:
      - {quote: "These findings were the basis of our ImageNet Challenge 2014 submission, where our team secured the first and the second places in the localisation and classification tracks respectively.", locator: {section: Abstract}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "In the classification task of ILSVRC-2014 challenge (Russakovsky et al., 2014), our “VGG” team secured the 2nd place with", locator: {section: "4.5 Comparison with the State of the Art", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "test error, our “VGG” team won the localisation challenge of ILSVRC-2014 (Russakovsky et al., 2014).", locator: {section: "A.2 Localisation Experiments (Comparison with the state of the art.)", paragraph: 1}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "Our result is also competitive with respect to the classification task winner (GoogLeNet with", locator: {section: "4.5 Comparison with the State of the Art", paragraph: 2}, url: "https://arxiv.org/html/1409.1556"}
    note: "transcription (flagged): classification '... 2nd place with $7.3\\%$ test error using an ensemble of 7 models'; post-submission '$6.8\\%$' with 2 models; the winner GoogLeNet had '$6.7\\%$'; localisation 'With $25.3\\%$ test error, ...'."
  - candidate: "VGG IMPROVES_ON Krizhevsky et al. (2012) on ILSVRC classification (Table 7)."
    verdict: supported
    evidence:
      - {quote: "As can be seen from Table 7, our very deep ConvNets significantly outperform the previous generation of models, which achieved the best results in the ILSVRC-2012 and ILSVRC-2013 competitions.", locator: {section: "4.5 Comparison with the State of the Art", paragraph: 2}, url: "https://arxiv.org/html/1409.1556"}
      - {quote: "Only the results obtained without outside training data are reported.", locator: {table: "Table 7", part: caption}, url: "https://arxiv.org/html/1409.1556"}
    note: "Table 7 lists Krizhevsky et al. at 16.4% top-5 test (5 nets) and 18.2% top-5 val (1 net, no test number). It leaves out AlexNet's 15.3% because that entry used outside data (Fall 2011 pre-training). VGG reaches 6.8% (2 nets) and 7.0% (1 net)."
results:
  - {benchmark: "ILSVRC classification (ILSVRC-2012 data, used for 2012-2014 challenges)", metric: "top-1 val. error (%) / top-5 val. error (%) / top-5 test error (%)", values: {"VGG (2 nets, multi-crop & dense eval.)": "23.7 / 6.8 / 6.8", "VGG (1 net, multi-crop & dense eval.)": "24.4 / 7.1 / 7.0", "VGG (ILSVRC submission, 7 nets, dense eval.)": "24.7 / 7.5 / 7.3", "GoogLeNet (Szegedy et al., 2014) (1 net)": "- / 7.9 (one cell spanning top-5 val and top-5 test)", "GoogLeNet (Szegedy et al., 2014) (7 nets)": "- / 6.7 (one cell spanning top-5 val and top-5 test)", "MSRA (He et al., 2014) (11 nets)": "- / - / 8.1", "MSRA (He et al., 2014) (1 net)": "27.9 / 9.1 / 9.1", "Clarifai (Russakovsky et al., 2014) (multiple nets)": "- / - / 11.7", "Clarifai (Russakovsky et al., 2014) (1 net)": "- / - / 12.5", "Zeiler & Fergus (Zeiler & Fergus, 2013) (6 nets)": "36.0 / 14.7 / 14.8", "Zeiler & Fergus (Zeiler & Fergus, 2013) (1 net)": "37.5 / 16.0 / 16.1", "OverFeat (Sermanet et al., 2014) (7 nets)": "34.0 / 13.2 / 13.6", "OverFeat (Sermanet et al., 2014) (1 net)": "35.7 / 14.2 / -", "Krizhevsky et al. (Krizhevsky et al., 2012) (5 nets)": "38.1 / 16.4 / 16.4", "Krizhevsky et al. (Krizhevsky et al., 2012) (1 net)": "40.7 / 18.2 / -"}, locator: {table: "Table 7"}, conditions: "only results obtained without outside training data; ensembles vs single nets as labelled; values cross-checked against the arXiv v6 PDF", url: "https://arxiv.org/html/1409.1556"}
  - {benchmark: "ILSVRC-2014 localisation", metric: "top-5 val. error (%) / top-5 test error (%)", values: {"VGG": "26.9 / 25.3", "GoogLeNet (Szegedy et al., 2014)": "- / 26.7", "OverFeat (Sermanet et al., 2014)": "30.0 / 29.9", "Krizhevsky et al. (Krizhevsky et al., 2012)": "- / 34.2"}, locator: {table: "Table 10"}, conditions: "localisation challenge; VGG uses configuration-D localisation ConvNets", url: "https://arxiv.org/html/1409.1556"}
```

```yaml
paper: ioffe2015-batchnorm
title: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"
authors: ["Sergey Ioffe", "Christian Szegedy"]
earliest_public_date: 2015-02-11
latest_arxiv_version: v3
venue: "ICML 2015"
venue_source: "https://proceedings.mlr.press/v37/ioffe15.html"
ids:
  arxiv: "1502.03167"
  doi: ""
  arxiv_doi: "10.48550/arXiv.1502.03167"
  openalex:
    - {id: "W1836465849", kind: preprint, title_as_listed: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"}
    - {id: "W2949117887", kind: preprint, title_as_listed: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"}
  s2: "995c5f5e62614fcb4d2796ad2faab969da51713e"
  s2_corpus_id: 5808102
  dblp: "conf/icml/IoffeS15"
openalex_primary_topic: {id: "T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition [subfields/1707]", field: "Computer Science [fields/17]", domain: "Physical Sciences [domains/3]"}
fulltext_url_used: "https://arxiv.org/html/1502.03167"
raw_file: "src/ioffe2015-batchnorm.html"
metadata_notes:
  - "arXiv history: v1 2015-02-11 01:44:18 UTC, v2 2015-02-13, v3 2015-03-02. The HTML is v3. S2 gives publicationDate 2015-02-10, which is the US-time-zone date of v1."
  - "PMLR page: 'Proceedings of the 32nd International Conference on Machine Learning, PMLR 37:448-456, 2015'. No DOI."
  - "OpenAlex W2949117887 is a second preprint-type record: DataCite DOI 10.57702/o9raffed (TIB Data Manager), date 2024-01-01, author list just 'Sergey Ioffe', landing page export.arxiv.org/pdf/1502.03167. No separate PMLR proceedings work was found. Main work = W1836465849."
  - "S2 externalIds: DBLP conf/icml/IoffeS15, MAG 1836465849, ArXiv 1502.03167, CorpusId 5808102; venue 'International Conference on Machine Learning'."
  - "DBLP: conf/icml/IoffeS15 comes from S2 externalIds; the arXiv abs page links journals/corr/IoffeS15. Neither was checked on dblp.org (bot-check)."
claims:
  - candidate: "Ioffe & Szegedy INTRODUCES Batch Normalization."
    verdict: supported
    evidence:
      - {quote: "Our method draws its strength from making normalization a part of the model architecture and performing the normalization for each training mini-batch.", locator: {section: Abstract}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "We propose a new mechanism, which we call Batch Normalization, that takes a step towards reducing internal covariate shift, and in doing so dramatically accelerates the training of deep neural nets.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://arxiv.org/html/1502.03167"}
    note: "transcription (flagged), Algorithm 1: '\\mu_{\\mathcal{B}} = \\frac{1}{m}\\sum_{i=1}^{m}x_i;\\ \\sigma_{\\mathcal{B}}^2 = \\frac{1}{m}\\sum_{i=1}^{m}(x_i-\\mu_{\\mathcal{B}})^2;\\ \\widehat{x}_i = \\frac{x_i-\\mu_{\\mathcal{B}}}{\\sqrt{\\sigma_{\\mathcal{B}}^2+\\epsilon}};\\ y_i = \\gamma\\widehat{x}_i+\\beta'."
  - candidate: "BN ADDRESSES internal covariate shift (ICS)."
    verdict: supported
    evidence:
      - {quote: "Training Deep Neural Networks is complicated by the fact that the distribution of each layer’s inputs changes during training, as the parameters of the previous layers change.", locator: {section: Abstract}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "We refer to this phenomenon as internal covariate shift, and address the problem by normalizing layer inputs.", locator: {section: Abstract}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "We define Internal Covariate Shift as the change in the distribution of network activations due to the change in network parameters during training.", locator: {section: "2 Towards Reducing Internal Covariate Shift", paragraph: 1}, url: "https://arxiv.org/html/1502.03167"}
    note: "The paper defines ICS and names it as BN's target problem. Whether BN actually reduces ICS, and whether that explains BN's benefit, is disputed by Santurkar et al. 2018 (next block)."
  - candidate: "Ioffe & Szegedy report experimental evidence that BN reduces internal covariate shift."
    verdict: supported
    evidence:
      - {quote: "To verify the effects of internal covariate shift on training, and the ability of Batch Normalization to combat it, we considered the problem of predicting the digit class on the MNIST dataset LeCun et al. (1998a).", locator: {section: "4.1 Activations over time", paragraph: 1}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "Batch Normalization makes the distribution more stable and reduces the internal covariate shift.", locator: {figure: "Figure 1", part: caption}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "we show, for one typical activation from the last hidden layer of each network, how its distribution evolves.", locator: {section: "4.1 Activations over time", paragraph: 2}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "In contrast, the distributions in the batch-normalized network are much more stable as training progresses, which aids the training.", locator: {section: "4.1 Activations over time", paragraph: 2}, url: "https://arxiv.org/html/1502.03167"}
      - {quote: "We also verified that the reduction in internal covariate shift allows deep networks with Batch Normalization to be trained when sigmoid is used as the nonlinearity, despite the well-known difficulty of training such networks.", locator: {section: "4.2.2 Single-Network Classification", paragraph: 9}, url: "https://arxiv.org/html/1502.03167"}
    note: "Supported only as 'the paper claims and shows evidence'. The direct evidence is qualitative and narrow: {15,50,85}th percentiles of the input to ONE 'typical' sigmoid in the last hidden layer of a small MLP (28x28 input, 3 fully-connected hidden layers of 100 sigmoid units) on MNIST (Fig. 1b,c). No quantitative ICS metric is reported. The sigmoid result in 4.2.2 shows trainability, not a measured drop in ICS. Do NOT store 'BN reduces ICS' as a verified fact; Santurkar et al. 2018 contest it."
results:
  - {benchmark: "ImageNet (LSVRC2012) validation, single crop", metric: "Steps to 72.2% / Max accuracy", values: {"Inception": "31.0·10^6 / 72.2%", "BN-Baseline": "13.3·10^6 / 72.7%", "BN-x5": "2.1·10^6 / 73.0%", "BN-x30": "2.7·10^6 / 74.8%", "BN-x5-Sigmoid": "(blank) / 69.8%"}, locator: {table: "Figure 3 (table rendered as a figure)"}, conditions: "step counts are rendered as math; transcribed (flagged) as '31.0\\cdot 10^{6}' etc.; single networks; validation accuracy @1", url: "https://arxiv.org/html/1502.03167"}
  - {benchmark: "ImageNet classification, validation set (50000 images)", metric: "Top-1 error / Top-5 error", values: {"GoogLeNet ensemble (224, 144 crops, 7 models)": "- / 6.67%", "Deep Image low-res (256, -, 1)": "- / 7.96%", "Deep Image high-res (512, -, 1)": "24.88 / 7.42%", "Deep Image ensemble (variable, -, -)": "- / 5.98%", "BN-Inception single crop (224, 1, 1)": "25.2% / 7.82%", "BN-Inception multicrop (224, 144, 1)": "21.99% / 5.82%", "BN-Inception ensemble (224, 144, 6)": "20.1% / 4.9%*"}, locator: {table: "Figure 4 (table rendered as a figure)"}, conditions: "row parentheses = Resolution, Crops, Models; *BN-Inception ensemble reached 4.82% top-5 on the 100000-image test set per the test server (abstract rounds this to '4.8% test error')", url: "https://arxiv.org/html/1502.03167"}
```

```yaml
paper: santurkar2018-bn-optimization
title: "How Does Batch Normalization Help Optimization?"
authors: ["Shibani Santurkar", "Dimitris Tsipras", "Andrew Ilyas", "Aleksander Madry"]
earliest_public_date: 2018-05-29
latest_arxiv_version: v5
venue: "NeurIPS 2018"
venue_source: "https://papers.nips.cc/paper_files/paper/2018/hash/905056c1ac1dad141560467e0a99e1cf-Abstract.html"
ids:
  arxiv: "1805.11604"
  doi: ""
  arxiv_doi: "10.48550/arXiv.1805.11604"
  openalex:
    - {id: "W2898211994", kind: preprint, title_as_listed: "How Does Batch Normalization Help Optimization?"}
  s2: "미확인"
  s2_corpus_id: "미확인"
  dblp: "미확인"
openalex_primary_topic: {id: "T11612", name: "Stochastic Gradient Optimization Techniques", subfield: "Artificial Intelligence [subfields/1702]", field: "Computer Science [fields/17]", domain: "Physical Sciences [domains/3]"}
fulltext_url_used: "https://arxiv.org/html/1805.11604"
raw_file: "src/santurkar2018-bn-optimization.html"
metadata_notes:
  - "arXiv history: v1 2018-05-29, v2 2018-06-05, v3 2018-10-27, v4 2019-03-06, v5 2019-04-15. The HTML is v5. arXiv comment: 'In NeurIPS'18'. The proceedings page reads 'Advances in Neural Information Processing Systems 31 (NeurIPS 2018)'. No DOI."
  - "arXiv lists the last author as 'Aleksander Madry'; OpenAlex and the paper's acknowledgements spell it 'Mądry'."
  - "OpenAlex search with the literal title failed with HTTP 400 because of the '?': {\"error\":\"Invalid query parameters error.\",\"message\":\"Wildcards (* or ?) require exact (no-stem) search. The default search is stemmed, so the literal text before the wildcard is removed when the work is indexed and the search returns wrong results. Use the search.exact= parameter instead (or the default.search.exact filter), e.g. search.exact=How Does Batch Normalization Help Optimization?.\"}. Re-running without '?' and with the title.search filter found only W2898211994 (preprint); OpenAlex has no NeurIPS proceedings work for it."
  - "Semantic Scholar /paper/arXiv:1805.11604 returned HTTP 429 ('Too Many Requests') on the first try and all 3 retries (waits >=5 s), so 미확인. DBLP: 미확인 (dblp.org bot-check)."
claims:
  - candidate: "Santurkar et al. state that BN's success has little to do with reducing internal covariate shift."
    verdict: supported
    evidence:
      - {quote: "In this work, we demonstrate that such distributional stability of layer inputs has little to do with the success of BatchNorm.", locator: {section: Abstract}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "Our point of start is demonstrating that there does not seem to be any link between the performance gain of BatchNorm and the reduction of internal covariate shift.", locator: {section: "1 Introduction (Our Contributions.)", paragraph: 1}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "The “noisy” BatchNorm model nearly matches the performance of standard BatchNorm model, despite complete distributional instability.", locator: {figure: "Figure 2", part: caption}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "Clearly, these findings are hard to reconcile with the claim that the performance gain due to BatchNorm stems from increased stability of layer input distributions.", locator: {section: "2.1 Does BatchNorm’s performance stem from controlling internal covariate shift?", paragraph: 5}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "We find that the widely believed connection between the performance of BatchNorm and the internal covariate shift is tenuous, at best.", locator: {section: "6 Conclusions", paragraph: 1}, url: "https://arxiv.org/html/1805.11604"}
    note: "The abstract says 'such distributional stability of layer inputs', i.e. ICS in the distributional sense of Ioffe & Szegedy. The Contributions paragraph hedges right after: 'Or that this link is tenuous, at best.' Evidence: VGG on CIFAR-10 with noise of non-zero mean and non-unit variance injected after each BN layer, changing every step (Sec. 2.1). Edge suggestion: santurkar2018 CONTRADICTS (or CHALLENGES) the ioffe2015 claim that BN works by reducing ICS."
  - candidate: "Santurkar et al. offer an alternative explanation: BN makes the optimization landscape smoother."
    verdict: supported
    evidence:
      - {quote: "Instead, we uncover a more fundamental impact of BatchNorm on the training process: it makes the optimization landscape significantly smoother.", locator: {section: Abstract}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "This smoothness induces a more predictive and stable behavior of the gradients, allowing for faster training.", locator: {section: Abstract}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "Indeed, we identify the key impact that BatchNorm has on the training process: it reparametrizes the underlying optimization problem to make its landscape significantly more smooth.", locator: {section: "3.1 The smoothing effect of BatchNorm", paragraph: 1}, url: "https://arxiv.org/html/1805.11604"}
    note: "'Smoother' is made precise as better Lipschitzness of the loss and better 'effective' beta-smoothness, i.e. Lipschitz gradients (Sec. 3.1, Fig. 4; proofs in Sec. 4). The paper also finds the effect is not specific to BN: l_p normalizations give similar smoothing and similar performance (Sec. 3.3)."
  - candidate: "Santurkar et al. report that BN may not even reduce internal covariate shift."
    verdict: supported
    evidence:
      - {quote: "In fact, we find that in a certain sense BatchNorm might not even be reducing internal covariate shift.", locator: {section: "1 Introduction (Our Contributions.)", paragraph: 1}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "Surprisingly, we observe that networks with BatchNorm often exhibit an increase in ICS (cf. Figure 3).", locator: {section: "2.2 Is BatchNorm reducing internal covariate shift?", paragraph: 6}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "This evidence suggests that, from optimization point of view BatchNorm might not even reduce the internal covariate shift.", locator: {section: "2.2 Is BatchNorm reducing internal covariate shift?", paragraph: 6}, url: "https://arxiv.org/html/1805.11604"}
      - {quote: "Models with BatchNorm have similar, or even worse, internal covariate shift, despite performing better in terms of accuracy and loss.", locator: {figure: "Figure 3", part: caption}, url: "https://arxiv.org/html/1805.11604"}
    note: "This finding is hedged ('in a certain sense', 'might not', 'often'). It uses the authors' own gradient-based ICS definition (Definition 2.1: the l2 difference / cosine between a layer's gradients before and after the preceding layers are updated), measured on VGG and a 25-layer deep linear network, not the distributional definition. Sec. 2.2 calls the stabilization of the BN VGG net later in training an artifact of faster convergence."
results: []
```

```yaml
paper: he2015-resnet
title: "Deep Residual Learning for Image Recognition"
authors: ["Kaiming He", "Xiangyu Zhang", "Shaoqing Ren", "Jian Sun"]
earliest_public_date: 2015-12-10
latest_arxiv_version: v1
venue: "CVPR 2016"
venue_source: "https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html"
ids:
  arxiv: "1512.03385"
  doi: "10.1109/CVPR.2016.90"
  arxiv_doi: "10.48550/arXiv.1512.03385"
  openalex:
    - {id: "W2194775991", kind: proceedings, title_as_listed: "Deep Residual Learning for Image Recognition"}
    - {id: "W2949650786", kind: preprint, title_as_listed: "Deep Residual Learning for Image Recognition"}
  s2: "2c03df8b48bf3fa39054345bafabfeff15bfd11d"
  s2_corpus_id: 206594692
  dblp: "conf/cvpr/HeZRS16"
openalex_primary_topic: {id: "T10036", name: "Advanced Neural Network Applications", subfield: "Computer Vision and Pattern Recognition [subfields/1707]", field: "Computer Science [fields/17]", domain: "Physical Sciences [domains/3]"}
fulltext_url_used: "https://arxiv.org/html/1512.03385"
raw_file: "src/he2015-resnet.html"
metadata_notes:
  - "arXiv has only v1 (2015-12-10), with the comment 'Tech report'. CVPR 2016, pp. 770-778, per the CVF open-access page and Crossref (event start 2016-06-27)."
  - "S2 externalIds: DBLP conf/cvpr/HeZRS16, DOI 10.1109/cvpr.2016.90, ArXiv 1512.03385, MAG 2949650786. S2 year 2015 / publicationDate 2015-12-10 reflect the arXiv date. The arXiv abs page links DBLP journals/corr/HeZRS15."
  - "OpenAlex main work = W2194775991 (CVPR proceedings, DOI). W2949650786 is the arXiv preprint (also has Zenodo locations)."
  - "HTML conversion artifact: LaTeXML gave the single-model table (captioned 'Table 4') the id S4.T5, so the HTML text says 'In Table 5 we compare with the previous best single-model results' where the arXiv v1 PDF (src/he2015-resnet.arxiv-v1.pdf) says 'In Table 4'. Some later table cross-refs in the HTML are also shifted (e.g. the VOC table is captioned 'Table 7' but referenced as 8). Captions are correct; quotes below avoid the shifted references, and table values were cross-checked against the PDF."
claims:
  - candidate: "He et al. INTRODUCES the residual learning framework / ResNet."
    verdict: supported
    evidence:
      - {quote: "We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.", locator: {section: Abstract}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions.", locator: {section: Abstract}, url: "https://arxiv.org/html/1512.03385"}
    note: "transcription (flagged), Sec. 1/3.1: the stacked layers fit '\\mathcal{F}(\\mathbf{x}) := \\mathcal{H}(\\mathbf{x}) - \\mathbf{x}' and the original mapping becomes '\\mathcal{F}(\\mathbf{x}) + \\mathbf{x}'."
  - candidate: "He et al. INTRODUCES identity shortcut connections (Sec. 3.2)."
    verdict: partially_supported
    evidence:
      - {quote: "In our case, the shortcut connections simply perform identity mapping, and their outputs are added to the outputs of the stacked layers (Fig. 2).", locator: {section: "1 Introduction", paragraph: 6}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "The shortcut connections in Eqn.(1) introduce neither extra parameter nor computation complexity.", locator: {section: "3.2 Identity Mapping by Shortcuts", paragraph: 2}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "But we will show by experiments that the identity mapping is sufficient for addressing the degradation problem and is economical, and thus", locator: {section: "3.2 Identity Mapping by Shortcuts", paragraph: 3}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Practices and theories that lead to shortcut connections [2, 34, 49] have been studied for a long time.", locator: {section: "2 Related Work", paragraph: 3}, url: "https://arxiv.org/html/1512.03385"}
    note: "transcription (flagged), Eqn. (1): '\\mathbf{y}=\\mathcal{F}(\\mathbf{x},\\{W_{i}\\})+\\mathbf{x}'; Eqn. (2), used only to match dimensions: '\\mathbf{y}=\\mathcal{F}(\\mathbf{x},\\{W_{i}\\})+W_{s}\\mathbf{x}'. The paper itself calls shortcut connections long-studied prior art [2, 34, 49] and credits highway networks with concurrent gated shortcuts. What is new is the parameter-free identity shortcut added to a residual branch (the residual block). Suggested wording: 'INTRODUCES the residual block with parameter-free identity shortcuts' or 'USES identity shortcut connections', not 'INTRODUCES shortcut connections'."
  - candidate: "ResNet ADDRESSES the degradation problem."
    verdict: supported
    evidence:
      - {quote: "When deeper networks are able to start converging, a degradation problem has been exposed: with the network depth increasing, accuracy gets saturated (which might be unsurprising) and then degrades rapidly.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher training error, as reported in [11, 42] and thoroughly verified by our experiments.", locator: {section: "1 Introduction", paragraph: 3}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "In this paper, we address the degradation problem by introducing a deep residual learning framework.", locator: {section: "1 Introduction", paragraph: 5}, url: "https://arxiv.org/html/1512.03385"}
    note: "The paper does not claim to have discovered degradation; it was 'reported in [11, 42]' (He & Sun, CVPR 2015; Srivastava et al., Highway networks). Degradation here means higher training error, which is why overfitting is ruled out."
  - candidate: "Residual learning MITIGATES degradation (ImageNet, Table 2 + Sec. 4.1)."
    verdict: supported
    evidence:
      - {quote: "We have observed the degradation problem - the 34-layer plain net has higher training error throughout the whole training procedure, even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one.", locator: {section: "4.1 ImageNet Classification", paragraph: 3}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "First, the situation is reversed with residual learning – the 34-layer ResNet is better than the 18-layer ResNet (by 2.8%).", locator: {section: "4.1 ImageNet Classification", paragraph: 6}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "This indicates that the degradation problem is well addressed in this setting and we manage to obtain accuracy gains from increased depth.", locator: {section: "4.1 ImageNet Classification", paragraph: 6}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Second, compared to its plain counterpart, the 34-layer ResNet reduces the top-1 error by 3.5% (Table 2), resulting from the successfully reduced training error (Fig. 4 right vs. left).", locator: {section: "4.1 ImageNet Classification", paragraph: 7}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Here the ResNets have no extra parameter compared to their plain counterparts.", locator: {table: "Table 2", part: caption}, url: "https://arxiv.org/html/1512.03385"}
    note: "Table 2 (top-1 error, %, 10-crop testing, ImageNet val): plain-18 27.94, plain-34 28.54, ResNet-18 27.88, ResNet-34 25.03. Deeper plain gets worse (+0.60); deeper ResNet gets better (-2.85, printed as 2.8%); ResNet-34 vs plain-34 = -3.51 (printed 3.5%). These ResNets use option A (identity + zero-padding shortcuts). Sec. 4.1 p8: 18-layer plain and residual nets are about equally accurate, but the ResNet converges faster."
  - candidate: "CIFAR-10 (Figure 1): the 56-layer plain net has higher training and test error than the 20-layer plain net."
    verdict: supported
    evidence:
      - {quote: "Training error (left) and test error (right) on CIFAR-10 with 20-layer and 56-layer “plain” networks.", locator: {figure: "Figure 1", part: caption}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "The deeper network has higher training error, and thus test error.", locator: {figure: "Figure 1", part: caption}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "The deep plain nets suffer from increased depth, and exhibit higher training error when going deeper.", locator: {section: "4.2 CIFAR-10 and Analysis", paragraph: 4}, url: "https://arxiv.org/html/1512.03385"}
    note: "Figure 1 is a plot; no numbers are printed for it. The next caption sentence says 'Similar phenomena on ImageNet is presented in Fig. 4.'"
  - candidate: "Vanishing/exploding gradients have been largely addressed by normalized initialization and intermediate normalization layers (ref [16] = Batch Normalization)."
    verdict: supported
    evidence:
      - {quote: "An obstacle to answering this question was the notorious problem of vanishing/exploding gradients [1, 9], which hamper convergence from the beginning.", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "This problem, however, has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers [16], which enable networks with tens of layers to start converging for stochastic gradient descent (SGD) with backpropagation [22].", locator: {section: "1 Introduction", paragraph: 2}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Batch normalization: Accelerating deep network training by reducing internal covariate shift.", locator: {section: "References [16]"}, url: "https://arxiv.org/html/1512.03385"}
    note: "[16] = S. Ioffe and C. Szegedy, 'Batch normalization: Accelerating deep network training by reducing internal covariate shift', ICML 2015 (the third quote is from the reference list, not body text). [23] LeCun et al. 1998 Efficient backprop; [9] Glorot & Bengio 2010; [37] Saxe et al. 2013; [13] He et al. 2015 (PReLU/'Delving deep'). This is the authors' assessment, not an experiment, though Sec. 4.1 p4 checks it for their plain nets: 'So neither forward nor backward signals vanish.'"
  - candidate: "ResNet USES Batch Normalization (Sec. 3.4)."
    verdict: supported
    evidence:
      - {quote: "We adopt batch normalization (BN) [16] right after each convolution and before activation, following [16].", locator: {section: "3.4 Implementation", paragraph: 1}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances.", locator: {section: "4.1 ImageNet Classification", paragraph: 4}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "So neither forward nor backward signals vanish.", locator: {section: "4.1 ImageNet Classification", paragraph: 4}, url: "https://arxiv.org/html/1512.03385"}
    note: "BN is used in both the plain and the residual nets, on ImageNet and CIFAR-10 (Sec. 4.2). Sec. 3.4 also says the nets use no dropout, 'following the practice in [16]'."
  - candidate: "ResNet's plain baselines are INSPIRED_BY VGG (Sec. 3.3)."
    verdict: supported
    evidence:
      - {quote: "Our plain baselines (Fig. 3, middle) are mainly inspired by the philosophy of VGG nets [41] (Fig. 3, left).", locator: {section: "3.3 Network Architectures", paragraph: 2}, url: "https://arxiv.org/html/1512.03385"}
    note: "[41] = Simonyan & Zisserman, ICLR 2015. The residual net is the plain net plus shortcuts (Sec. 3.3, 'Residual Network'). So the chain is ResNet built on a VGG-inspired plain net, not ResNet built directly on VGG."
  - candidate: "Highway networks are described as concurrent work with gated shortcuts (Sec. 2)."
    verdict: supported
    evidence:
      - {quote: "Concurrent with our work, “highway networks” [42, 43] present shortcut connections with gating functions [15].", locator: {section: "2 Related Work", paragraph: 4}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "These gates are data-dependent and have parameters, in contrast to our identity shortcuts that are parameter-free.", locator: {section: "2 Related Work", paragraph: 4}, url: "https://arxiv.org/html/1512.03385"}
    note: "[42] Srivastava, Greff, Schmidhuber, 'Highway networks', arXiv:1505.00387; [43] 'Training very deep networks', arXiv:1507.06228; [15] Hochreiter & Schmidhuber 1997 (LSTM), cited for gating functions."
  - candidate: "ResNet IMPROVES_ON VGG: Table 4 single-model ImageNet-val errors for VGG-16 vs ResNet-152; the ensemble reaches 3.57% top-5 test error and won 1st place in ILSVRC 2015."
    verdict: partially_supported
    evidence:
      - {quote: "An ensemble of these residual nets achieves 3.57% error on the ImageNet test set.", locator: {section: Abstract}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "This result won the 1st place on the ILSVRC 2015 classification task.", locator: {section: Abstract}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Our 152-layer residual net is the deepest network ever presented on ImageNet, while still having lower complexity than VGG nets [41].", locator: {section: "1 Introduction", paragraph: 9}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "Our 152-layer ResNet has a single-model top-5 validation error of 4.49%.", locator: {section: "4.1 ImageNet Classification", paragraph: 16}, url: "https://arxiv.org/html/1512.03385"}
      - {quote: "VGG-16 is based on our test.", locator: {table: "Table 3", part: caption}, url: "https://arxiv.org/html/1512.03385"}
    note: "IMPROVES_ON VGG holds, but the locator in the candidate is wrong. Table 4 has NO 'VGG-16' row. VGG-16 [41] is in Table 3 (10-crop, ImageNet val, 'based on our test'): 28.07 top-1 / 9.33 top-5, against ResNet-152 at 21.43 / 5.71. Table 4 (single model, val unless †) has 'VGG [41] (ILSVRC’14)' at - / 8.43† (test) and 'VGG [41] (v5)' at 24.4 / 7.1, against ResNet-152 at 19.38 / 4.49. Table 5 (ensembles, test top-5): VGG (ILSVRC’14) 7.32 and VGG (v5) 6.8 against ResNet (ILSVRC’15) 3.57. The 3.57% ensemble combines six models of different depth. transcription (flagged), abstract: 'depth of up to 152 layers—8$\\times$ deeper than VGG nets [41] but still having lower complexity'; FLOPs 11.3 billion (ResNet-152) vs 15.3/19.6 billion (VGG-16/19), Sec. 4.1."
results:
  - {benchmark: "ImageNet 2012 classification, validation", metric: "top-1 error (%)", values: {"plain 18 layers": "27.94", "ResNet 18 layers": "27.88", "plain 34 layers": "28.54", "ResNet 34 layers": "25.03"}, locator: {table: "Table 2"}, conditions: "10-crop testing; single models; ResNets use option A (identity shortcuts, zero-padding), with no extra parameters vs plain", url: "https://arxiv.org/html/1512.03385"}
  - {benchmark: "ImageNet 2012 classification, validation", metric: "top-1 err. / top-5 err. (%)", values: {"VGG-16 [41]": "28.07 / 9.33", "GoogLeNet [44]": "- / 9.15", "PReLU-net [13]": "24.27 / 7.38", "plain-34": "28.54 / 10.02", "ResNet-34 A": "25.03 / 7.76", "ResNet-34 B": "24.52 / 7.46", "ResNet-34 C": "24.19 / 7.40", "ResNet-50": "22.85 / 6.71", "ResNet-101": "21.75 / 6.05", "ResNet-152": "21.43 / 5.71"}, locator: {table: "Table 3"}, conditions: "10-crop testing; single models; VGG-16 is based on the authors' own test; ResNet-50/101/152 use option B (projection shortcuts only when dimensions increase)", url: "https://arxiv.org/html/1512.03385"}
  - {benchmark: "ImageNet 2012 classification", metric: "top-1 err. / top-5 err. (%)", values: {"VGG [41] (ILSVRC’14)": "- / 8.43†", "GoogLeNet [44] (ILSVRC’14)": "- / 7.89", "VGG [41] (v5)": "24.4 / 7.1", "PReLU-net [13]": "21.59 / 5.71", "BN-inception [16]": "21.99 / 5.81", "ResNet-34 B": "21.84 / 5.71", "ResNet-34 C": "21.53 / 5.60", "ResNet-50": "20.74 / 5.25", "ResNet-101": "19.87 / 4.60", "ResNet-152": "19.38 / 4.49"}, locator: {table: "Table 4"}, conditions: "single-model results on the validation set, except † (test set); ResNets use fully-convolutional multi-scale testing (Sec. 3.4)", url: "https://arxiv.org/html/1512.03385"}
  - {benchmark: "ImageNet 2012 classification, test (server)", metric: "top-5 err. (test, %)", values: {"VGG [41] (ILSVRC’14)": "7.32", "GoogLeNet [44] (ILSVRC’14)": "6.66", "VGG [41] (v5)": "6.8", "PReLU-net [13]": "4.94", "BN-inception [16]": "4.82", "ResNet (ILSVRC’15)": "3.57"}, locator: {table: "Table 5"}, conditions: "ensembles; test set, reported by the test server; ResNet entry = six models of different depth (only two 152-layer models at submission time)", url: "https://arxiv.org/html/1512.03385"}
```
