import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Input, Button, Table, Icon, Form, Popup } from 'semantic-ui-react';
function SearchKeyWord({ keyword, setKeyword }) {
    return (
        <Form.Field>
            <label>Mots-clés</label>
            <Input
                placeholder="Mots-clés"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
            />
        </Form.Field>
    );
}

function SearchDateRange({ beginDate, setBeginDate, endDate, setEndDate, numberTweet, setNumberTweet }) {
    return (
        <Form.Group>
            <Form.Field>
                <label>Date de début</label>
                <Input
                    type="date"
                    placeholder="Date de début"
                    value={beginDate}
                    onChange={(e) => setBeginDate(e.target.value)}
                />
            </Form.Field>
            <Form.Field>
                <label>Date de fin</label>
                <Input
                    type="date"
                    placeholder="Date de fin"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </Form.Field>
            <Form.Field>
                <label>Nb de tweets</label>
                <Input
                    type="number"
                    placeholder="Nb de tweets"
                    value={numberTweet}
                    onChange={(e) => setNumberTweet(e.target.value)}
                />
            </Form.Field>
        </Form.Group>
    );
}

function SubmitButtonId({ handleSubmit, isLoading }) {
    return (
        <Button loading={isLoading} primary icon labelPosition='left' type="submit" style={{ backgroundColor: '#b63a3a' }}>
            <Icon name='search' />
            Rechercher
        </Button>
    );
}

function SubmitButtonKeyword({ handleSubmit, isLoading }) {
    return (
        <Button loading={isLoading} primary icon labelPosition='left' type="submit" style={{ backgroundColor: '#b63a3a' }}>
            <Icon name='search' />
            Rechercher
        </Button>
    );
}

function SearchReqId({ reqId, setReqId }) {
    return (
        <Form.Field>
            <label>ID de la requête</label>
            <Input
                type="text"
                placeholder="ID de la requête"
                value={reqId}
                onChange={(e) => setReqId(e.target.value)}
            />
        </Form.Field>
    );
}
function CommentPopup({ tweet, handleCommentClick }) {
    const [popupOpen, setPopupOpen] = useState(false);

    return (
        <Popup
            trigger={<Icon name='comment' onClick={() => {setPopupOpen(true); handleCommentClick(tweet.id);}} />}
            on='click'
            wide
            position='bottom center'
            open={popupOpen}
            onClose={() => setPopupOpen(false)}
            style={{ padding: '20px', maxWidth: '50vw' }} // Style du popup
        >
            <div style={{ maxHeight: '60vh', overflowY: 'auto' }}>
                <Button icon='close' color='red' onClick={() => setPopupOpen(false)} style={{ position: 'absolute', top: '10px', right: '10px', zIndex: '9999' }} />
                <ul style={{ listStyleType: 'none', padding: 0 }}> {/* Supprimez les puces de la liste */}
                    {tweet.comment_tweet.map((comment, index) => (
                        <li key={index} style={{ marginBottom: '10px', borderBottom: '1px solid #ccc', paddingBottom: '5px' }}> {/* Ajoutez une bordure inférieure pour séparer les commentaires */}
                            {comment}
                        </li>
                    ))}
                </ul>
            </div>
        </Popup>
    );
}


function SearchBar() {
    // Définition des variables d'état
    const [keyword, setKeyword] = useState('');
    const [beginDate, setBeginDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [numberTweet, setNumberTweet] = useState('');
    const [tweets, setTweets] = useState([]);
    const [start, setStart] = useState(0);
    const [end, setEnd] = useState(5);
    const [isLoadingKeyword, setIsLoadingKeyword] = useState(false);
    const [isLoadingId, setIsLoadingId] = useState(false);
    const [currentReqId, setCurrentReqId] = useState('');
    const [reqId, setReqId] = useState('');
    const [requestStatus, setRequestStatus] = useState('');
    
    // initialisation tweets à une liste vide


    useEffect(() => {
        console.log(tweets);
    }, [tweets]);

    let now = new Date();
    //Pour avoir l'id de la requête dans le même format que dans le backend
    let year = now.getFullYear();
    let month = String(now.getMonth() + 1).padStart(2, '0'); // Les mois commencent à 0 en JavaScript
    let day = String(now.getDate()).padStart(2, '0');
    let hour = String(now.getHours()).padStart(2, '0');
    let minute = String(now.getMinutes()).padStart(2, '0');
    let req_id = `${year}${month}${day}${hour}${minute}`;

    //Fonctions de soumission (va faire requete get_tweets par le biais url)
    const handleSubmitByKeyword = async (event) => {
        event.preventDefault();
        now = new Date();
        year = now.getFullYear();
        month = String(now.getMonth() + 1).padStart(2, '0'); // Les mois commencent à 0 en JavaScript
        day = String(now.getDate()).padStart(2, '0');
        hour = String(now.getHours()).padStart(2, '0');
        minute = String(now.getMinutes()).padStart(2, '0');
        req_id = `${year}${month}${day}${hour}${minute}`;
        setCurrentReqId(req_id);
        event.preventDefault();
        setRequestStatus('envoyé'); // La requête est envoyée
        // Effectuer la requête get_tweets avec keyword, beginDate et endDate
        try{
            setIsLoadingKeyword(true); // Définir isLoading à true lors de la requête
            const response = await axios.get(`http://localhost:8000/api/search/${keyword}/${endDate}/${beginDate}/${numberTweet}`);
            //const response = await axios.get(`https://scrappertwitter.pythonanywhere.com/api/search/${keyword}/${endDate}/${beginDate}/${numberTweet}`);
            // afficher la réponse dans la console
            // On pourrait ajouter un élement montrant que la requête a été effectuée
            // et un autre pour montrer que la requête est toujours en cours
            // On pourrait aussi ajouter un élement montrant que la requête est terminée
            // et un autre pour montrer que la requête a échoué
            setTweets(response.data);
            console.log(response);
        } catch (error){
            console.error(error);
            setRequestStatus('échoué'); // La requête a échoué

        } finally {
            setIsLoadingKeyword(false); // Définir isLoading à false lorsque la requête est terminée
            setRequestStatus('terminé'); // La requête est terminée
        }
    }


    const handleSubmitById = async (event) => {
        event.preventDefault();
        // Effectuer la requête get_tweets avec l'ID de la requête
        const id = reqId !== '' ? reqId : currentReqId;
        try {
            setIsLoadingId(true); // Définir isLoading à true lors de la requête
            const response = await axios.get(`http://localhost:8000/api/display_new/${id}`);
            setTweets(response.data);
            console.log(response);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoadingId(false); // Définir isLoading à false lorsque la requête est terminée
        }
    };

    const handleNext = () => {
        setStart((oldStart) => oldStart + 5);
        setEnd((oldEnd) => oldEnd + 5);
    };

    const handlePrevious = () => {
        setStart((oldStart) => oldStart - 5);
        setEnd((oldEnd) => oldEnd - 5);
    }

    // Définition de la fonction pour gérer l'ouverture/fermeture du popup des commentaires
    const handleCommentClick = (index) => {
        // Mettez en œuvre la logique pour ouvrir/fermer le popup des commentaires
        console.log('Comment popup clicked for tweet at index', index);
    }

    

    // Affichage 
    return (
        <div className="FormsAndTweet" style={{ width: '90%', height: '70vh', margin: '0 auto', overflowY: 'auto' }}>
            <Form onSubmit={handleSubmitByKeyword} style={{ mrginBottom: '20px' }}>
                <SearchKeyWord keyword={keyword} setKeyword={setKeyword} />
                <SearchDateRange
                    beginDate={beginDate}
                    setBeginDate={setBeginDate}
                    endDate={endDate}
                    setEndDate={setEndDate}
                    numberTweet={numberTweet}
                    setNumberTweet={setNumberTweet}
                />
                <SubmitButtonKeyword handleSubmit={handleSubmitByKeyword} style={{ marginBottom: '20px' }} isLoading={isLoadingKeyword} 
                />
            </Form>

            <Form onSubmit={handleSubmitById} style={{ marginBottom: '20px' }}>
                <SearchReqId reqId={reqId} setReqId={setReqId} />
                <SubmitButtonId handleSubmit={handleSubmitById} isLoading={isLoadingId} />
            </Form>

            <div className="TweetTable"  >
                <Button onClick={handlePrevious} disabled={start === 0} style={{ marginRight: '10px' }}>Previous</Button>
                <Button onClick={handleNext} disabled={end >= tweets.length} style={{ marginRight: '10px' }}>Next</Button>
                <Table celled>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Tweet</Table.HeaderCell>
                            <Table.HeaderCell>Views</Table.HeaderCell>
                            <Table.HeaderCell>Likes</Table.HeaderCell>
                            <Table.HeaderCell>Replies</Table.HeaderCell>
                            <Table.HeaderCell>Comments</Table.HeaderCell>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {tweets.slice(start, end).map((tweet, index) => (
                            <Table.Row key={index}>
                                <Table.Cell>{tweet.text_tweet}</Table.Cell>
                                <Table.Cell>{tweet.nombre_views}</Table.Cell>
                                <Table.Cell>{tweet.nombre_likes}</Table.Cell>
                                <Table.Cell>{tweet.nombre_replies}</Table.Cell>
                                <Table.Cell>
                        <CommentPopup tweet={tweet} handleCommentClick={handleCommentClick} />
                    </Table.Cell>
                            </Table.Row>
                        ))}
                    </Table.Body>
                </Table>
            </div>
        </div>
    );
}

export default SearchBar;
