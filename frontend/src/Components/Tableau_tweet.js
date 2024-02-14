import React, {useState} from 'react';
const TWEETS = [
    {
        content: "Ceci est le contenu du premier tweet",
        views: 100,
        likes: 50,
        replies: 20
    },
    {
        content: "Ceci est le contenu du deuxième tweet",
        views: 29400,
        likes: 100,
        replies: 50
    },
    // Ajoutez plus de tweets de test ici
    {
        content: "Ceci est le contenu du 3 tweet",
        views: 13100,
        likes: 550,
        replies: 2620
    },
    {
        content: "Ceci est le contenu du 4 tweet",
        views: 11500,
        likes: 550,
        replies: 220
    },
    {
        content: "Ceci est le contenu du 5 tweet",
        views: 100,
        likes: 550,
        replies: 220
    },
    {
        content: "Ceci est le contenu du 6 tweet",
        views: 11,
        likes: 550,
        replies: 220
    },
    {
        content: "Ceci est le contenu du 7 tweet",
        views: 1100,
        likes: 5,
        replies: 220
    },
    {
        content: "Ceci est le contenu du 8 tweet",
        views: 1100,
        likes: 550,
        replies: 220
    },

];

function TweetContent({tweets = TWEETS}){
    const [start,setStart] = useState(0);
    const [end,setEnd] = useState(5);

    const handleNext = () => {
        setStart(oldStart =>oldStart+5);
        setEnd(oldEnd=>oldEnd+5);
    }

    const handlePrevious = () => {
        setStart(oldStart => oldStart-5);
        setEnd(oldEnd => oldEnd-5);
    }



    return(
        <div className="TableauTweet">
            <button onClick = {handlePrevious}>Previous</button>
            <button onClick = {handleNext}>Next</button>
            <div>
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
    );
}

export default TweetContent;