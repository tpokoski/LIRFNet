// Get the current date
let currentDate = new Date();

// Get the current month and year
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

// Get the months of the year
let months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

// Get the element that will display the month and year
let monthYear = document.getElementById("month-year");

// Get the element that will hold the calendar dates
let calendarDates = document.getElementById("calendar-dates");

// Get the previous and next buttons
let prevButton = document.getElementById("prev-month");
let nextButton = document.getElementById("next-month");

// Create the calendar
function createCalendar() {
  // Clear any existing dates
  calendarDates.innerHTML = "";

  // Create the first row of the calendar
  let firstRow = document.createElement("tr");

  // Get the first day of the month
  let firstDay = new Date(currentYear, currentMonth, 1);

  // Get the number of blank spaces before the first day of the month
  let blankSpaces = firstDay.getDay();

  // Add the blank spaces to the first row

  for (i = 0; i < blankSpaces; i++) {
    let blankSpace = document.createElement("td");
    firstRow.appendChild(blankSpace);
  }

  // Get the number of days in the current month
  let daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

  // Add the days of the month to the calendar
  for (i = 1; i <= daysInMonth; i++) {
    let date = document.createElement("td");
    date.innerHTML = i;

    // Add an event listener to each date
    date.addEventListener("click", function() {
      // Add code here to add a task or event to the selected date
    });

    firstRow.appendChild(date);

    // If the first row has 7 days, create a new row
    if (firstRow.childNodes.length === 7) {
      calendarDates.appendChild(firstRow);
      firstRow = document.createElement("tr");
    }
  }

  // Add the remaining days in the first row to the calendar
  calendarDates.appendChild(firstRow);

  // Update the month and year
  monthYear.innerHTML = months[currentMonth] + " " + currentYear;
};

// Go to the previous month
prevButton.addEventListener("click", function() {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  createCalendar();
});

// Go to the next month
nextButton.addEventListener("click", function() {
    currentMonth++;
    if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }
    createCalendar();
  });
  
  // Create the initial calendar
  createCalendar();



