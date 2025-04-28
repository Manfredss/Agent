import gradio as gr
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

model = ''

def seleceModel(modelName: str) -> str:
    global model
    model = modelName
    # 调试
    print(f"Model selected: {model}")
def echo(message: str, history: list) -> list:
    return message

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# A Simple AI Agent")
        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown("### Select Your Model")
                selModel = gr.Dropdown(choices=['ChatGPT o4-mini', 'QWen', 'DeepSeek R1'], 
                                        value='ChatGPT o4-mini',
                                        label='Select Your Model')
                chatbot = gr.ChatInterface(fn=echo,
                                            type="messages",
                                            examples=['Hello!', 'Hello! Good to see you!'])
            with gr.Column(scale=3):
                gr.Markdown("### Reasoning Process")
                gr.Textbox(label="Reasoning Process", placeholder="Reasoning Process", interactive=False, lines=10)
            
        selModel.change(fn=seleceModel,
                        inputs=selModel,
                        outputs=[])
    demo.launch()

if __name__ == "__main__":
    main()
