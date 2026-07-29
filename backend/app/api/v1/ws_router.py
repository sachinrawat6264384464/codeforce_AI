from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        if run_id not in self.active_connections:
            self.active_connections[run_id] = []
        self.active_connections[run_id].append(websocket)

    def disconnect(self, run_id: str, websocket: WebSocket):
        if run_id in self.active_connections:
            self.active_connections[run_id].remove(websocket)

    async def broadcast(self, run_id: str, message: dict):
        if run_id in self.active_connections:
            for connection in self.active_connections[run_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/projects/{project_id}/runs/{run_id}")
async def websocket_run_stream(websocket: WebSocket, project_id: str, run_id: str):
    await manager.connect(run_id, websocket)
    try:
        if not run_id.startswith("sync_"):
            # Stream live simulated steps
            steps = [
                {"step": "Planner Agent", "status": "running", "log": "Decomposing prompt into modules..."},
                {"step": "Planner Agent", "status": "done", "log": "Created module plan: Auth, Patients, Doctors, Billing."},
                {"step": "Context Agent (DataHub)", "status": "running", "log": "Retrieving schema context..."},
                {"step": "Context Agent (DataHub)", "status": "done", "log": "Matched users & patients schemas in DataHub GMS."},
                {"step": "Impact Analysis Agent", "status": "running", "log": "Evaluating downstream risk..."},
                {"step": "Impact Analysis Agent", "status": "done", "log": "Risk Score: MEDIUM. 2 APIs & 1 BI Dashboard affected."},
                {"step": "Approval Step", "status": "pending_approval", "log": "Awaiting human approval before file generation."}
            ]

            for step in steps:
                await manager.broadcast(run_id, step)
                await asyncio.sleep(0.5)

        while True:
            # Keep connection open for client messages
            data = await websocket.receive_text()
            payload = json.loads(data)
            if payload.get("action") == "approve":
                # Stream generation steps
                gen_steps = [
                    {"step": "Backend Generator", "status": "running", "log": "Writing FastAPI models, routers & Dockerfile to disk..."},
                    {"step": "Backend Generator", "status": "done", "log": "Generated 5 FastAPI files on disk."},
                    {"step": "Frontend Generator", "status": "running", "log": "Writing Next.js + Tailwind TSX pages to disk..."},
                    {"step": "Frontend Generator", "status": "done", "log": "Generated 2 TSX page stubs on disk."},
                    {"step": "Pipeline Completed", "status": "completed", "log": "All files generated successfully!"}
                ]
                for g_step in gen_steps:
                    await manager.broadcast(run_id, g_step)
                    await asyncio.sleep(0.6)

    except WebSocketDisconnect:
        manager.disconnect(run_id, websocket)
