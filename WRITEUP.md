# WRITEUP.md

# Smart Job Match Agent – Technical Write-up

## 1. Design Choices

For the job matching part, I first tried using modern embedding models like Sentence Transformers and Gemini/OpenAI embeddings because they understand semantic meaning better than simple keyword matching.

Initially, I used the `all-MiniLM-L6-v2` sentence-transformer model with cosine similarity. The matching quality was good, but while deploying the project on Vercel, I faced problems because these models required large libraries like PyTorch and Transformers. This made the deployment size too large for Vercel free tier.

I also tried Gemini and OpenAI APIs, but I faced free-tier quota limits and API call restrictions during testing. Because of this, I decided to switch to a lightweight TF-IDF based approach using Scikit-Learn.

In the final version:

* TF-IDF is used to convert resumes and job descriptions into vectors
* Cosine similarity is used to compare them
* The top matching jobs are returned based on similarity score

Even though TF-IDF is simpler than transformer embeddings, it is lightweight, fast, fully free, and easy to deploy.

Technologies used:

* FastAPI for backend
* Scikit-Learn for TF-IDF and cosine similarity
* HTML/CSS/JavaScript for frontend
* Vercel for deployment

I chose this final setup mainly to make the project stable, deployable, and fully working within the assignment time.

---

## 2. Agentic Architecture

My original plan was to build a proper LLM-based agent using Gemini/OpenAI APIs with tool calling.

The flow was supposed to be:

1. Resume Parser Tool → extract structured information from resume text
2. Match Reasoning Tool → explain why jobs match the candidate

I did create initial versions using Gemini and Hugging Face APIs, but I faced:

* API quota limits
* free-tier restrictions
* deployment failures
* large dependency issues

Because of these issues, I simplified the final deployed version into a local rule-based system.

The current architecture is still modular:

* `embeddings.py` handles vector generation
* `matcher.py` handles ranking logic
* `llm_agent.py` handles parsing and explanations
* `index.py` handles API routes

I kept the system modular because it makes debugging and future improvements easier.

One limitation is that the final deployed version does not use real native LLM tool-calling anymore. Instead, it uses local structured logic. If I had more time or better API access, I would restore actual LLM tool-calling using Gemini or OpenAI.

Possible failure cases:

* Short resumes may give weak matches
* Missing skills affect ranking
* TF-IDF cannot understand deep semantic meaning like transformer models

---

## 3. Honest Weaknesses

The biggest weakness is that TF-IDF is not as powerful as transformer embeddings. It works mainly based on important words and skill overlap, so resumes written in unusual wording may not perform well.

Another weakness is that the current reasoning system is mostly rule-based instead of fully LLM-driven. Because of API limits and deployment issues, I could not keep the full LLM pipeline in the final deployed version.

At large scale, the current system would also face issues because:

* embeddings are generated dynamically
* there is no caching
* there is no vector database
* there is no async processing

For handling very large traffic, I would need:

* precomputed embeddings
* vector databases like FAISS/Pinecone
* caching
* async workers

Due to the assignment time limit, I focused more on making the full project work end-to-end and deploy successfully.

---

## 4. Next Steps

If I had two more days, the biggest improvement would be restoring proper LLM-based tool calling using Gemini/OpenAI APIs along with sentence-transformer embeddings.

This would improve:

* semantic understanding
* reasoning quality
* clarifying questions
* recommendation accuracy

I would also add:

* better resume parsing
* vector database support
* caching
* stronger `/refine` endpoint logic
* evaluation metrics for recommendation quality

Overall, this project taught me a lot about deployment challenges, debugging real production issues, API limitations, and making practical engineering tradeoffs under time constraints.
