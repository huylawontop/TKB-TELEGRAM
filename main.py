# Made by huylaw
# fb.com/huylaw.info | https://huylaw.notion.site/Huylaw-11d24dbef1024b7dbe3dafed1c7a3cb1
# 
#

from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pandas as pd
import numpy as np

dfs = pd.read_excel(r"D:\tkb telegram\TKB-TELEGRAM\tkb.xlsx", sheet_name=0)


TOKEN = '6851514752:AAGvlOnlj28V2I3gjTdFYUbZZnf-2eY0rMA'
BOT_USERNAME: Final = '@huylaw_bot'


mapping = {
    "10A1": 1, "10A2": 2, "10A3": 3, "10A4": 4, "10A5": 5, "10A6": 6, "10A7": 7,
    "11A1": 8, "11A2": 9, "11A3": 10, "11A4": 11, "11A5": 12, "11A6": 13, "11A7": 14,
    "12A1": 15, "12A2": 16, "12A3": 17, "12A4": 18, "12A5": 19, "12A6": 20
}


dfs = pd.read_excel('tkb.xlsx', sheet_name=0)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! huylaw, Vui lòng Nhập lớp (vd: 10A1, 11A2,12A3,..)")

def handle_message(update, context):
    message_text = update.message.text.strip()

    if message_text in mapping:
        context.user_data['class'] = message_text
        context.bot.send_message(chat_id=update.effective_chat.id, text="đã cập nhật lớp, nhập thứ (vd: 2 (tương ứng với thứ 2), 3 (tương ứng với thứ 3),...)")
    elif 'class' not in context.user_data:
        context.user_data['class'] = message_text
        context.bot.send_message(chat_id=update.effective_chat.id, text="nhập thứ (vd: 2 (tương ứng với thứ 2), 3 (tương ứng với thứ 3),...)")
    elif 'day' not in context.user_data:
        day_input = message_text
        print(f"Received day input: {day_input}")  # Debug statement

        # Ensure day_input is an integer
        try:
            day_index = int(day_input) - 2  

            class_input = context.user_data['class']
            x = mapping.get(class_input)
            if x is not None:
                column_index = x + 1

                # Accessing values horizontally
                row_values = dfs.iloc[7:37, 0:].values  # Exclude the first two columns
                
                # Replace empty cells or NaN values with "Trống"
                row_values[row_values == ""] = "Trống"
                row_values = np.where(pd.isna(row_values), "Trống", row_values)

                line_count = 0  # Variable to keep track of the line count
                days = ["thứ 2", "thứ 3", "thứ 4", "thứ 5", "thứ 6", "thứ 7"]

                # Print the values for the specified day of the week
                response = f"{class_input} - {days[day_index]}\n"
                for row in row_values:
                    if line_count % 5 == 0 and line_count // 5 == day_index:
                        response += str(row[column_index]) + "\n"
                        line_count += 1
                    elif line_count // 5 == day_index:
                        response += str(row[column_index]) + "\n"
                        line_count += 1 
                    else:
                        line_count += 1
                
                context.bot.send_message(chat_id=update.effective_chat.id, text=response)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Khong Tim Thay")
        except ValueError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sai Ngày vui lòng nhập lại (vd: 2 (tương ứng với thứ 2), 3 (tương ứng với thứ 3),...)(Nếu chọn lại lớp vui lòng viết Đẩy đủ hoa lớp VD: 10A2,11A2,...)")
    else:
        context.user_data['class'] = message_text
        context.bot.send_message(chat_id=update.effective_chat.id, text="đã cập nhật lớp, nhập thứ (vd: 2 (tương ứng với thứ 2), 3 (tương ứng với thứ 3),...)(Nếu chọn lại lớp vui lòng viết Đẩy đủ hoa lớp VD: 10A2,11A2,...)")


if __name__ == '__main__':
    
    updater = Updater(token=TOKEN, use_context=True)

    
    dp = updater.dispatcher

    
    dp.add_handler(CommandHandler("start", start))

    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    
    updater.start_polling()

    
    updater.idle()
