![Chonkie Logo](assets/chonkie_logo_br_transparent_bg.png)
# 🦛 Chonkie

so i found myself making another RAG bot (for the 2342148th time) and meanwhile, explaining to my juniors about why we should use chunking in our RAG bots, only to realise that i would have to write chunking all over again unless i use the bloated software library X or the extremely feature-less library Y. _WHY CAN I NOT HAVE GOOD THINGS IN LIFE, UGH?_

Can't i just install, import and run chunking and not have to worry about dependencies, bloat, speed or other factors?

Well, with chonkie you can! (chonkie boi is a gud boi)

✅ All the CHONKs you'd ever need </br>
✅ Easy to use: Install, Import, CHONK </br>
✅ No bloat, just CHONK </br>
✅ Cute CHONK mascoot </br>
✅ Moto Moto's favorite python library </br>

What're you waiting for, **just CHONK it**!

# Table of Contents
- [🦛 Chonkie](#-chonkie)
- [Table of Contents](#table-of-contents)
- [Why do we need Chunking?](#why-do-we-need-chunking)
- [Approaches to doing chunking](#approaches-to-doing-chunking)
- [Installation](#installation)
- [Usage](#usage)
- [Citation](#citation)

# Why do we need Chunking?

Here are some arguments for why one would like to chunk their texts for a RAG scenario:

- Most RAG pipelines are bottlenecked by context length as of today. While we expect future LLMs to exceed 1Mill token lenghts, even then, it's not only LLMs inside the pipeline, but other aspects too, namely, bi-encoder retriever, cross-encoder reranker and even models for particular aspects like answer relevancy models and answer attribution models, that could lead to the context length bottleneck.
- Even with infinite context, there's no free lunch on the context side - the minimum it takes to understand a string is o(n) and we would never be able to make models more efficient on scaling context. So, if we have smaller context, our search and generation pipeline would be more efficient (in response latency)
- Research suggests that a lot of random, noisy context can actually lead to higher hallucination in the model responses. However, if we ensure that each chunk that get's passed onto the model is only relevant, the model would end up with better responses.

# Approaches to doing chunking

1. Token Chunking (a.k.a Fixed Size Chunking or Sliding Window Chunking)
2. Word Chunking
3. Sentence Chunking
4. Semantic Chunking
5. Semantic Double-Pass Merge (SDPM) Chunking
6. Context-aware Chunking

# Installation

To install chonkie, simply run:

```bash
pip install chonkie
```

# Usage

Here's a basic example to get you started:

```python
from chonkie import TokenChunker

# Initialize the chunker
chunker = TokenChunker()

# Chunk some text
chunks = chunker.chunk("Your text here")
print(chunks)
```

# Citation

If you use Chonkie in your research, please cite it as follows:

```
@misc{chonkie2024,
  author = {Minhas, Bhavnick},
  title = {Chonkie: A Lightweight Chunking Library for RAG Bots},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bhavnick/chonkie}},
}
```