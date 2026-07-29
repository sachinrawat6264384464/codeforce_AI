"use client";

import React, { useState } from "react";
import { MonacoEditor } from "@/features/workspace/MonacoEditor";
import { MetadataViewer } from "@/features/datahub/MetadataViewer";
import { AgentTimeline } from "@/features/agents/AgentTimeline";
import { Bot, Play, Layers } from "lucide-react";

export default function WorkspaceIDPage({ params }: { params: { id: string } }) {
  const [prompt, setPrompt] = useState("");

  return (
    <div className="flex h-screen w-full flex-col bg-[#090d16] text-slate-200">
      {/* Header */}
      <header className="flex h-14 items-center justify-between border-b border-slate-800 bg-slate-950 px-4">
        <div className="flex items-center space-x-3">
          <span className="font-semibold text-lg text-white">ContextForge Workspace</span>
          <span className="text-xs text-slate-500 font-mono">Project ID: {params.id}</span>
        </div>
      </header>

      {/* Main split view */}
      <div className="flex flex-1 overflow-hidden">
        <aside className="w-64 border-r border-slate-800 bg-slate-950/50 p-3 hidden md:flex flex-col">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Layers className="h-3.5 w-3.5" /> Explorer
          </div>
          <div className="text-xs text-slate-400 font-mono space-y-1">
            <div className="bg-slate-800/60 p-1.5 rounded text-blue-400">app/main.py</div>
            <div className="p-1.5 hover:bg-slate-800/40 rounded">app/models/base.py</div>
            <div className="p-1.5 hover:bg-slate-800/40 rounded">app/api/v1/api.py</div>
          </div>
        </aside>

        <main className="flex flex-1 flex-col overflow-hidden">
          <div className="grid flex-1 grid-cols-1 lg:grid-cols-2 overflow-hidden border-b border-slate-800">
            <MonacoEditor />
            <MetadataViewer />
          </div>

          <div className="h-64 border-t border-slate-800 bg-slate-950 flex flex-col p-4">
            <div className="mb-3">
              <AgentTimeline />
            </div>

            <div className="flex items-center gap-2">
              <input
                type="text"
                placeholder="Ask ContextForge AI to build or refactor code with DataHub metadata..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="flex-1 rounded-md border border-slate-800 bg-slate-900 px-4 py-2 text-sm text-slate-100 placeholder-slate-500 focus:border-blue-500 focus:outline-none"
              />
              <button className="flex items-center gap-2 rounded-md bg-blue-600 px-5 py-2 text-sm font-medium text-white hover:bg-blue-500">
                <Play className="h-4 w-4 fill-white" /> Execute Pipeline
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
