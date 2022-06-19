import DataVis from '../components/DataVis'

export default function RentalAssistance(props) {
    const { chartTypes } = props
    return (
        <div>
            <DataVis program="Rental Assistance" chartTypes={chartTypes} />
        </div>
    );
}