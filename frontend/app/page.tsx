'use client';
import { useEffect, useState } from 'react';

type Patient = {
  patient_id: string;
  name: string;
  status: 'critical' | 'watch' | 'stable';
  note: string;
};

const statusColors = {
  critical: 'border-red-500 bg-red-50',
  watch: 'border-yellow-500 bg-yellow-50',
  stable: 'border-green-500 bg-green-50',
};

const statusBadge = {
  critical: 'bg-red-500 text-white',
  watch: 'bg-yellow-500 text-white',
  stable: 'bg-green-500 text-white',
};

export default function Home() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const es = new EventSource('http://localhost:8000/handoffs/stream');
    es.onmessage = (e) => {
      const patient = JSON.parse(e.data);
      setPatients((prev) => [...prev, patient]);
      setLoading(false);
    };
    es.onerror = () => es.close();
    return () => es.close();
  }, []);

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Rounding Copilot</h1>
      <p className="text-gray-500 mb-8">End-of-shift handoff dashboard</p>
      {loading && (
        <p className="text-gray-400 animate-pulse">Generating handoff notes...</p>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {patients.map((p) => (
          <div key={p.patient_id} className={`rounded-xl border-l-4 p-6 shadow-sm ${statusColors[p.status]}`}>
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-lg font-semibold text-gray-800">{p.name}</h2>
              <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase ${statusBadge[p.status]}`}>
                {p.status}
              </span>
            </div>
            <p className="text-sm text-gray-600 whitespace-pre-wrap">{p.note}</p>
          </div>
        ))}
      </div>
    </main>
  );
}