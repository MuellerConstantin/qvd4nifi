"""
This module defines a minimal processor for reading QVD files.
"""

import io
import json
from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult

class ReadQvd(FlowFileTransform):
    """
    A minimal processor that reads the content of a QVD file.
    """
    class Java:
        """
        This inner class is used to specify the Java interfaces that this processor implements.
        """
        implements = ["org.apache.nifi.python.processor.FlowFileTransform"]

    class ProcessorDetails:
        """
        This inner class is used to provide metadata about the processor.
        """
        version = "0.1.0"
        description = "Reads the content of a QVD file"
        tags = ["qvd", "qlik", "json", "convert", "qlikview", "qliksense"]
        dependencies = ["PyQvd==2.3.0"]

    def __init__(self, **kwargs):
        """
        Initialize the processor with any necessary configuration.
        """

    def transform(self, context, flowFile):
        """
        This method is called for each flow file that the processor receives.
        """
        # Lazy import so NiFi can install dependency first
        # pylint: disable=import-outside-toplevel
        from pyqvd import QvdTable

        stream = io.BytesIO(flowFile.getContentsAsBytes())
        table = QvdTable.from_stream(stream)

        def convert_value(value):
            if hasattr(value, "display_value"):
                return value.display_value
            return value

        lines = []

        for row in table.data:
            record = {
                col: convert_value(val)
                for col, val in zip(table.columns, row)
            }
            lines.append(json.dumps(record))

        ndjson = "\n".join(lines)

        attributes = {
            "mime.type": "application/x-ndjson",
            "qvd.record.count": str(len(table.data)),
            "qvd.columns.count": str(len(table.columns))
        }

        return FlowFileTransformResult(
            relationship="success",
            contents=ndjson,
            attributes=attributes
        )
