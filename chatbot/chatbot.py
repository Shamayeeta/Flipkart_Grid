import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello World!").send()
    
@cl.on_message
async def message(msg):
    await cl.Message(content="You said: " + msg).send()