import React, { useState } from 'react';
import { Button, Header, Icon, Image, Segment } from 'semantic-ui-react'; // Import des composants Semantic UI React
import App from './App'; // Import du composant App
import './Home.css'; // Import du fichier CSS
import twitterLogo from './twitterlogo.png';

function Home() {
  const [showApp, setShowApp] = useState(false); // État pour gérer l'affichage du composant App

  // Fonction pour changer l'état de showApp lorsque le bouton est cliqué
  const handleStartClick = () => {
    setShowApp(true);
  };

  // Rendu conditionnel : afficher le composant App si showApp est true, sinon afficher le contenu par défaut
  return (
    <div className="home-container">
      {!showApp && (
        <>
          <Segment padded="very" textAlign="center">
        <Image src={twitterLogo} alt="Twitter Logo" className="logo" size='medium' centered />
        <Header as='h1' className="title">Bienvenue sur notre site</Header>
        <p className="description">
          Sur ce site, vous pouvez explorer Twitter et découvrir ce que les gens en disent.
          Vous pouvez effectuer des recherches par mots-clés, par dates, etc.
        </p>
        {/* Bouton start qui, si on appuie dessus, change l'interface avec App */}
        <Button primary size='large' className="start-button" onClick={handleStartClick}>
          <Icon name='play' />
          Commencer
        </Button>
      </Segment>

      <Segment textAlign="center">
        <Header as='h2' className="feature-header">Fonctionnalités</Header>
        <p className="feature-description">
          Notre site vous permet de rechercher des tweets par mots-clés, de spécifier des dates de début et de fin pour votre recherche, et de limiter le nombre de tweets à afficher. 
        </p>
        <p className="feature-description">
          Vous pouvez également visualiser les résultats de votre recherche sous forme de tableau avec des informations détaillées sur chaque tweet.
        </p>
      </Segment>

      <Segment textAlign="center">
        <Header as='h2' className="contact-header">Contactez-nous</Header>
        <p className="contact-info">
          Pour toute question ou suggestion, n'hésitez pas à nous contacter à l'adresse email suivante : contact@notresite.com
        </p>
      </Segment>
        </>
      )}
      {showApp && <App />}
    </div>
  );
}

export default Home;
