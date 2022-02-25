<p align="center"><img src="preview/header.png" width="100%" ></p>
<h1 align="center">|><|===> Go_Screen-CineMatrix 🎥 <===|><|</h1>

### Hey There Cinephiles !, have you ever wasted time on deciding which movie to watch, and end up being watching no movie. <b> NO MORE TIME WASTING ON DECIDING WHICH MOVIE TO WATCH COZ WE DO THAT FOR YOU  HERE IN GO_SCREEN-CINEMATRIX</b>
  
#### CineMatrix is one of its kind versatile, diversified movie recommending system which is based on not one or two but a combination five different recommending algorithms.CineMatrix is built on a solid foundation of advanced algorithms and methods like K-Nearest-Neighbours,term-frequency-inverse-document-frequency(tfidf),cosine similarity,SVD and many more other advanced techniques which gives at most most accurate recommendations almost instantly. With an interactive and user friendly UI/UX CineMatrix stands out from the rest of the other recommenders on the internet.
 
### Here is a sneakpeak of our website:
<p align="center"><img src="preview/website.png"></p>
  
- ### All you have to do is enter the movie of you're choice and hit search, our recommender fetches the best matching results from our database containing more than a Lakh movies and displays simila rmovies to the movie you entered.
- ### Not just the similar movies, you are also greeted with other great movies in the segment that are liked by other users with a similar taste as you.
- ### Our Recommender works on both Item_Based and User_based Collabrative Filtering giving you most flawless recommendations
- ### Here in CineMatrix we value you're time, we are thriving and trying our best to provide you with best user experience free of cost.
  
  <h1 align='center'>About The Team</h1>
  <p align="center"><img src="preview/aboutus.png" width="100%" ></p>
  
  
  ### Also CheckOut our one of its kind Song Recommender <a href="www.google.com">JAXXTOPIA</a>
  <p align="center"><img src="preview/jaxxtopia.gif" width="100%" >( under construction, will be available shortly )</p>

  ___
  
 ### That's all for the website promotion, now for the nerd like me who are interested in how this thing works, here is brief summary of the backend:
  ## For starters What is a Recommender system?
A recommender system is a simple algorithm whose aim is to provide the most relevant information to a user by discovering patterns in a dataset. The algorithm rates the items and shows the user the items that they would rate highly. An example of recommendation in action is when you visit Amazon and you notice that some items are being recommended to you or when Netflix recommends certain movies to you. They are alsoused by Music streaming applications such as Spotify and Deezer to
recommend music that you might like. During the last few decades, with the rise of Youtube, Amazon, Netflix and many other such web services, recommender systems have taken more and more place in our lives. From e-commerce (suggest to buyers articles that could interest them) to online advertisement (suggest to users the right contents, matching their preferences), recommender systems are today unavoidable in our daily online journeys.
 
  <p align="center"><img src="https://www.researchgate.net/profile/Alan-Eckhardt/publication/220827211/figure/fig2/AS:394007092973580@1470950019808/Structure-of-a-recommender-system.png" width="100%" ></p>

 ## Classification of Recommending system:
  <p align="center"><img src="https://ars.els-cdn.com/content/image/1-s2.0-S1319157819304963-gr1.jpg" width="100%" ></p>
 
## In CineMatrix i employed content and collabrative systems</br></br>
  - Under **content** based system i used item based filtering, techniques i implemented are: </br></br>
       - **TF-IDF (term frequency-inverse document frequency)** is a statistical measure that evaluates how relevant a word is to a document in a collection of documents.
        It works by increasing proportionally to the number of times a word appears in a document, but is offset by the number of documents that contain the word. So, words that         are common in every document. Multiplying and these two(term frequency,inverse document frequency) numbers results in the TF-IDF score of a word in a document. The               higher the score, the more relevant that word is in that particular document.</br>
        <p align="center"><img src="https://3.bp.blogspot.com/-u928a3xbrsw/UukmRVX_JzI/AAAAAAAAAKE/wIhuNmdQb7E/s1600/td-idf-graphic.png"></p>
      - **CountVectorizer** is a great tool provided by the scikit-learn library in Python. It is used to transform a given text into a vector on the basis of the frequency              (count) of each word that occurs in the entire text.CountVectorizer creates a matrix in which each unique word is represented by a column of the matrix, and each text            sample from the document is a row in the matrix. The value of each cell is nothing but the count of the word in that particular text sample.</br> 
      - **Cosine similarity** measures the similarity between two vectors of an inner product space. It is measured by the cosine of the angle between two vectors and determines whether two vectors are pointing in roughly the same direction. It is often used to measure document similarity in text analysis.the smaller the angle and the greater the match between vectors.</br>
      <p align="center"><img src="https://miro.medium.com/max/1400/0*koI1MIvINGYn2vU1.png" width="600"></p>
      - That's all for the concept part, i first read the datset cleaned it for potential null values
      added couple of coloumns to make the workflow easier, then took the user input, searched for the matrching result in the dataset using dfflib, dfflib searches for the best matching string and returns the value. Then i made two objects of classes TfidfVectorizer() and CountVectorizer(), then i used fit_transform() method for tfidf and count seperately to convert the text data into numerical data and finally used cosine similarity to find the best matching result i.e the words that are makign less angle with the word i given i.e the user movie title. Remaining is to enumerate through the similar movies that cosine similariity has found and print the top results after sorting similarity scores in descending order. The execution time and system resources consumed from this approach are very less compared to other techniques. 
      - i observed tfidf produces great results for some given inputs, and countvectorizer provied great results for other inputs. so i combined the results of both tfidf and            count vectorizer to get atmost precise results, then i passed the obtained combined matrix to the find the cosine similarity.</br>The final output is result of both tfidf and count vectorizer, i selected the top 10 best results and displayed them. Thanks to the pre-processing i've done to the dataset it takes less than second to compute and display recommended movies.</br></br>
      
  - Under **collabrative** based system i used item based memory based filtering, under memory based i implemented both user based and item based techniques: </br></br>
    -,efmwe.fm
     

  
