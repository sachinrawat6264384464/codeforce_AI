"use client";

import React from "react";
import { CheckCircle2, AlertTriangle, Clock } from "lucide-react";
import { useWorkspaceStore } from "@/store/useWorkspaceStore";

export function AgentTimeline() {
  const { agentSteps } = useWorkspaceStore();

  const defaultSteps = [
    { agent_name: "Planner Agent", status: "COMPLETED", output: "Requirements analyzed." },
    { agent_name: "Context Agent (DataHub)", status: "COMPLETED", output: "Metadata retrieved." },
    { agent_name: "Impact Analysis Agent", status: "COMPLETED", output: "No breaking changes detected." },
    { agent_name: "Backend Generator Agent", status: "RUNNING", output: "Generating FastAPI Routers." },
    { agent_name: "Code Review Agent", status: "PENDING", output: "Awaiting generation." },
  ];

  const displaySteps = agentSteps.length > 0 ? agentSteps : defaultSteps;

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-2 w-full">
      {displaySteps.map((step, idx) => (
        <div key={idx} className="rounded border border-slate-800 bg-slate-900/60 p-2.5 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="font-semibold text-slate-200">{step.agent_name}</span>
            {step.status === "COMPLETED" && <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />}
            {step.status === "RUNNING" && <Clock className="h-3.5 w-3.5 text-blue-400 animate-spin" />}
            {step.status === "PENDING" && <Clock className="h-3.5 w-3.5 text-slate-500" />}
            {step.status === "FAILED" && <AlertTriangle className="h-3.5 w-3.5 text-red-400" />}
          </div>
          <p className="text-[10px] text-slate-400 line-clamp-2">{step.output || "Processing..."}</p>
        </div>
      ))}
    </div>
  );
}
