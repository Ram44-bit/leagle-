const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
async function request(path, options={}) {
  const res = await fetch(`${API}${path}`, options)
  if (!res.ok) {
    let msg = `Request failed (${res.status})`
    try { const data = await res.json(); msg = data.detail || msg } catch {}
    throw new Error(msg)
  }
  if (res.status === 204) return null
  return res.json()
}
export const api = {
  stats: () => request('/api/analytics/dashboard'),
  deadlines: () => request('/api/analytics/deadlines'),
  cases: (search='') => request(`/api/cases?search=${encodeURIComponent(search)}`),
  createCase: data => request('/api/cases', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)}),
  updateCase: (id,data) => request(`/api/cases/${id}`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)}),
  deleteCase: id => request(`/api/cases/${id}`, {method:'DELETE'}),
  tasks: () => request('/api/tasks'),
  createTask: data => request('/api/tasks', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)}),
  toggleTask: id => request(`/api/tasks/${id}/toggle`, {method:'PATCH'}),
  documents: () => request('/api/documents'),
  upload: (caseId,file) => { const f=new FormData(); f.append('case_id',caseId); f.append('file',file); return request('/api/documents',{method:'POST',body:f}) }
}
export const fileUrl = id => `${API}/api/documents/${id}/download`
