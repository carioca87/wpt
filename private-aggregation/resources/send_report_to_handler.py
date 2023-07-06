"""Methods for the report-protected-audience endpoints which only support
operation read and write defined in parameters."""
import json
from typing import List, Tuple

from wptserve.request import Request

Header = Tuple[str, str]
Status = Tuple[int, str]
ResponseTuple = Tuple[Status, List[Header], str]

def main(request: Request, response: ResponseTuple) -> ResponseTuple:
    operation = request.GET.first(b"operation").decode('utf-8')
    uuid = request.GET.first(b"uuid").decode('utf-8')

    if operation == "read":
        with request.server.stash.lock:
            report = request.server.stash.take(key=uuid)
            request.server.stash.put(key=uuid, value=report)

            return 200, [("Content-Type", "application/json")], json.dumps(report)
    elif operation == "write":
        report = request.GET.first(b"report").decode('utf-8')
        if report is None:
            return 400, [("Content-Type", "application/json")], json.dumps({'error': 'Missing report.', 'uuid': uuid})

        with request.server.stash.lock:
            request.server.stash.put(key=uuid, value=report)

        return 200, [("Content-Type", "application/json")], json.dumps({'Recorded report' + uuid})
    else:
        return 400, [("Content-Type", "application/json")], json.dumps({'error': 'Invalid operation.', 'uuid': uuid})
