import Toast from 'react-bootstrap/Toast';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons';

const ToastContainer = ({ message, showToast, onToastClose, type }) => {
    const messageMap = {
        success: {
            icon: <FontAwesomeIcon className='align-self-center' icon={faCheckCircle} color='green' />,
            text: 'Success!'
        },
        error: {
            icon: <FontAwesomeIcon className='align-self-center' icon={faTimesCircle} color='red' />,
            text: 'Error!'
        },
        warning: {
            icon: <FontAwesomeIcon className='align-self-center' icon={faTimesCircle} color='yellow' />,
            text: 'Warning!'
        }
    };
    if (!message) {
        return null;
    }
    return (<Toast
        style={{
            position: 'fixed',
            bottom: 20,
            right: 20,
        }}
        show={showToast}
        onClose={() => onToastClose({ showToast: false })}
        delay={5000}
        autohide
    >
        <Toast.Header>
            <div className='d-flex gap-2'>
                {messageMap[type].icon}
                <strong className="mr-auto">{messageMap[type].text}</strong>
            </div>
        </Toast.Header>
        <Toast.Body>{message}</Toast.Body>
    </Toast>
    );
}

export default ToastContainer;