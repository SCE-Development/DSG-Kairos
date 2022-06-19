import DataVis from '../components/DataVis'

export default function Scholarship(props) {
    const { chartTypes } = props
    return (
        <div>
            <DataVis program="Scholarship" chartTypes={chartTypes} />
        </div>
    );
}