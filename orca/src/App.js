import "./App.css";
//import orcaLogo from "orcasrcassetsorcaLogo.png";
import "bootstrap/dist/css/bootstrap.min.css";
import React from "react";
import { FaUpload, FaArrowRight } from "react-icons/fa";
import {
    HashRouter as Router,
    Routes,
    Route,
    useNavigate,
} from "react-router-dom";

//Page import
import { PlaygroundPage } from "./Pages/PlaygroundPage";
import { JobsPage } from "./Pages/JobsPage";
import { DataPage } from "./Pages/DataPage";
import { DeployPage } from "./Pages/DeployPage";

//Component import
import { Sidebar } from "./Components/Sidebar";

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

// function Sidebar() {
//     const navigate = useNavigate();

//     return (
//         <aside
//             className="bg-light border-end p-3 d-flex flex-column"
//             style={{ width: "250px" }}
//         >
//             <div className="d-flex align-items-center mb-4">
//                 <img
//                     src={orcaLogo}
//                     alt="Orca Logo"
//                     className="me-2"
//                     width="80"
//                 />
//                 <h5 className="mb-0">ORCA</h5>
//             </div>

//             <nav className="d-flex flex-column gap-2">
//                 <button
//                     className="btn btn-light text-start"
//                     onClick={() => navigate("/menu")}
//                 >
//                     Menu
//                 </button>
//                 <button
//                     className="btn btn-light text-start"
//                     onClick={() => navigate("/jobs")}
//                 >
//                     Jobs
//                 </button>
//                 <button
//                     className="btn btn-light text-start"
//                     onClick={() => navigate("/data")}
//                 >
//                     Data
//                 </button>
//                 <button
//                     className="btn btn-light text-start"
//                     onClick={() => navigate("/deploy")}
//                 >
//                     Deploy
//                 </button>
//             </nav>
//         </aside>
//     );
// }

// function Layout() {
//     return (
//         <div className="d-flex vh-100">
//             <Sidebar />

//             <main className="flex-grow-1 d-flex flex-column">
//                 <header className="d-flex justify-content-end p-3 border-bottom">
//                     <button className="btn btn-outline-dark">Account</button>
//                 </header>

//                 <div className="d-flex flex-column align-items-center justify-content-center flex-grow-1 p-4">
//                     <Routes>
//                         <Route path="/" element={<MenuPage />} />
//                         <Route path="/jobs" element={<JobsPage />} />
//                         <Route path="/data" element={<DataPage />} />
//                         <Route path="/deploy" element={<DeployPage />} />
//                         <Route path="*" element={<h2>Welcome to ORCA!</h2>} />
//                     </Routes>
//                 </div>
//             </main>
//         </div>
//     );
// }

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<PlaygroundPage />} />
                <Route path="/jobs" element={<JobsPage />} />
                <Route path="/data" element={<DataPage />} />
                <Route path="/deploy" element={<DeployPage />} />
            </Routes>
        </Router>
    );
}

export default App;
