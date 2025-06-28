import base64
from typing import List, Tuple, Union

from google.ai.generativelanguage_v1.types import Content, Part

# Define type alias
ContentListUnion = List[Content]

from browser_use.llm.messages import (
    AssistantMessage,
    BaseMessage,
    SystemMessage,
    UserMessage,
)


class GoogleMessageSerializer:
    """Serializer for converting messages to Google Gemini format."""

    @staticmethod
    def serialize_messages(messages: List[BaseMessage]) -> Tuple[ContentListUnion, Union[str, None]]:
        """
        Convert a list of BaseMessages to Google format, extracting system message.

        Returns:
            A tuple of (formatted_messages, system_message)
        """
        messages = [m.model_copy(deep=True) for m in messages]

        formatted_messages: ContentListUnion = []
        system_message: Union[str, None] = None

        for message in messages:
            role = getattr(message, "role", None)

            # Extract system/developer messages
            if isinstance(message, SystemMessage) or role in ['system', 'developer']:
                if isinstance(message.content, str):
                    system_message = message.content
                elif message.content is not None:
                    parts = []
                    for part in message.content:
                        if part.type == 'text':
                            parts.append(part.text)
                    system_message = '\n'.join(parts)
                continue

            # Determine role
            if isinstance(message, UserMessage):
                role = 'user'
            elif isinstance(message, AssistantMessage):
                role = 'model'
            else:
                role = 'user'

            message_parts: List[Part] = []

            # Handle string content
            if isinstance(message.content, str):
                message_parts = [Part(text=message.content)]

            elif message.content is not None:
                for part in message.content:
                    if part.type == 'text':
                        message_parts.append(Part(text=part.text))

                    elif part.type == 'refusal':
                        message_parts.append(Part(text=f"[Refusal] {part.refusal}"))

                    elif part.type == 'image_url':
                        url = part.image_url.url
                        header, data = url.split(",", 1)
                        image_bytes = base64.b64decode(data)
                        image_part = Part(
                            inline_data={
                                "mime_type": "image/png",
                                "data": image_bytes
                            }
                        )
                        message_parts.append(image_part)

            if message_parts:
                final_message = Content(role=role, parts=message_parts)
                formatted_messages.append(final_message)

        return formatted_messages, system_message
