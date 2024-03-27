import React, { useState } from 'react';
import 'semantic-ui-css/semantic.min.css';
import { Icon, Button, Dropdown} from 'semantic-ui-react'; // Import des boutons Semantic UI React
import { Link } from 'react-router-dom'; // Import de Link depuis React Router
import { KeywordSearch, KeywordSearchBase, IdSearch} from './Components/Recherche_tweet.js'; // Import des composants de recherche de tweets
import ReqTable from './Components/Recherche_base.js';
import './App.css'; // Import du fichier CSS
import VisualisationTweets from './Components/Visualisation'; // Import du composant VisualisationTweets
import { set } from 'date-fns';


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


  const [showTweetsDropdown, setShowTweetsDropdown] = useState(false); // État pour suivre l'état d'ouverture du menu déroulant des tweets
  const [showAnalysisDropdown, setShowAnalysisDropdown] = useState(false); // État pour suivre l'état d'ouverture du menu déroulant de l'analyse
  const [showVisualisationDropdown, setShowVisualisationDropdown] = useState(true); // État pour suivre l'état d'ouverture du menu déroulant de la visualisation

  const handleTweetsDropdownOpen = () => {
    setShowTweetsDropdown(!showTweetsDropdown); // Inverse l'état d'ouverture du menu déroulant des tweets lors du clic sur le bouton "Actions"
  };

  const handleAnalysisDropdownOpen = () => {
    setShowAnalysisDropdown(!showAnalysisDropdown); // Inverse l'état d'ouverture du menu déroulant de l'analyse lors du clic sur le bouton "Analyse"
  };

  const handleVisualisationDropdownOpen = () => {
    setShowVisualisationDropdown(!showVisualisationDropdown); // Inverse l'état d'ouverture du menu déroulant de la visualisation lors du clic sur le bouton "Visualisation"
  }

  const actionsOptions = [
    // Options du menu déroulant des tweets pour les différentes actions
    { key: 'recherches-tweets', text: 'Recherches de tweets', value: 'recherches-tweets' },
    { key: 'recherches-requetes', text: 'Recherches de requêtes', value: 'recherches-requetes' },
    { key: 'recherche-base', text: 'Recherche de base', value: 'recherche-base' },
  ];

  const analysisOptions = [
    // Options du menu déroulant de l'analyse pour les différentes options d'analyse
    { key: 'analyse-requetes', text: 'Analyse des requêtes', value: 'analyse-requetes' },
    { key: 'analyse-resultats', text: 'Analyse des résultats', value: 'analyse-resultats' },
  ];

  const visualisationOptions = [
    // Options du menu déroulant des visualisations pour les différentes options de visualisation
    { key: 'visualisation-tweets', text: 'Visualisation des tweets', value: 'visualisation-tweets' },
    { key: 'visualisation-requêtes', text: 'Visualisation des requêtes', value: 'visualisation-requetes' },
  ];

  // État pour suivre le choix de l'utilisateur dans le menu déroulant
  const [OptionAction1, setOptionAction1] = useState(false);
  const [OptionAction2, setOptionAction2] = useState(false);
  const [OptionAction3, setOptionAction3] = useState(false);
  const [OptionAnalyse1, setOptionAnalyse1] = useState(false);
  const [OptionAnalyse2, setOptionAnalyse2] = useState(false);
  const [OptionVisualisation1, setOptionVisualisation1] = useState(false);
  const [OptionVisualisation2, setOptionVisualisation2] = useState(false);


  const handleDropdownChange = (event, data) => {
    const selectedValue = data.value;
    if (data && data.value) {
      setShowTweets(false);
      setShowAnalyse(false);
      setShowVisualisation(false);
    }
    if (data.value === 'recherches-tweets') {
      setShowTweets(true);
      setOptionAction1(true);
      setOptionAction2(false);
      setOptionAction3(false);
      setOptionAnalyse1(false);
      setOptionAnalyse2(false);
      setOptionVisualisation1(false);
      setOptionVisualisation2(false);
    }

    if (data.value === 'recherches-requetes') {
      setShowTweets(true);
      setOptionAction1(false);
      setOptionAction2(true);
      setOptionAction3(false);
      setOptionAnalyse1(false);
      setOptionAnalyse2(false);
      setOptionVisualisation1(false);
      setOptionVisualisation2(false);
    }

    if (data.value === 'recherche-base') {
      setShowTweets(true);
      setOptionAction1(false);
      setOptionAction2(false);
      setOptionAction3(true);
      setOptionAnalyse1(false);
      setOptionAnalyse2(false);
      setOptionVisualisation1(false);
      setOptionVisualisation2(false);
    }

    if (data.value === 'analyse-requetes') {
      setOptionAction1(false);
      setOptionAction2(false);
      setOptionAction3(false);
      setOptionAnalyse1(true);
      setOptionAnalyse2(false);
      setOptionVisualisation1(false);
      setOptionVisualisation2(false);
    }

    if (data.value === 'analyse-resultats') {
      setOptionAction1(false);
      setOptionAction2(false);
      setOptionAction3(false);
      setOptionAnalyse1(false);
      setOptionAnalyse2(true);
      setOptionVisualisation1(false);
      setOptionVisualisation2(false);
    }

    if (data.value === 'visualisation-tweets') {
      setOptionAction1(false);
      setOptionAction2(false);
      setOptionAction3(false);
      setOptionAnalyse1(false);
      setOptionAnalyse2(false);
      setOptionVisualisation1(true);
      setOptionVisualisation2(false);
    }

    if (data.value === 'visualisation-requetes') {
      setOptionAction1(false);
      setOptionAction2(false);
      setOptionAction3(false);
      setOptionAnalyse1(false);
      setOptionAnalyse2(false);
      setOptionVisualisation1(false);
      setOptionVisualisation2(true);
    }

  };

  const handleActionSelect = (action) => {
    setShowTweetsDropdown(false); // Ferme le menu déroulant après la sélection d'une action
  };

  const handleAnalysisSelect = (analysis) => {
    setShowAnalysisDropdown(false); // Ferme le menu déroulant après la sélection d'une option d'analyse
  };

  const handleVisualisationSelect = (visualisation) => {
    setShowVisualisationDropdown(false); // Ferme le menu déroulant après la sélection d'une action
  }
  

   return (
    <div className="main-container" style={{ height: '100vh', overflowY: 'auto' }}>
      <header className="header">
      {/* Bouton "Actions" avec le menu déroulant */}
      <div className="button-container">
      <Button className="black-button" circular size='massive' onClick={handleTweetsDropdownOpen}><Icon name='twitter' />Actions</Button>
      {showTweetsDropdown && (
      <Dropdown
    className="dropdown-menu"
    options={actionsOptions}
    onChange={(event, data) => handleDropdownChange(event, data)} // Pass both event and data
    onClose={() => setShowTweetsDropdown(false)}
    open={showTweetsDropdown}
    closeOnChange
    selection
  />
      )}
      
          {/*Bouton "Analyse" avec le menu déroulant*/}
          <Button className="black-button" circular size='massive' onClick={handleAnalysisDropdownOpen}><Icon name='chart bar'/>Analyse</Button>
      {showAnalysisDropdown && (
       <Dropdown
       className="dropdown-menu"
       options={analysisOptions}
       onChange={(event, data) => handleDropdownChange(event, data)} // Pass both event and data
       onClose={() => setShowAnalysisDropdown(false)}
       open={showAnalysisDropdown}
       closeOnChange
       selection
     />
      )}
   {/* Bouton "Visualisation" avec le menu déroulant */}
    <Button className="black-button" circular size='massive' onClick={handleVisualisationDropdownOpen}><Icon name='eye'/>Visualisation</Button>
    {showVisualisationDropdown && (
      <Dropdown
      className="dropdown-menu"
      options={visualisationOptions}
      onChange={(event, data) => handleDropdownChange(event, data)} // Pass both event and data
      onClose={() => setShowVisualisationDropdown(false)}
      open={showVisualisationDropdown}
      closeOnChange
      selection
    />

    )}
</div>

    </header>
        
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
  
  <div className="content">
  {showTweets && OptionAction1 && (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: '1', marginRight: '20px' }}>
        <div className="search-tweet-bar">
          <KeywordSearch />
        </div>
      </div>
      <div style={{ flex: '1' }}>
        <Link to="/recherches-tweets">
          <Button className="black-button" circular size='massive'>
            Go to Recherches Tweets
          </Button>
        </Link>
      </div>
    </div>
    )}
    {showTweets && OptionAction2&& (
      <div style={{ display: 'flex' }}>
        <div style={{ flex: '1', marginRight: '20px' }}>
          <div className="search-tweet-bar">
            <h2>Search Requests</h2>
            <IdSearch />
          </div>
        </div>
      </div>
    )}
    {showTweets && OptionAction3 && (
      <div style={{ display: 'flex' }}>
        <div style={{ flex: '1', marginRight: '20px' }}>
          <div className="search-tweet-bar">
            <h2>Search Base</h2>
            <KeywordSearchBase />
          </div>
        </div>
      </div>
    )}

    {/* {selectedOption == 'analyse-requetes' && (
      <div className="search-req-bar">
        <h2>AnalyseRequest</h2>
        <ReqTable />
      </div>
    )} */}

    {OptionAnalyse1 && (
      <div className="search-req-bar">
        <h2>Analyse</h2>
      </div>
    )}

    {/* OptionAnalyse2 && (
      <div className="search-req-bar">
        <h2>VisualisationTweets</h2>
        <VisualisationTweets />
      </div>
    )} */}

    {OptionVisualisation1 && (
      <div className="search-req-bar">
        <h2>Visualisation</h2>
        <VisualisationTweets />
      </div>
    )}
  </div>
</div>

);
}
export default App;