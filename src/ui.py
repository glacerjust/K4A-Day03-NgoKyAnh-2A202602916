import gradio as gr
import json
from app import run_react_agent
from providers import get_llm_provider
from mcp_server import MCPRecruitmentServer
from dotenv import load_dotenv

# Tải cấu hình biến môi trường
load_dotenv()

# Khởi tạo các thành phần Core
provider = get_llm_provider()
mcp_server = MCPRecruitmentServer()

def chat_interface(user_message, history):
    """
    Xử lý tin nhắn từ UI, đẩy vào Core ReAct Agent và trả kết quả về UI.
    """
    if not user_message.strip():
        return "", history

    # Chạy ReAct Loop
    logs = run_react_agent(user_message, provider, mcp_server)
    
    # Lấy câu trả lời cuối cùng từ log (Final Answer)
    final_answer = "Xin lỗi, tôi không thể xử lý yêu cầu này."
    if logs and logs[-1].get("action_type") == "FINAL_ANSWER":
        final_answer = logs[-1].get("output", final_answer)
        
    # Tạo nội dung Thought Process (để hiển thị dưới dạng accordion/debug trong UI nếu cần)
    thought_process = ""
    for log in logs:
        if log.get("action_type") == "TOOL_EXECUTION":
            thought_process += f"🛠️ **Gọi công cụ:** `{log.get('tool_name')}`\n"
            thought_process += f"👁️ **Kết quả (Observation):** {json.dumps(log.get('observation'), ensure_ascii=False)}\n\n"
        elif log.get("action_type") == "FINAL_ANSWER":
            thought_process += f"🧠 **Suy luận (Thought):** {log.get('thought')}\n"

    # Trả về câu trả lời cho chat interface
    return final_answer

# Xây dựng giao diện Gradio Blocks
with gr.Blocks(title="Trợ lý Tuyển dụng AI") as demo:
    gr.Markdown("# 🏢 TRỢ LÝ AI TUYỂN DỤNG & SÀNG LỌC CV")
    gr.Markdown(f"**LLM Provider:** {provider.__class__.__name__} | **MCP Server:** {mcp_server.server_name}")
    
    chatbot = gr.ChatInterface(
        fn=chat_interface,
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(placeholder="Nhập câu hỏi, ví dụ: 'Hãy tra cứu thông tin ứng viên UV2024001'", container=False, scale=7),
        title="Giao diện Tương tác Agent",
        description="Trợ lý ReAct (Reasoning + Acting) tự động suy luận và sử dụng công cụ MCP Server để giải quyết tác vụ nhân sự.",
        examples=[
            "Quy trình tuyển dụng của công ty như thế nào?",
            "Hãy tra cứu tiêu chí tuyển dụng cho vị trí Data Scientist",
            "Kiểm tra thông tin của ứng viên UV2024001",
            "Đặt lịch phỏng vấn cho UV2024001 vào lúc 14:00 chiều mai"
        ]
    )

if __name__ == "__main__":
    print("🚀 Đang khởi động Web UI (Gradio)...")
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
