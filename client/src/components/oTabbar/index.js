import "./styles.css"
import React, { useEffect, useState } from 'react';

function OTabbar({childToParent}) {
    const [ageGroups, setAgeGroups] = useState();
    const [mostActiveUsers, setmostActiveUsers] = useState();

    const chartTypes = {
        // "most-popular-categories": ("bar", "data"),
        "age-groups": ("bar", ageGroups),
        "most-active-users": ("bar", mostActiveUsers),
        "consistent-client-dropping-off": ("bar", "data") // table?
    }

    useEffect(() => {
        getAgeGroups();
        childToParent(chartTypes);
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
        childToParent(chartTypes);
    }

    return (
        <div class="tab-bar">
            <nav id="doc-nav" class="doc-nav" role="navigation">
                <ul class="side">
                    {/* <li class="nav-overview">
                        <button class="btn" id="popular-categories" onClick={onClick}>Most popular categories</button>
                    </li> */}
                    <li class="nav-overview">
                        <button class="btn active" id="age-groups" onClick={onClick}>Age groups</button>
                    </li>
                    <li class="nav-overview">
                        <button class="btn" id="active-users" onClick={onClick}>Most active users</button>
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