import React, {useState, useEffect} from 'react'  

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/clients").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>     
      { (typeof data.clients === 'undefined') ? (
        <p>Loading...</p>
      ) : ( 
        data.clients.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )
      } 
    </div>
  );
}

export default App;
