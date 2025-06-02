from aiogram.types import InlineKeyboardButton
from bot import callbacks
from bot.types import NavigationHistory
from ..sourcefile import links


class buttons:

    def __call__(self, lang: str = None):
        return self.ru

    class ru:
        class InlineButton(InlineKeyboardButton):
            position: str = None

            def __call__(self, history: NavigationHistory = (), url: str = None) -> 'InlineButton':
                copy = self.model_copy()
                if history:
                    if self.callback_data:
                        history += (self.callback_data,)
                    copy.callback_data = callbacks.pack_history(history)
                elif url:
                    copy.url = url
                return copy

        def keyboard_from_buttons(buttons: list[InlineButton]) -> list[list[InlineButton]]:
            positional_buttons = []
            other_buttons = []
            for button in buttons:
                if getattr(button, 'position', None):
                    positional_buttons.append(button)
                else:
                    other_buttons.append(button)
            positional_buttons.sort(key=lambda x: x.position)

            keyboard = []
            for button in positional_buttons:
                button_row = int(button.position.split(':')[0])
                while len(keyboard) < button_row:
                    keyboard.append([])
                keyboard[button_row - 1].append(button)

            keyboard = (
                    [row for row in keyboard if len(row) != 0] +
                    [[button] for button in other_buttons]
            )
            return keyboard

        def organize_buttons(buttons: list):
            if len(buttons) % 2 == 0:
                return [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
            return [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

        NextMenu = InlineButton(text='Далее', callback_data=callbacks.NEXT)
        Payment = InlineButton(text='Оплатить', callback_data=callbacks.PAY)
        NextExamples = InlineButton(text='Понятно, дальше', callback_data=callbacks.EXAMPLES)
        Price = InlineButton(text='А сколько стоит?', callback_data=callbacks.PRICE)

        Stars = InlineButton(text='Telegram stars', callback_data=callbacks.STARS)
        StarsPayment = InlineButton(text='Telegram stars', pay=True)
        Card = InlineButton(text='Карта РФ', callback_data=callbacks.CARD)
        Stripe = InlineButton(text='Stripe (в $)', callback_data=callbacks.STRIPE)
        Lava = InlineButton(text='Lava (в $)', callback_data=callbacks.LAVA)
        Support = InlineButton(text='Служба заботы', url='https://t.me/cheeseaimanager')
        Pay = InlineButton(text='Оплатить', url='google.com')
