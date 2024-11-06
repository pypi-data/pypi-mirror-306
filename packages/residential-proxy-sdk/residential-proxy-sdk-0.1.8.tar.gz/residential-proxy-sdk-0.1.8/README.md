# ProxySDK

ProxySDK là một giải pháp proxy xoay dân cư cho các dự án tại Việt Nam, đặc biệt phù hợp cho MMO và Airdrop.

## Nội Dung

- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [API](#api)
- [Đóng góp](#đóng-góp)
- [Giấy phép](#giấy-phép)

## Giới thiệu

ProxySDK cung cấp các tính năng chính như quản lý proxy, xoay IP theo tỉnh, và tích hợp dễ dàng vào các dự án hiện có.

## Cài đặt

Cài đặt với `pip`:

```bash
pip install residential-proxy-sdk
```

## Sử dụng

Hướng dẫn cách sử dụng dự án. Dưới đây là một ví dụ mã nguồn:

```python
from residential_proxy_sdk import ProxySDK

# Khởi tạo SDK
sdk = ProxySDK("https://vinproxy.net", "YOUR_API_KEY")

# Đăng nhập
login_result = sdk.login("username", "password")

# Lấy danh sách tỉnh
provinces = sdk.get_provinces()
print(provinces)

# Lấy IP mới từ một tỉnh cụ thể
new_ip = sdk.get_new_ip("your_proxy_key", province_id=1)
print(new_ip)
```

## API

ProxySDK cung cấp các API sau:

### Quản lý tài khoản

#### Đăng nhập

- **Phương thức**: `login(username: str, password: str)`
- **Mô tả**: Đăng nhập vào hệ thống.
- **Tham số**:
  - `username`: Tên đăng nhập
  - `password`: Mật khẩu

#### Đăng ký

- **Phương thức**: `register(username: str, email: str, password: str)`
- **Mô tả**: Đăng ký tài khoản mới.
- **Tham số**:
  - `username`: Tên đăng nhập
  - `email`: Email
  - `password`: Mật khẩu

#### Quên mật khẩu

- **Phương thức**: `forgot_password(email: str)`
- **Mô tả**: Yêu cầu đặt lại mật khẩu.
- **Tham số**:
  - `email`: Email đăng ký

#### Đặt lại mật khẩu

- **Phương thức**: `reset_password(token: str, new_password: str)`
- **Mô tả**: Đặt lại mật khẩu với token được cung cấp.
- **Tham số**:
  - `token`: Token xác thực
  - `new_password`: Mật khẩu mới

### Quản lý Proxy

#### Lấy danh sách tỉnh

- **Phương thức**: `get_provinces(search_text: str = None)`
- **Mô tả**: Trả về danh sách các tỉnh thành có sẵn proxy.
- **Tham số**:
  - `search_text` (tùy chọn): Chuỗi tìm kiếm để lọc danh sách tỉnh.

#### Lấy IP mới

- **Phương thức**: `get_new_ip(proxy_key: str, province_id: int = None)`
- **Mô tả**: Lấy một IP mới từ proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy
  - `province_id` (tùy chọn): ID của tỉnh cần lấy IP

#### Lấy IP hiện tại

- **Phương thức**: `get_current_ip(proxy_key: str)`
- **Mô tả**: Lấy thông tin IP hiện tại của proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy

#### Xóa IP cũ

- **Phương thức**: `remove_old_ip(proxy_key: str)`
- **Mô tả**: Xóa IP cũ của proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy

### Quản lý khóa Proxy

#### Lấy danh sách khóa

- **Phương thức**: `get_key_list()`
- **Mô tả**: Lấy danh sách các khóa proxy của người dùng.

#### Lấy chi tiết khóa

- **Phương thức**: `get_key_detail(proxy_key: str)`
- **Mô tả**: Lấy thông tin chi tiết của một khóa proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy cần lấy thông tin

#### Mua khóa mới

- **Phương thức**: `buy_new_key(buy_key_dto: dict)`
- **Mô tả**: Thực hiện giao dịch mua khóa proxy mới.
- **Tham số**:
  - `buy_key_dto`: Đối tượng chứa thông tin mua khóa mới

#### Gia hạn khóa

- **Phương thức**: `renew_key(renew_key_dto: dict)`
- **Mô tả**: Gia hạn một khóa proxy hiện có.
- **Tham số**:
  - `renew_key_dto`: Đối tượng chứa thông tin gia hạn khóa

#### Xóa khóa

- **Phương thức**: `remove_key(proxy_key: str)`
- **Mô tả**: Xóa một khóa proxy.
- **Tham số**:
  - `proxy_key`: Khóa proxy cần xóa

### Thông tin người dùng

#### Lấy thông tin người dùng

- **Phương thức**: `get_user_info()`
- **Mô tả**: Lấy thông tin của người dùng hiện tại.

## Đóng góp

Chúng tôi rất hoan nghênh mọi đóng góp cho ProxySDK. Nếu bạn muốn đóng góp, vui lòng làm theo các bước sau:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit các thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

# residential-proxy-sdk
