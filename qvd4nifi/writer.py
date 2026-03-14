"""
This module defines a minimal processor for writing QVD files from NDJSON input.
"""

import io
import json
from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult

class WriteQvd(FlowFileTransform):
    """
    Processor that converts NDJSON input into a QVD file.
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
        version = "0.1.0-dev.1"
        description = "Converts NDJSON input into a QVD file."
        tags = ["qvd", "qlik", "json", "convert", "qlikview", "qliksense"]
        dependencies = ["PyQvd==2.3.1"]

    def __init__(self, **kwargs):
        pass

    def transform(self, context, flowFile):
        """
        This method is called for each flow file that the processor receives.
        """
        # Lazy import
        # pylint: disable=import-outside-toplevel
        from pyqvd import QvdTable
        from pyqvd.io import QvdFileWriter

        input_stream = io.BytesIO(flowFile.getContentsAsBytes())
        text_stream = io.TextIOWrapper(input_stream, encoding="utf-8")

        columns = None
        data = []
        record_count = 0

        for line in text_stream:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)

            if columns is None:
                columns = list(obj.keys())

            row = [obj.get(col) for col in columns]
            data.append(row)

            record_count += 1

        if columns is None:
            raise ValueError("Input NDJSON contained no records")

        table = QvdTable.from_dict({
            "columns": columns,
            "data": data
        })

        output_stream = io.BytesIO()
        writer = QvdFileWriter(output_stream, table)
        writer.write()

        qvd_bytes = output_stream.getvalue()

        attributes = {
            "mime.type": "application/x-qvd",
            "qvd.record.count": str(record_count),
            "qvd.columns.count": str(len(columns))
        }

        return FlowFileTransformResult(
            relationship="success",
            contents=qvd_bytes,
            attributes=attributes
        )
