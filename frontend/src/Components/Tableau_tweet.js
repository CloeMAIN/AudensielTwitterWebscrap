import React, {useState} from 'react';


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
