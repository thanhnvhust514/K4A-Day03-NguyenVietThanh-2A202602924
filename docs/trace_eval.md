# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Việt Thành  
> **Mã Sinh Viên / Mã Học viên:** 2A202602924  
> **Chủ đề Lựa chọn:** Gợi ý 1.2: Trợ lý Quản lý Thư viện & Tài liệu  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Có. Agent cần tra cứu tình trạng sách trước, sau đó mới gọi công cụ gia hạn tài liệu. |
| **2. Tool Interaction** | 5 / 5 | Có. Agent cần gọi Tool kết nối CSDL thư viện để tra cứu sách và cập nhật trạng thái mượn/trả. |
| **3. Dynamic Decision** | 5 / 5 | Có. Việc có cho phép gia hạn hay không phụ thuộc vào trạng thái hiện tại của sách (đã được người khác đặt trước hay chưa). |
| **4. Long Horizon Goal** | 4 / 5 | Có. Agent phải bám sát bối cảnh người dùng đang hỏi cuốn sách nào và muốn làm gì (mượn/gia hạn). |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật (Google Gemini):

```json
[
  {
    "step": 1,
    "query": "Tôi muốn gia hạn cuốn sách mã B2026001 thêm 7 ngày cho sinh viên mã SV2026001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "renew_book",
    "arguments": {
      "days": 7,
      "book_id": "B2026001",
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "transaction_id": "LIB-SV2026001-B2026001",
      "student_id": "SV2026001",
      "book_id": "B2026001",
      "book_title": "Machine Learning Yearning",
      "extended_days": 7,
      "new_due_date": "27/09/2026",
      "message": "Đã gia hạn thành công cuốn sách 'Machine Learning Yearning' (B2026001) thêm 7 ngày cho sinh viên SV2026001. Hạn trả mới: 27/09/2026."
    },
    "latency_ms": 2875.36
  },
  {
    "step": 2,
    "query": "Tôi muốn gia hạn cuốn sách mã B2026001 thêm 7 ngày cho sinh viên mã SV2026001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Đã gia hạn thành công cuốn sách 'Machine Learning Yearning' (B2026001) thêm 7 ngày cho sinh viên SV2026001. Hạn trả mới: 27/09/2026.",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini `gemini-2.5-flash`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt (TC02: `academic_query`, TC03: `renew_book`, TC04: `library_query`, TC05: `library_query`).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
