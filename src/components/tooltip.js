import React from 'react';
import { Button, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { InfoCircle,InfoCircleFill,InfoSquare, InfoSquareFill } from 'react-bootstrap-icons'; // Example Bootstrap icon

const IconButton = ({ tooltips , keyName}) => {
    return (
        
        <OverlayTrigger
            placement="left"
            overlay={<Tooltip id={`button-tooltip-${keyName}`} className='custom-tooltip'>{tooltips[keyName]}</Tooltip>}
        >
            <Button variant="outline-primary" className="icon-button">
                <InfoCircleFill />
            </Button>
        </OverlayTrigger>
    );
};

export default IconButton;
