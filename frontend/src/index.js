import React from 'react';
import ReactDOM from 'react-dom'; // Importez ReactDOM.render
import './index.css';
import Home from './Home';
import reportWebVitals from './reportWebVitals';

import { BrowserRouter as Router } from 'react-router-dom';

ReactDOM.render(
  <Router>
    <Home />
  </Router>,
  document.getElementById('root')
);


// Si vous souhaitez mesurer les performances de votre application, passez une fonction
// pour enregistrer les résultats (par exemple: reportWebVitals(console.log))
// ou envoyez-les à un point de terminaison d'analyse. Apprenez-en plus: https://bit.ly/CRA-vitals
reportWebVitals();
