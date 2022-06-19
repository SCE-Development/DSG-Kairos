import "./styles.css"
import React, { useState } from 'react';

function OTabbar() {

    const onClick = (e) => {
        document.querySelectorAll('button').forEach(btn => {
            btn.classList.remove('active');
        })
        document.getElementById(e.target.id).classList.add('active');
    }

    return (
        <div class="tab-bar">
            <nav id="doc-nav" class="doc-nav" role="navigation">
                <ul class="side">
                    <li class="nav-overview">
                        <button class="btn active" id="popular-categories" onClick={onClick}>Most popular categories</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="active-users" onClick={onClick}>Most active users</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="age-groups" onClick={onClick}>Age groups</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="consistent-client" onClick={onClick}>Consistent client dropping off</button>
                    </li>
                </ul>
            </nav>
        </div >
    )
}

export default OTabbar