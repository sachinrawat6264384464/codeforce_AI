"use client";

import React from "react";
import { Database, AlertTriangle } from "lucide-react";

export function MetadataViewer() {
  return (
    <div className="flex flex-col gap-4 p-4 h-full bg-slate-950/40 overflow-y-auto">
      {/* DataHub Snapshot */}
      <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-4">
        <h3 className="flex items-center gap-2 font-medium text-slate-200 mb-2 text-sm">
          <Database className="h-4 w-4 text-blue-400" /> DataHub Metadata Graph
        </h3>
        <div className="text-xs text-slate-400 space-y-1.5 font-mono">
          <p><span className="text-slate-300 font-semibold">Matched Entities:</span> `users`, `projects`, `agent_runs`</p>
          <p><span className="text-slate-300 font-semibold">Ownership:</span> Platform Architecture (#core-platform)</p>
          <p><span className="text-slate-300 font-semibold">Domain:</span> Engineering & Automation</p>
          <p><span className="text-slate-300 font-semibold">Lineage:</span> PostgreSQL → DataHub MCP → LangGraph Agents</p>
        </div>
      </div>

      {/* Impact Analysis Warning Card */}
      <div className="rounded-lg border border-amber-500/30 bg-amber-950/20 p-4">
        <h3 className="flex items-center gap-2 font-medium text-amber-400 mb-1 text-sm">
          <AlertTriangle className="h-4 w-4" /> Downstream Impact Assessment
        </h3>
        <p className="text-xs text-amber-200/80 leading-relaxed">
          Risk Score: <span className="font-bold text-amber-300 uppercase">Low</span>. Schema additions will automatically generate non-breaking Alembic migrations.
        </p>
      </div>
    </div>
  );
}
