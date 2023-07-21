import requests
import socket
class TelegramBot:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = f"https://api.telegram.org/bot{api_token}/"


    def send_dataframe(self, chat_id, dataframe, caption=""):
        message = caption + "\n" + dataframe.to_string(index=False, justify='left', col_space=15)
        self.send_message(chat_id, message)   

    def get_updates(self):
        get_updates_url = f"{self.base_url}getUpdates"
        try:
            response = requests.get(get_updates_url)
            response_json = response.json()
            if response_json["ok"]:
                updates = response_json["result"]
                if updates:
                    for update in updates:
                        chat_id = update["message"]["chat"]["id"]
                        print("Received message from chat ID:", chat_id)
            else:
                print("Failed to get updates. Error:", response_json["description"])
        except requests.exceptions.RequestException as e:
            print("Error getting updates:", e)

    def send_message(self, chat_id, message):
        send_message_url = f"{self.base_url}sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
        }
        try:
            response = requests.post(send_message_url, data=data)
            response_json = response.json()
            if response_json["ok"]:
                print("Message sent successfully!")
            else:
                print("Failed to send message. Error:", response_json["description"])
        except requests.exceptions.RequestException as e:
            print("Error sending message:", e)

    def send_message_servername(self, chat_id):
        try: 
            computer_name = socket.gethostname()
        except socket.error as e:
            return None
        message = f"From server: {computer_name}"
        self.send_message(chat_id=chat_id, message=message)
    def send_dataframe_as_file(self, chat_id, dataframe, file_format="csv", caption=""):
        if file_format not in ["csv", "xlsx"]:
            raise ValueError("Invalid file_format. Supported formats are 'csv' and 'xlsx'.")

        filename = f"data.{file_format}"
        if file_format == "csv":
            dataframe.to_csv(filename, index=False)
        elif file_format == "xlsx":
            dataframe.to_excel(filename, index=False)

        send_document_url = f"{self.base_url}sendDocument"
        files = {"document": open(filename, "rb")}

        try:
            response = requests.post(send_document_url, data={"chat_id": chat_id, "caption": caption}, files=files)
            response_json = response.json()
            if response_json["ok"]:
                print("File sent successfully!")
            else:
                print("Failed to send file. Error:", response_json["description"])
        except requests.exceptions.RequestException as e:
            print("Error sending file:", e)
        finally:
            # Remove the temporary file
            import os
            os.remove(filename)
    # # Create an instance of the TelegramBot class
    # bot = TelegramBot(api_token)

    # # Send the message
    # bot.send_message(chat_id, message)
