import React from 'react'
import {Link} from 'react-router-dom'

function Header() {
    return (
        <div style={headerStyle}>
            <h1>Banking App</h1>
            <Link style={linkStyle} to="/">Home</Link> | <Link style={linkStyle} to="/about">About</Link>
        </div>
    )
}

const headerStyle = {
    position: 'sticky',
    top: '0',
    background: '#4285F4',
    color: '#fff',
    padding: '15px',
} as React.CSSProperties;

const linkStyle = {
    color: '#fff'
}


export default Header
