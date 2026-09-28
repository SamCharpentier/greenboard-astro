---
title: "Decoding the AI Revolution in Financial Compliance: A Deep Dive into LLMs"
summary: "In 1993 Jensen Huang co-founded Nvidia with Chris Malachowsky and Curtis Priem to build computer chips for video games. By 1999 they were listed on the Nasdaq exchange with an initial share price of $12 [1] and saw modest growth through the 2000s and into the mid 2010s. Now, they’re a household name and one of the most valuable companies in the world with a market cap of $2.87T USD having experienced growth of more than 2,500% [2] over the last five years. So, what changed?"
date: "2024-10-10"
author: "dave-feldman"
featured: false
whitepaperForm: false
coverUrl: "https://cdn.prod.website-files.com/67d0a8a9156b7b7bd46ffe28/67f018db75116b9233ec010c_cH962WKx5qY2R1x9PRQXtDLRxlc.avif"
status: "draft"
seo:
  description: "In 1993 Jensen Huang co-founded Nvidia with Chris Malachowsky and Curtis Priem to build computer chips for video games. By 1999 they were listed on the Nasdaq exchange with an initial share price of $12 [1] and saw modest growth through the 2000s and into the mid 2010s. Now, they’re a household name and one of the most valuable companies in the world with a market cap of $2.87T USD having experienced growth of more than 2,500% [2] over the last five years. So, what changed?"
---

## It Started with Video Games

In 1993 Jensen Huang co-founded Nvidia with Chris Malachowsky and Curtis Priem to build computer chips for video games. By 1999 they were listed on the Nasdaq exchange with an initial share price of $12 [[1](https://investor.nvidia.com/investor-resources/faqs/default.aspx)] and saw modest growth through the 2000s and into the mid 2010s. Now, they’re a household name and one of the most valuable companies in the world with a market cap of $2.87T USD having experienced growth of more than 2,500% [[2](https://finance.yahoo.com/quote/NVDA/)] over the last five years. So, what changed?

Nvidia’s recent success is largely driven by a foundational technology shift: parallelized computing. Up until the early 2000s computers processed information via computer chips called Central Processing Units (CPUs) which consisted of one, and subsequently a small number of,  cores - the micro-machinery used by a computer to make calculations. In an attempt to improve computer graphics Nvidia developed Graphic Processor Units (GPUs). GPUs are processors that break compute problems into smaller, simpler problems and evaluate them in parallel across thousands of cores (i.e., parallelized computing) [[3](https://www.ibm.com/think/topics/parallel-computing)].

![](https://cdn.prod.website-files.com/67d0a8a9156b7b7bd46ffe28/67f018b422d251993f89509f_FBHktQV16zItAifjY2etTUKZqE.png)

It turns out this computer chip architecture had benefits outside of graphics. They can process -  and draw conclusions from - exponentially larger datasets than earlier architectures. And thus, their newfound applications to machine learning, blockchain computing, and artificial intelligence caused demand to skyrocket.

## How Artificial Intelligence Actually Works

The artificial intelligence we have today (think ChatGPT, Anthropic, Perplexity, etc.) was born from statistical research going back to the type of regression you originally might have used Excel to run; e.g., quantifying the relationship between rainfall and corn prices. Statisticians noticed relationships between variables were nonlinear and complex - too much rain, after all, can ruin a corn crop and drive prices up, and there are countless additional variables that can drive fluctuations. For a while, the best way to model these relationships was with complex equations composed of many variables.

[[4](https://mobidev.biz/blog/essential-machine-learning-algorithms-for-business-applications)]

![](https://cdn.prod.website-files.com/67d0a8a9156b7b7bd46ffe28/67f018b4dd816d871cf626c8_wGC2dxqdUeKGGaFAp9sdxSjm1M.webp)

Historically, the blocker to more complex models was the computing power required to produce them. With the introduction of GPUs and parallel computing, models which were more complex, and accurate, became possible (i.e., neural networks).

Neural networks are composed of exponentially more parameters than a statistician could ever keep track of; GPT4, for instance, has **~1.8 trillion** parameters [[5](https://the-decoder.com/gpt-4-architecture-datasets-costs-and-more-leaked/)]. By executing an immense number of parallel computations, training data is used to adjust these parameters until the neural network has developed a representation of the data in aggregate. This representation can be tremendously nuanced.

[[6](https://spectrum.ieee.org/what-is-deep-learning)]

![](https://cdn.prod.website-files.com/67d0a8a9156b7b7bd46ffe28/67f018b4a300755204560f5f_zzFzPDBHBjT2c3mUS5aID6yG6vU.png)

Inference is the process by which the AI model we interact with takes a new piece of data (e.g., a prompt given) and probabilistically assesses how it aligns with the broader dataset it was trained on. ChatGPT, for example, works by predicting the highest probability next word that will occur given each word that occurred before it. Our CEO Dave aptly put it this way: “in the same way that Excel was developed to be really good at crunching numbers, this generation of artificial intelligence is really good at crunching words” in [a recent episode of The Trust Podcast](https://greenboard.com/resources/kitces).

**What Does this Mean for Compliance?**‍

It wasn’t always the case that financial firms could count on cheap hard drives and cloud storage to keep records. Back when filing cabinets (and file rooms) were the norm, businesses needed to dedicate substantial resources to keeping their files organized and accessible. But it turns out computers are cheaper and better than humans at storing files by a wide margin. And so, there are no longer roles for file clerks in the economy and computers became the tools that these employees used to become more efficient and productive.

So, this brings us to the question of what does any of this have to do with compliance? A huge part of compliance professionals’ mandate is to identify and mitigate risk. The rise of parallel computing allows us to calculate compliance risk probabilities across the vast digital data that is generated by regulated financial firms, as well as by their regulatory counterparts, every day.

**The effect**: mostly accurate but clearly actionable recommendations on areas to examine for compliance risk.

AI systems can now instantly process the latest regulatory updates and cross-reference them against a firm's internal policies, flagging any areas that need attention. They can evaluate vendor information and generate risk assessments that highlight potential data exposures. And when it comes to marketing materials, these systems can review them to ensure all necessary disclosures are present and content aligns with complex regulatory requirements.

By automating the most time-consuming and detail-oriented aspects of compliance work (i.e., ‘clerical work’), AI is freeing professionals to focus on higher-level strategy, decision-making, and client service. It's a shift that has the potential to make compliance more efficient, more accurate, and more responsive in a business environment where the regulatory landscape is constantly shifting.

Another stellar use for this technology is screening archived communications for potentially problematic interactions often missed by common methods such as random sampling or lexicon matching…**more on this next week**.

To contact the author or learn more about Greenboard please contact [cameron@greenboard.com](mailto:cameron@greenboard.com).

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

[1] <https://investor.nvidia.com/investor-resources/faqs/default.aspx>

[2] <https://finance.yahoo.com/quote/NVDA/> (*note: figure quoted as of mkt. close 10.01.2024*)

[3] <https://www.ibm.com/think/topics/parallel-computing>

[4] <https://mobidev.biz/blog/essential-machine-learning-algorithms-for-business-applications>

[5] <https://the-decoder.com/gpt-4-architecture-datasets-costs-and-more-leaked/>

[6] <https://spectrum.ieee.org/what-is-deep-learning>

‍
