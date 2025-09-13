function saveNote() {
  const note = document.getElementById('noteInput').value.trim();
  if (!note) return alert("Note can't be empty!");

  // Simulate saving note (replace with backend call)
  console.log("Note saved:", note);
  document.getElementById('noteInput').value = '';
  alert("Note saved successfully!");
}

function askQuery() {
  const query = document.getElementById('queryInput').value.trim();
  if (!query) return alert("Please enter a question!");

  // Simulate AI response (replace with backend call)
  const fakeResponse = `Here's a smart answer to: "${query}"`;

  document.getElementById('responseText').textContent = fakeResponse;
  document.getElementById('responseSection').classList.remove('hidden');
}