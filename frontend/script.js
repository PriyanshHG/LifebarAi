document.getElementById("foodForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const food = document.getElementById("foodInput").value;

  fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ food })
  })
  .then(res => res.json())
  .then(data => {
    const impactText = data.impact > 0 ? `+${data.impact} mins` : `${data.impact} mins`;
    document.getElementById("result").innerHTML = `
      <h2>🍽️ ${data.food}</h2>
      <p>Calories: ${data.calories}</p>
      <p>Life Impact: <strong>${impactText}</strong></p>
      <p>${data.message}</p>
    `;
  })
  .catch(err => {
    console.error(err);
    alert("Error analyzing food!");
  });
});

function previewImage(event) {
  const reader = new FileReader();
  reader.onload = function() {
    const output = document.getElementById("preview");
    output.src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
}
