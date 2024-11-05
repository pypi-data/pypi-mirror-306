import json
from typing import Any, Dict
import uuid
from nats.aio.msg import Msg


class EventMeta:
    """Class representing metadata for an event message.
    
    Attributes:
        trace_id (str): Unique identifier for tracing a request across services.
        span_id (str): Unique identifier for this specific operation within the trace.
        job_id (str): Identifier for the job associated with this event.
    """
    def __init__(self, meta_data: Dict):
        self.trace_id: str = meta_data.get("trace_id")
        self.job_id: str = meta_data.get("job_id")

        # generate a new span_id for each event
        self.span_id: str = str(uuid.uuid4())

    def to_dict(self) -> Dict:
        """Returns a dictionary representation of the event metadata."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "job_id": self.job_id,
        }


class PublishEventMessage:
    """Base class for creating standardized event messages to be published to message brokers.
    
    This class provides a consistent format for event messages with support for distributed
    tracing through trace_id and span_id. If trace_id or span_id are not provided in the
    input dictionary, they will be automatically generated using UUID4.
    
    Attributes:
        event_dict (Dict[str, Any]): Dictionary containing complete event data including:
            - event_name: Name of the event being published
            - payload: Event payload containing event-specific data
            - event_meta: Dictionary containing trace_id and span_id
    """

    def __init__(self, event_dict: Dict[str, Any]):
        """Initialize the message with a complete event dictionary.
        
        Args:
            event_dict: Dictionary containing event data in the format:
                {
                    "event_name": str,
                    "event_payload": dict,
                    "event_meta": {
                        "trace_id": str,
                        "span_id": str
                    }
                }
        """
        self.event_dict = event_dict
        self._validate_and_set_trace_ids()

    def _validate_and_set_trace_ids(self):
        """Validates and sets trace_id and span_id in the event dictionary.
        
        If event_meta section doesn't exist, creates it.
        If trace_id or span_id don't exist, generates them using UUID4.
        """
        # ensure event_meta dictionary exists
        if "event_meta" not in self.event_dict or not self.event_dict["event_meta"]["trace_id"]:
            raise Exception("Message metdata or trace_id not found.")

        # always generate a new job_id
        self.event_dict["event_meta"]["job_id"] = str(uuid.uuid4())

    def to_dict(self) -> dict:
        """Convert the event to a dictionary format"""
        return self.event_dict

    def to_json(self) -> str:
        """Convert the event to a JSON string"""
        return json.dumps(self.event_dict)


class EventMessage:
    """Base class for handling received event messages from message brokers.
    
    This class provides a standardized way to parse and access event message data
    regardless of the message broker source.
    
    Attributes:
        raw_message (dict): The original raw message received.
        event_name (str): Name of the received event.
        event_payload (dict): Event payload containing event-specific data.
        event_meta (EventMeta): Metadata object including trace_id and span_id.
    """
    def __init__(self, raw_message: dict):
        self.raw_message = raw_message
        self.event_name = raw_message.get("event_name")

        # event payload will contain entity_id, connector_id and other info
        # needed for specific events
        self.event_payload: dict = raw_message.get("event_payload", {})

        # initialize EventMeta object
        self.event_meta = EventMeta(raw_message.get("event_meta", {}))

        # update raw message to include generated span_id
        self.raw_message["event_meta"] = self.event_meta.to_dict()


class NATSEventMessage(EventMessage):
    """Handler for event messages received from NATS message broker.
    
    This class extends EventMessage to handle NATS-specific message format
    and provides access to the original NATS message object.
    
    Attributes:
        message_object (Msg): Original NATS message object
    """
    def __init__(self, message_object: Msg):
        # decode message data from NATs and parse it as JSON
        event_data: dict = json.loads(message_object.data.decode())
        super().__init__(event_data)
        self.message_object = message_object


class AWSEventMessage(EventMessage):
    """Handler for event messages received from AWS SQS.
    
    This class extends EventMessage to handle AWS SQS-specific message format
    and provides access to the SQS receipt handle for message acknowledgment.
    
    Attributes:
        receipt_handle (str): SQS receipt handle used for message acknowledgment
    """
    def __init__(self, raw_message: dict):
        sqs_message_body: dict = json.loads(raw_message.get("Body", "{}"))
        super().__init__(sqs_message_body.get("detail"))
        self.receipt_handle = raw_message.get("ReceiptHandle")
