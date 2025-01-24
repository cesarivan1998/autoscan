import {Link} from 'react-router-dom'

export function Navigation() {
    return (
        <div>
            <Link to="/brands">
                <h1>AutoSCAN</h1>
            </Link>
            <Link to="/brands-create">Create Brand</Link>
            <Link to="/cars-create">Create Car</Link>

        </div>
    )
}