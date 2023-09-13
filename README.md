# Thiết lập ban đầu
### Khởi động container
```
docker compose up -d --build 
```

Server sẽ chạy ở localhost:8000

### Database
Có thể xem ở MongoDB Compass với URI:
```
mongodb+srv://admin:admin123@cluster0.ymqhm3k.mongodb.net/?retryWrites=true&w=majority
```

### Quy ước:
1. Toàn bộ dữ liệu được lưu trong database `db`
2. Collection user: lưu các thông tin về user
3. ... (còn tiếp)

# API

FastAPI hỗ trợ tạo doc tự động với Swagger UI tại `localhost:8000/docs`

Sau đây là các nhóm API

### Default: kiểm tra xem server đã khởi động chưa
GET: `localhost:8000`

Output:
```json
{
  "Hello": "World"
}
```

### Register: các chức năng đăng kí (hiện tại chỉ có 1 cách)

### Login: các chức năng đăng nhập (gồm đăng nhập với tài khoản đã đăng kí và đăng nhập với gmail)
Đăng nhập với google: nhận vào json, bắt buộc phải có gmail từ đó query vào mongo để trả về user nếu có rồi, hoặc tạo mời user nếu chưa có với pass 123 (sau này sẽ thay đổi)

GET: localhost:8000/api/login-google

Input: JSON
```json
{
    "gmail": "shiraishi2612@gmail.com",
    "username": "Đoàn Dũng"
}
```

Output:
```json
{
  "_id": "64f2fa942cd8a9ca30f44676",
  "gmail": "shiraishi2612@gmail.com",
  "username": "Đoàn Dũng",
  "password": 123
}
```

(còn tiếp)



