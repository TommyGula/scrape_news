# scrape_news
 The porpuse of this project is to extract news data from the investing.com page, to later be analyzed at the user's convenience.
 
 **How does it work?**
 
 It has 3 main functions:
 
 1- doScroll: this function gets the driver and the lenght of the page you want to scrape, and, once inside the url, it will do as many scrolls as needed to get all ths posts you want to scrape
 2- scrape_investing: it receives a tag, a number of posts and an option of translating or not. The tag is the query for the search inside investing.com. The number of posts is how many news you want to srape. And, if you want to translate all scraped news to english, you can do it with the third parameter
 3- translate: it gets the google translator url and for each sentence in an array, it fills the "from" field with the initial sentence and gets a translation
 
 **How to make it work**
 
 Parameters:
 
 -t: -tag: The tag you want to seach. https://es.investing.com/search/?tab=news&q={*tag*}
 -n: -numOfPost: how many posts you want to scrape
 -g: -googleTranslator: If you want to translate, the type something with this parameter
 
 *Example*
 
 python scrape_investing -t AAPL -n 100 -g y (it can be "y", "1", "2312343", or whatever you want... it's enought if it is not False)
 
