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


printTotalMarks(students);