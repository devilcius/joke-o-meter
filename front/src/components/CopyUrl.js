import React from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShareAlt } from '@fortawesome/free-solid-svg-icons';

// renders a share icon button and shows a success message when the URL is copied to the clipboard
const CopyUrl = ({url, currentLanguage, textCopied}) => {
    
    const onCopy = (e) => {
        e.stopPropagation();        
        navigator.clipboard.writeText(url + '/share?lang=' + currentLanguage);
        textCopied();
    }

    return (
        <div>
            <button onClick={onCopy} className="btn btn-info share-url-button">
                <FontAwesomeIcon icon={faShareAlt} />
            </button>
        </div>
    );
};

export default CopyUrl;