const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 78 },
      { subject: "English", score: 82 },
      { subject: "Science", score: 74 },
      { subject: "History", score: 69 },
      { subject: "Computer", score: 88 },
    ],
    attendance: 82,
  },
  {
    name: "Vikas",
    marks: [
      { subject: "Math", score: 72 },
      { subject: "English", score: 68 },
      { subject: "Science", score: 70 },
      { subject: "History", score: 66 },
      { subject: "Computer", score: 74 },
    ],
    attendance: 80,
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math", score: 90 },
      { subject: "English", score: 85 },
      { subject: "Science", score: 80 },
      { subject: "History", score: 76 },
      { subject: "Computer", score: 92 },
    ],
    attendance: 91,
  },
  {
    name: "Karan",
    marks: [
      { subject: "Math", score: 45 },
      { subject: "English", score: 50 },
      { subject: "Science", score: 48 },
      { subject: "History", score: 52 },
      { subject: "Computer", score: 55 },
    ],
    attendance: 60,
  },
  {
    name: "Pooja",
    marks: [
      { subject: "Math", score: 81 },
      { subject: "English", score: 79 },
      { subject: "Science", score: 83 },
      { subject: "History", score: 77 },
      { subject: "Computer", score: 85 },
    ],
    attendance: 88,
  },
];

// function to print total marks of each student
function printTotalMarks(students) {
  students.forEach(student => {
    let total = 0;

    // calculate total inside same function
    student.marks.forEach(m => {
      total += m.score;
    });

    console.log(`${student.name} Total Marks: ${total}`);
  });
}
// printTotalMarks(students);


// function to print average marks of each student
function printAverages(students) {
  students.forEach(student => {
    let total = 0;

    // calculate total marks
    student.marks.forEach(m => {
      total += m.score;
    });

    // calculate average
    const avg = (total / student.marks.length).toFixed(1);

    console.log(`${student.name} Average: ${avg}`);
  });
}
// printAverages(students);


// function to print highest marks in each subject
function printHighestBySubject(students) {
  const highest = {};

  students.forEach(student => {
    student.marks.forEach(mark => {

      if (!highest[mark.subject] || mark.score > highest[mark.subject].score) {
        highest[mark.subject] = {
          name: student.name,
          score: mark.score
        };
      }

    });
  });

  console.log("Subject-wise Highest Score in the Class");

  for (let subject in highest) {
    console.log(`Highest in ${subject}: ${highest[subject].name} (${highest[subject].score})`);
  }
}
// printHighestBySubject(students);

// function to print average marks in each subject
function printSubjectAverages(students) {
  const totals = {};
  const counts = {};

  students.forEach(student => {
    student.marks.forEach(mark => {

      // initialize if subject not present
      if (!totals[mark.subject]) {
        totals[mark.subject] = 0;
        counts[mark.subject] = 0;
      }

      totals[mark.subject] += mark.score;
      counts[mark.subject]++;

    });
  });

  console.log("Subject-wise Average Score");

  for (let subject in totals) {
    const avg = totals[subject] / counts[subject];
    console.log(`Average ${subject} Score: ${avg.toFixed(1)}`);
  }
}
// printSubjectAverages(students);

// function to find overall class topper
function findClassTopper(students) {
  let topper = null;
  let highestMarks = 0;

  students.forEach(student => {
    let total = 0;

    // calculate total marks
    student.marks.forEach(mark => {
      total += mark.score;
    });

    // check if current student has highest marks
    if (total > highestMarks) {
      highestMarks = total;
      topper = student.name;
    }
  });

  console.log(`Class Topper: ${topper} with ${highestMarks} marks`);
}
findClassTopper(students);



