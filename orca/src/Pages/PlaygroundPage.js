import orcaLogo from "./orcaLogo.png";
// import "bootstrap/dist/css/bootstrap.min.css";
// import React from "react";
import { FaUpload, FaArrowRight } from "react-icons/fa";
import { Link } from "react-router-dom";

export function PlaygroundPage() {
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
                    {/* <button className="btn btn-light text-start">Jobs</button> */}
                    <Link to="jobs" className="btn btn-light text-start">
                        Jobs
                    </Link>
                    <Link to="data" className="btn btn-light text-start">
                        Data
                    </Link>
                    <Link to="deploy" className="btn btn-light text-start">
                        Deploy
                    </Link>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-grow-1 d-flex flex-column">
                {/* Top Bar */}
                <header className="d-flex justify-content-end p-3 border-bottom">
                    <button className="btn btn-outline-dark">Account</button>
                </header>

                {/* Center Content */}
                <div className="d-flex flex-column align-items-center justify-content-center flex-grow-1">
                    <h1 className="mb-4">What Can I Help With?</h1>

                    {/* Search Bar */}
                    <div className="d-flex border rounded-pill overflow-hidden shadow-sm w-50">
                        {/* Upload button */}
                        <button className="btn btn-light px-3">
                            <FaUpload />
                        </button>

                        {/* Search Input */}
                        <input
                            type="text"
                            className="form-control border-0"
                            placeholder="Type something..."
                        />

                        {/* Arrow button */}
                        <button className="btn btn-light px-3">
                            <FaArrowRight />
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
}

// function App() {
//     return (
//         <div className="d-flex vh-100">
//             {/* Sidebar */}
//             <aside
//                 className="bg-light border-end p-3 d-flex flex-column"
//                 style={{ width: "250px" }}
//             >
//                 {/* Logo */}
//                 <div className="d-flex align-items-center mb-4">
//                     <img
//                         src={orcaLogo}
//                         alt="Orca Logo"
//                         className="me-2"
//                         width="80"
//                     />
//                     <h5 className="mb-0">ORCA</h5>
//                 </div>

//                 {/* Sidebar Menu */}
//                 <nav className="d-flex flex-column gap-2">
//                     <button className="btn btn-light text-start">Menu</button>
//                     <button className="btn btn-light text-start">Jobs</button>
//                     <button className="btn btn-light text-start">Data</button>
//                     <button className="btn btn-light text-start">Deploy</button>
//                 </nav>
//             </aside>

//             {/* Main Content */}
//             <main className="flex-grow-1 d-flex flex-column">
//                 {/* Top Bar */}
//                 <header className="d-flex justify-content-end p-3 border-bottom">
//                     <button className="btn btn-outline-dark">Account</button>
//                 </header>

//                 {/* Center Content */}
//                 <div className="d-flex flex-column align-items-center justify-content-center flex-grow-1">
//                     <h1 className="mb-4">What Can I Help With?</h1>

//                     {/* Search Bar */}
//                     <div className="d-flex border rounded-pill overflow-hidden shadow-sm w-50">
//                         {/* Upload button */}
//                         <button className="btn btn-light px-3">
//                             <FaUpload />
//                         </button>

//                         {/* Search Input */}
//                         <input
//                             type="text"
//                             className="form-control border-0"
//                             placeholder="Type something..."
//                         />

//                         {/* Arrow button */}
//                         <button className="btn btn-light px-3">
//                             <FaArrowRight />
//                         </button>
//                     </div>
//                 </div>
//             </main>
//         </div>
//     );
// }
