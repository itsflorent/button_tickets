import discord
from discord.ui import Button, View
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

GUILD_ID = 123
TEAM_ROLE = 123
TICKET_CHANNEL = 123
CATEGORY_ID = 123


@bot.event
async def on_ready():
    print("Online!")

@bot.command()
async def ticketmsg(ctx):
    button1 = Button(label="Ticket opened!", style=discord.ButtonStyle.blurple, custom_id="ticket_button")
    view = View()
    view.add_item(button1)
    embed = discord.Embed(description=f"Open a ticket via. Button", title=f"Ticket System")
    channel = bot.get_channel(TICKET_CHANNEL)
    await channel.send(embed=embed, view=view)
    await ctx.reply("Done!")


@bot.event
async def on_interaction(interaction):
    if interaction.channel.id == TICKET_CHANNEL:

        
        if "ticket_button" in str(interaction.data):
            guild = bot.get_guild(GUILD_ID)
            for ticket in guild.channels:
                if str(interaction.user.id) in ticket.name:
                    embed = discord.Embed(description=f"You can have only one ticket open at a time!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            category = bot.get_channel(CATEGORY_ID)
            ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.id}", category=category,
                                                            topic=f"Ticket von {interaction.user} \nClient-ID: {interaction.user.id}")

            
            await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE), send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True)
            embed = discord.Embed(description=f'Welcome in your Ticket {interaction.user.mention}.\n'
                                            f'On of our staff will be help soon as possible!\n'
                                            f'If you want to close the ticket write `!close` in this channel.',
                                color=62719)
            embed.set_author(name=f'New Ticket')
            mess_2 = await ticket_channel.send(embed=embed)
            embed = discord.Embed(title="???? | Ticket opened",
                                description=f'Your ticket was created!',
                                color=discord.colour.Color.green())
            try:
                await interaction.author.send(embed=embed)
            except:
                pass
            return


@bot.command()
async def close(ctx):
    if "ticket" in ctx.channel.name:
        embed = discord.Embed(
                description=f'This Ticket will be closed in 5 seconds!',
                color=16711680)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()


bot.run("TOKEN")
