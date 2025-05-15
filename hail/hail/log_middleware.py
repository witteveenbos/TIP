from collections import deque
from fastapi import Request, Query
import re
from datetime import datetime
from typing import Dict, List, Optional, Callable
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

log_buffer = deque(maxlen=250)

TOP_LEVEL_FOLDER = Path(__file__).parent.parent

LOG_FOLDER = TOP_LEVEL_FOLDER / "logs"
LOG_FOLDER.mkdir(exist_ok=True)
LOG_FILE = LOG_FOLDER / "app.log"

TEMPLATE_FOLDER = Path(__file__).parent / "templates"

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)


def classify_log_line(line: str) -> Dict:
    line = line.strip()
    if re.search(r"\b(DEBUG|debug)\b", line):
        level = "debug"
    elif re.search(r"\b(INFO|info)\b", line):
        level = "info"
    elif re.search(r"\b(WARN|WARNING|warn|warning|Warning)\b", line):
        level = "warning"
    elif re.search(r"\b(ERROR|error|CRITICAL|critical)\b", line):
        level = "error"
    else:
        level = "debug"

    return {"level": level, "content": line}


class DualHandler(logging.Handler):
    def __init__(self, file_handler):
        super().__init__()
        self.file_handler = file_handler

    def emit(self, record):
        try:
            # Format the record
            msg = self.format(record)
            timestamp = datetime.fromtimestamp(record.created).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            # Add formatted log to buffer and file
            log_entry = f"{record.levelname} [{timestamp}] {msg}"
            log_buffer.append(log_entry)

            # Also send to file handler
            self.file_handler.emit(record)
        except Exception:
            self.handleError(record)


class LogMiddleware:
    def __init__(self, app):
        self.app = app
        # Set up logging
        self.setup_logging()

    def setup_logging(self):
        # Create rotating file handler (7 days of logs)
        file_handler = TimedRotatingFileHandler(
            LOG_FILE, when="D", interval=1, backupCount=7, encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
        )

        # Create our dual handler that writes to both file and memory
        dual_handler = DualHandler(file_handler)
        dual_handler.setFormatter(logging.Formatter("%(message)s"))

        # Get the root logger and add our handler
        root_logger = logging.getLogger()
        root_logger.addHandler(dual_handler)

        # Set level to DEBUG to capture all logs
        root_logger.setLevel(logging.DEBUG)

        # Also capture logs from other modules we care about
        for logger_name in ["uvicorn", "fastapi", "root", "hail"]:
            logger = logging.getLogger(logger_name)
            logger.addHandler(dual_handler)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Create a request object
        request = Request(scope)

        # Log the request
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"[{timestamp}] {request.method} {request.url.path}")

        try:
            # Process the request
            response = await self.app(scope, receive, send)
            return response
        except Exception as e:
            # Log any unhandled exceptions
            logging.error(f"Unhandled exception: {str(e)}")
            raise


def tail_file(filename: str, n: int) -> List[str]:
    """Return the last n lines of a file"""
    try:
        with open(filename, "r") as f:
            return list(deque(f, n))
    except FileNotFoundError:
        return []


async def get_logs(
    request: Request, lines: Optional[int] = Query(250, gt=0)
) -> HTMLResponse:
    """Get logs with optional number of lines parameter"""
    log_lines = tail_file(LOG_FILE, lines)
    formatted_logs = [classify_log_line(line) for line in log_lines]
    return templates.TemplateResponse(
        "logformatted.html",
        {"request": request, "logs": formatted_logs, "containers": []},
    )


async def download_logs(request: Request) -> FileResponse:
    """Download complete log file"""
    return FileResponse(LOG_FILE, media_type="text/plain", filename="application.log")
