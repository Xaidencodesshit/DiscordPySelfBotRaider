import discord
from discord.errors import LoginFailure
import asyncio
from colorama import Fore, init
import os
import re 
import requests

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    terminal_width = os.get_terminal_size().columns
    centered_lines = [line.center(terminal_width) for line in text.splitlines()]
    return "\n".join(centered_lines)

def display_logo():
    logo = r"""
    {pink} __   __          _____ _____  ______ _   _  _____    _____ ______ _      ______ ____   ____ _______ 
    {blue} \ \ / /    /\   |_   _|  __ \|  ____| \ | |/ ____|  / ____|  ____| |    |  ____|  _ \ / __ \__   __|
    {pink}  \ V /    /  \    | | | |  | | |__  |  \| | (___   | (___ | |__  | |    | |__  | |_) | |  | | | |   
    {blue}   > <    / /\ \   | | | |  | |  __| | .  |\___ \   \___ \|  __| | |    |  __| |  _ <| |  | | | |   
    {pink}  / . \  / ____ \ _| |_| |__| | |____| |\  |____) |  ____) | |____| |____| |    | |_) | |__| | | |   
    {blue} /_/ \_\/_/    \_\_____|_____/|______|_| \_|_____/  |_____/|______|______|_|    |____/ \____/  |_|   
    """.format(pink=Fore.MAGENTA, blue=Fore.CYAN)
    print(center_text(logo))

async def press_enter():
    print(center_text(Fore.CYAN + '-' * 80))  
    print(center_text(Fore.GREEN + "Press Enter to continue..."))  
    input()

def get_option_input():
    """Display a cool arrow-styled prompt for choosing an option."""
    arrow_prompt = f"{Fore.MAGENTA}➜ {Fore.CYAN}user@xaidselfbot {Fore.GREEN}> {Fore.RESET}"
    return input(arrow_prompt + " Choose your option: ")  

def display_menu():
    terminal_width = os.get_terminal_size().columns
    border_colors = [Fore.MAGENTA, Fore.CYAN]
    option_colors = [Fore.MAGENTA, Fore.CYAN]

    border = "+" + "-" * (terminal_width - 2) + "+"
    menu_options = [
        f"{option_colors[i % 2]}{i + 1}. {option}"
        for i, option in enumerate([
            "Message Spammer", "Server Nuker", 
            "Mass Ban", "Mass DM", 
            "Server Info", "Account Nuker", "Server Permissions", "Webhook Spammer",
            "@everyone Spammer", "Mass Create Channels", "Purge Messages", "Full Nuke", "Webhook Deleter", "Exit"
        ])
    ]

    print(border_colors[0] + border)
    print(center_text(border_colors[1] + " Main Menu "))
    print(border_colors[0] + border)

    for option in menu_options:
        print(center_text(f"| {option.ljust(terminal_width - 4)} |"))

    print(border_colors[0] + border)

class MySelfbot(discord.Client):
    async def on_ready(self):
        clear_screen()
        display_logo()
        print(f"{Fore.GREEN}Logged in as {self.user.name}#{self.user.discriminator}")
        print(center_text(Fore.WHITE + "Made By https://github.com/Xaidencodesshit"))  
        await self.main_menu()

    async def send_message(self, channel_id, message, spam_count):
        """Send multiple spam messages to a specific channel."""
        channel = self.get_channel(channel_id)
        if channel:
            for i in range(spam_count):
                await channel.send(message)
                print(f'{Fore.RED}Sent message {i + 1}: {message}')
                await asyncio.sleep(0.05)
        else:
            print(f'Channel with ID {channel_id} not found.')

    async def nuker(self, server):
        """Delete all roles and channels in a server."""
        print(f"Nuking server: {server.name}...")
        for role in server.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(f"Deleted role: {role.name}")
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Failed to delete role: {e}")

        for channel in server.channels:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"Failed to delete channel: {e}")

    async def mass_ban(self, server):
        """Ban all members in the server."""
        print(f"Banning all members in: {server.name}")
        for member in server.members:
            if member.id != self.user.id:
                try:
                    await member.ban(reason="Mass ban initiated by self-bot")
                    print(f"Banned: {member.name}#{member.discriminator}")
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Failed to ban {member.name}: {e}")
                await asyncio.sleep(0.05)

    async def mass_dm(self, server, message):
        """Send DMs to all members in the server."""
        print(f"Sending DM to all members in {server.name}...")
        successful = failed = 0

        for member in server.members:
            if member != self.user and not member.bot:
                try:
                    await member.send(message)
                    print(f"Sent DM to: {member.name}#{member.discriminator}")
                    successful += 1
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Failed to DM {member.name}: {e}")
                    failed += 1
                await asyncio.sleep(1)

        print(f"\nMass DM Summary:\nSuccessful: {successful}\nFailed: {failed}")

    async def delete_all_servers(self):
        """Leave all servers."""
        print(f"{Fore.RED}Leaving all servers...")
        for guild in self.guilds:
            try:
                await guild.leave()
                print(f"Left server: {guild.name}")
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"Failed to leave {guild.name}: {e}")
            await asyncio.sleep(0.05)

    async def mass_dm_friends(self, message):
        """Send DMs to all friends."""
        print(f"{Fore.RED}Sending DM to all friends...")
        successful = failed = 0
        for user in self.user.friends:
            try:
                await user.send(message)
                print(f"Sent DM to: {user.name}")
                successful += 1
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"Failed to DM {user.name}: {e}")
                failed += 1
            await asyncio.sleep(1)

        print(f"\nMass DM Summary:\nSuccessful: {successful}\nFailed: {failed}")

    async def account_nuker(self):
        """Execute the account nuker: leave servers and DM friends."""
        print(f"{Fore.RED}WARNING: This action is irreversible, Make sure you are logged into the account you want to nuke..")
        confirmation = input("Type 'CONFIRM' to proceed: ")

        if confirmation == "CONFIRM":
            await self.delete_all_servers()
            message = input("Enter the DM message for all friends: ")
            await self.mass_dm_friends(message)
            print(f"{Fore.GREEN}Account nuker completed.")
        else:
            print("Action cancelled.")

    async def main_menu(self):
        """Display and handle the main menu."""
        while True:
            display_menu()
            choice = get_option_input()

            if choice == '1':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.list_channels(server)
                channel = server.channels[int(input("Choose a channel: ")) - 1]
                message = input("Enter the message: ")
                count = int(input("Times to send: "))
                await self.send_message(channel.id, message, count)

            elif choice == '2':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.nuker(server)

            elif choice == '3':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.mass_ban(server)

            elif choice == '4':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                message = input("Enter the DM message: ")
                await self.mass_dm(server, message)

            elif choice == '5':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.server_info(server)

            elif choice == '6':
                await self.account_nuker()

            elif choice == '7':
                await self.list_server_permissions()

            elif choice == '8':
                await self.webhook_spammer()

            elif choice == '9':
                await self.everyone_spammer()

            elif choice == '10':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.create_channels(server)

            elif  choice == '11':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.list_channels(server)
                channel = server.channels[int(input("Choose a channel: ")) - 1]
                count = int(input("Enter the number of messages to delete: "))
                await self.purge_messages(channel, count)

            elif choice == '12':
                await self.list_servers()
                server = self.guilds[int(input("Choose a server: ")) - 1]
                await self.full_server_nuke(server)  
            
            elif choice == '13':
                webhook_deleter()

            elif choice == '14':
                print("Exiting...")
                await self.logout()
                break

            else:
                print("Invalid choice, try again.")

    async def list_servers(self):
        """List all servers the bot is in."""
        print("Servers you are in:")
        for idx, guild in enumerate(self.guilds):
            print(f"{idx + 1}. {guild.name}")

    async def list_channels(self, server):
        """List all channels in a specific server."""
        print(f"Channels in {server.name}:")
        for idx, channel in enumerate(server.channels):
            print(f"{idx + 1}. {channel.name} (ID: {channel.id})")

    async def server_info(self, server):
        """Display server information."""
        print(f"Server name: {server.name}")
        print(f"Owner: {server.owner}")
        print(f"Total members: {server.member_count}")
        print(f"Channels: {len(server.channels)}")
        print(f"Roles: {len(server.roles)}")

    async def list_server_permissions(self):
        """Display permissions for each server the bot is in."""
        print("Server Permissions:")
        for idx, guild in enumerate(self.guilds):
            permissions = guild.me.guild_permissions  
            print(f"\n{idx + 1}. {guild.name} - Permissions:")
            for perm, value in permissions:
                print(f"   - {perm}: {'Yes' if value else 'No'}")

    async def webhook_spammer(self):
        """Create 5 webhooks in a channel and spam a message."""
        await self.list_servers()
        server = self.guilds[int(input("Choose a server: ")) - 1]
        await self.list_channels(server)
        channel = server.channels[int(input("Choose a channel: ")) - 1]
        message = input("Enter the spam message: ")
        spam_count = int(input("How many times to send: "))
        print("Making webhooks...")

        webhooks = []
        for i in range(5):
            webhook = await channel.create_webhook(name=f"SpammerWebhook{i+1}")
            webhooks.append(webhook)

        for i in range(spam_count):
            for webhook in webhooks:
                await webhook.send(message)
                print(f'Webhook {webhook.name} sent message: {message}')
                await asyncio.sleep(0.05)

        for webhook in webhooks:
            await webhook.delete()
            print(f'Deleted webhook: {webhook.name}')

    async def everyone_spammer(self):
        """Send an @everyone message to all text channels in a selected server."""
        await self.list_servers()
        server = self.guilds[int(input("Choose a server: ")) - 1]
        count = int(input("How many times to send @everyone message: "))
        message = input("Enter the message to send with @everyone: ")

        for channel in server.channels:
            if isinstance(channel, discord.TextChannel):  
                for i in range(count):
                    try:
                        await channel.send(f"@everyone {message}")
                        print(f'{Fore.RED}Sent @everyone message {i + 1} to {channel.name}: {message}')
                        await asyncio.sleep(0.005)
                    except (discord.Forbidden, discord.HTTPException) as e:
                        print(f"Failed to send @everyone message in {channel.name}: {e}")

    async def create_channels(self, server):
        """Create multiple channels with the same name."""
        count = int(input("How many channels do you want to create? "))
        name = input("Enter the name for the channels: ")

        print(f"Creating {count} channels named '{name}' in {server.name}...")
        for i in range(count):
            try:
                await server.create_text_channel(name)
                print(f"Created channel: {name} ({i + 1}/{count})")
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"Failed to create channel {i + 1}: {e}")
            await asyncio.sleep(0.05)

    async def purge_messages(self, channel, count):
        """Delete a specified number of messages from a channel."""
        print(f"Purging {count} messages from {channel.name}...")
        try:
            deleted = await channel.purge(limit=count)
            print(f"{len(deleted)} messages deleted successfully.")
        except (discord.Forbidden, discord.HTTPException) as e:
            print(f"Failed to purge messages: {e}")

    async def full_server_nuke(self, server):
        """Perform a full server nuke by deleting channels and creating new ones."""
        print(f"Performing full nuke on server: {server.name}...")
        
        for channel in server.channels:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"Failed to delete channel: {e}")

        for i in range(35):
            try:
                new_channel = await server.create_text_channel('xaid-on-top')
                print(f"Created channel: {new_channel.name}")
                for j in range(4):  
                    await new_channel.send("@everyone https://imgur.com/a/inMuil5")
                    print(f'Sent @everyone message in {new_channel.name}.')
                    await asyncio.sleep(0.05)  
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"Failed to create channel {i + 1}: {e}")
            await asyncio.sleep(0.05)

def webhook_deleter():
    """Delete a Discord webhook."""
    while True:
        webhook_url = input("Enter the full Discord webhook URL (or type 'exit' to cancel): ").strip()
        
        if webhook_url.lower() == "exit":
            print(f"{Fore.YELLOW}Canceled: Returning to the main menu.")
            return
        
        if not re.match(r"^https://discord\.com/api/webhooks/[\w-]+/[\w-]+$", webhook_url):
            print(f"{Fore.RED}Error: Invalid webhook URL format. Please try again.")
            continue
        
        try:
            response = requests.delete(webhook_url)
            if response.status_code == 204:
                print(f"{Fore.GREEN}Success: The webhook was successfully deleted.")
            elif response.status_code == 404:
                print(f"{Fore.RED}Error: Webhook not found (it may already be deleted).")
            else:
                print(f"{Fore.RED}Error: Failed to delete the webhook. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"{Fore.RED}Error: An exception occurred while deleting the webhook. Details: {e}")
        break

async def main():
    """Main entry point for the selfbot."""
    clear_screen()
    display_logo()
    await press_enter()

    arrow_prompt = f"{Fore.MAGENTA}➜ {Fore.CYAN}user@xaidselfbot {Fore.GREEN}> {Fore.RESET}"
    token = input(arrow_prompt + " Enter your Discord token: ")  

    print(f"{Fore.GREEN}Logging in...")

    selfbot = MySelfbot()

    try:
        await selfbot.start(token)
    except LoginFailure:
        print(f"{Fore.RED}Error: Invalid token. Please check and try again.")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}, Please try again.")

if __name__ == '__main__':
    asyncio.run(main())
