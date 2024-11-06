
import datetime
from ai_chat_domain.model.HaleyChatMessage import HaleyChatMessage


class HaleyChatBotMessage(HaleyChatMessage):
        agentInstallURI: str
        chatGeneratedMessage: str
        chatIncrementalGeneratedMessage: str
        chatPartialGeneratedMessage: str
        chatPriorUserMessage: str
        chatVoiceMessage: str
        haleyChatQuotaStatusURI: str
        haleyChatReplyToIntentURI: str
        chatContinueListening: bool

