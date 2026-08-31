// ===============================
// ResumeIntel Frontend
// ===============================


// ===============================
// GET ELEMENTS
// ===============================

const companyInput = document.getElementById("company");

const roleInput = document.getElementById("role");

const resumeInput = document.getElementById("resume");

const uploadArea = document.querySelector(".upload-area");

const analyzeButton = document.getElementById("analyze-btn");

const resultsSection = document.getElementById("results");

const newAnalysisButton =
    document.getElementById("new-analysis-btn");

const navAnalyzeButton =
    document.getElementById("nav-analyze-btn");


// ===============================
// ALLOWED FILE TYPES
// ===============================

const allowedTypes = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
];


// ===============================
// HANDLE RESUME FILE
// ===============================

function handleResumeFile(file) {

    if (!file) {
        return;
    }


    if (!allowedTypes.includes(file.type)) {

        alert(
            "Please upload a PDF, DOC, or DOCX file."
        );

        resumeInput.value = "";

        return;
    }


    const uploadText =
        uploadArea.querySelector("strong");

    const uploadDescription =
        uploadArea.querySelector("p");


    uploadText.textContent = file.name;

    uploadDescription.textContent =
        "Resume selected successfully ✓";


    uploadArea.style.borderColor =
        "#635bff";

    uploadArea.style.background =
        "#f6f5ff";
}


// ===============================
// NORMAL FILE UPLOAD
// ===============================

resumeInput.addEventListener(
    "change",
    function () {

        const file = this.files[0];

        handleResumeFile(file);
    }
);


// ===============================
// DRAG OVER
// ===============================

uploadArea.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        uploadArea.style.borderColor =
            "#635bff";

        uploadArea.style.background =
            "#f6f5ff";
    }
);


// ===============================
// DRAG LEAVE
// ===============================

uploadArea.addEventListener(
    "dragleave",
    function () {

        uploadArea.style.borderColor =
            "#cdd2df";

        uploadArea.style.background =
            "#fafaff";
    }
);


// ===============================
// DROP
// ===============================

uploadArea.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();


        uploadArea.style.borderColor =
            "#cdd2df";

        uploadArea.style.background =
            "#fafaff";


        const file =
            event.dataTransfer.files[0];


        if (!file) {
            return;
        }


        if (!allowedTypes.includes(file.type)) {

            alert(
                "Please upload a PDF, DOC, or DOCX file."
            );

            return;
        }


        const dataTransfer =
            new DataTransfer();


        dataTransfer.items.add(file);


        resumeInput.files =
            dataTransfer.files;


        handleResumeFile(file);
    }
);


// ===============================
// MOCK ANALYSIS DATA
// ===============================
//
// This is ONLY for the frontend prototype.
//
// Later your backend response can replace
// this object.
//

const mockResults = {

    overall: 82,

    ats: 88,

    match: 79,

    skills: 84

};


// ===============================
// UPDATE RESULTS
// ===============================

function updateResults(
    company,
    role,
    resume
) {

    // Target information

    document.getElementById(
        "result-company"
    ).textContent = company;


    document.getElementById(
        "result-role"
    ).textContent = role;


    document.getElementById(
        "result-resume"
    ).textContent = resume.name;


    // Overall

    document.getElementById(
        "overall-score"
    ).textContent =
        mockResults.overall;


    // ATS

    document.getElementById(
        "ats-score"
    ).textContent =
        mockResults.ats + "%";


    // Job Match

    document.getElementById(
        "match-score"
    ).textContent =
        mockResults.match + "%";


    // Skills

    document.getElementById(
        "skills-score"
    ).textContent =
        mockResults.skills + "%";


    // Progress bars

    document.getElementById(
        "ats-progress"
    ).style.width =
        mockResults.ats + "%";


    document.getElementById(
        "match-progress"
    ).style.width =
        mockResults.match + "%";


    document.getElementById(
        "skills-progress"
    ).style.width =
        mockResults.skills + "%";


    // Circular overall score

    const circumference = 327;


    const offset =
        circumference -
        (
            mockResults.overall / 100
        ) * circumference;


    document.querySelector(
        ".score-progress"
    ).style.strokeDashoffset =
        offset;
}


// ===============================
// ANALYZE BUTTON
// ===============================

analyzeButton.addEventListener(
    "click",
    function () {


        const company =
            companyInput.value.trim();


        const role =
            roleInput.value.trim();


        const resume =
            resumeInput.files[0];


        // ===============================
        // VALIDATE COMPANY
        // ===============================

        if (!company) {

            alert(
                "Please enter the target company."
            );

            companyInput.focus();

            return;
        }


        // ===============================
        // VALIDATE ROLE
        // ===============================

        if (!role) {

            alert(
                "Please enter the target role."
            );

            roleInput.focus();

            return;
        }


        // ===============================
        // VALIDATE RESUME
        // ===============================

        if (!resume) {

            alert(
                "Please upload your resume."
            );

            return;
        }


        // ===============================
        // LOADING STATE
        // ===============================

        analyzeButton.disabled = true;


        analyzeButton.innerHTML =
            "Analyzing Resume <span>...</span>";


        // ===============================
        // FRONTEND DEMO DELAY
        // ===============================

        setTimeout(
            function () {


                // Update results

                updateResults(
                    company,
                    role,
                    resume
                );


                // Restore button

                analyzeButton.disabled =
                    false;


                analyzeButton.innerHTML =
                    "Analysis Complete ✓";


                // Hide landing hero

                document.querySelector(
                    ".hero"
                ).style.display =
                    "none";


                // Show results

                resultsSection.classList.add(
                    "active"
                );


                // Scroll to top of results

                resultsSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });


            },
            1500
        );
    }
);


// ===============================
// ANALYZE ANOTHER RESUME
// ===============================

newAnalysisButton.addEventListener(
    "click",
    function () {


        // Hide results

        resultsSection.classList.remove(
            "active"
        );


        // Show hero

        document.querySelector(
            ".hero"
        ).style.display =
            "block";


        // Reset inputs

        companyInput.value = "";

        roleInput.value = "";

        resumeInput.value = "";


        // Reset upload UI

        const uploadText =
            uploadArea.querySelector("strong");


        const uploadDescription =
            uploadArea.querySelector("p");


        uploadText.textContent =
            "Drop your resume here";


        uploadDescription.textContent =
            "PDF, DOC or DOCX";


        uploadArea.style.borderColor =
            "#cdd2df";


        uploadArea.style.background =
            "#fafaff";


        // Reset button

        analyzeButton.disabled = false;


        analyzeButton.innerHTML =
            "Analyze Resume <span>→</span>";


        // Scroll back

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });
    }
);

uploadArea.addEventListener("click", function (event) {

    if (event.target !== resumeInput) {
        resumeInput.click();
    }

});

// ===============================
// NAVBAR ANALYZE BUTTON
// ===============================

navAnalyzeButton.addEventListener(
    "click",
    function () {

        document.getElementById(
            "analyzer"
        ).scrollIntoView({

            behavior: "smooth",

            block: "center"

        });
    }
);