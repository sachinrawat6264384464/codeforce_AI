import React from "react";

export function 1. analyze datahub metadataTable({ items }: { items: any[] }) {
  return (
    <table className="w-full text-left text-xs text-slate-300">
      <thead className="bg-slate-800 text-slate-400 font-mono">
        <tr>
          <th className="p-2">ID</th>
          <th className="p-2">Name</th>
          <th className="p-2">Status</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item, idx) => (
          <tr key={idx} className="border-b border-slate-800">
            <td className="p-2">{item.id}</td>
            <td className="p-2 font-medium text-white">{item.name}</td>
            <td className="p-2 text-emerald-400">{item.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
