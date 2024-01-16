import React, { useEffect, useState } from 'react';
import axios from 'axios';

function SearchKeyWord({keyword,setKeyword}){
    return(
        <form>
            <input type="text" placeholder="Mot Clés" value={keyword} onChange={(e) => setKeyword(e.target.value)}/>
        </form>
    );
}

function SearchBeginDate({beginDate,setBeginDate}){
    return(
        <form>
            <input type="date" placeholder="Début" value={beginDate} onChange={(e) => setBeginDate(e.target.value)}/>
        </form>
    );
}


function SearchEndDate({endDate,setEndDate}){
    return(
        <form>
            <input type="date" placeholder="Fin" value={endDate} onChange={(e) => setEndDate(e.target.value)}/>
        </form>
    );
}

function SearchNumberTweet({numberTweet,setNumberTweet}){
    return(
        <form>
            <input type="number" placeholder="Nb de tweet demander" value={numberTweet} onChange={(e) => setNumberTweet(e.target.value)}/>
        </form>
    );
}

function SubmitButton({handleSubmit,isLoading}){
    return(
        <button type="submit" onClick = {handleSubmit} disabled={isLoading}>Rechercher</button>
    );
}

function SearchReqId({reqId, setReqId}){
    return(
        <form>
            <input type="text" placeholder="ID de la requête" value={reqId} onChange={(e) => setReqId(e.target.value)}/>
        </form>
    );
}

function SearchBar(){
    // Definition fonction

    //Definition des variables d'état
    const [keyword, setKeyword] = useState('');
    const [beginDate, setBeginDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [numberTweet, setNumberTweet] = useState('');
    const [tweets, setTweets] = useState([]);
    const [start,setStart] = useState(0);
    const [end,setEnd] = useState(5);
    const [isLoading, setIsLoading] = useState(false);
    const [currentReqId,setCurrentReqId] = useState('');
    const [reqId, setReqId] = useState('');
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
    const handleSubmit = async (event) => {
        event.preventDefault();
        now = new Date();
        year = now.getFullYear();
        month = String(now.getMonth() + 1).padStart(2, '0'); // Les mois commencent à 0 en JavaScript
        day = String(now.getDate()).padStart(2, '0');
        hour = String(now.getHours()).padStart(2, '0');
        minute = String(now.getMinutes()).padStart(2, '0');
        
        req_id = `${year}${month}${day}${hour}${minute}`;
        setCurrentReqId(req_id);
        // Effectuer la requête get_tweets avec keyword, beginDate et endDate
        try{
            //const response = await axios.get(`http://localhost:8000/api/search/${keyword}/${endDate}/${beginDate}/${numberTweet}`);
            const response = await axios.get(`https://scrappertwitter.pythonanywhere.com/api/search/${keyword}/${endDate}/${beginDate}/${numberTweet}`);
            console.log(response);
            // On pourrait ajouter un élement montrant que la requête a été effectuée
            // et un autre pour montrer que la requête est toujours en cours
            // On pourrait aussi ajouter un élement montrant que la requête est terminée
            // et un autre pour montrer que la requête a échoué
        } catch (error){
            console.error(error);

        } finally {
            setIsLoading(false); // Définir isLoading à false lorsque la requête est terminée
        }
    }

    //Faire tourner cela toutes les 20 secondes ou a chaque update demandé par l'utilisateur 
    const handleUpdate = async (event) => {
        event.preventDefault();
        const id = reqId !== '' ? reqId : currentReqId;
        try{
            const response = await axios.get(`http://localhost:8000/api/display_new/${id}`);
            setTweets(response.data);
            console.log(response);
            
        }
        catch (error){
            console.error(error);
        }
    }


    const handleNext = () => {
        setStart(oldStart =>oldStart+5);
        setEnd(oldEnd=>oldEnd+5);
    }

    const handlePrevious = () => {
        setStart(oldStart => oldStart-5);
        setEnd(oldEnd => oldEnd-5);
    }


    //Affichage 
    return(
        <div className="FormsAndTweet">

            <form onSubmit={handleSubmit}>
                <SearchKeyWord keyword={keyword} setKeyword={setKeyword}/>
                <SearchBeginDate beginDate={beginDate} setBeginDate={setBeginDate}/>
                <SearchEndDate endDate={endDate} setEndDate={setEndDate}/>
                <SearchNumberTweet numberTweet={numberTweet} setNumberTweet={setNumberTweet}/> 
                <SubmitButton handleSubmit={handleSubmit} isLoading={isLoading}/> 
                <SearchReqId reqId={reqId} setReqId={setReqId}/>
                {/*On doit add la fonction handleUpdate si handleSubmit pressed
                Soit on utilise un useState de submitPressed,setSubmitPressed
                pour déterminer quand arrêter de faire la boucle de handleUpdate*/}
                
            </form>

            <div className = "TweetTable">
                <button onClick = {handlePrevious}>Previous</button>
                <button onClick = {handleNext}>Next</button>
                <button onClick={handleUpdate}>Update</button>

                <div className = "TableElement">
                    <table>
                        <thead>
                            <tr>
                                <th>Tweet</th>
                                <th>Views</th>
                                <th>Likes</th>
                                <th>Replies</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tweets.slice(start, end).map((tweet, index) => (
                                <tr key={index}>
                                    <td>{tweet.text_tweet}</td>
                                    <td>{tweet.nombre_views}</td>
                                    <td>{tweet.nombre_likes}</td>
                                    <td>{tweet.nombre_replies}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    );
}



export default SearchBar;