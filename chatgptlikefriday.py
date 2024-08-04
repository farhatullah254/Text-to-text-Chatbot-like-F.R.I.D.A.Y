import time
import gradio as gr
import openai

def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.05)
        yield "You typed: " + message[: i + 1]
custom_css = """
.gradio-container {
height:100% !important;
width:100% !Important;
background-color:black !important;

}
.main.svelte-wpkpf6 {
display: flex !important;
    height: 100% !important;
}

.lg.primary.svelte-cmf5ev {
background-color:#0000ff !important;
    color: white;

    
}
"""

openai.api_key = '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'

farhat_ullah_bio = "Farhat Ullah is developer of F.R.I.D.A.Y skilled in Web Development Python, WordPress, HTML, CSS, PHP, Python web scraping, and automation. He has experience in creating websites and automating tasks, and aims to portray himself as a technical expert proficient in coding."

response_cache = {}

def get_chatgpt_response(user_message: str, max_retries: int=5) -> str:
    if user_message in response_cache:
        return response_cache[user_message]
    
    try:
        messages = [
            {"role": "system", "content": "HI! I'm, F.R.I.D.A.Y developed by Farhat Ullah. I can help with various tasks and information that usually can be daunting to find via Search Engines."},
            {"role": "user", "content": user_message}
        ]
        instructions = [
            {"role": "system", "content": "Provide short, concise responses suitable for a quick understanding or brief descriptions."}
        ]

        messages = instructions + messages

        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=messages,
                     temperature=0.1,  # Adjust temperature for more focused responses
                    n=1,
                    max_tokens=150  # Limiting the response length
                    )
                
                
                assistant_message = response.choices[0].message.content
                response_cache[user_message] = assistant_message
                return assistant_message
            
            except openai.error.RateLimitError as e:
                if attempt == max_retries - 1:
                    return f"Error: Rate limit exceeded. Please try again later. Details: {str(e)}"
                
                wait_time = (2 ** attempt) + random.random()  # Exponential backoff with jitter
                print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            
            except Exception as e:
                return f"Error in get_chatgpt_response: {str(e)}"

    except Exception as e:
        return f"Error in get_chatgpt_response: {str(e)}"

def respond(user_message: str, history: list) -> str:
    print(f"User message: {user_message}")
    print(f"History: {history}")
    keywords = ["farhat ullah", "who developed you", "do you know about farhat ullah", "who is your developer"]
    if any(keyword in user_message.lower() for keyword in keywords):
        response = farhat_ullah_bio
    elif "may i know your name" in user_message.lower():
        names = ["I'm F.R.I.D.A.Y, your helpful assistant developed by Farhat Ullah.", "You can call me F.R.I.D.A.Y.", "Hello, I'm F.R.I.D.A.Y, here to assist you."]
        response = random.choice(names)
    else:
        response = get_chatgpt_response(user_message)
    
    if not history:
        response = "Welcome, I'm F.R.I.D.A.Y, your helpful assistant developed by Farhat Ullah. \n" + response
    
    print(f"Returning: {response}")
    return response

demo = gr.ChatInterface(slow_echo,
                        theme="soft",
                        css="custom_css",
                        chatbot=gr.Chatbot(height=620),
                        textbox=gr.Textbox(placeholder="Who is Donald Trump?", container=False, scale=7),
                        
                
                       ) 

                        
demo.launch()
