import React from "react";
import Toast from 'react-bootstrap/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faShareAlt } from '@fortawesome/free-solid-svg-icons';
import { useTranslation } from 'react-i18next';

// renders a share icon button and shows a success message when the URL is copied to the clipboard
const CopyUrl = ({url, currentLanguage}) => {
    const { t } = useTranslation();
    const [showToast, setShowToast] = React.useState(false);
    const message = t('toast.copy_url_success');
    const onToastClose = (e) => {
        // sanity check, it could be called on autohide
        if (e) {
            e.stopPropagation();
        }
        setShowToast(false);
    }
    
    const onCopy = (e) => {
        e.stopPropagation();        
        navigator.clipboard.writeText(url + '/share?lang=' + currentLanguage);
        setShowToast(true);
    }

    return (
        <div>
            <button onClick={onCopy} className="btn btn-info share-url-button">
                <FontAwesomeIcon icon={faShareAlt} />
            </button>
            <Toast
                style={{
                    position: 'fixed',
                    top: 'auto',
                    right: 20,
                }}
                show={showToast}
                onClose={onToastClose}
                delay={5000}
                autohide
            >
                <Toast.Header>
                    <div className='d-flex gap-2'>
                        <FontAwesomeIcon className='align-self-center' icon={faCheckCircle} color='green' />
                        <strong className="mr-auto">{t('toast.success')}</strong>
                    </div>
                </Toast.Header>
                <Toast.Body>{message}</Toast.Body>
            </Toast>
        </div>
    );
};

export default CopyUrl;