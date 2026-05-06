# Genetic Algorithm Assignment

**Sinh viên thực hiện:** Nguyễn Tiến Đạt  
**MSSV:** 2410712

## Giới thiệu
Dự án này triển khai thuật toán di truyền (Genetic Algorithm) để giải quyết hai bài toán tối ưu hóa: **One Max** và **0/1 Knapsack**. Thuật toán được hiện thực hóa bằng hai phương pháp lập trình khác nhau: Lập trình hướng đối tượng (OOP) và Lập trình hàm (FP).

## Cấu trúc thư mục
- `oop/`: Triển khai theo mô hình Hướng đối tượng.
- `fp/`: Triển khai theo mô hình Lập trình hàm.
- `reports/`: Chứa các tệp kết quả JSON và biểu đồ tiến trình.
- `visualize_results.py`: Script dùng để vẽ đồ thị so sánh.

## Hướng dẫn sử dụng

Để chạy phiên bản OOP:
```bash
python oop/run.py
```

Để chạy phiên bản FP:
```bash
python fp/run.py
```

Để vẽ lại biểu đồ:
```bash
python visualize_results.py
```

Để chạy unit tests:
```powershell
# Test OOP
cd oop
python -m unittest discover -s tests -v
cd ..

# Test FP
cd fp
python -m unittest discover -s tests -v
cd ..
```

## Kết quả thí nghiệm

Dưới đây là kết quả thực nghiệm sau 300 thế hệ (Generations) với `seed = 42`. 

| Problem | OOP Best Fitness | FP Best Fitness |
|---|---:|---:|
| OneMax | 100 | 100 |
| Knapsack | 3709 | 3725 |


## Phân tích nâng cao: Tính mở rộng và Phân tích kết quả thực nghiệm

### 1. Thiết kế có khả năng mở rộng (Extensible Design)
Kiến trúc của cả hai phiên bản đều được thiết kế để dễ dàng mở rộng mà không cần thay đổi logic cốt lõi của bộ máy GA:

- **Trong OOP**: Việc áp dụng **Strategy Pattern** cho phép ta thêm các phương pháp chọn lọc mới (như Roulette Wheel, Rank Selection), các kiểu lai ghép (như Two-point, Uniform) hay các kiểu đột biến khác chỉ bằng cách hiện thực hóa các Interface tương ứng (`SelectionStrategy`, `CrossoverStrategy`, `MutationStrategy`). Lớp `GeneticAlgorithm` đóng vai trò là một "orchestrator" thuần túy, hoàn toàn độc lập với chi tiết của các toán tử.
- **Trong FP**: Tính mở rộng được thể hiện qua việc sử dụng các hàm bậc cao. Ta có thể thay đổi hành vi của GA chỉ bằng cách truyền các hàm (function passing) khác nhau vào hàm `run_ga_fp`.
- **Tái sử dụng pipeline**: Cả OneMax và Knapsack đều sử dụng chung một quy trình tiến hóa; sự khác biệt duy nhất nằm ở hàm đánh giá Fitness và dữ liệu bài toán, minh chứng cho tính module hóa cao.

| Điểm mở rộng | Cách tiếp cận OOP | Cách tiếp cận FP |
|---|---|---|
| Hàm Fitness mới | Tạo class kế thừa `Problem` | Truyền hàm Fitness thuần túy mới |
| Phương pháp chọn lọc | Implement `SelectionStrategy` | Truyền hàm selection mới |
| Toán tử lai ghép | Implement `CrossoverStrategy` | Truyền hàm crossover mới |
| Toán tử đột biến | Implement `MutationStrategy` | Truyền hàm mutation mới |
| Bài toán benchmark mới | Tái sử dụng `GeneticAlgorithm` | Tái sử dụng `run_ga_fp` |

### 2. Hành vi hội tụ (Convergence Behavior)
Dựa trên các biểu đồ tại `reports/onemax_curve.png` và `reports/knapsack_curve.png`, ta có thể rút ra các nhận xét sau:

- **Bài toán OneMax**: Có không gian tìm kiếm (search landscape) trơn tru. Thuật toán hội tụ rất nhanh về giá trị tối ưu 100. Việc cả hai phiên bản đều đạt 100 khẳng định các toán tử và tham số GA đã được thiết lập chính xác.
- **Bài toán Knapsack**: Phức tạp hơn do có các vùng "phẳng" (fitness 0 khi vượt quá tải trọng). Đồ thị hội tụ có thể xuất hiện các bước nhảy lớn hoặc các giai đoạn đi ngang lâu hơn.
- **Vai trò của Elitism (e=2)**: Giúp bảo tồn những cá thể tốt nhất qua từng thế hệ, ngăn chặn sự suy giảm fitness ngẫu nhiên và đảm bảo đường cong "Best Fitness" luôn là hàm không giảm.

### 3. Đánh đổi kỹ thuật giữa OOP và FP
- **OOP** mạnh về việc đóng gói trạng thái và mô hình hóa các thực thể, phù hợp để xây dựng các Framework GA lớn và phức tạp.
- **FP** vượt trội về tính an toàn, dễ dàng viết Unit Test (vì không có side-effects) và đảm bảo tính tất định cao. Dù FP có chi phí bộ nhớ lớn hơn do phải sinh các `tuple` mới liên tục, nhưng nó mang lại sự tường minh tuyệt đối về dòng chảy dữ liệu (data flow).

### 4. Hạn chế và Cải tiến tương lai
Mặc dù kết quả hiện tại là khả quan, dự án vẫn có những hướng có thể phát triển thêm:
- **Phân tích thống kê**: Hiện tại chỉ sử dụng một `seed=42`. Để có kết luận khoa học hơn, cần chạy trên nhiều seed khác nhau (ví dụ 30-50 seeds) để báo cáo giá trị trung bình (mean) và độ lệch chuẩn (std dev).
- **Cải tiến toán tử**: Áp dụng **Adaptive Mutation Rate** (tỷ lệ đột biến tự điều chỉnh) hoặc sử dụng **Repair Function** để biến các nhiễm sắc thể lỗi (vượt quá tải trọng) trong Knapsack thành các giải pháp hợp lệ thay vì gán fitness 0.
- **Bài toán mới**: Thử nghiệm với các bài toán có không gian tìm kiếm lừa dối hơn như Deceptive Trap hay LeadingOnes.

## Reproducibility

Tính tái lập (Reproducibility) là yếu tố tiên quyết trong các nghiên cứu thuật toán tiến hóa. Dự án đảm bảo tính tái lập như sau:
- **OOP Implementation**: Quá trình tiến hóa được kiểm soát bằng cách thiết lập `random.seed(42)` tại cấp độ thực nghiệm (`run.py`). Riêng việc khởi tạo bài toán Knapsack sử dụng instance `random.Random(seed)` nội bộ để tránh làm thay đổi trạng thái ngẫu nhiên toàn cục một cách không cần thiết.
- **FP Implementation**: Tính ngẫu nhiên được kiểm soát thông qua việc truyền giá trị seed cụ thể hoặc sử dụng các đối tượng RNG cục bộ, giúp kết quả mang tính tất định với cùng một đầu vào và seed. Phương pháp này giúp loại bỏ sự phụ thuộc vào trạng thái ngẫu nhiên toàn cục có thể thay đổi (global mutable state).

## Giải thích thiết kế OOP và FP

### Thiết kế Hướng đối tượng (OOP)
Phiên bản OOP được thiết kế với tính đóng gói (Encapsulation) cao và mô-đun hóa độc lập:
- Lớp `Chromosome`: Đóng gói chuỗi gen và fitness. Gen bên trong được bảo vệ và chỉ trả về bản sao khi được truy xuất.
- Lớp `Population`: Quản lý quần thể, danh sách `individuals` được bảo vệ bằng cách chỉ trả về immutable view (tuple). Việc cập nhật được kiểm soát nghiêm ngặt qua hàm `replace()`.
- **Strategy Pattern**: Ứng dụng interface (`SelectionStrategy`, `CrossoverStrategy`, `MutationStrategy`) giúp quy trình tiến hóa trong `GeneticAlgorithm` linh hoạt, không bị phụ thuộc vào cài đặt chi tiết của các toán tử.

### Thiết kế Lập trình hàm (FP)
Phiên bản FP được thiết kế theo hướng lập trình hàm, hạn chế **side effects** và ưu tiên dữ liệu **bất biến (immutable)**:
- Không sử dụng bất kỳ Class hay global mutable state nào. Quần thể, cá thể, và tập items của Knapsack đều được mô hình hóa bằng `tuple` lồng nhau.
- Các hàm như `crossover_op` hay `mutation_op` luôn nhận đầu vào và sinh ra đầu ra mới mà không gây tác dụng phụ (side effects).
- Tính ngẫu nhiên được kiểm soát nghiêm ngặt bằng việc truyền explicitly tham số `seed` vào từng hàm thông qua một chuỗi các giá trị `rng.random()`.
- Việc vận hành tiến hóa qua các thế hệ sử dụng **Higher-Order Functions**: dùng `map` để biểu diễn việc tính fitness trên toàn bộ quần thể theo phong cách hàm, và dùng `reduce` như một accumulator mạnh mẽ để duyệt toàn bộ 300 thế hệ tiến hóa mà không cần vòng lặp for mang tính thủ tục.

## Reflection: So sánh OOP và FP trong triển khai GA

Quá trình triển khai GA bằng hai hệ tư tưởng mang lại góc nhìn sâu sắc về đánh đổi trong thiết kế phần mềm (Design Trade-offs):

**Về Lập trình Hướng đối tượng (OOP):**
OOP cực kì tự nhiên và trực quan khi mô phỏng thuật toán di truyền. Các thực thể sinh học (Nhiễm sắc thể, Quần thể) map 1-1 với các Object. Việc áp dụng Design Patterns (như Strategy) khiến khả năng mở rộng (Extensibility) rất mạnh—ví dụ muốn thêm Rank Selection, ta chỉ cần kế thừa interface mà không cần chạm vào lõi `GeneticAlgorithm`. Tính đóng gói (Encapsulation) đã che giấu được các mảng mutation, cho phép tối ưu hiệu năng tốt bằng việc in-place update mảng nếu cần thiết (dù ở bài này vẫn tôn trọng strict replacement).

**Về Lập trình Hàm (FP):**
FP lại đem đến sự thanh lịch về toán học. Bằng việc loại bỏ state, loại bỏ classes và chuyển hoàn toàn sang immutable tuples cùng Higher-Order functions (`map`, `reduce`), mã nguồn trở nên hoàn toàn khai báo (declarative) và cực kì dễ test. Mỗi unit test đơn thuần chỉ là "Input A luôn ra Output B", không phải set up context phức tạp. Tính tất định (Determinism) được đảm bảo khi chạy với cùng đầu vào, cùng tham số và cùng seed. Dù hiệu năng FP bị ảnh hưởng nhẹ do chi phí sinh cấu trúc dữ liệu mới và tái khởi tạo object `Random`, sự tự tin về an toàn luồng (thread-safety) khi chạy song song trên diện rộng hoàn toàn bù đắp được điều đó.

**Kết luận:** OOP phù hợp khi xây dựng các thư viện GA hướng người dùng (cần state encapsulation và object mapping), trong khi FP là công cụ phù hợp cho các hệ thống tối ưu cần tính tái lập cao, luồng dữ liệu rõ ràng và khả năng kiểm thử tốt.
