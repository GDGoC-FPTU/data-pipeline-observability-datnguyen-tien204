[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23574016&assignment_repo_type=AssignmentRepo)
# Day 10 Lab: Data Pipeline & Data Observability

**Student Email:** datnguyen.tien204@vinuni.edu.vn
**Name:** Dat Nguyen Tien — AI20K-2004

---

## Mo ta

Bai lab nay xay dung mot ETL pipeline (Extract → Validate → Transform → Load) hoan chinh bang Python de xu ly du lieu san pham dang JSON. Pipeline thuc hien kiem tra chat luong du lieu (loai bo gia am, category rong), ap dung business logic (giam gia 10%, chuan hoa Title Case), va luu ket qua ra CSV. Phan thi nghiem Stress Test chung minh tam quan trong cua Data Observability trong he thong AI.

---

## Cach chay (How to Run)

### Prerequisites

```bash
pip install pandas pytest
```

### Chay ETL Pipeline

```bash
python solution.py
```

Ket qua: file `processed_data.csv` se duoc tao ra voi cac records hop le.

### Chay Agent Simulation (Stress Test)

```bash
# Buoc 1: Tao garbage data
python generate_garbage.py

# Buoc 2: Chay agent voi ca 2 bo du lieu
python agent_simulation.py
```

### Chay Tests

```bash
pytest tests/test_autograder.py -v
```

---

## Cau truc thu muc

```
├── solution.py              # ETL Pipeline (Extract / Validate / Transform / Load)
├── generate_garbage.py      # Tao du lieu "rac" de thu nghiem
├── agent_simulation.py      # Gia lap AI Agent voi Clean vs Garbage data
├── raw_data.json            # Du lieu nguon (5 san pham, 2 record loi co san)
├── processed_data.csv       # Output cua pipeline (tu dong tao sau khi chay)
├── garbage_data.csv         # Output cua generate_garbage.py
├── experiment_report.md     # Bao cao thi nghiem & phan tich
└── README.md                # File nay
```

---

## Ket qua

| Buoc | Chi tiet |
|------|----------|
| Raw records | 5 |
| Records bi loai | 2 (id=3: price=-10, id=4: category rong) |
| Records xu ly thanh cong | 3 (Laptop, Chair, Monitor) |
| Columns them moi | `discounted_price`, `processed_at` |
| Output | `processed_data.csv` |

**Stress Test:**
- **Clean data** → Agent de xuat: *"Laptop at $1200"* (chinh xac)
- **Garbage data** → Agent de xuat: *"Nuclear Reactor at $999,999"* (sai hoan toan do outlier)

> **Ket luan:** Data quality > Prompt quality. Du lieu sach la nen tang cua moi AI Agent chinh xac.
