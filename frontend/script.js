// ===============================
// ResumeIntel Frontend
// ===============================


// ===============================
// GET ELEMENTS
// ===============================

const companyInput = document.getElementById("company");

const roleInput = document.getElementById("role");

const jobDescriptionInput =
    document.getElementById("job-description");

const resumeInput = document.getElementById("resume");

const uploadArea =
    document.querySelector(".upload-area");

const analyzeButton =
    document.getElementById("analyze-btn");

const resultsSection =
    document.getElementById("results");

const newAnalysisButton =
    document.getElementById("new-analysis-btn");

const navAnalyzeButton =
    document.getElementById("nav-analyze-btn");


// ===============================
// BACKEND URL
// ===============================

const API_URL = "http://localhost:8080";


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

    uploadText.textContent =
        file.name;

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
// UPDATE RESULTS
// ===============================

function updateResults(
    company,
    role,
    resume,
    data
) {

    // ===============================
    // TARGET INFORMATION
    // ===============================

    document.getElementById(
        "result-company"
    ).textContent = company;

    document.getElementById(
        "result-role"
    ).textContent = role;

    document.getElementById(
        "result-resume"
    ).textContent = resume.name;


    // ===============================
    // FIT SCORE
    // ===============================

    const fitScore =
        Number(data.fit_score) || 0;


    // ===============================
    // OVERALL SCORE
    // ===============================

    document.getElementById(
        "overall-score"
    ).textContent =
        Math.round(fitScore);


    // ===============================
    // JOB MATCH
    // ===============================

    document.getElementById(
        "match-score"
    ).textContent =
        fitScore.toFixed(2) + "%";

    document.getElementById(
        "match-progress"
    ).style.width =
        fitScore + "%";


    // ===============================
    // SKILLS MATCH
    // ===============================

    let skillsScore = 0;

    if (
        data.required_skills &&
        data.required_skills.length > 0
    ) {

        skillsScore =
            (
                data.matched_skills.length /
                data.required_skills.length
            ) * 100;
    }

    document.getElementById(
        "skills-score"
    ).textContent =
        skillsScore.toFixed(2) + "%";

    document.getElementById(
        "skills-progress"
    ).style.width =
        skillsScore + "%";


    // ===============================
    // ATS SCORE
    // ===============================

    // Backend currently does not
    // calculate a real ATS score.

    document.getElementById(
        "ats-score"
    ).textContent =
        "N/A";

    document.getElementById(
        "ats-progress"
    ).style.width =
        "0%";


    // ===============================
    // OVERALL MESSAGE
    // ===============================

    const overallMessage =
        document.getElementById(
            "overall-message"
        );

    if (fitScore >= 80) {

        overallMessage.textContent =
            "Your resume is a strong match for this position.";

    } else if (fitScore >= 60) {

        overallMessage.textContent =
            "Your resume is a moderate match. Some improvements could increase your chances.";

    } else {

        overallMessage.textContent =
            "Your resume needs improvement to better match this position.";
    }


    // ===============================
    // MISSING KEYWORDS
    // ===============================

    const keywordList =
        document.querySelector(".keyword-list");

    keywordList.innerHTML = "";


    if (
        data.missing_skills &&
        data.missing_skills.length > 0
    ) {

        data.missing_skills.forEach(
            function (skill) {

                const span =
                    document.createElement("span");

                span.textContent =
                    skill;

                keywordList.appendChild(span);
            }
        );

    } else {

        const span =
            document.createElement("span");

        span.textContent =
            "No missing skills 🎉";

        keywordList.appendChild(span);
    }


    // ===============================
    // RESUME STRENGTHS
    // ===============================

    const resultList =
        document.querySelector(".result-list");

    resultList.innerHTML = "";


    if (
        data.matched_skills &&
        data.matched_skills.length > 0
    ) {

        data.matched_skills.forEach(
            function (skill) {

                const li =
                    document.createElement("li");

                const check =
                    document.createElement("span");

                check.textContent = "✓";

                li.appendChild(check);

                li.appendChild(
                    document.createTextNode(
                        " Strong match in " + skill
                    )
                );

                resultList.appendChild(li);
            }
        );

    } else {

        const li =
            document.createElement("li");

        li.innerHTML =
            "<span>!</span> No matching skills found.";

        resultList.appendChild(li);
    }


    // ===============================
    // CIRCULAR OVERALL SCORE
    // ===============================

    const circumference = 327;

    const offset =
        circumference -
        (
            fitScore / 100
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
    async function () {

        const company =
            companyInput.value.trim();

        const role =
            roleInput.value.trim();

        const jobDescription =
            jobDescriptionInput.value.trim();

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
        // VALIDATE JOB DESCRIPTION
        // ===============================

        if (!jobDescription) {

            alert(
                "Please paste the job description."
            );

            jobDescriptionInput.focus();

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


        try {

            // ===============================
            // CREATE FORM DATA
            // ===============================

            const formData =
                new FormData();


            // Add resume

            formData.append(
                "resume",
                resume
            );


            // ===============================
            // JOB DESCRIPTION → TEXT FILE
            // ===============================

            const jobBlob =
                new Blob(
                    [jobDescription],
                    {
                        type: "text/plain"
                    }
                );


            formData.append(
                "job",
                jobBlob,
                "job_description.txt"
            );


            // ===============================
            // SEND REQUEST TO BACKEND
            // ===============================

            const response =
                await fetch(
                    `${API_URL}/full-analyze`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            // ===============================
            // READ BACKEND RESPONSE
            // ===============================

            const data =
                await response.json();
             console.log("BACKEND DATA:", data);

            // ===============================
            // HANDLE ERROR
            // ===============================

            if (!response.ok) {

                throw new Error(
                    data.message ||
                    "Analysis failed."
                );
            }


            // ===============================
            // UPDATE RESULTS
            // ===============================

            updateResults(
                company,
                role,
                resume,
                data
            );


            // ===============================
            // SUCCESS
            // ===============================

            analyzeButton.innerHTML =
                "Analysis Complete ✓";


            // Hide hero

            document.querySelector(
                ".hero"
            ).style.display =
                "none";


            // Show results

            resultsSection.classList.add(
                "active"
            );


            // Scroll to results

            resultsSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });


        } catch (error) {

            console.error(
                "Analysis Error:",
                error
            );
alert("Error: " + error.message);
            

            analyzeButton.disabled =
                false;

            analyzeButton.innerHTML =
                "Analyze Resume <span>→</span>";

            return;
        }


        // Enable button after success

        analyzeButton.disabled =
            false;
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

        jobDescriptionInput.value = "";

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

        analyzeButton.disabled =
            false;

        analyzeButton.innerHTML =
            "Analyze Resume <span>→</span>";


        // Scroll back

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });
    }
);


// ===============================
// UPLOAD AREA CLICK
// ===============================

uploadArea.addEventListener(
    "click",
    function (event) {

        if (event.target !== resumeInput) {

            resumeInput.click();
        }
    }
);


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