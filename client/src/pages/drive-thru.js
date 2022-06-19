import DataVis from '../components/DataVis'

export default function DriveThru(props) {
    const { chartTypes } = props
    return (
        <div>
            <DataVis program="Drive Thru" chartTypes={chartTypes} />
        </div>
    );
}