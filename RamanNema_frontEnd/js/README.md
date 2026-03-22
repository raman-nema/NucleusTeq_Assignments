

Raman Nema | JS

## Student Performance Analyzer

## Overview / Description:
A  console-based  JavaScript  application  that  analyzes  student  performance  using
structured  data.  It  calculates  total  and  average  marks,  performs  subject-wise
analysis, assigns grades based on defined criteria, and identifies the class topper.
The  program  also  applies  validation  rules  such  as  minimum  subject  scores  and
attendance  requirements  to  determine  pass  or  fail  status,  providing  a  clear
summary of overall performance through terminal output.


## Features:
- Calculates total marks for each student

- Computes average marks with precision formatting

- Identifies subject-wise highest scores along with top-performing students

- Calculates subject-wise average performance across the class

- Determines the overall class topper based on total marks

- Implements a comprehensive grading system (A, B, C, Fail)

- Applies fail conditions based on:

    • Minimum subject score (≤ 40)
    • Attendance below 75%

- Provides detailed performance output directly in the console

- Uses a structured and scalable data model (array of student objects)


## Tech Stack:
• JavaScript (ES6)
• Node.js


## Project Structure:
```
RamanNema_frontEnd/
├── js/
│   ├── RamanNema_student_analyzer.js   # Main application logic
│   └── README.md
```


## How to run:
• Open terminal in the project folder
• Run:
    - node RamanNema_student_analyzer.js


## Data Structure:
The application uses an array of objects to represent student data.


1. Structure Overview

- The main variable, students, is an array.

- Each element in the array is a student object.

- Every student object contains:

- name → String (student’s name)

- marks → Array of subject objects

- attendance → Number (percentage)


2. Student Object Format

    {
        name: "Lalit",
        marks: [
            { subject: "Math", score: 100 },
            { subject: "English", score: 82 }
        ],
        attendance: 82
    }


3. Marks Structure

- marks is an array of objects.

- Each object represents a subject and its score:

- subject → Name of the subject

- score → Marks obtained


## Key Concepts Used
• Arrays & Objects

• Nested Data Structures

• Array Methods (forEach)

• Conditional Logic

• Aggregation (sum, average)

• Data Analysis Logic


## Output:
## Task 1: Total Marks for Each Student

# Expected Output Format:
    Lalit Total Marks: 391
    Rahul Total Marks: 423

# Logic:
- A dataset of students is defined, where each student contains subject-wise marks.

- A function printTotalMarks is created to calculate the total marks for each student.

- The logic iterates through each student using forEach.
•For  every  student,  it  loops  through  their  subject  mark  and  accumulates  total
score.

![image alt](https://github.com/raman-nema/NucleusTeq_Assignments/blob/3940887d256bf1a0a36b67953c17953ee8a796a0/RamanNema_frontEnd/js/ScreenShots/JS%201.png)

## Task 2: Average Marks for Each Student

# Expected Output Format:
    Lalit Average: 78.2
    Rahul Average: 84.6

# Logic:
- A function printAverages is defined to calculate the average marks of each student

- The program iterates through the students array using forEach.

- For each student:
    • Total marks are calculated by summing all subject scores.
    • The  average  is  computed  by  dividing  the  total  marks  by  the  number  of
subjects.
    • The result is formatted to one decimal place using .toFixed(1).
  
![image alt](https://github.com/raman-nema/NucleusTeq_Assignments/blob/3940887d256bf1a0a36b67953c17953ee8a796a0/RamanNema_frontEnd/js/ScreenShots/JS%202.png)

## Task 3: Subject-wise Highest Score in the Class

# Expected Output Format:
    Highest in Math: Rahul (90)
    Highest in English: Rahul (85)
    Highest in Science: Rahul (80)
    Highest in History: Rahul (76)
    Highest in Computer: Rahul (92)

#  Logic:
- A function is used to compute the highest marks for each subject.

- An object is maintained to store the highest score for every subject.

- The program iterates through each student and their marks.

- For each subject:
    • It checks if the subject is not yet recorded or if the current score is higher
than the stored score.
    • Updates the subject with the new highest score and student name
    • Finally, the results are printed subject-wise.

![image alt](https://github.com/raman-nema/NucleusTeq_Assignments/blob/3940887d256bf1a0a36b67953c17953ee8a796a0/RamanNema_frontEnd/js/ScreenShots/JS%203.png)

## Task 4: Subject-wise Average Score

# Expected Output Format:
    Average Math Score: 84
    Average English Score: 83.5
    Average Science Score: 77
    Average History Score: 72.5
    Average Computer Score: 90

# Logic:
- Two objects are used:
    • One to store total marks for each subject
    • One to store the count of entries per subject

- The program iterates through each student and their marks.

- For each subject:
    • If the subject is encountered for the first time, it is initialized
    • Marks are added to the total and count is incremented

- After processing all students:
    • The average for each subject is calculated
    • Results are formatted and displayed

![image alt](https://github.com/raman-nema/NucleusTeq_Assignments/blob/3940887d256bf1a0a36b67953c17953ee8a796a0/RamanNema_frontEnd/js/ScreenShots/JS%204.png)

## Task 5: Determine Overall Class Topper

# Expected Output Format:
    Class Topper: Rahul with 423 marks

# Logic:
- A function findClassTopper is defined to identify the top-performing student

- The program iterates through each student

- For every student:
    • Total marks are calculated by summing all subject scores
    • The total is compared with the current highest marks

- If a higher total is found:
    • The topper and highest marks are update

- After processing all students, the topper is displayed

![image alt](https://github.com/raman-nema/NucleusTeq_Assignments/blob/3940887d256bf1a0a36b67953c17953ee8a796a0/RamanNema_frontEnd/js/ScreenShots/JS%205.png)

## Task 6. Assign Grades to Students

# Expected Output Format:
    Lalit Grade: A
    Vikas Grade: B
    Rahul Grade: B
    Karan Grade: Fail (Low Attendance)
    Pooja Grade: B

# Logic:
- A function printGrades(students) is used to assign and display grades for each
student.

- The program iterates through each student in the dataset.

- For every student:
    • The total marks are calculated by summing all subject scores.
    • The average marks are computed based on the total.

- The program then checks fail conditions:
    • If attendance is below 75%, the student is marked as Fail (Low Attendance).
    • If any subject score is ≤ 40, the student is marked as Fail with the
respective subject.

- If the student passes all fail conditions:
    • Grades are assigned based on average marks:
        A. 85 and above → Grade A
        B.70 – 84 → Grade B
        C.50 – 69 → Grade C
        D.Below 50 → Fail

- The final grade for each student is displayed in the console.

![image alt](https://github.com/raman-nema/NucleusTeq_Assignments/blob/3940887d256bf1a0a36b67953c17953ee8a796a0/RamanNema_frontEnd/js/ScreenShots/JS%206.png)

