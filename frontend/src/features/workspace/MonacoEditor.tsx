"use client";

import React from "react";
import { Code2 } from "lucide-react";
import { useWorkspaceStore } from "@/store/useWorkspaceStore";

export function MonacoEditor() {
  const { generatedCode } = useWorkspaceStore();

  return (
    <div className="flex flex-col h-full bg-[#0b101d] border-r border-slate-800">
      <div className="flex h-10 items-center justify-between border-b border-slate-800 px-4 bg-slate-900/60">
        <span className="text-xs font-mono text-slate-300 flex items-center gap-2">
          <Code2 className="h-3.5 w-3.5 text-blue-400" /> Monaco Live Code Editor
        </span>
        <span className="text-xs text-emerald-400 font-semibold">FastAPI Clean Architecture</span>
      </div>
      <div className="flex-1 p-4 font-mono text-xs text-slate-300 overflow-y-auto leading-relaxed">
        <pre>{generatedCode}</pre>
      </div>
    </div>
  );
}
