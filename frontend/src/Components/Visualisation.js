import 'chart.js/auto';
import 'chartjs-adapter-date-fns'; // Importez le module de l'adaptateur pour utiliser date-fns avec Chart.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Line } from 'react-chartjs-2'; // Importer le composant de graphique en courbes

function VisualisationTweets() {
    const [requestsData, setRequestsData] = useState([]);

    useEffect(() => {
        // Récupérer les données sur le nombre de tweets par requête depuis votre API
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/display_req');
                setRequestsData(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    // Extraire les noms des requêtes et le nombre de tweets associés
    const requestData = requestsData.map(request => ({
        name: request.req_id,
        nbtweets: request.nb_tweets
    }));

    // Extraire les noms des requêtes pour l'étiquette de l'axe X
    const labels = requestData.map(request => request.name);

    // Extraire le nombre de tweets pour chaque requête pour les données du graphique
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Nombre de Tweets',
                data: requestData.map(request => request.nbtweets),
                backgroundColor: 'red',
                borderColor: 'black',
                borderWidth: 1,
            },
        ],
    };

    const options = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: false,
                    stepSize: 1, // Définir le pas à 1 pour garantir des nombres entiers
                    precision: 0 // Définir la précision à 0 pour éviter les valeurs décimales
                }
            }],
            xAxes: [{
                type: 'category',
                labels: labels
            }]
        }
    };

    return (
        <div style={{ width: '1100px', height: '600px' }}> {/* Ajoutez des styles pour la taille du graphe */}
            <h2>Visualisation du nombre de Tweets par requête</h2>
            {/* Utilisez le composant de graphique en courbes (Line) au lieu de Bar */}
            <Bar data={data} options={options} />
        </div>
    );
}


export default VisualisationTweets;

