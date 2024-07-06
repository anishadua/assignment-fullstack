import React from 'react';

function DocumentViewer({ text }) {
    return (
        <div className="document-viewer">
            <pre>{text}</pre>
        </div>
    );
}

export default DocumentViewer;
