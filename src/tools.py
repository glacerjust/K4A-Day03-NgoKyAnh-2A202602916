"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "query_job_requirements",
        "description": "Tra cứu tiêu chí tuyển dụng cho một vị trí công việc cụ thể.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "Tên vị trí công việc cần tra cứu (ví dụ: 'Data Scientist', 'AI Engineer')"
                }
            },
            "required": ["job_title"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_interview'
    # --------------------------------------------------------------------------
    {
        "name": "schedule_interview",
        "description": "Đặt lịch hẹn phỏng vấn cho ứng viên với nhà tuyển dụng.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần đặt lịch (ví dụ: 'UV2024001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 20/10/2026')"
                },
                "interviewer_name": {
                    "type": "string",
                    "description": "Tên người phỏng vấn"
                }
            },
            "required": ["candidate_id", "datetime_str"]
        }
    },
    
    {
        "name": "query_candidate_profile",
        "description": "Tra cứu hồ sơ ứng viên bằng mã ứng viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Mã ứng viên cần tra cứu (ví dụ: 'UV2024001', 'UV2024002')"
                }
            },
            "required": ["candidate_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_JOB_DB = {
    "DATA SCIENTIST": {
        "department": "Khối AI & Data",
        "level": "Middle/Senior",
        "requirements": [
            "Tối thiểu 2 năm kinh nghiệm làm việc với Python, SQL.",
            "Có kinh nghiệm xây dựng các mô hình Machine Learning/Deep Learning.",
            "Kỹ năng xử lý dữ liệu lớn (Big Data)."
        ],
        "salary_range": "2000$ - 3500$"
    },
    "AI ENGINEER": {
        "department": "Khối AI & Data",
        "level": "Junior/Middle",
        "requirements": [
            "Có kiến thức vững về LLM, NLP, Computer Vision.",
            "Thành thạo PyTorch hoặc TensorFlow.",
            "Tiếng Anh đọc hiểu tài liệu chuyên ngành tốt."
        ],
        "salary_range": "1500$ - 2500$"
    }
}

MOCK_CANDIDATE_DB = {
    "UV2024001": {
        "full_name": "Nguyễn Văn An",
        "applied_position": "AI Engineer",
        "experience": "1 năm",
        "skills": ["Python", "PyTorch", "NLP", "LLM"],
        "email": "an.nv@email.com",
        "status": "Đang chờ phỏng vấn"
    },
    "UV2024002": {
        "full_name": "Trần Thị Bình",
        "applied_position": "Data Scientist",
        "experience": "3 năm",
        "skills": ["Python", "SQL", "Machine Learning", "Spark"],
        "email": "binh.tt@email.com",
        "status": "Đang xem xét CV"
    }
}


def execute_query_job_requirements(job_title: str) -> str:
    """Thực thi tra cứu tiêu chí tuyển dụng"""
    job = MOCK_JOB_DB.get(job_title.strip().upper())
    if job:
        return json.dumps({
            "status": "SUCCESS",
            "job_title": job_title,
            "data": job
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy vị trí tuyển dụng '{job_title}'"
        }, ensure_ascii=False)

def execute_query_candidate_profile(candidate_id: str) -> str:
    """Thực thi tra cứu hồ sơ ứng viên"""
    candidate = MOCK_CANDIDATE_DB.get(candidate_id.strip().upper())
    if candidate:
        return json.dumps({
            "status": "SUCCESS",
            "candidate_id": candidate_id,
            "data": candidate
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy hồ sơ ứng viên có mã '{candidate_id}'"
        }, ensure_ascii=False)

def execute_schedule_interview(candidate_id: str, datetime_str: str, interviewer_name: str = "HR Dept") -> str:
    """Thực thi đặt lịch phỏng vấn"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"INT-{candidate_id}-99",
        "candidate_id": candidate_id,
        "datetime": datetime_str,
        "interviewer": interviewer_name,
        "message": f"Đặt lịch phỏng vấn thành công cho ứng viên {candidate_id} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "query_job_requirements": execute_query_job_requirements,
    "query_candidate_profile": execute_query_candidate_profile,
    "schedule_interview": execute_schedule_interview
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
