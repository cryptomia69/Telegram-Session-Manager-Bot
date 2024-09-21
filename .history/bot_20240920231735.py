import os
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

api_id = 123456  # Your Telegram API ID
api_hash = 'your_api_hash'  # Your Telegram API hash
session_dir = 'sessions'  # Directory where session files are stored

def list_sessions():
    """List all session files in the 'sessions' directory."""
    return [os.path.join(session_dir, f) for f in os.listdir(session_dir) if f.endswith('.session')]

def create_session():
    """Prompt the user to create a new session."""
    print("Creating a new session:")
    phone = input("Enter phone number: ")
    session_name = input("Enter session name (e.g., session1): ")
    client = TelegramClient(f'sessions/{session_name}', api_id, api_hash)
    client.start(phone)
    print(f"Session '{session_name}' created successfully!")

def join_channel(channel_link):
    """Join a channel for all session files."""
    for session_file in list_sessions():
        client = TelegramClient(session_file, api_id, api_hash)
        with client:
            try:
                client(JoinChannelRequest(channel_link))
                print(f"Joined channel {channel_link} using session {session_file}")
            except Exception as e:
                print(f"Failed to join channel for {session_file}: {str(e)}")

def react_to_post(post_link):
    """React to a post for all session files."""
    for session_file in list_sessions():
        client = TelegramClient(session_file, api_id, api_hash)
        with client:
            try:
                message = client.get_messages(post_link, limit=1)
                if message:
                    # React with a fire emoji
                    client.send_reaction(post_link, '🔥')
                    print(f"Reacted with fire emoji to post {post_link} using session {session_file}")
            except Exception as e:
                print(f"Failed to react to post for {session_file}: {str(e)}")

def main():
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
        print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
