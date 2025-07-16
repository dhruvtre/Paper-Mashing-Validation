Research question 1 - Can an automated system come up with “good” research ideas in AI/ML, where good is defined as ideas that human scientists would consider worthwhile to explore.

Hypothesis 1 - Mashing ideas from a foundational paper in a domain with papers accepted in a top conferences generates good ideas
Testing hypothesis 1 - mashing up ideas
take papers that are cited by the papers that we are mashing but are published on arxiv beyond the model cut off date
Setup two prompts for idea generation::
Control: generate a new research idea in AI/ML
Idea bashing: given these two papers, come up with ideas
Measure:
Perplexity on these two prompts for actual papers that are cited
Similarity of generated ideas to actual papers that are cited
Cosine or LLM as judge
Alternative approach
let’s mash ideas and see if they already exist (how will we find them from the whole universe)
Llm as judge on semantically related papers on arxiv repo
