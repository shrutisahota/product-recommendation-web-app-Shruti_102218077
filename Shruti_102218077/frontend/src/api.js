const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function recommendByQuery(query, top_k=6) {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({query, top_k})
  });
  return res.json();
}

export async function getAnalytics() {
  const res = await fetch(`${API_BASE}/analytics`);
  return res.json();
}

export async function generateDescription({title, material, category, brand, tone='friendly'}) {
  const res = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({title, material, category, brand, tone})
  });
  return res.json();
}
