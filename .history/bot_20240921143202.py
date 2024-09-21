import os
from pyrogram import Client
from pyrogram.errors import FloodWait
import time

# Create 'sessions' directory if it doesn't exist
if not os.path.exists("sessions"):
    os.makedirs("sessions")

# Function to create a Pyrogram client, storing session files in the 'sessions' folder
def create_client(session_name):
    return Client(
        session_name=session_name, 
        api_id="25311593", 
        api_hash="4a552211f7d23d042f9f33155beba5f3",
        workdir="sessions"  # Store session files in 'sessions' folder
    )

# Function to create a session
async def create_session(session_name):
    async with create_client(session_name) as app:
        print(f"Session '{session_name}' created successfully.")

# Function to join a Telegram channel using all existing sessions
async def join_channel(channel_link):
    sessions = os.listdir("sessions")  # List all session files
    if not sessions:
        print("No sessions found. Please create a session first.")
        return

    for session_file in sessions:
        session_name = os.path.splitext(session_file)[0]  # Strip the file extension
        try:
            async with create_client(session_name) as app:
                await app.join_chat(channel_link)
            print(f"Successfully joined channel {channel_link} using session '{session_name}'.")
        except Exception as e:
            print(f"Failed to join channel with session '{session_name}': {e}")

# Function to react to a Telegram post using all existing sessions
async def react_to_post(chat_id, message_id, emoji):
    sessions = os.listdir("sessions")  # List all session files
    if not sessions:
        print("No sessions found. Please create a session first.")
        return

    for session_file in sessions:
        session_name = os.path.splitext(session_file)[0]  # Strip the file extension
        try:
            async with create_client(session_name) as app:
                await app.send_reaction(chat_id=chat_id, message_id=message_id, emoji=emoji)
            print(f"Successfully reacted with {emoji} using session '{session_name}'.")
        except FloodWait as e:
            print(f"Rate limited for session '{session_name}'. Waiting for {e.x} seconds.")
            time.sleep(e.x)
        except Exception as e:
            print(f"Failed to react with session '{session_name}': {e}")

# Menu function
def show_menu():
    print("Welcome to Telegram Session Bot!")
    print("1. Create session")
    print("2. Join channel with all sessions")
    print("3. React to post with all sessions")
    return input("Enter your choice (1/2/3): ")

# Main program
if __name__ == "__main__":
    choice = show_menu()

    if choice == '1':
        session_name = input("Enter a unique session name: ")
        create_client(session_name).run(create_session(session_name))

    elif choice == '2':
        channel_link = input("Enter the channel link: ")
        create_client("").run(join_channel(channel_link))

    elif choice == '3':
        post_link = input("Enter the post link: ")
        try:
            # Split post link to get chat_id and message_id
            chat_id, message_id = post_link.replace('https://t.me/', '').split('/')
            message_id = int(message_id)  # Convert message_id to integer
            emoji = "🔥"  # Fire emoji for reacting
            create_client("").run(react_to_post(chat_id, message_id, emoji))
        except ValueError:
            print("Invalid post link format.")
    
    else:
        print("Invalid choice. Exiting...")
