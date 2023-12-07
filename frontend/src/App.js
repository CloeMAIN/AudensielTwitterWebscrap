import React from 'react';
import SearchBar from './Components/Recherche_tweet.js';
import TweetContent from './Components/Tableau_tweet.js';

function App() {
  return (
    <div className="Main">
      <div className="SearchTweetBar">
        <SearchBar/>
      </div>
      <div className="TweetTable">
        <TweetContent/>
      </div>
    </div>
  );
}

export default App;