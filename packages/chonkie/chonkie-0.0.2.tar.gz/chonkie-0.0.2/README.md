![Chonkie Logo](https://github.com/bhavnicksm/chonkie/blob/6b1b1953494d47dda9a19688c842975184ccc986/assets/chonkie_logo_br_transparent_bg.png)
# 🦛 Chonkie

so i found myself making another RAG bot (for the 2342148th time) and meanwhile, explaining to my juniors about why we should use chunking in our RAG bots, only to realise that i would have to write chunking all over again unless i use the bloated software library X or the extremely feature-less library Y. _WHY CAN I NOT HAVE GOOD THINGS IN LIFE, UGH?_

Can't i just install, import and run chunking and not have to worry about dependencies, bloat, speed or other factors?

Well, with chonkie you can! (chonkie boi is a gud boi)

✅ Feature-rich: All the CHONKs you'd ever need </br>
✅ Easy to use: Install, Import, CHONK </br>
✅ Fast: CHONK at the speed of light! zooooom </br>
✅ Wide support: Supports all your favorite tokenizer CHONKS </br>
✅ Light-weight: No bloat, just CHONK </br>
✅ Cute CHONK mascoot </br>
✅ Moto Moto's favorite python library </br>

What're you waiting for, **just CHONK it**!

# Installation
To install chonkie, simply run:

```bash
pip install chonkie
```

Chonkie follows the rule to have minimal defualt installs, read the [DOCS](/DOCS.md) to know the installation for your required chunker, or simply install `all` if you don't want to think about it (not recommended).

```bash
pip install chonkie[all]
```

# Usage

Here's a basic example to get you started:

```python
# First import the chunker you want from Chonkie 
from chonkie import TokenChunker

# Import your favorite tokenizer library
# Also supports AutoTokenizers, TikToken and AutoTikTokenizer
from tokenizers import Tokenizer 
tokenizer = Tokenizer.from_pretrained("gpt2)

# Initialize the chunker
chunker = TokenChunker(tokenizer)

# Chunk some text
chunks = chunker("Woah! I believe Chonkie, the chunking library is so cool! I love the tiny hippo hehe.")
print(chunks)
```

More example usages given inside the [DOCS](/DOCS.md)

# Supported Methods

Chonkie provides several chunkers to help you split your text efficiently for RAG applications. Here's a quick overview of the available chunkers:

- **TokenChunker**: Splits text into fixed-size token chunks.
- **WordChunker**: Splits text into chunks based on words.
- **SentenceChunker**: Splits text into chunks based on sentences.
- **SemanticChunker**: Splits text into chunks based on semantic similarity.
- **SPDMChunker**: Splits text using a Semantic Double-Pass Merge approach.

More on these methods and the approaches taken inside the [DOCS](/DOCS.md)

# Acknowledgements

Chonkie was developed with the support and contributions of the open-source community. We would like to thank the following projects and individuals for their invaluable help:

- **Hugging Face** for their amazing [tokenizers](https://github.com/huggingface/tokenizers) library, which provides the backbone for our tokenization needs.
- **spaCy** for their powerful [spaCy](https://spacy.io/) library, which we use for advanced sentence segmentation.
- **Sentence Transformers** for their [sentence-transformers](https://www.sbert.net/) library, which enables semantic chunking.
- The contributors and maintainers of various open-source projects that have inspired and supported the development of Chonkie.

Special thanks to **Moto Moto** for endorsing Chonkie with his famous quote: 
> "I like them big, I like them chonkie."

And to all the users and contributors who have provided feedback, reported issues, and helped improve Chonkie.

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
