"""
Model for interactions to be sent to the interactions service.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer, ConfigDict


class Surface(str, Enum):
    SLACK = "Slack"
    WEB = "NoraWebapp"


class Annotation(BaseModel):
    # Need this config to stringify numeric values in attributes.
    # Otherwise, we'll get 'Input should be a valid string' error.
    model_config = ConfigDict(coerce_numbers_to_str=True)

    tag: str
    span: Tuple[int, int]
    attributes: Optional[Dict[str, str]] = None


class AnnotationBatch(BaseModel):
    actor_id: UUID
    message_id: str
    annotations: List[Annotation]

    @field_serializer("actor_id")
    def serialize_actor_id(self, actor_id: UUID):
        return str(actor_id)


class Message(BaseModel):
    message_id: str
    actor_id: UUID
    text: str
    thread_id: str
    channel_id: str
    surface: Surface
    ts: datetime
    annotations: List[Annotation] = Field(default_factory=list)

    @field_serializer("actor_id")
    def serialize_actor_id(self, actor_id: UUID):
        return str(actor_id)

    @field_serializer("ts")
    def serialize_ts(self, ts: datetime):
        return ts.isoformat()

    @staticmethod
    def from_returned_message(message: "ReturnedMessage") -> "Message":
        if message.message_id is None:
            raise ValueError("Message ID is required")
        if message.thread_id is None:
            raise ValueError("Thread ID is required")
        if message.channel_id is None:
            raise ValueError("Channel ID is required")
        if message.surface is None:
            raise ValueError("Surface is required")
        return Message(
            message_id=message.message_id,
            actor_id=message.actor_id,
            text=message.text,
            thread_id=message.thread_id,
            channel_id=message.channel_id,
            surface=message.surface,
            ts=message.ts,
            annotations=message.annotations,
        )


class Event(BaseModel):
    """event object to be sent to the interactions service; requires association with a message, thread or channel id"""

    type: str
    actor_id: UUID = Field(
        description="identifies actor writing the event to the interaction service"
    )
    timestamp: datetime
    text: Optional[str] = None
    data: dict = Field(default_factory=dict)
    message_id: Optional[str] = None
    thread_id: Optional[str] = None
    channel_id: Optional[str] = None

    @field_serializer("actor_id")
    def serialize_actor_id(self, actor_id: UUID):
        return str(actor_id)

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: datetime):
        return timestamp.isoformat()

    @staticmethod
    def from_returned_event(event: "ReturnedEvent") -> "Event":
        if event.channel_id is None:
            raise ValueError("Channel ID is required")
        elif event.thread_id is None and event.message_id is not None:
            raise ValueError("Thread ID is required if Message ID is present")
        return Event(
            type=event.type,
            actor_id=event.actor_id,
            timestamp=event.timestamp,
            text=event.text,
            data=event.data,
            message_id=event.message_id,
            thread_id=event.thread_id,
            channel_id=event.channel_id,
        )


class EventType(Enum):
    """Enumeration of event types"""

    STEP_COST = "step_cost"
    STEP_PROGRESS = "step_progress"


class Thread(BaseModel):
    thread_id: str
    channel_id: str
    surface: Surface


class ReturnedEvent(BaseModel):
    """Event format returned by the interaction service"""

    event_id: str
    type: str
    actor_id: UUID = Field(
        description="identifies actor writing the event to the interaction service"
    )
    timestamp: datetime
    text: Optional[str] = None
    data: dict = Field(default_factory=dict)
    message_id: Optional[str] = None
    thread_id: Optional[str] = None
    channel_id: Optional[str] = None
    surface: Optional[Surface] = None

    @field_serializer("actor_id")
    def serialize_actor_id(self, actor_id: UUID):
        return str(actor_id)

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: datetime):
        return timestamp.isoformat()


class ReturnedMessage(BaseModel):
    """Message format returned by interaction service"""

    actor_id: UUID
    text: str
    ts: datetime
    message_id: Optional[str] = None
    annotated_text: Optional[str] = None
    events: List[Event] = Field(default_factory=list)
    preceding_messages: List["ReturnedMessage"] = Field(default_factory=list)
    thread_id: Optional[str] = None
    channel_id: Optional[str] = None
    surface: Optional[Surface] = None
    annotations: List[Annotation] = Field(default_factory=list)

    @classmethod
    def from_event(cls, event: Event) -> "ReturnedMessage":
        """Convert an event to a message"""
        return ReturnedMessage(
            actor_id=event.actor_id,
            text=json.dumps(event.data),
            ts=event.timestamp,
            message_id=event.message_id,
        )


class AgentMessageData(BaseModel):
    """capture requests to and responses from tools within Events"""

    message_data: dict  # dict of agent/tool request/response format
    data_sender_actor_id: Optional[str] = None  # agent sending the data
    virtual_thread_id: Optional[str] = None  # tool-provided thread
    tool_call_id: Optional[str] = None  # llm-provided thread
    tool_name: Optional[str] = None  # llm identifier for tool


class ReturnedAgentContextEvent(BaseModel):
    """Event format returned by interaction service for agent context events"""

    actor_id: UUID  # agent that saved this context
    timestamp: datetime
    data: AgentMessageData
    type: str


class ReturnedAgentContextMessage(BaseModel):
    """Message format returned by interaction service for search by thread"""

    message_id: str
    actor_id: UUID
    text: str
    ts: str
    annotated_text: Optional[str] = None
    events: List[ReturnedAgentContextEvent] = Field(default_factory=list)


class ThreadRelationsResponse(BaseModel):
    """Thread format returned by interaction service for thread relations in a search response"""

    thread_id: str
    events: List[Event] = Field(
        default_factory=list
    )  # events associated only with the thread
    messages: List[ReturnedMessage] = Field(
        default_factory=list
    )  # includes events associated with each message


class VirtualThread:
    """Virtuals threads are an event type used to sub-divide a thread into sb-conversations"""

    # The type of event that represetns a virtual thread
    EVENT_TYPE = "virtual_thread"

    # Data field in the event that contains the ID of the virtual thread id
    ID_FIELD = "virtual_thread_id"

    # Data field in the event that contains the type of other events in the virtual thread
    EVENT_TYPE_FIELD = "event_type"


class CostDetail(BaseModel):
    """
    Base class to store details of cost to service a request by an agent.
    If an agent has different cost details,
    it should create another class inheriting this class and add those fields.
    See LLMCost and LLMTokenBreakdown below for examples.
    """

    model_config = ConfigDict(protected_namespaces=())
    pass


class LLMCost(CostDetail):
    """LLM cost detail"""

    token_count: int
    model_name: str


class LLMTokenBreakdown(CostDetail):
    """Token usage breakdown"""

    prompt_tokens: int
    completion_tokens: int


class LangChainRun(CostDetail):
    """LangChain Run"""

    # Subset of run fields which allow future lookup of run details.
    run_id: UUID
    run_name: Optional[str] = None
    trace_id: Optional[UUID] = None
    session_name: Optional[str] = None  # Alias: project_name
    session_id: Optional[UUID] = None  # Alias: project_id

    # Serialize the UUIDs as strings
    @field_serializer("run_id")
    def serialize_id(self, run_id: UUID):
        return str(run_id)

    @field_serializer("trace_id")
    def serialize_trace_id(self, trace_id: UUID):
        return str(trace_id)

    @field_serializer("session_id")
    def serialize_session_id(self, session_id: UUID):
        return str(session_id)


class ServiceCost(BaseModel):
    """Cost of servicing a request by an agent"""

    dollar_cost: float
    service_provider: Optional[str] = Field(
        default=None, description="For example, OpenAI/Anthropic/Modal/Cohere"
    )
    description: Optional[str] = Field(
        default=None, description="Describe the function within the agent"
    )
    tool_name: Optional[str] = Field(default=None, description="For example, PaperQA")
    task_id: Optional[str] = Field(
        default=None,
        description="Agent generated task_id used to track nora assigned tasks",
    )
    tool_call_id: Optional[str] = None
    details: List[CostDetail] = []


class StepCost(BaseModel):
    """Wrapping service cost with event metadata so that it can be converted to an Event object."""

    actor_id: UUID
    message_id: str
    service_cost: ServiceCost

    @field_serializer("actor_id")
    def serialize_actor_id(self, actor_id: UUID):
        return str(actor_id)

    def to_event(self) -> Event:
        return Event(
            type=EventType.STEP_COST.value,
            actor_id=self.actor_id,
            timestamp=datetime.now(),
            text=self.service_cost.description,
            # This flag is needed to serialize subclass
            # https://docs.pydantic.dev/latest/concepts/serialization/#serializeasany-annotation
            data=self.service_cost.model_dump(serialize_as_any=True),
            message_id=self.message_id,
        )


def thread_message_lookup_request(message_id: str, event_type: str) -> dict:
    """retrieve messages and events for the thread associated with a message"""
    return {
        "id": message_id,
        "relations": {
            "thread": {
                "relations": {
                    "messages": {
                        "relations": {"events": {"filter": {"type": event_type}}},
                        "apply_annotations_from_actors": ["*"],
                    },
                }
            }
        },
    }
