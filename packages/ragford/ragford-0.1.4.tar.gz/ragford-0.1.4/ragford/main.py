import os
import io
import time
import json
import logging
import inspect
import asyncio
import aiohttp
import sqlite3
import argparse
from datetime import datetime
import hashlib
import io
import tempfile

import hikari
import lightbulb
from lightbulb import errors
from dotenv import load_dotenv

import swarmauri_core
import swarmauri
from swarmauri.llms.concrete.GroqModel import GroqModel
from swarmauri.llms.concrete.DeepInfraModel import DeepInfraModel
from swarmauri.llms.concrete.OpenAIModel import OpenAIModel
from swarmauri.llms.concrete.PlayHTModel import PlayHTModel
from swarmauri.vector_stores.concrete.TfidfVectorStore import TfidfVectorStore
from swarmauri.documents.concrete.Document import Document
from swarmauri.agents.concrete.RagAgent import RagAgent
from swarmauri.conversations.concrete.MaxSystemContextConversation import MaxSystemContextConversation
from swarmauri.messages.concrete.SystemMessage import SystemMessage

# Initialize available models and set the default model index
model_list = ["GroqModel", "DeepInfraModel", "OpenAIModel"]
current_model_index = 0

# Initialize a dictionary to track repeated prompts for the `collaborate_command`
collaborate_repetitions = {}

# Function to load environment variables from a specified file
def load_environment(env_file):
    load_dotenv(env_file)

# Main function to initialize argument parsing
def main():
    parser = argparse.ArgumentParser(description="Run the Discord bot with a specified .env file.")
    parser.add_argument("--env_file", type=str, default="development.env", help="Path to the .env file to load")
    args = parser.parse_args()

    # Load environment variables from specified .env file
    load_environment(args.env_file)

        # Configuration Constants from environment variables
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_DEFAULT_NAME = os.getenv('GROQ_DEFAULT_NAME', 'llama-3.1-8b-instant')
    DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')
    DEEPINFRA_DEFAULT_NAME = os.getenv('DEEPINFRA_DEFAULT_NAME', 'meta-llama/Meta-Llama-3.1-8B-Instruct')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_DEFAULT_NAME = os.getenv('OPENAI_DEFAULT_NAME', 'gpt-4o')
    PLAYHT_USER_ID = os.getenv('PLAYHT_USER_ID')
    PLAYHT_API_KEY = os.getenv('PLAYHT_API_KEY')
    PLAYHT_DEFAULT_NAME = os.getenv('PLAYHT_DEFAULT_NAME')
    SYSTEM_CONTEXT_INSTRUCTION = os.getenv('SYSTEM_CONTEXT_INSTRUCTION', 'You are a python developer...')
    TEMPERATURE_VALUE = float(os.getenv('TEMPERATURE_VALUE', 0.9))
    MAX_TOKEN_VALUE = int(os.getenv('MAX_TOKEN_VALUE', 1500))
    MAX_CONVERSATION_SIZE = int(os.getenv('MAX_TOKEN_VALUE', 5))
    TOP_K_VALUE = int(os.getenv('TOP_K_VALUE', 20))
    CACHE_EXPIRATION = int(os.getenv('CACHE_EXPIRATION', 3600))
    DB_PATH = os.getenv('DB_PATH', 'conversations.db')
    CONVERSE_PREFIX = os.getenv('CONVERSE_PREFIX', 'converse')
    COLLABORATE_PREFIX = os.getenv('COLLABORATE_PREFIX', 'collaborate')
    PEER_PREFIX = os.getenv('PEER_PREFIX', 'converse')
    IGNORE_BOTS = os.getenv('IGNORE_BOTS', True)
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'GroqModel')
    FOLDER_TO_LOAD = os.getenv('FOLDER_TO_LOAD', 'swarmauri-sdk')
    

    
    global current_model
    current_model = DEFAULT_MODEL
    
    # Initialize the Bot
    bot = lightbulb.BotApp(token=DISCORD_BOT_TOKEN, prefix='!', intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT, ignore_bots=False)
    cache = {}
    
    # Initialize Models
    groq_model = GroqModel(api_key=GROQ_API_KEY, name=GROQ_DEFAULT_NAME)
    deep_infra_model = DeepInfraModel(api_key=DEEPINFRA_API_KEY, name=DEEPINFRA_DEFAULT_NAME)
    openai_model = OpenAIModel(api_key=OPENAI_API_KEY, name=OPENAI_DEFAULT_NAME)
    playht_model = PlayHTModel(user_id=PLAYHT_USER_ID, api_key=PLAYHT_API_KEY)
    
    
    # Initialize Global Conversation and Vector Store
    global_conversation = MaxSystemContextConversation(system_context=SystemMessage(content=SYSTEM_CONTEXT_INSTRUCTION), max_size=MAX_CONVERSATION_SIZE)
    vector_store = TfidfVectorStore()
    
    # Initialize Global Agent
    global_agent = RagAgent(llm=groq_model, conversation=global_conversation, system_context=SystemMessage(content=SYSTEM_CONTEXT_INSTRUCTION), vector_store=vector_store)
    llm_kwargs = {"temperature": TEMPERATURE_VALUE, "max_tokens": MAX_TOKEN_VALUE, "stop":[]}
    thread_agents = {}  # Dictionary to store agents for each thread
    
    # Utility to Load Documents from a Folder
    def load_documents_from_folder(folder_path, include_extensions=None, exclude_extensions=None,
                                   include_folders=None, exclude_folders=None):
        documents = []
        include_all_files = not include_extensions and not exclude_extensions
        include_all_folders = not include_folders and not exclude_folders
    
        for root, dirs, files in os.walk(folder_path):
            current_folder_name = os.path.basename(root)
            if not include_all_folders:
                if include_folders and current_folder_name not in include_folders:
                    logging.info(f"Skipping folder: {current_folder_name}")
                    continue
                if exclude_folders and current_folder_name in exclude_folders:
                    logging.info(f"Skipping folder: {current_folder_name}")
                    continue
    
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_extension = file_name.split(".")[-1]
                if include_all_files or (include_extensions and file_extension in include_extensions) or \
                   (exclude_extensions and file_extension not in exclude_extensions):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            document = Document(content=content, metadata={"filepath": file_path})
                            documents.append(document)
                    except (json.JSONDecodeError, Exception) as e:
                        logging.warning(f"Skipping file: {file_name} ({e})")
        return documents
    
    # Load and Add Documents to Vector Store
    documents = load_documents_from_folder(FOLDER_TO_LOAD, exclude_folders=["__pycache__", "scripts"], exclude_extensions=["mp3", "png", "pdf"])
    vector_store.add_documents(documents)
    print(f"{len(vector_store.documents)} documents added to the vector store.")
    
    # Retry Decorator
    def retry_on_empty(retries=3):
        def decorator(func):
            def wrapper(*args, **kwargs):
                for attempt in range(retries):
                    result = func(*args, **kwargs)
                    if result:
                        print('got a result')
                        return result
                    print('Retrying due to empty result...')
                return result
            return wrapper
        return decorator

    # Function to switch models in a round-robin manner
    def switch_model():
        global current_model_index
        current_model_index = (current_model_index + 1) % len(model_list)
        print(f"Switched to model: {model_list[current_model_index]}")
    
    # Updated converse function to support three models
    @retry_on_empty(retries=2)
    def converse(prompt, agent):
        def get_model_instance():
            # Get the current model instance based on `current_model_index`
            if model_list[current_model_index] == "GroqModel":
                return groq_model
            elif model_list[current_model_index] == "DeepInfraModel":
                return deep_infra_model
            elif model_list[current_model_index] == "OpenAIModel":
                return openai_model
    
        # Try using the current model, with fallback logic to switch models upon failure
        for _ in range(len(model_list)):  # Iterate through all models once if needed
            try:
                agent.llm = get_model_instance()  # Set the agent to use the current model
                return agent.exec(input_data=prompt, top_k=TOP_K_VALUE, llm_kwargs=llm_kwargs)
            except Exception as e:
                logging.warning(f"{model_list[current_model_index]} failed with error: {e}. Switching models.")
                switch_model()  # Switch to the next model
    
        # If all models fail, return an error message
        logging.error("All models failed. Please try again later.")
        return "An error occurred with all models. Please try again later."

    
    def converse_with_cache(prompt, agent):
        if prompt in cache:
            result, timestamp = cache[prompt]
            if time.time() - timestamp < CACHE_EXPIRATION:
                return result
        result = converse(prompt, agent)
        if result:
            cache[prompt] = (result, time.time())
        return result
    
    # Helper to create a unique agent for each thread or channel
    def get_or_create_agent(channel_id):
        if channel_id not in thread_agents:
            conversation = MaxSystemContextConversation(
                system_context=SystemMessage(content=SYSTEM_CONTEXT_INSTRUCTION),
                max_size=MAX_CONVERSATION_SIZE
            )
            agent = RagAgent(
                llm=groq_model,
                conversation=conversation,
                system_context=SystemMessage(content=SYSTEM_CONTEXT_INSTRUCTION),
                vector_store=vector_store
            )
            thread_agents[channel_id] = agent
        return thread_agents[channel_id]
    
    # Slash Command to Create a New Thread and Start a Conversation
    @bot.command
    @lightbulb.option("topic", "The topic for the new thread.", type=str)
    @lightbulb.command("create_thread", "Create a new thread and start a conversation.")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def create_thread_command(ctx: lightbulb.Context):
        topic = ctx.options.topic
        channel_id = ctx.channel_id
    
        # Send initial response
        intro_message = f"A new thread on '{topic}' has been created! Feel free to ask questions here."
        await ctx.respond(intro_message)
    
        # Wait briefly to allow the message to send, then retrieve it
        await asyncio.sleep(1)  # Short delay to ensure message is posted
    
        # Fetch the last message in the channel to get its ID
        messages = await bot.rest.fetch_messages(channel_id)
        message_id = messages[0].id  # Get the ID of the most recent message (sent by ctx.respond)
    
        # Create a new thread in reply to this message
        thread = await bot.rest.create_message_thread(channel_id, message_id, topic)
        thread_id = thread.id
    
        # Initialize a new agent for this thread
        agent = get_or_create_agent(thread_id)
    
    # Prefix Command to Create a New Thread and Start a Conversation
    @bot.command
    @lightbulb.command("create", "Create a new thread and start a conversation.")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def create_thread_from_prefix_command(ctx: lightbulb.Context):
        # Retrieve the topic from the message content
        topic = ctx.event.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:].strip()
        channel_id = ctx.channel_id
    
        # Send initial response
        intro_message = f"A new thread on '{topic}' has been created! Feel free to ask questions here."
        await ctx.respond(intro_message)
    
        # Wait briefly to ensure message is posted, then retrieve it
        await asyncio.sleep(1)  # Short delay to ensure message is posted
    
        # Fetch the last message in the channel to get its ID
        messages = await bot.rest.fetch_messages(channel_id)
        message_id = messages[0].id  # Get the ID of the most recent message (sent by ctx.respond)
    
        # Create a new thread in reply to this message
        thread = await bot.rest.create_message_thread(channel_id, message_id, topic)
        thread_id = thread.id
    
        # Initialize a new agent for this thread
        agent = get_or_create_agent(thread_id)

    
    # Initialize Database and Create/Upgrade Table
    def init_db():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Create or modify table to store conversations with required fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT,
                sender_id TEXT,
                model_class TEXT,
                model_name TEXT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    # Insert a conversation record with all necessary fields
    def log_conversation(channel_id, sender_id, model_class, model_name, prompt, response):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (channel_id, sender_id, model_class, model_name, prompt, response, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (channel_id, sender_id, model_class, model_name, prompt, response, datetime.now()))
        conn.commit()
        conn.close()
    
    # Updated converse_command to log conversations with extended details
    @bot.command
    @lightbulb.command(CONVERSE_PREFIX, "Interact with the bot using the AI agent.")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def converse_command(ctx: lightbulb.Context):
        prompt = ctx.event.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:].strip()
        thread_id = ctx.channel_id
        sender_id = str(ctx.author.id)
    
        # Check if the user has attached a file
        file_content = ""
        if ctx.event.message.attachments:
            attachment = ctx.event.message.attachments[0]
            
            # Read the file content
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as response:
                    if response.status == 200:
                        try:
                            file_content = await response.text()
                        except UnicodeDecodeError:
                            await ctx.respond("Sorry, I could not read the attached file. Make sure it's a text file.")
                            return
    
        # Combine prompt and file content if both are provided
        combined_input = f"{prompt}\n\n{file_content}".strip() if prompt or file_content else "No input provided."
    
        # Get or create agent for the specific thread
        agent = get_or_create_agent(thread_id)
        await ctx.respond("Processing your request...", flags=hikari.MessageFlag.EPHEMERAL)
    
        # Converse with agent and get response
        result = converse_with_cache(combined_input, agent)
    
        # Log the conversation details in the database
        model_class = agent.llm.__class__.__name__
        model_name = agent.llm.name
        log_conversation(channel_id=thread_id, sender_id=sender_id, model_class=model_class, model_name=model_name, prompt=combined_input, response=result)
    
        # Send response based on length
        if len(result) == 0:
            await ctx.respond("I couldn't generate a response. Please try again.")
        elif len(result) > 2000:
            file_bytes = io.BytesIO(result.encode('utf-8'))
            await ctx.respond("The response is too lengthy. Sending as an attachment...", attachment=hikari.Bytes(file_bytes, "response.md"))
        else:
            await ctx.respond(result)


    # Define the new command to generate audio
    @bot.command
    @lightbulb.command("speak", "Generate audio from text using the PlayHT model.")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def speak_command(ctx: lightbulb.Context):
        # Extract the text to convert to speech
        text_to_speak = ctx.event.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:].strip()
        
        # Check if there's text provided
        if not text_to_speak:
            await ctx.respond("Please provide the text you want to convert to audio.")
            return
    
        # Generate audio using PlayHT model
        try:
            # This assumes PlayHTModel has a `predict` method that outputs binary audio data
            audio_data = playht_model.predict(text=text_to_speak)
            
            # Create a temporary file for the audio output
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(audio_data)
                audio_file_path = tmp_file.name
            
            # Send the audio file back as an attachment
            await ctx.respond("Here is the generated audio:", attachment=hikari.File(audio_file_path, "output.mp3"))
        
        except Exception as e:
            logging.error(f"Failed to generate audio: {e}")
            await ctx.respond("Sorry, I couldn't generate audio. Please try again later.")
    
        # Clean up the temporary file if needed
        finally:
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

    
    # Define a general error handler for your bot commands
    @bot.listen(lightbulb.CommandErrorEvent)
    async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
        # Capture the context and the exception from the event
        ctx = event.context
        exception = event.exception
        return
        
        # Handle specific error types
        if isinstance(exception, errors.CommandNotFound):
            await ctx.respond("Sorry, that command doesn't exist. Please check the available commands.")
        elif isinstance(exception, errors.MissingRequiredArgument):
            await ctx.respond("It looks like you're missing an argument. Please check the command format.")
        elif isinstance(exception, errors.CheckFailure):
            await ctx.respond("You don't have permission to use this command.")
        elif isinstance(exception, errors.CommandInvocationError):
            await ctx.respond("An error occurred while executing the command. Please try again.")
        else:
            # Log unexpected errors for further inspection
            logging.error(f"Unexpected error: {exception}")
            await ctx.respond("Oops, something went wrong. Please try again later.")

    async def reconnect_if_disconnected():
        while True:
            if not bot.is_alive:
                print("Connection lost, attempting to reconnect...")
                await bot.close()
                await bot.start()
            await asyncio.sleep(10)  # Check every 10 seconds for faster reconnection

    @bot.listen(hikari.StartedEvent)
    async def on_start(event):
        init_db()
        print("Bot is online and started!")
        asyncio.create_task(reconnect_if_disconnected())
    
    @bot.listen(hikari.StoppedEvent)
    async def bot_stop(event):
        print('\nBot stopping successfully.\n')

    bot.run()

if __name__ == "__main__":
    main()
    
