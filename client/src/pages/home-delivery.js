import DataVis from '../components/DataVis'

export default function HomeDelivery(props) {
    const { chartTypes } = props
    return (
        <div>
            <DataVis program="Home Delivery" chartTypes={chartTypes} />
        </div>
    );
}