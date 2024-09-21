import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetMessages

api_id = '25311593'
api_hash = '4a552211f7d23d042f9f33155beba5f3'
session_dir = 'sessions'  # Directory for session files

def create_session():
    session_name = input("Enter session name (e.g., user1): ")
    client = TelegramClient(os.path.join(session_dir, session_name), api_id, api_hash)
    client.start()
    print(f"Session for {session_name} created and logged in!")
    client.disconnect()

def join_channel(channel_link):
    session_files = os.listdir(session_dir)
    for session_file in session_files:
        client = TelegramClient(os.path.join(session_dir, session_file), api_id, api_hash)
        client.start()
        print(f"Joining channel for session: {session_file}")
        client(JoinChannelRequest(channel_link))
        print(f"Joined channel {channel_link} for session {session_file}")
        client.disconnect()

def react_to_post(post_link):
    session_files = os.listdir(session_dir)
    for session_file in session_files:
        client = TelegramClient(os.path.join(session_dir, session_file), api_id, api_hash)
        client.start()
        try:
            print(f"Reacting to post for session: {session_file}")
            # Split the link to get the channel and message ID
            parts = post_link.split('/')
            channel_username = parts[-2]  # e.g., 'test89809ok'
            message_id = int(parts[-1])  # e.g., 2
            entity = client.get_entity(channel_username)
            # Fetch the message object
            message = client(GetMessages(id=[message_id]))
            client.send_reaction(entity=entity, message_id=message_id, reaction="🔥")  # Fire emoji
            print(f"Successfully reacted to post {post_link} for session {session_file}")
        except Exception as e:
            print(f"Failed to react to post for session {session_file}: {e}")
        finally:
            client.disconnect()

def main():
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    print("Welcome to Telegram Session Bot!")
    print("1. Create session")
    print("2. Join channel")
    print("3. React to post")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        create_session()
    elif choice == '2':
        channel_link = input("Enter the channel link: ")
        join_channel(channel_link)
    elif choice == '3':
        post_link = input("Enter the post link: ")
        react_to_post(post_link)
    else:
        print("Invalid choice!")

if __name__ == '__main__':
    main()
