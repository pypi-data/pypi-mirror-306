from dataclasses import dataclass

from pynput import keyboard

from src.agents.basic_agent import LLMAgent
from src.conversations.base_conversation import ConversationWithAgents
from src.conversations.messages import ConversationMessage
from src.conversations.participants import HumanParticipant, SystemParticipant


@dataclass(kw_only=True)
class CLIConversation(ConversationWithAgents):

    def _handle_new_message_for_human(self,
                                      incoming_message: ConversationMessage):
        super()._handle_new_message_for_human(incoming_message)

        human = self.get_human()
        print("\n\n<<Requesting human input>>")
        print(self.format_history_in_xml())

        recipient = self.choose_recipient([
            p for p in self.participants
            if not isinstance(p, HumanParticipant)
            and not isinstance(p, SystemParticipant)
        ])
        user_input = input(f"\n\nEnter your response > ")

        self.prepare_new_message(
            ConversationMessage(sender=human,
                                recipient=recipient,
                                content=user_input))

    def choose_recipient(self, recipients: list[LLMAgent]):
        print("Choose a recipient of the message or -1 to exit:")
        choices = {str(idx): i for idx, i in enumerate(recipients, start=1)}
        for k, v in choices.items():
            print(f"{k}: {v.name}")
        while True:
            user_input = print(">")
            if user_input in ["-1", "exit"]:
                exit()
            if user_input in choices:
                return choices[user_input]
            else:
                print("invalid selection.")

    def start_interruptable_conversation(self,
                                         first_message: ConversationMessage):
        print(
            "Starting conversation, press the 'F1' key to interrupt the conversation at any point"
        )
        self._start_keyboard_listener()

        self.prepare_new_message(first_message)
        self._run_conversation()

    def _start_keyboard_listener(self):

        def on_press(key):
            if key == keyboard.Key.f1:
                print("Triggering interrupt")
                self.manual_interrupt_flag = True

        def on_release(key):
            return key not in ["\x03", keyboard.Key.esc]

        listener = keyboard.Listener(on_press=on_press,
                                     on_release=on_release)  # type: ignore

        listener.start()

    def _run_conversation(self):
        while self.unprocessed_message:
            if self.manual_interrupt_flag:
                self.manual_interrupt_flag = True
                self.manual_interrupt_flag = False
            self.advance()
            self.advance()
            self.advance()
