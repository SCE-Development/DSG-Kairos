import DataVis from '../components/DataVis'

export default function Overview(props) {
    const {chartTypes} = props;
    return (
        <div>
            <DataVis program="Overview" chartTypes={chartTypes}/>
        </div>
    );
}