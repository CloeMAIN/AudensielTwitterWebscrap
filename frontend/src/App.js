import React, { useState } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Button, Icon } from 'semantic-ui-react'; // Import des boutons Semantic UI React
import SearchBar from './Components/Recherche_tweet.js';
import ReqTable from './Components/Recherche_base.js';
import './App.css'; // Import du fichier CSS
import VisualisationTweets from './Components/Visualisation'; // Import du composant VisualisationTweets


function App() {
  // États pour gérer l'affichage des différents composants
  const [showTweets, setShowTweets] = useState(false);
  const [showAnalyse, setShowAnalyse] = useState(false);
  const [showVisualisation, setShowVisualisation] = useState(false);

  // Gestion des clics sur les boutons pour afficher les composants correspondants
  const handleTweetsClick = () => {
    setShowTweets(true);
    setShowAnalyse(false);
    setShowVisualisation(false);
  };

  const handleAnalyseClick = () => {
    setShowTweets(false);
    setShowAnalyse(true);
    setShowVisualisation(false);
  };

  const handleVisualisationClick = () => {
    setShowTweets(false);
    setShowAnalyse(false);
    setShowVisualisation(true);
  };

  return (
    <div className="main-container" style={{height: '100vh', overflowY: 'auto' }}>
       <header className="header">
       <div className="title">Scrapping </div>
        <div className="buttons-container">
          {/* Utilisation des boutons Semantic UI React avec des icônes */}
          <Button className="black-button" circular size='massive' onClick={handleTweetsClick}>
            <Icon name='twitter' />
            Récolte de tweets
          </Button>
          <Button className="black-button" circular size='massive' onClick={handleAnalyseClick}>
            <Icon name='chart bar' />
            Analyse
          </Button>
          <Button className="black-button" circular size='massive' onClick={handleVisualisationClick}>
            <Icon name='eye' />
            Visualisation
          </Button>
        </div>
      </header>
      <div className="content">
        {showTweets && (
          <>
            <div className="left-bar" >
              <div className="search-tweet-bar">
                <h2>Search Tweets</h2>
                <SearchBar/>
              </div>
            </div>
            <div className="right-bar">
              <div className="search-req-bar">
                <h2>Search Requests</h2>
                <ReqTable/>
              </div>
            </div>
          </>
        )}
        {showAnalyse && (
          <div className="search-req-bar">
            <h2>Analyse</h2>
            {/* Composant pour l'analyse */}
          </div>
        )}
        {showVisualisation && (
          <div className="search-req-bar">
            <h2>Visualisation</h2>
            <VisualisationTweets/>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
