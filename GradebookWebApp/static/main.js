let method;
let baseURL = "http://localhost:5000";
let async = true;

const tableHeadings = { // object containing table headings
    enrolledTableHeadings: ["Name", "Instructor", "Time", "Enrollment"],
    addTableHeadings: ["Add or Remove", "Name", "Instructor", "Time", "Enrollment"],
    instructorCoursesHeadings: ["Name", "Instructor", "Time", "Enrollment"],
    courseGradebookHeadings: ["Student", "Grade"]
}

function updateCourseEnrollmentStatus(studentName, enrollOption, courseName) { // enrollOption = add or remove
    let xhttp3 = new XMLHttpRequest();

    method = "POST";
    let url = `${baseURL}/student/${studentName}`;

    xhttp3.open(method, url, true);
    xhttp3.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp3.send(`course_name=${courseName}&enroll_option=${enrollOption}`);
}

function generateHTML(tableData, headings, studentName) { // tableData = data from server, headings = table headings
    let headingsHTML = "";
    let tableBodyHTML = "";
    let tableRowLength;

    for (let i = 0; i < headings.length; i++) { // generate table headings
        headingsHTML += `<th>${headings[i]}</th>`; // add table headings to headingsHTML
    }

    for (let j = 0; j < tableData.length; j++) { // generate table body
        tableBodyHTML += "<tr>" // start of table row

        tableRowLength = Object.keys(tableData[j]).length;  // get number of keys in object

        let startingPosition = 0;

        if (headings === tableHeadings.addTableHeadings) { // if add table, add checkbox
            ++startingPosition; 

            let enrollOption = tableData[j].enrolled ? "Remove" : "Add"; // if enrolled, set enrollOption to remove, else set to add
            let courseName = tableData[j].name; // get course name

            tableBodyHTML += 
                `<td>
                    <button class="options-button" onclick="updateCourseEnrollmentStatus('${studentName}', '${enrollOption.toLowerCase()}', '${courseName}')">
                        ${enrollOption}
                    </button>
                </td>`;
        }

        for (let k = startingPosition; k < tableRowLength; k++) { // generate table data

            tableBodyHTML += `<td>${tableData[j][headings[k].toLowerCase()]}</td>`; // add table data to tableBodyHTML
        }

        tableBodyHTML += "</tr>"; // end of table row
    }

    return { // return headingsHTML and tableBodyHTML
        headingsHTML,
        tableBodyHTML
    };
}

function generateTable(headingType, dataFromServer, studentName) { // headingType = enrolled or add, dataFromServer = data from server
    let headingsRow = document.querySelector(".headings-row");
    let tableBody = document.querySelector(".data-table-body");

    let tableData = dataFromServer;

    switch (headingType) {  
        case ("enrolled"):
            tableHTML = generateHTML(tableData, tableHeadings.enrolledTableHeadings, studentName); // generate table headings and table body
            break;
        case ("add"):
            tableHTML = generateHTML(tableData, tableHeadings.addTableHeadings, studentName); // generate table headings and table body
            break;
    }

    headingsRow.innerHTML = tableHTML.headingsHTML; 
    tableBody.innerHTML = tableHTML.tableBodyHTML;
}


function getTable(nameOfTab, studentName) { // nameOfTab = enrolled or add, studentName = student name
    let enrolledTab = document.querySelector(".enrolled-tab");
    let addTab = document.querySelector(".add-tab");

    if (nameOfTab === "enrolled") { // if enrolled tab is clicked
        // change tab styling
        if (!enrolledTab.classList.contains("active-tab")) { // if enrolled tab is not active
            enrolledTab.classList.add("active-tab");
        }

        if (addTab.classList.contains("active-tab")) { // if add tab is active
            addTab.classList.remove("active-tab");
        }

        let xhttp = new XMLHttpRequest(); 
        method = "GET"; 
        let url = `${baseURL}/enrolled/${studentName}`; 
        xhttp.open(method, url, async);

        xhttp.onload = function () { // when data is received from server
            let enrolledData = JSON.parse(this.response);
            generateTable(nameOfTab, enrolledData, studentName);
        };

        xhttp.send();
    }

    else if (nameOfTab === "add") { // if add tab is clicked
        // change tab styling
        if (!addTab.classList.contains("active-tab")) { // if add tab is not active  
            addTab.classList.add("active-tab");
        }

        if (enrolledTab.classList.contains("active-tab")) {
            enrolledTab.classList.remove("active-tab");
        }

        let coursesData;
        let enrolledData;

        let xhttp1 = new XMLHttpRequest(); 
        let xhttp2 = new XMLHttpRequest();
        method = "GET"; 
        let url1 = `${baseURL}/enrolled/${studentName}`; 
        let url2 = `${baseURL}/courses`;

        xhttp1.open(method, url1, async); // 

        let enrolledCourses = [];

        xhttp1.onload = function () { // when data is received from server
            enrolledData = JSON.parse(this.response);

            for (let i = 0; i < enrolledData.length; i++) { // get enrolled courses
                enrolledCourses.push(enrolledData[i].name);
            }

            xhttp2.open(method, url2, async);

            xhttp2.onload = function () { 
                coursesData = JSON.parse(this.response);

                let isEnrolled = false;
                for (let i = 0; i < coursesData.length; i++) { // remove enrolled courses from coursesData
                    for (let j = 0; j < enrolledCourses.length; j++) { // check if course is enrolled
                        if (coursesData[i].name === enrolledCourses[j]) { // if course is enrolled
                            coursesData[i].enrolled = !isEnrolled; // set enrolled to true
                            break;
                        }
                        else {
                            coursesData[i].enrolled = isEnrolled; // set enrolled to false
                        }


                    }
                }

                generateTable(nameOfTab, coursesData, studentName); 
            }

            xhttp2.send();
        };

        xhttp1.send();
    }
}


// let govtname = '';

// //gives username and password to backend
// function auth(){
//     const username = document.getElementById("username").value;
//     const password = document.getElementById("password").value;
//     var xhttp = new XMLHttpRequest();
//     xhttp.open("POST", "http://127.0.0.1:5000/pyauth");
//     xhttp.setRequestHeader("Content-Type", "application/json");
//     const body = {"name": username, "password": password};
//     xhttp.send(JSON.stringify(body));
//     // xhttp.onload = function() {
//     //     govtname = this.responseText;
//     // };
// }

// //get student enrolled classes
// function enrolledTable(){
//     const name = govtname;
//     const xhttp = new XMLHttpRequest();
//     const method = "GET"; 
//     const url = "http://127.0.0.1:5000/enrolled/"+name;
//     const async = true;
//     xhttp.onload = function() {
//         document.getElementById("studentparagraph").innerHTML = this.responseText;
//         };
//     xhttp.open(method, url, async);
//     xhttp.send();
// }

// //shows all the classes
// function showAllTable(){
//     const xhttp = new XMLHttpRequest();
//     const method = "GET";  
//     const url = "http://127.0.0.1:5000/allclasses";
//     const async = true;
//     xhttp.onload = function() {
//         document.getElementById("studentparagraph").innerHTML = this.responseText;
//     };
//     xhttp.open(method, url, async);
//     xhttp.send();
// }

// //sign out takes you back to login and govtname is reset
// function signout(){
//     govtname = '';
//     window.location.href = "http://127.0.0.1:5000/";
// }

// //gets all the classes the instructors teaches
// function instructorClasses(){
//     const name = govtname;
//     const xhttp = new XMLHttpRequest();
//     const method = "GET"; 
//     const url = "http://127.0.0.1:5000/classesTaught/"+name;
//     const async = true;
//     xhttp.onload = function() {
//         document.getElementById("instructorparagraph").innerHTML = this.responseText;
//         };
//     xhttp.open(method, url, async);
//     xhttp.send();
// }

// // gets the specific details about the class thats clicked
// function specificCourse(classname){
//     //const classname = classname;
//     const xhttp = new XMLHttpRequest();
//     const method = "GET"; 
//     const url = "http://127.0.0.1:5000/specificCourse/"+classname;
//     const async = true;
//     xhttp.onload = function() {
//         document.getElementById("specific_course").innerHTML = this.responseText;
//         };
//     xhttp.open(method, url, async);
//     xhttp.send();
// }

// //editing grade in the specificCourse html//instructors gradebook
// function editGrade(){
//     const name = document.getElementById("????studentname????").value;//get name from td
//     const grade = document.getElementById("newgradeinput").value;//get grade from new grade input
//     var xhttp = new XMLHttpRequest();
//     xhttp.open("PUT", "http://127.0.0.1:5000/edit/"+name);
//     xhttp.setRequestHeader("Content-Type", "application/json");
//     // const body = {"name": name, "grade": grade};
//     const body = {"grade": grade};
//     xhttp.send(JSON.stringify(body));
//     // xhttp.onload = function() {
//     //     getname();
//     //     displayall();
//     // };
// }