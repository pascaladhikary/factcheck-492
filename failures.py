# import spacy
# import pytextrank

# # example text
# text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

# # load a spaCy model, depending on language, scale, etc.
# nlp = spacy.load("en_core_web_sm")

# # add PyTextRank to the spaCy pipeline
# nlp.add_pipe("textrank")
# doc = nlp(text)

# # examine the top-ranked phrases in the document
# for phrase in doc._.phrases:
#     print(phrase.text)
#     print(phrase.rank, phrase.count)
#     print(phrase.chunks)

# from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
# from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
# from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

# document = "Natural language generation (NLG) is the natural language processing task of generating natural language from a machine representation system such as a knowledge base or a logical form. Psycholinguists prefer the term language production when such formal representations are interpreted as models for mental representations."

# # Object of automatic summarization.
# auto_abstractor = AutoAbstractor()
# # Set tokenizer.
# auto_abstractor.tokenizable_doc = SimpleTokenizer()
# # Set delimiter for making a list of sentence.
# auto_abstractor.delimiter_list = [".", "\n"]
# # Object of abstracting and filtering document.
# abstractable_doc = TopNRankAbstractor()
# # Summarize document.
# result_dict = auto_abstractor.summarize(document, abstractable_doc)

# # Output result.
# for sentence in result_dict["summarize_result"]:
#     print(sentence)

# import gensim
# from gensim.summarization import keywords

# # input text
# text = "Python is a popular programming language. It is easy to learn and has many useful libraries."

# # extract keywords
# result = keywords(text)

# # print keywords
