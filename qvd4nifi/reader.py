"""
This module defines a minimal processor for reading QVD files.
"""

import io
import json
from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult

class ReadQvd(FlowFileTransform):
    """
    A minimal processor that reads the content of a QVD file and converts it to NDJSON format.
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
        description = "Reads the content of a QVD file and converts it to NDJSON format."
        tags = ["qvd", "qlik", "json", "convert", "qlikview", "qliksense"]
        dependencies = ["PyQvd==2.3.1"]

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

        def convert_value(value):
            if hasattr(value, "display_value"):
                return value.display_value
            return value

        output = io.StringIO()
        record_count = 0
        column_count = 0
        first_line = True

        tables = QvdTable.from_stream(stream, chunk_size=10000)

        for table in tables:
            column_count = len(table.columns)

            for row in table.data:
                record = {
                    col: convert_value(val)
                    for col, val in zip(table.columns, row)
                }

                if not first_line:
                    output.write("\n")

                output.write(json.dumps(record))

                first_line = False
                record_count += 1

        ndjson = output.getvalue()

        attributes = {
            "mime.type": "application/x-ndjson",
            "qvd.record.count": str(record_count),
            "qvd.columns.count": str(column_count)
        }

        return FlowFileTransformResult(
            relationship="success",
            contents=ndjson,
            attributes=attributes
        )
