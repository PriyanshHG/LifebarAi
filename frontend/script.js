document.getElementById("foodForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const food = document.getElementById("foodInput").value;

  fetch("http://localhost:5000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ food })
  })
  .then(res => res.json())
  .then(data => {
    const impactText = data.impact > 0 ? `+${data.impact} mins` : `${data.impact} mins`;
    document.getElementById("result").innerHTML = `
      <h3>${data.food}</h3>
      <p>Calories: ${data.calories}</p>
      <p>Life Impact: ${impactText}</p>
    `;
  })
  .catch(err => {
    console.error(err);
    alert("Error analyzing food!");
  });
});
