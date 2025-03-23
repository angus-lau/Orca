import { Link } from "react-router-dom";
import orcaLogo from "./orcaLogo.png";

export function DataPage() {
    return (
        <div className="d-flex vh-100">
            {/* Sidebar */}
            <aside
                className="bg-light border-end p-3 d-flex flex-column"
                style={{ width: "250px" }}
            >
                {/* Logo */}
                <div className="d-flex align-items-center mb-4">
                    <img
                        src={orcaLogo}
                        alt="Orca Logo"
                        className="me-2"
                        width="80"
                    />
                    <h5 className="mb-0">ORCA</h5>
                </div>

                {/* Sidebar Menu */}
                <nav className="d-flex flex-column gap-2">
                    <h6>Menu</h6>
                    <Link to="/" className="btn btn-light text-start">
                        Home
                    </Link>
                    <Link to="/jobs" className="btn btn-light text-start">
                        Jobs
                    </Link>
                    <Link to="/data" className="btn btn-light text-start">
                        Data
                    </Link>
                    <Link to="/deploy" className="btn btn-light text-start">
                        Deploy
                    </Link>
                </nav>
            </aside>
        </div>
    );
}
