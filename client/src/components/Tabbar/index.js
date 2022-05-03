import "./styles.css"
import React, { useState } from 'react';

function Tabbar(props) {

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
                        <button class="btn active" id="client-frequency" onClick={onClick}>Client frequency at events</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="active-users" onClick={onClick}>Most active users</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="age-groups" onClick={onClick}>Age groups</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="another-metric" onClick={onClick}>Popular Categories</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="one-more" onClick={onClick}>Client Drop-Off</button>
                    </li>
                </ul>
            </nav>
        </div >
    )
}

export default Tabbar