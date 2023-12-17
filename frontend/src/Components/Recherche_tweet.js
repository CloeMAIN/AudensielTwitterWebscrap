import axios from 'axios';

function SearchKeyWord({keyword,setKeyord}){
    return(
        <form>
            <input type="mot" placeholder="Mot Clés"/>
        </form>
    );
}

function SearchBeginDate({beginDate,setBeginDate}){
    return(
        <form>
            <input type="date" placejolder="Début"/>
        </form>
    );
}


function SearchEndDate({endDate,setEndDate}){
    return(
        <form>
            <input type="date" placejolder="Fin"/>
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
    const now = new Date();
    const req_id = now.toISOString().slice(0,12);

    
    //Fonctions de soumission (va faire requete get_tweets par le biais url)
    const handleSubmit = async (event) => {
        event.preventDefault();
        now = new Date();
        // Effectuer la requête get_tweets avec keyword, beginDate et endDate
        try{
            const response = await axios.get(`search/${keyword}/${beginDate}/${endDate}`);
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
            const response = await axios.get(`search_new/${req_id}`);
        }
        catch (error){
            console.error(error);
        }
    }


    //Affichage 
    return(
    <form onSubmit={handleSubmit}>
        <SearchKeyWord keyword={keyword} setKeyword={setKeyword}/>
        <SearchBeginDate beginDate={beginDate} setBeginDate={setBeginDate}/>
        <SearchEndDate endDate={endDate} setEndDate={setEndDate}/> 
        <SubmitButton handleSubmit={handleSubmit}/> 
        {/*On doit add la fonction handleUpdate si handleSubmit pressed
        Soit on utilise un useState de submitPressed,setSubmitPressed
        pour déterminer quand arrêter de faire la boucle de handleUpdate*/}

    </form>
    );
}



export default SearchBar;