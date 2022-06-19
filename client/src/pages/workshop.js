import DataVis from '../components/DataVis'

export default function Workshop(props) {
    const { chartTypes } = props
    return (
        <div>
            <DataVis program="Workshop" chartTypes={chartTypes} />
        </div>
    );
}