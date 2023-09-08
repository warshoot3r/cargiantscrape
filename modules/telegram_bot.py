import requests
import socket
import re
class TelegramBot:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = f"https://api.telegram.org/bot{api_token}/"

    def send_dataframe(self, chat_id, dataframe, caption="", show_header=False):
        # Format URLs using the provided code
        hyperlink_column = dataframe['URL'].apply(lambda url: f'<a href="{url}">{url.split("/")[-1]}</a>')

        # Create a copy of the DataFrame and sort it
        sorted_dataframe = dataframe.copy()
        sorted_dataframe.sort_values(by=["Price","Manufacturer"], inplace=True)

        # Update the 'URL' column with hyperlinks
        sorted_dataframe['URL'] = hyperlink_column

        # Convert the DataFrame to a formatted string with adjusted spacing
        header = sorted_dataframe.columns.to_list()
        formatted_rows = []

        # Format header
        if not(show_header):
            sorted_dataframe.columns = [None] * len(sorted_dataframe.columns) 
        else: #  show column names if show_header is true
            formatted_header = ' | '.join(header)
            formatted_rows.append(formatted_header)
        
           
        
        # Format data rows
        for _, row in sorted_dataframe.iterrows():
            formatted_row = ' | '.join(row.astype(str).values)
            formatted_rows.append(formatted_row)

        # Combine the caption and formatted DataFrame
        message = caption + "\n" + '\n'.join(formatted_rows)

        # Send the message
        self.send_message(chat_id, message, ParserType="HTML")




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

    def send_message(self, chat_id, message, ParserType="Markdownv2", max_message_length=4096):
        send_message_url = f"{self.base_url}sendMessage"
        try:
            if len(message) <= max_message_length:
                # Message is within the length limit, send it as is
                data = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": ParserType
                }
                response = requests.post(send_message_url, data=data)
                response_json = response.json()
                if response_json["ok"]:
                    print("Message sent successfully!", flush=True)
                else:
                    print("Failed to send message. Error:", response_json["description"])
            else:
                # Message is too long, split it into chunks and send each chunk
                chunks = [message[i:i+max_message_length] for i in range(0, len(message), max_message_length)]
                for i, chunk in enumerate(chunks, start=1):
                    data = {
                        "chat_id": chat_id,
                        "text": chunk,
                        "parse_mode": ParserType
                    }
                    response = requests.post(send_message_url, data=data)
                    response_json = response.json()
                    if response_json["ok"]:
                        print(f"Chunk {i} sent successfully!", flush=True)
                    else:
                        print(f"Failed to send chunk {i}. Error:", response_json["description"])
        except requests.exceptions.RequestException as e:
            print("Error sending message:", e)

    def send_message_servername(self, chat_id, message):
        try: 
            get_computer_name = socket.gethostname()
            computer_name = re.sub(r'[^w\w\s]', '', get_computer_name)        
        except socket.error as e:
            return None
        message = f"From server: {computer_name} {message}"
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
                print("File sent successfully!", flush="True")
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
