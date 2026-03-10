from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult

class DummyProcessor(FlowFileTransform):
    """
    A minimal test processor that transforms the content of a flow file to a static string.
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
        description = "Minimal dummy processor for testing purposes."

    def __init__(self, **kwargs):
        pass

    def transform(self, context, flowfile):
        """
        This method is called for each flow file that the processor receives.
        It transforms the content of the flow file to a static string.
        """
        return FlowFileTransformResult(
            relationship="success",
            contents="0xCAFEBABE"
        )
