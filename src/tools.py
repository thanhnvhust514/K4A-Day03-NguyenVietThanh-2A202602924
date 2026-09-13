"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Chủ đề: Gợi ý 1.2 — Trợ lý Quản lý Thư viện & Tài liệu VinUni
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu học vụ sinh viên (hỗ trợ xác thực sinh viên mượn sách & TC02)
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn tư vấn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập phụ trách (ví dụ: 'PGS.TS Nguyễn Văn A')"
                }
            },
            "required": ["student_id", "datetime_str"]
        }
    },

    # --------------------------------------------------------------------------
    # TOOL CHỦ ĐỀ 1.2 (THƯ VIỆN & TÀI LIỆU): library_query
    # --------------------------------------------------------------------------
    {
        "name": "library_query",
        "description": "Tra cứu thông tin, vị trí lưu trữ và tình trạng mượn/trả của sách trong thư viện VinUni bằng mã sách (book_id).",
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "Mã sách cần tra cứu trong thư viện (ví dụ: 'B2026001', 'B2026002')"
                }
            },
            "required": ["book_id"]
        }
    },

    # --------------------------------------------------------------------------
    # TOOL CHỦ ĐỀ 1.2 (THƯ VIỆN & TÀI LIỆU): renew_book
    # --------------------------------------------------------------------------
    {
        "name": "renew_book",
        "description": "Gia hạn thời gian mượn sách hoặc đăng ký mượn sách thư viện VinUni cho sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên yêu cầu gia hạn/mượn sách (ví dụ: 'SV2026001')"
                },
                "book_id": {
                    "type": "string",
                    "description": "Mã cuốn sách cần gia hạn hoặc mượn (ví dụ: 'B2026001')"
                },
                "days": {
                    "type": "integer",
                    "description": "Số ngày muốn gia hạn thêm (mặc định là 7 ngày)"
                }
            },
            "required": ["student_id", "book_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

MOCK_LIBRARY_DATABASE = {
    "B2026001": {
        "title": "Machine Learning Yearning",
        "author": "Andrew Ng",
        "category": "Trí tuệ nhân tạo / Khoa học máy tính",
        "status": "Đang được mượn",
        "borrower_id": "SV2026001",
        "due_date": "20/09/2026",
        "location": "Kệ A3-Tầng 2 Thư viện VinUni"
    },
    "B2026002": {
        "title": "Deep Learning with Python",
        "author": "François Chollet",
        "category": "Trí tuệ nhân tạo / Học sâu",
        "status": "Sẵn sàng (Còn sách)",
        "borrower_id": None,
        "due_date": None,
        "location": "Kệ A1-Tầng 2 Thư viện VinUni"
    }
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


def execute_library_query(book_id: str) -> str:
    """Thực thi tra cứu thông tin sách trong thư viện VinUni"""
    book_id_clean = book_id.strip().upper()
    book = MOCK_LIBRARY_DATABASE.get(book_id_clean)
    if book:
        return json.dumps({
            "status": "SUCCESS",
            "book_id": book_id_clean,
            "data": book,
            "message": f"Cuốn sách '{book['title']}' (Mã: {book_id_clean}) của tác giả {book['author']}. Tình trạng: {book['status']}. Vị trí: {book['location']}."
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "book_id": book_id_clean,
            "message": f"Không tìm thấy thông tin cuốn sách có mã '{book_id_clean}' trong cơ sở dữ liệu thư viện VinUni."
        }, ensure_ascii=False)


def execute_renew_book(student_id: str, book_id: str, days: int = 7) -> str:
    """Thực thi gia hạn hoặc mượn sách thư viện VinUni"""
    book_id_clean = book_id.strip().upper()
    student_id_clean = student_id.strip().upper()
    book = MOCK_LIBRARY_DATABASE.get(book_id_clean)
    
    if not book:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không thể gia hạn: Sách '{book_id_clean}' không tồn tại trong hệ thống thư viện."
        }, ensure_ascii=False)
        
    return json.dumps({
        "status": "SUCCESS",
        "transaction_id": f"LIB-{student_id_clean}-{book_id_clean}",
        "student_id": student_id_clean,
        "book_id": book_id_clean,
        "book_title": book["title"],
        "extended_days": days,
        "new_due_date": "27/09/2026",
        "message": f"Đã gia hạn thành công cuốn sách '{book['title']}' ({book_id_clean}) thêm {days} ngày cho sinh viên {student_id_clean}. Hạn trả mới: 27/09/2026."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment,
    "library_query": execute_library_query,
    "renew_book": execute_renew_book
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
