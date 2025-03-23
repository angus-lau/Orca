import orcaLogo from "./orcaLogo.png";
// import "bootstrap/dist/css/bootstrap.min.css";
// import React from "react";
import { FaUpload, FaArrowRight } from "react-icons/fa";
import { Link } from "react-router-dom";
import React, { useRef, useState } from "react";

export function PlaygroundPage() {
    const fileInputRef = useRef(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [promptText, setPromptText] = useState("");

    // Function to trigger the hidden file input when button is clicked
    const handleUploadClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    // Handler to do something with the selected file
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            // You can add further processing here, such as uploading the file to a server.
        }
    };

    // Handle prompt text change
    const handlePromptChange = (event) => {
        setPromptText(event.target.value);
    };

<<<<<<< HEAD
   // When arrow is pressed, ensure both a file and prompt exist before proceeding
   const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please upload a file.");
      return;
    }
    if (!promptText.trim()) {
      alert("Please enter a prompt.");
      return;
    }
    // MODIFIED, NEED TO RECHECK 
    const formData = new FormData();
    formData.append('file', selectedFile)
    formData.append('prompt', promptText);

    try {
        const response = await fetch('http://localhost:5001/process', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        console.log("✅ Response from server:", data);
        } catch (err) {
        console.error("❌ Error uploading to backend:", err);
    }
  };

    // Both file and prompt are provided. Process them.
    console.log("File:", selectedFile);
    console.log("Prompt:", promptText);
    // Call your submission function here
    // e.g., processSubmission(selectedFile, promptText);
  };
=======
    // When arrow is pressed, ensure both a file and prompt exist before proceeding
    const handleSubmit = () => {
        if (!selectedFile) {
            alert("Please upload a file.");
            return;
        }
        if (!promptText.trim()) {
            alert("Please enter a prompt.");
            return;
        }
        // Both file and prompt are provided. Process them.
        console.log("File:", selectedFile);
        console.log("Prompt:", promptText);
        // Call your submission function here
        // e.g., processSubmission(selectedFile, promptText);
    };
>>>>>>> eafe0de7f6e9e430c176db9152cec27d618adf30

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

            {/* Main Content */}
            <main className="flex-grow-1 d-flex flex-column">
                {/* Top Bar */}
                <header className="d-flex justify-content-end p-3 border-bottom">
                    <button className="btn btn-outline-dark">Account</button>
                </header>

                {/* Center Content */}
                <div className="d-flex flex-column align-items-center justify-content-center flex-grow-1">
                    <h1 className="mb-4">What Can I Help With?</h1>

                    {/* Search / Submission Bar */}
                    <div className="d-flex flex-column align-items-center w-100">
                        <div className="d-flex border rounded-pill overflow-hidden shadow-sm w-50">
                            {/* Upload button */}
                            <button
                                className="btn btn-light px-3"
                                onClick={handleUploadClick}
                            >
                                <FaUpload />
                            </button>

                            {/* Hidden file input */}
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: "none" }}
                                onChange={handleFileChange}
                            />

                            {/* Search Input */}
                            <input
                                type="text"
                                className="form-control border-0"
                                placeholder="Type something..."
                                value={promptText}
                                onChange={handlePromptChange}
                            />

                            {/* Arrow button */}
                            <button
                                className="btn btn-light px-3"
                                onClick={handleSubmit}
                            >
                                <FaArrowRight />
                            </button>
                        </div>

                        {/* File name bubble */}
                        {selectedFile && (
                            <div
                                className="mt-2 px-3 py-1 bg-secondary text-white rounded"
                                style={{ fontSize: "0.9rem" }}
                            >
                                {selectedFile.name}
                            </div>
                        )}
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
