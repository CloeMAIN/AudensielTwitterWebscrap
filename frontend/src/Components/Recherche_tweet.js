import React, { useState } from 'react';
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

function SubmitButton({handleSubmit}){
    return(
        <button type="submit">Rechercher</button>
    );
}


function SearchBar(){
    // Definition fonction

    //Definition des variables d'état
    const [keyword, setKeyword] = useState('');
    const [beginDate, setBeginDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [tweets, setTweets] = useState([]);
    const [start,setStart] = useState(0);
    const [end,setEnd] = useState(5);




    let now = new Date();
    //Pour avoir l'id de la requête dans le même format que dans le backend
    let req_id = now.toISOString().slice(0,12);

    
    //Fonctions de soumission (va faire requete get_tweets par le biais url)
    const handleSubmit = async (event) => {
        event.preventDefault();
        now = new Date();
        // Effectuer la requête get_tweets avec keyword, beginDate et endDate
        try{
            const response = await axios.get(`http://localhost:8000/search/${keyword}/3A${beginDate}/3A${endDate}/`);
            console.log(response);
            // On pourrait ajouter un élement montrant que la requête a été effectuée
            // et un autre pour montrer que la requête est toujours en cours
            // On pourrait aussi ajouter un élement montrant que la requête est terminée
            // et un autre pour montrer que la requête a échoué
        } catch (error){
            console.error(error);
        }
    }

    //Faire tourner cela toutes les 20 secondes
    const handleUpdate = async (event) => {
        event.preventDefault();
        req_id = now.toISOString().slice(0,12);
        try{
            const response = await axios.get(`http://localhost:8000/search_new/${req_id}`);
            setTweets(response.data);
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
                <SubmitButton handleSubmit={handleSubmit}/> 
                {/*On doit add la fonction handleUpdate si handleSubmit pressed
                Soit on utilise un useState de submitPressed,setSubmitPressed
                pour déterminer quand arrêter de faire la boucle de handleUpdate*/}
            </form>

            <div className = "TweetTable">
                <button onClick = {handlePrevious}>Previous</button>
                <button onClick = {handleNext}>Next</button>
                <button onClick={handleUpdate}>Update</button>

                <div className = "TableElement">
                    {tweets.slice(start, end).map((tweet, index) => (
                        <div key={index}>
                            <p>{tweet.content}</p>
                            <p>Views: {tweet.views}</p>
                            <p>Likes: {tweet.likes}</p>
                            <p>Replies: {tweet.replies}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}



export default SearchBar;