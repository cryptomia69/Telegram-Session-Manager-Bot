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
    print(f"Session '{session_name}' created successfully.")

# Function to join a Telegram channel
async def join_channel(session_name, channel_link):
    try:
        async with create_client(session_name) as app:
            await app.join_chat(channel_link)
        print(f"Successfully joined channel: {channel_link}")
    except Exception as e:
        print(f"Failed to join channel: {e}")

# Function to react to a Telegram post
async def react_to_post(session_name, chat_id, message_id, emoji):
    try:
        async with create_client(session_name) as app:
            await app.send_reaction(chat_id=chat_id, message_id=message_id, emoji=emoji)
        print(f"Successfully reacted to post in chat {chat_id} with {emoji}")
    except FloodWait as e:
        print(f"Rate limited. Waiting for {e.x} seconds.")
        time.sleep(e.x)
    except Exception as e:
        print(f"Failed to react to post: {e}")

# Menu function
def show_menu():
    print("Welcome to Telegram Session Bot!")
    print("1. Create session")
    print("2. Join channel")
    print("3. React to post")
    return input("Enter your choice (1/2/3): ")

# Main program
if __name__ == "__main__":
    session_name = input("Enter the session name: ")  # Unique session name for each user/session
    choice = show_menu()
    
    if choice == '1':
        create_client(session_name).run(create_session(session_name))
    
    elif choice == '2':
        channel_link = input("Enter the channel link: ")
        create_client(session_name).run(join_channel(session_name, channel_link))
    
    elif choice == '3':
        post_link = input("Enter the post link: ")
        try:
            # Split post link to get chat_id and message_id
            chat_id, message_id = post_link.replace('https://t.me/', '').split('/')
            message_id = int(message_id)  # Convert message_id to integer
            emoji = input("Enter the reaction emoji: ")
            create_client(session_name).run(react_to_post(session_name, chat_id, message_id, emoji))
        except ValueError:
            print("Invalid post link format.")
    
    else:
        print("Invalid choice. Exiting...")
