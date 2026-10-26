import React from 'react'
export default function StatCard({label,value,icon,tone='blue',note}) {
  return <div className="stat-card"><div className={`stat-icon ${tone}`}>{icon}</div><div><p className="muted">{label}</p><strong>{value ?? '—'}</strong>{note && <small>{note}</small>}</div></div>
}
