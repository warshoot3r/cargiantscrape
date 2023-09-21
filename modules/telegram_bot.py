import requests
import socket
import re
import zipfile
import tempfile
import os
class TelegramBot:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = f"https://api.telegram.org/bot{api_token}/"

    def send_dataframe(self, chat_id, dataframe, caption="", show_header=False, MessageThreadID = None):
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
        if show_header == False:
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
        self.send_message(chat_id, message, ParserType="HTML", MessageThreadID=MessageThreadID)




    def get_updates(self):
        get_updates_url = f"{self.base_url}getUpdates"
        try:
            response = requests.get(get_updates_url)
            response_json = response.json()
            
            if response_json["ok"]:
                updates = response_json["result"]
                if updates:
                    for key in updates:

                        if 'message' in key and 'chat' in key['message']:
                            chat = key['message']['chat']
                            chat_id = chat['id']
                            chat_title = chat.get('title', 'Private Chat')
                            chat_type = chat['type']
                            print(f"Chat ID: {chat_id}, Title: {chat_title}, Type: {chat_type}")
                            if 'text' in key['message']:
                                text = key['message']['text']
                                message_id = key['message']['message_id']
                                from_person = key['message']['from']['first_name']+ " " +  key['message']['from']['last_name']
                                print(f"Chat ID: {chat_id}, Title: {chat_title}, Type: {chat_type}")
                                print(f"Message: \"{text}\" MessageID:{message_id} From: {from_person} ")
                else:
                    print("Failed to get updates. Error:", response_json["description"], flush=True)
        except requests.exceptions.RequestException as e:
            print("Error getting updates:", e, flush=True)


    def get_recent_messages(self):
        get_updates_url = f"{self.base_url}getUpdates"
        try:
            response = requests.get(get_updates_url)
            response_json = response.json()
            
            if response_json["ok"]:
                updates = response_json["result"]
                if updates:
                    for key in updates:

                        if 'message' in key and 'chat' in key['message']:
                            chat = key['message']['chat']
                            chat_id = chat['id']
                            chat_title = chat.get('title', 'Private Chat')
                            chat_type = chat['type']
                            if 'text' in key['message']:
                                text = key['message']['text']
                                message_id = key['message']['message_id']
                                from_person = key['message']['from']['first_name']+ " " +  key['message']['from']['last_name']
                                print(f"Message: \"{text}\" MessageID: {message_id} From: {from_person} ChatID: {chat_id}")
                else:
                    print("Failed to get updates. Error:", response_json["description"], flush=True)
        except requests.exceptions.RequestException as e:
            print("Error getting updates:", e, flush=True)

    def send_message(self, chat_id, message, ParserType="Markdownv2", max_message_length=4096, MessageThreadID=None):
        send_message_url = f"{self.base_url}sendMessage"
        try:
            if len(message) <= max_message_length:
                # Message is within the length limit, send it as is
                data = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": ParserType,
                    "reply_to_message_id": MessageThreadID
                }
                response = requests.post(send_message_url, data=data)
                response_json = response.json()
                if response_json["ok"]:
                    print("Message sent successfully!", flush=True)
                else:
                    print("Failed to send message. Error:", response_json["description"], flush=True)
            else:
                # Message is too long, split it into chunks and send each chunk
                chunks = [message[i:i+max_message_length] for i in range(0, len(message), max_message_length)]
                for i, chunk in enumerate(chunks, start=1):
                    data = {
                        "chat_id": chat_id,
                        "text": chunk,
                        "parse_mode": ParserType,
                        "reply_to_message_id": MessageThreadID,
                    }
                    response = requests.post(send_message_url, data=data)
                    response_json = response.json()
                    if response_json["ok"]:
                        print(f"Chunk {i} sent successfully!", flush=True)
                    else:
                        print(f"Failed to send chunk {i}. Error:", response_json["description"], flush=True)
        except requests.exceptions.RequestException as e:
            print("Error sending message:", e, flush=True)

    def send_message_servername(self, chat_id, message, MessageThreadID):
        try: 
            get_computer_name = socket.gethostname()
            computer_name = re.sub(r'[^w\w\s]', '', get_computer_name)        
        except socket.error as e:
            return None
        message = f"From server: {computer_name} {message}"
        self.send_message(chat_id=chat_id, message=message, MessageThreadID=MessageThreadID)
    def send_dataframe_as_file(self, chat_id, dataframe, file_format="csv", caption="", file_name="data", MessageThreadID=None):
        if file_format not in ["csv", "xlsx"]:
            raise ValueError("Invalid file_format. Supported formats are 'csv' and 'xlsx'.")

        filename = f"{file_name}.{file_format}"
        if file_format == "csv":
            dataframe.to_csv(filename, index=False)
        elif file_format == "xlsx":
            dataframe.to_excel(filename, index=False)

        send_document_url = f"{self.base_url}sendDocument"
        files = {"document": open(filename, "rb")}

        try:
            response = requests.post(send_document_url, data={"chat_id": chat_id, "caption": caption, "reply_to_message_id": MessageThreadID}, files=files, )
            response_json = response.json()
            if response_json["ok"]:
                print("File sent successfully!", flush=True)
            else:
                print("Failed to send file. Error:", response_json["description"], flush=True)
        except requests.exceptions.RequestException as e:
            print("Error sending file:", e, flush=True)
        # finally:
        #     # Remove the temporary file
        #     import os
        #     os.remove(filename)
    def send_dataframe_as_csv_files(self, chat_id, dataframes, captions=None, file_names=None, MessageThreadID=None) :
        if not captions:
            captions = [""] * len(dataframes)
        if not file_names:
            file_names = ["data"] * len(dataframes)

        if len(dataframes) != len(captions) or len(dataframes) != len(file_names):
            raise ValueError("Length of dataframes, captions, and file_names should be the same.")

     #   try:
        for i, dataframe in enumerate(dataframes):
            file_name = f"{file_names[i]}.csv"
            file_path = os.path.join(tempfile.gettempdir(), file_name)

            dataframe.to_csv(file_path, index=False)

            send_document_url = f"{self.base_url}sendDocument"
            files = {"document": (file_name, open(file_path, "rb"))}
            caption = captions[i]

            try:
                response = requests.post(send_document_url, data={"chat_id": chat_id, "caption": caption, "reply_to_message_id": MessageThreadID}, files=files)
                response_json = response.json()
                if response_json["ok"]:
                    print(f"File '{file_name}' sent successfully!", flush=True)
                else:
                    print(f"Failed to send file '{file_name}'. Error:", response_json["description"], flush=True)
            except requests.exceptions.RequestException as e:
                print(f"Error sending file '{file_name}':", e, flush=True)
        # finally:
        #     # Remove the temporary CSV files
        #     for i in range(len(dataframes)):
        #         file_name = f"{file_names[i]}.csv"
        #         file_path = os.path.join(tempfile.gettempdir(), file_name)
        #         os.remove(file_path)

    
    def send_dataframe_as_multiple_files_as_zip(self, chat_id, dataframes, file_formats=None, captions=None, file_names=None, MessageThreadID=None):
        """
                # Example usage:
        # dataframes = [df1, df2]  # List of dataframes to send
        # file_formats = ["csv", "xlsx"]  # List of file formats corresponding to dataframes
        # captions = ["Caption 1", "Caption 2"]  # List of captions for files
        # file_names = ["data1", "data2"]  # List of file names
        # your_bot.send_dataframe_as_files(chat_id="your_chat_id_here", dataframes=dataframes, file_formats=file_formats, captions=captions, file_names=file_names)
        """
        if not file_formats:
            file_formats = ["csv"] * len(dataframes)
        if not captions:
            captions = [""] * len(dataframes)
        if not file_names:
            file_names = ["data"] * len(dataframes)

        if len(dataframes) != len(file_formats) or len(dataframes) != len(captions) or len(dataframes) != len(file_names):
            raise ValueError("Length of dataframes, file_formats, captions, and file_names should be the same.")

        # Create a temporary directory to store the individual files
        temp_dir = tempfile.mkdtemp()

        try:
            file_paths = []
            for i, dataframe in enumerate(dataframes):
                file_format = file_formats[i]
                file_name = f"{file_names[i]}.{file_format}"
                file_path = os.path.join(temp_dir, file_name)

                if file_format == "csv":
                    dataframe.to_csv(file_path, index=False)
                elif file_format == "xlsx":
                    dataframe.to_excel(file_path, index=False)

                file_paths.append(file_path)

            # Create a zip file containing all the individual files
            zip_filename = "data.zip"
            zip_file_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for file_path in file_paths:
                    zipf.write(file_path, os.path.basename(file_path))

            send_document_url = f"{self.base_url}sendDocument"
            files = {"document": (zip_filename, open(zip_file_path, "rb"))}

            try:
                response = requests.post(send_document_url, data={"chat_id": chat_id, "reply_to_message_id": MessageThreadID}, files=files)
                response_json = response.json()
                if response_json["ok"]:
                    print("Files sent successfully!", flush=True)
                else:
                    print("Failed to send files. Error:", response_json["description"], flush=True)
            except requests.exceptions.RequestException as e:
                print("Error sending files:", e, flush=True)
        finally:
            # Remove the temporary directory and its contents
            for file_path in file_paths:
                os.remove(file_path)
            os.remove(zip_file_path)
            os.rmdir(temp_dir)
    # # Create an instance of the TelegramBot class
    # bot = TelegramBot(api_token)

    # # Send the message
    # bot.send_message(chat_id, message)
