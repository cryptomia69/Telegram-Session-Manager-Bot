from pyrogram import Client
from pyrogram.errors import FloodWait
import time

# Initialize the Pyrogram Client with API ID and API Hash
app = Client("my_account", api_id="your_api_id", api_hash="your_api_hash")

# Function to create a session
async def create_session():
    print("Session created successfully.")

# Function to join a Telegram channel
async def join_channel(channel_link):
    try:
        async with app:
            await app.join_chat(channel_link)
        print(f"Successfully joined channel: {channel_link}")
    except Exception as e:
        print(f"Failed to join channel: {e}")

# Function to react to a Telegram post
async def react_to_post(chat_id, message_id, emoji):
    try:
        async with app:
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
    choice = show_menu()
    
    if choice == '1':
        app.run(create_session())
    
    elif choice == '2':
        channel_link = input("Enter the channel link: ")
        app.run(join_channel(channel_link))
    
    elif choice == '3':
        post_link = input("Enter the post link: ")
        # Split post link to get chat_id and message_id
        try:
            chat_id, message_id = post_link.replace('https://t.me/', '').split('/')
            message_id = int(message_id)  # Convert message_id to integer
            emoji = input("Enter the reaction emoji: ")
            app.run(react_to_post(chat_id, message_id, emoji))
        except ValueError:
            print("Invalid post link format.")
    
    else:
        print("Invalid choice. Exiting...")
