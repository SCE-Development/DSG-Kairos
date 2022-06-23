import "./styles.css"
import React, { useState, useEffect } from 'react';

function Tabbar() {
    const [ageGroups, setAgeGroups] = useState();
    const [mostActiveUsers, setmostActiveUsers] = useState();
    // const [clientFrequency, setClientFrequency] = useState();

    useEffect(() => {
        getAgeGroups();
    }, [])

    const getAgeGroups = () => {
        fetch('/ageGroups').then(results => results.json())
        .then(data => {
            setAgeGroups(data);
            console.log(data);
        })
    }

    const getActiveClients = () => {
        fetch('/get-active-clients').then(results => results.json())
        .then(data => {
            setmostActiveUsers(data);
            console.log(data);
        })
    }

    // const getClientFrequency = () => {
    //     fetch('/get-client-frequency').then(results => results.json())
    //     .then(data => {
    //         setClientFrequency(data);
    //         console.log(data);
    //     })
    // }

    const onClick = (e) => {
        document.querySelectorAll('button').forEach(btn => {
            btn.classList.remove('active');
        })
        document.getElementById(e.target.id).classList.add('active');
        if (e.target.id === "age-groups") {
            getAgeGroups();
        }
        if (e.target.id === "active-users") {
            getActiveClients();
        }
    }

    return (
        <div class="tab-bar">
            <nav id="doc-nav" class="doc-nav" role="navigation">
                <ul class="side">
                    <li class="nav-overview">
                        <button class="btn active" id="age-groups" onClick={onClick}>Age groups</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="active-users" onClick={onClick}>Most active users</button>
                    </li>
                    {/* <li class="nav-overview">
                        <button class="btn" id="client-frequency" onClick={onClick}>Client frequency at events</button>
                    </li> */}
                </ul>
            </nav>
        </div >
    )
}

export default Tabbar