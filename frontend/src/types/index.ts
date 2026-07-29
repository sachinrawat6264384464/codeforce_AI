export interface User {
  id: string;
  email: string;
  role: "ADMIN" | "DEVELOPER" | "VIEWER";
  is_active: boolean;
  created_at: string;
}

export interface Project {
  id: string;
  name: string;
  repository_url?: string;
  status: "ACTIVE" | "ARCHIVED";
  created_at: string;
}

export interface AgentStep {
  agent_name: string;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";
  output?: any;
  timestamp: string;
}
