import React, { useState } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Button, Icon } from 'semantic-ui-react'; // Import des boutons Semantic UI React
import { KeywordSearch, KeywordSearchBase, IdSearch} from './Components/Recherche_tweet.js'; // Import des composants de recherche de tweets
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
    <div className="main-container" style={{ height: '100vh', overflowY: 'auto' }}>
      <header className="header">
      <div className="title">        </div>
        { !showTweets && !showAnalyse && !showVisualisation && (
          <>
            <div className="title">Sur ce site vous pouvez </div>
            {/* Trois blocs qui expliquent chacune des fonctionnalités */}
            <div className="feature-explanation">
              <div className="feature">
                <div className="feature-icon">
                  <Icon name='twitter' size='huge' />
                </div>
                <div className="feature-details">
                  <h2>Récolte de tweets</h2>
                  <p>Explorez et récupérez des tweets en fonction de critères spécifiques.</p>
                </div>
              </div>
              <div className="feature">
                <div className="feature-icon">
                  <Icon name='chart bar' size='huge' />
                </div>
                <div className="feature-details">
                  <h2>Analyse</h2>
                  <p>Analysez les données collectées pour obtenir des insights précieux.</p>
                </div>
              </div>
              <div className="feature">
                <div className="feature-icon">
                  <Icon name='eye' size='huge' />
                </div>
                <div className="feature-details">
                  <h2>Visualisation</h2>
                  <p>Visualisez les résultats de manière claire et intuitive.</p>
                </div>
              </div>
            </div>
          </>
        )}
        {/* Mettre les boutons au centre puis une fois l'une d'elle cliquée, les mettre toutes en haut */}
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
  <div style={{ display: 'flex' }}>
    <div style={{ flex: '1', marginRight: '20px' }}>
      <div className="search-tweet-bar">
        <h2>Search Tweets</h2>
        <KeywordSearch />
      </div>
      <div className="search-tweet-bar">
        <h2>Search Requests</h2>
        <IdSearch />
      </div>
      <div className="search-tweet-bar">
        <h2>Search Base</h2>
        <KeywordSearchBase />
      </div>
    </div>
    <div style={{ flex: '1' }}>
      <div className="search-req-bar">
        <h1>Table Requests</h1>
        <ReqTable />
      </div>
    </div>
  </div>
)}

        {showAnalyse && (
          <div className="search-req-bar">
            <h2>Analyse</h2>
            {/* Composant pour l'analyse */}
          </div>
        )}
        {showVisualisation && (
          <h1>Visualisation
          <div className="search-req-bar">
            <VisualisationTweets />
          </div>
          </h1>
        )}
      </div>
    </div>
  );
}
export default App;