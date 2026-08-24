# ============================================================
# AgentX - Advanced Tracing & Observability
# Task 7
# File: observability/tracer.py
# ============================================================

import json
import time
import uuid
from datetime import datetime
from pathlib import Path


# ============================================================
# TRACE DIRECTORY
# ============================================================

TRACE_DIR = Path("observability/traces")
TRACE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# AGENT TRACER
# ============================================================

class AgentTracer:

    def __init__(self, task=""):

        self.trace_id = str(uuid.uuid4())

        self.task = task

        self.start_time = time.time()

        self.events = []

        self.tool_calls = 0

        self.errors = []

        self.total_latency = 0

        self.estimated_tokens = 0

        self.status = "running"

        self.record_event(
            event_type="trace_started",
            name="AgentX",
            data={
                "task": task
            }
        )


    # ========================================================
    # RECORD EVENT
    # ========================================================

    def record_event(
        self,
        event_type,
        name,
        data=None
    ):

        event = {

            "timestamp":
                datetime.now().isoformat(),

            "elapsed_seconds":
                round(
                    time.time()
                    - self.start_time,
                    4
                ),

            "event_type":
                event_type,

            "name":
                name,

            "data":
                data or {}
        }

        self.events.append(event)


    # ========================================================
    # AGENT / NODE START
    # ========================================================

    def agent_start(
        self,
        agent_name,
        prompt=None
    ):

        self.record_event(

            event_type="agent_start",

            name=agent_name,

            data={
                "prompt": prompt
            }
        )


    # ========================================================
    # AGENT / NODE END
    # ========================================================

    def agent_end(
        self,
        agent_name,
        output=None
    ):

        output_text = str(
            output or ""
        )

        # Rough token estimation
        estimated = max(
            1,
            len(output_text) // 4
        )

        self.estimated_tokens += estimated

        self.record_event(

            event_type="agent_end",

            name=agent_name,

            data={
                "output_preview":
                    output_text[:500],

                "estimated_tokens":
                    estimated
            }
        )


    # ========================================================
    # DECISION / ROUTING TRACE
    # ========================================================

    def decision(
        self,
        decision_name,
        decision_value,
        reason=""
    ):

        self.record_event(

            event_type="decision",

            name=decision_name,

            data={

                "decision":
                    decision_value,

                "reason":
                    reason
            }
        )


    # ========================================================
    # TOOL CALL TRACE
    # ========================================================

    def tool_start(
        self,
        tool_name,
        tool_input=None
    ):

        self.tool_calls += 1

        self.record_event(

            event_type="tool_start",

            name=tool_name,

            data={
                "input":
                    str(tool_input)[:500]
            }
        )


    def tool_end(
        self,
        tool_name,
        output=None,
        latency=None
    ):

        output_text = str(
            output or ""
        )

        estimated = max(
            1,
            len(output_text) // 4
        )

        self.estimated_tokens += estimated

        self.record_event(

            event_type="tool_end",

            name=tool_name,

            data={

                "output_preview":
                    output_text[:500],

                "latency_seconds":
                    latency,

                "estimated_tokens":
                    estimated
            }
        )


    # ========================================================
    # ERROR TRACE
    # ========================================================

    def error(
        self,
        component,
        error
    ):

        error_data = {

            "component":
                component,

            "error_type":
                type(error).__name__,

            "message":
                str(error)
        }

        self.errors.append(
            error_data
        )

        self.record_event(

            event_type="error",

            name=component,

            data=error_data
        )


    # ========================================================
    # METRIC TRACE
    # ========================================================

    def metric(
        self,
        metric_name,
        value
    ):

        self.record_event(

            event_type="metric",

            name=metric_name,

            data={
                "value": value
            }
        )


    # ========================================================
    # FINISH TRACE
    # ========================================================

    def finish(
        self,
        status="success"
    ):

        self.status = status

        self.total_latency = (
            time.time()
            - self.start_time
        )

        self.record_event(

            event_type="trace_finished",

            name="AgentX",

            data={

                "status":
                    status,

                "total_latency_seconds":
                    round(
                        self.total_latency,
                        4
                    ),

                "tool_calls":
                    self.tool_calls,

                "estimated_tokens":
                    self.estimated_tokens,

                "error_count":
                    len(self.errors)
            }
        )

        return self.save()


    # ========================================================
    # SAVE TRACE
    # ========================================================

    def save(self):

        trace_data = {

            "trace_id":
                self.trace_id,

            "task":
                self.task,

            "status":
                self.status,

            "summary": {

                "total_latency_seconds":
                    round(
                        self.total_latency,
                        4
                    ),

                "tool_calls":
                    self.tool_calls,

                "estimated_tokens":
                    self.estimated_tokens,

                "error_count":
                    len(self.errors)
            },

            "errors":
                self.errors,

            "events":
                self.events
        }

        filename = (
            f"trace_"
            f"{self.trace_id}.json"
        )

        file_path = (
            TRACE_DIR
            / filename
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                trace_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"📡 Trace saved: {file_path}"
        )

        return trace_data