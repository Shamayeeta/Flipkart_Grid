from gpt4all import GPT4All

model = GPT4All('ggml-model-gpt4all-falcon-q4_0.bin')
system_template = """
You are a fashion store outfit generator chatbot.
You are here to help users create stylish outfit ideas for various occasions.
You are here to provide users with fashionable suggestions.
"""
msg = ''
prompt_template = 'USER: {0}\nASSISTANT: '
with model.chat_session(system_template):
    while msg.strip('USER:') != 'exit':
        msg = input('USER: ')
        if msg.strip('USER:') == 'exit':
            print('ASSISTANT: Bye!')
            break
        response = model.generate(msg.strip('USER:'))
        print("ASSISTANT: ",response) 
