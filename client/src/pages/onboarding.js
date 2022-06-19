import DataVis from '../components/DataVis'

export default function Onboarding(props) {
    const {chartTypes} = props;
    return (
        <div>
            <DataVis program="Onboarding" chartTypes={chartTypes} />
        </div>
    );
}