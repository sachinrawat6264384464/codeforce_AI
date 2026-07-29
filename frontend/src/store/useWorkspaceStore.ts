import { create } from "zustand";
import { AgentStep } from "@/types";

interface WorkspaceState {
  currentPrompt: string;
  isGenerating: boolean;
  agentSteps: AgentStep[];
  generatedCode: string;
  setPrompt: (prompt: string) => void;
  setIsGenerating: (generating: boolean) => void;
  updateAgentStep: (step: AgentStep) => void;
  setGeneratedCode: (code: string) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  currentPrompt: "",
  isGenerating: false,
  agentSteps: [],
  generatedCode: "// Select or generate code to display in editor",
  setPrompt: (prompt) => set({ currentPrompt: prompt }),
  setIsGenerating: (generating) => set({ isGenerating: generating }),
  updateAgentStep: (step) =>
    set((state) => ({
      agentSteps: [
        ...state.agentSteps.filter((s) => s.agent_name !== step.agent_name),
        step,
      ],
    })),
  setGeneratedCode: (code) => set({ generatedCode: code }),
}));
