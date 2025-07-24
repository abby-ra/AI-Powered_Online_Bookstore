// API utility for My Library and Save for Later

export async function addToLibrary(isbn) {
  const res = await fetch('http://localhost:5000/api/library', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ isbn })
  });
  return res.json();
}

export async function addToSaveForLater(isbn) {
  const res = await fetch('http://localhost:5000/api/save_for_later', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ isbn })
  });
  return res.json();
}

export async function getLibrary() {
  const res = await fetch('http://localhost:5000/api/library');
  return res.json();
}

export async function getSaveForLater() {
  const res = await fetch('http://localhost:5000/api/save_for_later');
  return res.json();
}
