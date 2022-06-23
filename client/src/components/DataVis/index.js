import React from "react"
import "./styles.css"
import Navbar from "../Navbar"
import Tabbar from "../Tabbar"
import OTabbar from "../OTabbar"
import Graph from "../Graph"
import Table from "../Table"
import { useEffect, useState } from "react"

const DataVis = (props) => {
    const { program } = props
    const [mostPopularCategories, setMostPopularCategories] = useState();
    const [ageGroups, setAgeGroups] = useState();
    const [inactiveClients, setInactiveClients] = useState();

    useEffect(() => {
        // fetch('/get-active-clients').then(data => {
        //     setMostPopularCategories(data);
        // })
        fetch('/ageGroups').then(data => {
            setAgeGroups(data);
        })
        // fetch('/get-inactive-clients').then(data => {
        //     setInactiveClients(data);
        // })
    }, [])


    const chartTypes = {
        "most-popular-categories": ("bar", "data"),
        "client-frequency": ("bar", "data"),
        "most-active-users": ("bar", "data"),
        "consistent-client-dropping-off": ("bar", "data") // table?
    }

    return (
        <div>
            {console.log(chartTypes)}
            <div>
                <Navbar />
            </div>
            <div class="section-content">
                <div class="row">
                    {/* Side navigation */}
                    <div class="column large-3 doc-nav-container">
                        {program === "Overview" && <OTabbar />}
                        {program !== "Overview" && <Tabbar />}
                    </div>
                    {/* Main content */}
                    <div class="large-9 hig-content">
                        <h2 id="program">{program}</h2>
                        <div class="graph">
                            <Graph />
                        </div>
                        <div class="table">
                            <Table />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DataVis;
