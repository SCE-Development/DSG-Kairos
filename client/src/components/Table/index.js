import "./styles.css"

const Table = () => {
  return (
    <div>
      <table>
        <thead>
          <tr>
            <th class="column1" id="header1">DATE</th>
            <th class="column2" id="header2">ATTENDEES</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="column1">Jan</td>
            <td class="column2">25</td>
          </tr>
          <tr>
            <td class="column1">Feb</td>
            <td class="column2">50</td>
          </tr>
          <tr>
            <td class="column1">Mar</td>
            <td class="column2">130</td>
          </tr>
          <tr>
            <td class="column1">Apr</td>
            <td class="column2">115</td>
          </tr>
          <tr>
            <td class="column1">May</td>
            <td class="column2">94</td>
          </tr>
          <tr>
            <td class="column1">Jun</td>
            <td class="column2">10</td>
          </tr>
          <tr>
            <td class="column1">Jul</td>
            <td class="column2">82</td>
          </tr>
          <tr>
            <td class="column1">Aug</td>
            <td class="column2">74</td>
          </tr>
          <tr>
            <td class="column1">Sep</td>
            <td class="column2">128</td>
          </tr>
          <tr>
            <td class="column1">Oct</td>
            <td class="column2">100</td>
          </tr>
          <tr>
            <td class="column1">Nov</td>
            <td class="column2">111</td>
          </tr>
          <tr>
            <td class="column1">Dec</td>
            <td class="column2">64</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default Table