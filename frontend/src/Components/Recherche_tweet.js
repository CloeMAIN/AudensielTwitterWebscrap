

function SearchKeyWord({keyword}){
    return(
        <form>
            <input type="mot" placeholder="Mot Clés"/>
        </form>
    );
}

function SearchBeginDate({date}){
    return(
        <form>
            <input type="date" placejolder="Début"/>
        </form>
    );
}


function SearchEndDate({date}){
    return(
        <form>
            <input type="date" placejolder="Fin"/>
        </form>
    );
}

function SubmitButton({submit}){
    return(
        <button type="submit">Rechercher</button>
    );
}


function SearchBar({whole}){
    return(
    <tr>
        <td>
            <SearchKeyWord/>
        </td>
        <td>
            <SearchBeginDate/>
        </td>
        <td>
            <SearchEndDate/>
        </td>
        <td>
            <SubmitButton/>
        </td>
    </tr>
    );
}



export default SearchBar;