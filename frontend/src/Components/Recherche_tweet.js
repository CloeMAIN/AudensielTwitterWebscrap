import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Input, Button, Table, Icon, Form, Popup } from 'semantic-ui-react';
import './Recherche_tweet.css';

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
////AJOUT Clément
function SearchByKeywords({searchByKeyword, setSearchByKeyword}) {
    return (
        <Form.Field>
            <label>Mot clé</label>
            <Input
                type="text"
                placeholder="Mot clés recherché"
                value={searchByKeyword}
                onChange={(e) => setSearchByKeyword(e.target.value)}
            />
        </Form.Field>
    );
}
////

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
                    {tweet.comment_tweet.map((commentobj, index) => (
                        <li key={index} style={{ marginBottom: '10px', borderBottom: '1px solid #ccc', paddingBottom: '5px' }}> {/* Ajoutez une bordure inférieure pour séparer les commentaires */}
                            {commentobj.commentaire}
                        </li>
                    ))}
                </ul>
            </div>
        </Popup>
    );
}


function KeywordSearch() {
    const [keyword, setKeyword] = useState('');
    const [beginDate, setBeginDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [numberTweet, setNumberTweet] = useState('');
    const [tweets, setTweets] = useState([]);
    const [start, setStart] = useState(0);
    const [end, setEnd] = useState(5);
    const [isLoadingKeyword, setIsLoadingKeyword] = useState(false);
    const [requestStatus, setRequestStatus] = useState('');

    useEffect(() => {
        console.log(tweets);
    }, [tweets]);

    const handleSubmitByKeyword = async (event) => {
        event.preventDefault();
        setIsLoadingKeyword(true);
        setRequestStatus('envoyé');

        try {
            const response = await axios.get(`http://localhost:8000/api/search/${keyword}/${endDate}/${beginDate}/${numberTweet}`);
            setTweets(response.data);
            console.log(response);
            setRequestStatus('terminé');
        } catch (error) {
            console.error(error);
            setRequestStatus('échoué');
        } finally {
            setIsLoadingKeyword(false);
        }
    }

    const handleNext = () => {
        setStart((oldStart) => oldStart + 5);
        setEnd((oldEnd) => oldEnd + 5);
    };

    const handlePrevious = () => {
        setStart((oldStart) => oldStart - 5);
        setEnd((oldEnd) => oldEnd - 5);
    }

    const handleCommentClick = (index) => {
        console.log('Comment popup clicked for tweet at index', index);
    }

    return (
        <>
            <div className="search-tweet-bar" style={{ display: 'block', width: '100%', margin: '0 auto' }}>
                <Form onSubmit={handleSubmitByKeyword}>
                    <SearchKeyWord keyword={keyword} setKeyword={setKeyword} />
                    <SearchDateRange
                        beginDate={beginDate}
                        setBeginDate={setBeginDate}
                        endDate={endDate}
                        setEndDate={setEndDate}
                        numberTweet={numberTweet}
                        setNumberTweet={setNumberTweet}
                    />
                    <SubmitButtonKeyword handleSubmit={handleSubmitByKeyword} style={{ marginBottom: '20px' }} isLoading={isLoadingKeyword} />
                </Form>
            </div>
            {/* Séparateur */}
            <hr style={{ border: '1px solid #000', marginBottom: '20px' }} />

            <div className="result-table" style={{ height: '50vh', overflowY: 'auto' }}>
                <Button onClick={handlePrevious} disabled={start === 0} style={{ marginRight: '10px' }}>Previous</Button>
                <Button onClick={handleNext} disabled={end >= tweets.length} style={{ marginRight: '10px' }}>Next</Button>
                <Table celled>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Tweet</Table.HeaderCell>
                            <Table.HeaderCell>Date</Table.HeaderCell>
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
                                <Table.Cell>{tweet.date_tweet}</Table.Cell>
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
        </>
    );
}

function KeywordSearchBase() {
    const [keyword, setKeyword] = useState('');
    const [beginDate, setBeginDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [numberTweet, setNumberTweet] = useState('');
    const [tweets, setTweets] = useState([]);
    const [start, setStart] = useState(0);
    const [end, setEnd] = useState(5);
    const [isLoadingKeyword, setIsLoadingKeyword] = useState(false);
    const [requestStatus, setRequestStatus] = useState('');
    const [isLoadingSearchByKeyword, setIsLoadingSearchByKeyword] = useState(false);
    const [searchByKeyword, setSearchByKeyword] = useState('');
    const [isLoadingId, setIsLoadingId] = useState(false);

    const handleSubmitSearchKeyword = async (event) => {
        event.preventDefault();
        const mot_cle = searchByKeyword;
        try {
            setIsLoadingSearchByKeyword(true);
            const response = await axios.get(`http://localhost:8000/api/display_tweet_by_keyword/${mot_cle}`);
            setTweets(response.data);
            console.log(response);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoadingSearchByKeyword(false);
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

    const handleCommentClick = (index) => {
        console.log('Comment popup clicked for tweet at index', index);
    }

    return (
        <>
            <div className="search-tweet-bar" style={{ display: 'block', width: '90%', margin: '0 auto' }}>
                <Form onSubmit={handleSubmitSearchKeyword}>
                    <SearchByKeywords searchByKeyword={searchByKeyword} setSearchByKeyword={setSearchByKeyword} />
                    <SubmitButtonId handleSubmit={handleSubmitSearchKeyword} isLoading={isLoadingId} />
                </Form>
            </div>
            {/* Séparateur */}
            <hr style={{ border: '1px solid #000', marginBottom: '20px' }} />
            <div className="result-table" style={{ height: '50vh', overflowY: 'auto' }}>
                <Button onClick={handlePrevious} disabled={start === 0} style={{ marginRight: '10px' }}>Previous</Button>
                <Button onClick={handleNext} disabled={end >= tweets.length} style={{ marginRight: '10px' }}>Next</Button>
                <Table celled>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Tweet</Table.HeaderCell>
                            <Table.HeaderCell>Date</Table.HeaderCell>
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
                                <Table.Cell>{tweet.date_tweet}</Table.Cell>
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
        </>
    );
}

function IdSearch() {
    const [reqId, setReqId] = useState('');
    const [tweets, setTweets] = useState([]);
    const [start, setStart] = useState(0);
    const [end, setEnd] = useState(5);
    const [isLoadingId, setIsLoadingId] = useState(false);

    const handleSubmitById = async (event) => {
        event.preventDefault();
        setIsLoadingId(true);

        try {
            const response = await axios.get(`http://localhost:8000/api/display_new/${reqId}`);
            setTweets(response.data);
            console.log(response);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoadingId(false);
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

    const handleCommentClick = (index) => {
        console.log('Comment popup clicked for tweet at index', index);
    }

    return (
        <>
            {/* Barre de recherche */}
            <div className="search-tweet-bar" style={{ display: 'block', width: '90%', margin: '0 auto' }}>
                <Form onSubmit={handleSubmitById}>
                    <SearchReqId reqId={reqId} setReqId={setReqId} />
                    <SubmitButtonId handleSubmit={handleSubmitById} isLoading={isLoadingId} />
                </Form>
            </div>
            
            {/* Séparateur */}
            <hr style={{ border: '1px solid #000', marginBottom: '20px' }} />
            
            {/* Tableau des résultats */}
            <div className="result-table" style={{ height: '50vh', overflowY: 'auto' }}>
                <Button onClick={handlePrevious} disabled={start === 0} style={{ marginRight: '10px' }}>Previous</Button>
                <Button onClick={handleNext} disabled={end >= tweets.length} style={{ marginRight: '10px' }}>Next</Button>
                <Table celled>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Tweet</Table.HeaderCell>
                            <Table.HeaderCell>Date</Table.HeaderCell>
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
                                <Table.Cell>{tweet.date_tweet}</Table.Cell>
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
        </>
    );
    
    
    
}



export { KeywordSearch, KeywordSearchBase, IdSearch};
