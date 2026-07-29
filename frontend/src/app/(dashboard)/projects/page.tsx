"use client";

import React from "react";
import Link from "next/link";
import { FolderGit2, Plus, ArrowRight } from "lucide-react";

export default function ProjectsDashboardPage() {
  const projects = [
    { id: "1", name: "Hospital Management Backend", repo: "org/hospital-backend", status: "ACTIVE", date: "2026-07-24" },
    { id: "2", name: "Fintech EMI Banking Service", repo: "org/banking-emi", status: "ACTIVE", date: "2026-07-23" },
  ];

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-white">ContextForge Engineering Workspace</h1>
            <p className="text-xs text-slate-400">Select a project to start context-aware code generation</p>
          </div>
          <button className="flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500">
            <Plus className="h-4 w-4" /> New Project
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((p) => (
            <div key={p.id} className="rounded-lg border border-slate-800 bg-slate-950 p-5 flex flex-col justify-between hover:border-slate-700 transition-colors">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <FolderGit2 className="h-5 w-5 text-blue-400" />
                  <h3 className="font-semibold text-slate-200">{p.name}</h3>
                </div>
                <p className="text-xs font-mono text-slate-500 mb-4">{p.repo}</p>
              </div>
              <div className="flex items-center justify-between pt-4 border-t border-slate-900">
                <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded font-mono">
                  {p.status}
                </span>
                <Link 
                  href={`/workspace/${p.id}`}
                  className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 font-medium"
                >
                  Open Workspace <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
