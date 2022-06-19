import DataVis from '../components/DataVis'

export default function EducationalActivity(props) {
    const { chartTypes } = props
    return (
        <div>
            <DataVis program="Educational Activity" chartTypes={chartTypes}/>
        </div>
    );
}