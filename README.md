# Content Based Article Recommendation System


## Introduction
To address the problem of increasing mental health issues among today's internet using generation. To devise a system by deploying technology in learning from the user's online behaviour and and thus assessing the mental state of the users, providing preventive and helpful feedback, using technologies like Deep Learning. This recommendation system is built as a part of Bachelor Thesis Project for the topic : "APPLYING THE CONCEPTS OF MACHINE LEARNING TO SOLVE MENTAL HEALTH ISSUES".  


## Proposed Solution
Our first intuition was that there should be a vector representation of each article and each user preference so that we could use some sort of similarity metric (cosine similarity) in our case so as to recommend articles to the users based on their similarity index with respect to a particular user's preference’s representation.
On comparing different similarity metrics we observed that cosine similarity was optimal in terms of performance as well as computational complexity.
#### Cosine Similarity 
There is a clear intuition behind using cosine similarity:
Given two vectors that are collinear it is straightforward to see that their similarity must be maximum that is 1 ands so also is the cosine of the angle between them. Moving to diametrically opposite vectors with an angle of 180 degrees between them we expect these to be minimally similar and thus the cosine of the angle is -1. Thus cosine similarity gives a good measure of similarity between two vectors using the angle between them as a measure. The output is on a scale of -1 to 1 with 1 being most similar and -1 being least similar. 
#### Stepwise working 
1. _Encoding of Articles:_ For this on the dataset gathered we trained an LDA model which gave us as output a vector of floating point values in the range 0-1 , indicating the probability value of that article falling under a particular topic. This served as the encoding of the articles.
2. _Encoding of User’s preference:_ We knew that the dimensions of the vectors should be same as that of the articles and thus we interpreted the vector as a series of values indicating the likelihood of the given user liking a given topic. The question that remained was how to assign these values. We had to come up with a deterministic function that satisfies the following criteria:
    1. The magnitude of the function needed to be in the range of 0-1. This is because it denotes a probability.
    2. It should be able to model how the interest of a user towards a particular topic varies with time. To this end we observe that users that regularly read something related to one topic develop a very high affinity towards that topic. However, if there is inaction of a user towards a given topic he would gradually lose interest, but it is not as if his interest would become negligible.
3. The last issue was how to decide when to generate spikes , for that we consider two events:
    1. If the user reads a given article: We know the article vector for the given articles and thus we can find the top k most influential topics of that articles and generate spikes for those k topics in the user vector.
    2. User gives his initial preference through tags: LDA provides us with the word distribution for each topic , so given some words representing tags of interest we can find the set of topics for which the given tags appear in the top m words of a particular topic. Once we have such a set of topics we can easily generate spikes for only the topics present in the set.

### LDA Model 

<p align="center">
  <img src="https://github.com/Amritha777/BB-TT-PP/blob/master/images/Screen%20Shot%202020-03-27%20at%209.10.17%20PM.png">
</p>

### Basic Flowchart

<p align="center">
  <img src="https://github.com/Amritha777/BB-TT-PP/blob/master/images/Screen%20Shot%202020-03-27%20at%209.11.00%20PM.png">
</p>

## Results 
### Evaluation Metrics used:
The fine tuning of the LDA model is done by varying the following parameters, which affect the training of the model. 
1. Num_of_topics : the number of topics will depend on both the data and the application. It can also be thought of as the number of different "labels" which we want the model to identify and differentiate.
2. Iterations : it controls how often we repeat a particular loop over each document. The no of iterations should be sufficiently high, without inducing overfitting of data.
3. Passes : Passes controls how often we train the model on the entire corpus. The no of passes should be sufficiently high. 
These parameters are varied to study their effect on the training of the model and in result the accuracy of the model. Since the LDA model is an unsupervised learning model, the accuracy cannot be determined directly. Hence evaluation of the LDA model is done using the following metrics that are obtained as an output of training.
4. Bound : Estimate the variational bound of documents from corpus
5. Diff : Difference topic to topic between two Lda models  is function that will be applied to calculate difference between any topic pair. The decrease in diff means enhancement of performance.
6. Perplexity : Calculate and return per-word likelihood bound, using the chunk of documents as evaluation corpus. Perplexity is to decrease with increase in performance.
7. Convergence : No of inputs that have converged in the current pass.
### Results-table
<p align="center">
  <img src="https://github.com/Amritha777/BB-TT-PP/blob/master/images/Screen%20Shot%202020-03-27%20at%209.11.20%20PM.png">
</p>

### Inferences
1. It has been observed that beyond 300 iteration of our model it leads to overfitting of the data. Hence the iterations are to be kept below 300
2. On increasing the no of passes from 20 to 50, a significant improvement in the performance of the model has been observed.
3. The number of dimensions must closely resemble the real life labels we wish the model to differentiate between. So the choice is made according to our data and application of our model.
